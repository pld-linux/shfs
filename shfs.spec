#
# Conditional build:
%bcond_without	dist_kernel	# without distribution kernel
%bcond_without	kernel		# don't build kernel modules
%bcond_without	smp		# don't build SMP module
%bcond_with	verbose		# verbose build (V=1)
%bcond_without	userspace	# don't build userspace tools
#
Summary:	(Secure) SHell FileSystem utilities
Summary(pl):	Narzêdzia obs³uguj±ce system plików przez ssh
Name:		shfs
Version:	0.33
%define		_rel	2
Release:	%{_rel}
License:	GPL
Group:		Applications/System
Source0:	http://dl.sourceforge.net/%{name}/%{name}-%{version}.tar.gz
# Source0-md5:	4a934725cc3a7695b0ddf248736c871a
Patch0:		%{name}-opt.patch
URL:		http://shfs.sourceforge.net/
%if %{with kernel}
%{?with_dist_kernel:BuildRequires:	kernel-module-build}
BuildRequires:	%{kgcc_package}
%endif
BuildRequires:	rpmbuild(macros) >= 1.118
Obsoletes:	shfsmount
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
SHFS is a simple and easy to use Linux kernel (2.4) module which
allows you to mount remote filesystems using plain shell (ssh/rsh)
connection. It supports some nice features like number of different
caches for access speedup, target system optimisations, etc.

This package contains utilities for SHFS.

%description -l pl
SHFS to prosty i ³atwy w u¿yciu modu³ j±dra Linuksa (2.4) pozwalaj±cy
montowaæ zdalne systemy plików przy u¿yciu zwyk³ego po³±czenia ze
zdaln± pow³ok± (ssh lub rsh). Obs³uguje pewne mi³e cechy, takie jak
ró¿ne sposoby buforowania dla przyspieszenia dostêpu, optymalizacje
pod k±tem zdalnego systemu itp.

Ten pakiet zawiera programy narzêdziowe dla SHFS.

%package -n kernel-fs-shfs
Summary:	SHell File System Linux kernel module
Summary(pl):	Modu³ j±dra Linuksa obs³uguj±cy pow³okowy system plików
Release:	%{_rel}@%{_kernel_ver_str}
Group:		Base/Kernel
%{?with_dist_kernel:%requires_releq_kernel_up}
Requires(post,postun):	/sbin/depmod
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
%{?with_dist_kernel:%requires_releq_kernel_smp}
Requires(post,postun):	/sbin/depmod
Obsoletes:	kernel-smp-misc-shfs

%description -n kernel-fs-shfs
SHell File System Linux kernel module.

%description -n kernel-smp-fs-shfs -l pl
Modu³ j±dra Linuksa obs³uguj±cy pow³okowy system plików.

%prep
%setup -q
%patch -p1

%build
%if %{with kernel}
cd shfs/Linux-2.6
for cfg in %{?with_dist_kernel:%{?with_smp:smp} up}%{!?with_dist_kernel:nondist}; do
    if [ ! -r "%{_kernelsrcdir}/config-$cfg" ]; then
	exit 1
    fi
    rm -rf include
    install -d include/{linux,config}
    ln -sf %{_kernelsrcdir}/config-$cfg .config
    ln -sf %{_kernelsrcdir}/include/linux/autoconf-$cfg.h include/linux/autoconf.h
    touch include/config/MARKER
    echo "obj-m := shfs.o" > Makefile
    echo "shfs-objs := dcache.o dir.o fcache.o file.o inode.o ioctl.o proc.o shell.o symlink.o" >> Makefile
    %{__make} -C %{_kernelsrcdir} clean modules \
	RCS_FIND_IGNORE="-name '*.ko' -o" \
	M=$PWD O=$PWD \
	%{?with_verbose:V=1}
    mv shfs.ko shfs-$cfg.ko
done
cd -
%endif

%if %{with userspace}
%{__make} -C shfsmount \
	CC="%{__cc}" \
	OPT="%{rpmcflags}" \
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
%attr(755,root,root) %{_bindir}/*
%attr(755,root,root) /sbin/*
%{_mandir}/man8/*
%endif

%if %{with kernel}
%files -n kernel-fs-shfs
%defattr(644,root,root,755)
/lib/modules/%{_kernel_ver}/kernel/fs/shfs/*.ko*

%if %{with smp} && %{with dist_kernel}
%files -n kernel-smp-fs-shfs
%defattr(644,root,root,755)
/lib/modules/%{_kernel_ver}smp/kernel/fs/shfs/*.ko*
%endif
%endif
