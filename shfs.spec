#
# Conditional build:
%bcond_without	dist_kernel	# without distribution kernel
%bcond_without	kernel		# don't build kernel modules
%bcond_without	smp		# don't build SMP module
%bcond_with	verbose		# verbose build (V=1)
%bcond_without	userspace	# don't build userspace tools
#
%ifarch sparc
%undefine	with_smp
%endif
#
%define		_rel	14
Summary:	(Secure) SHell FileSystem utilities
Summary(pl):	Narzêdzia obs³uguj±ce system plików przez ssh
Name:		shfs
Version:	0.35
Release:	%{_rel}
License:	GPL v2
Group:		Applications/System
Source0:	http://dl.sourceforge.net/shfs/%{name}-%{version}.tar.gz
# Source0-md5:	016f49d71bc32eee2b5d11fc1600cfbe
Patch0:		%{name}-opt.patch
Patch1:		%{name}-df.patch
Patch2:		%{name}-space_chars.patch
Patch3:		%{name}-uidgid32.patch
Patch4:		%{name}-gcc4.patch
Patch5:		%{name}-inode_oops.patch
URL:		http://shfs.sourceforge.net/
%if %{with kernel}
%{?with_dist_kernel:BuildRequires:	kernel-module-build >= 2.6.7}
BuildRequires:	rpmbuild(macros) >= 1.153
%endif
%{?with_dist_kernel:Requires:	kernel-fs-shfs}
Obsoletes:	shfsmount
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
SHFS is a simple and easy to use Linux kernel 2.4.10+ and 2.6 module
which allows you to mount remote filesystems using plain shell
(ssh/rsh) connection. It supports some nice features like number of
different caches for access speedup, target system optimisations, etc.

This package contains utilities for SHFS.

%description -l pl
SHFS to prosty i ³atwy w u¿yciu modu³ j±dra Linuksa 2.4.10+ i 2.6
pozwalaj±cy montowaæ zdalne systemy plików przy u¿yciu zwyk³ego
po³±czenia ze zdaln± pow³ok± (ssh lub rsh). Obs³uguje pewne mi³e
cechy, takie jak ró¿ne sposoby buforowania dla przyspieszenia dostêpu,
optymalizacje pod k±tem zdalnego systemu itp.

Ten pakiet zawiera programy narzêdziowe dla SHFS.

%package -n kernel-fs-shfs
Summary:	SHell File System Linux kernel module
Summary(pl):	Modu³ j±dra Linuksa obs³uguj±cy pow³okowy system plików
Release:	%{_rel}@%{_kernel_ver_str}
Group:		Base/Kernel
Requires(post,postun):	/sbin/depmod
%if %{with dist_kernel}
%requires_releq_kernel_up
Requires(postun):	%releq_kernel_up
%endif
Obsoletes:	kernel-misc-shfs

%description -n kernel-fs-shfs
SHell File System Linux kernel module.

%description -n kernel-fs-shfs -l pl
Modu³ j±dra Linuksa obs³uguj±cy pow³okowy system plików.

%package -n kernel-smp-fs-shfs
Summary:	SHell File System Linux SMP kernel module
Summary(pl):	Modu³ j±dra Linuksa SMP obs³uguj±cy pow³okowy system plików
Release:	%{_rel}@%{_kernel_ver_str}
Group:		Base/Kernel
Requires(post,postun):	/sbin/depmod
%if %{with dist_kernel}
%requires_releq_kernel_smp
Requires(postun):	%releq_kernel_smp
%endif
Provides:	kernel-fs-shfs
Obsoletes:	kernel-fs-shfs
Obsoletes:	kernel-smp-misc-shfs

%description -n kernel-fs-shfs
SHell File System Linux kernel module.

%description -n kernel-smp-fs-shfs -l pl
Modu³ j±dra Linuksa obs³uguj±cy pow³okowy system plików.

%prep
%setup -q
%patch0 -p1
%patch1 -p0
%patch2 -p1
%patch3 -p1
%patch4 -p1
%patch5 -p1

%build
%if %{with kernel}
cd shfs/Linux-2.6
for cfg in %{?with_dist_kernel:%{?with_smp:smp} up}%{!?with_dist_kernel:nondist}; do
	if [ ! -r "%{_kernelsrcdir}/config-$cfg" ]; then
		exit 1
	fi
        install -d o/include/linux
        ln -sf %{_kernelsrcdir}/config-$cfg o/.config
        ln -sf %{_kernelsrcdir}/Module.symvers-$cfg o/Module.symvers
        ln -sf %{_kernelsrcdir}/include/linux/autoconf-$cfg.h o/include/linux/autoconf.h
        %{__make} -C %{_kernelsrcdir} O=$PWD/o prepare scripts

	echo "obj-m := shfs.o" > Makefile
	echo "shfs-objs := dcache.o dir.o fcache.o file.o inode.o ioctl.o proc.o shell.o symlink.o" >> Makefile
	%{__make} -C %{_kernelsrcdir} clean \
		%{?with_verbose:V=1} \
		RCS_FIND_IGNORE="-name '*.ko' -o" \
		M=$PWD O=$PWD/o
	%{__make} -C %{_kernelsrcdir} modules \
%if "%{_target_base_arch}" != "%{_arch}"
                ARCH=%{_target_base_arch} \
                CROSS_COMPILE=%{_target_base_cpu}-pld-linux- \
%endif
                HOSTCC="%{__cc}" \
		%{?with_verbose:V=1} \
		M=$PWD O=$PWD/o
	mv shfs.ko shfs-$cfg.ko
done
cd -
%endif

%if %{with userspace}
%{__make} -C shfsmount \
	SHFS_VERSION=\"%{version}\" \
	CC="%{__cc} %{rpmcflags}" \
	LINKER="%{__cc}"	\
	LDFLAGS="%{rpmldflags}"
%{__make} docs
%endif

%install
rm -rf $RPM_BUILD_ROOT

%if %{with kernel}
cd shfs/Linux-2.6
install -d $RPM_BUILD_ROOT/lib/modules/%{_kernel_ver}{,smp}/kernel/fs/shfs
install shfs-%{?with_dist_kernel:up}%{!?with_dist_kernel:nondist}.ko \
	$RPM_BUILD_ROOT/lib/modules/%{_kernel_ver}/kernel/fs/shfs/shfs.ko
%if %{with smp} && %{with dist_kernel}
install shfs-smp.ko \
	$RPM_BUILD_ROOT/lib/modules/%{_kernel_ver}smp/kernel/fs/shfs/shfs.ko
%endif
cd -
%endif

%if %{with userspace}
%{__make} utils-install docs-install \
	ROOT=$RPM_BUILD_ROOT \
	MAN_PAGE_DIR=%{_mandir}
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%post	-n kernel-fs-shfs
%depmod %{_kernel_ver}

%postun	-n kernel-fs-shfs
%depmod %{_kernel_ver}

%post	-n kernel-smp-fs-shfs
%depmod %{_kernel_ver}smp

%postun -n kernel-smp-fs-shfs
%depmod %{_kernel_ver}smp

%if %{with userspace}
%files
%defattr(644,root,root,755)
%doc COPYRIGHT Changelog TODO docs/html
%attr(4754,root,wheel) %{_bindir}/shfsmount
%attr(4754,root,wheel) %{_bindir}/shfsumount
%attr(755,root,root) /sbin/*
%{_mandir}/man8/*
%endif

%if %{with kernel}
%files -n kernel-fs-shfs
%defattr(644,root,root,755)
/lib/modules/%{_kernel_ver}/kernel/fs/shfs

%if %{with smp} && %{with dist_kernel}
%files -n kernel-smp-fs-shfs
%defattr(644,root,root,755)
/lib/modules/%{_kernel_ver}smp/kernel/fs/shfs
%endif
%endif
