#
# Conditional build:
%bcond_without	dist_kernel	# without distribution kernel
%bcond_without	kernel		# don't build kernel modules
%bcond_without	up		# don't build UP module
%bcond_without	smp		# don't build SMP module
%bcond_with	verbose		# verbose build (V=1)
%bcond_without	userspace	# don't build userspace tools
%bcond_with	grsec_kernel	# build for kernel-grsecurity

%ifarch sparc
%undefine	with_smp
%endif

%if %{without kernel}
%undefine	with_dist_kernel
%endif
%if %{with kernel} && %{with dist_kernel} && %{with grsec_kernel}
%define	alt_kernel	grsecurity
%endif
%if "%{_alt_kernel}" != "%{nil}"
%undefine	with_userspace
%endif

%define		_rel	55
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
Patch6:		%{name}-d_entry.patch
Patch7:		%{name}-shfs_get_sb.patch
URL:		http://shfs.sourceforge.net/
%if %{with kernel}
%{?with_dist_kernel:BuildRequires:	kernel%{_alt_kernel}-module-build >= 3:2.6.7}
BuildRequires:	rpmbuild(macros) >= 1.330
%endif
%{?with_dist_kernel:Requires:	kernel(shfs)}
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

%package -n kernel%{_alt_kernel}-fs-shfs
Summary:	SHell File System Linux kernel module
Summary(pl):	Modu³ j±dra Linuksa obs³uguj±cy pow³okowy system plików
Release:	%{_rel}@%{_kernel_ver_str}
Group:		Base/Kernel
Requires(post,postun):	/sbin/depmod
%if %{with dist_kernel}
%requires_releq_kernel_up
Requires(postun):	%releq_kernel_up
%endif
Provides:	kernel(shfs)
%if "%{_alt_kernel}" == "%{nil}"
Obsoletes:	kernel-misc-shfs
%endif

%description -n kernel%{_alt_kernel}-fs-shfs
SHell File System Linux kernel module.

%description -n kernel%{_alt_kernel}-fs-shfs -l pl
Modu³ j±dra Linuksa obs³uguj±cy pow³okowy system plików.

%package -n kernel%{_alt_kernel}-smp-fs-shfs
Summary:	SHell File System Linux SMP kernel module
Summary(pl):	Modu³ j±dra Linuksa SMP obs³uguj±cy pow³okowy system plików
Release:	%{_rel}@%{_kernel_ver_str}
Group:		Base/Kernel
Requires(post,postun):	/sbin/depmod
%if %{with dist_kernel}
%requires_releq_kernel_smp
Requires(postun):	%releq_kernel_smp
%endif
Provides:	kernel(shfs)
%if "%{_alt_kernel}" == "%{nil}"
Obsoletes:	kernel-smp-misc-shfs
%endif

%description -n kernel%{_alt_kernel}-fs-shfs
SHell File System Linux kernel module.

%description -n kernel%{_alt_kernel}-smp-fs-shfs -l pl
Modu³ j±dra Linuksa obs³uguj±cy pow³okowy system plików.

%prep
%setup -q
%patch0 -p1
%patch1 -p0
%patch2 -p1
%patch3 -p1
%patch4 -p1
%patch5 -p1
%patch6 -p1
%patch7 -p1

cat > shfs/Linux-2.6/Makefile <<'EOF'
obj-m := shfs.o
shfs-objs := dcache.o dir.o fcache.o file.o inode.o \
		ioctl.o proc.o shell.o symlink.o
EOF

%build
%if %{with kernel}
%build_kernel_modules -C shfs/Linux-2.6 -m shfs
%endif

%if %{with userspace}
%{__make} -C shfsmount \
	SHFS_VERSION="\"%{version}\"" \
	CC="%{__cc} %{rpmcflags}" \
	LINKER="%{__cc}"	\
	LDFLAGS="%{rpmldflags}"
%{__make} docs
%endif

%install
rm -rf $RPM_BUILD_ROOT

%if %{with kernel}
%install_kernel_modules -m shfs/Linux-2.6/shfs -d kernel/fs/shfs
%endif

%if %{with userspace}
%{__make} utils-install docs-install \
	ROOT=$RPM_BUILD_ROOT \
	MAN_PAGE_DIR=%{_mandir}
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%post	-n kernel%{_alt_kernel}-fs-shfs
%depmod %{_kernel_ver}

%postun	-n kernel%{_alt_kernel}-fs-shfs
%depmod %{_kernel_ver}

%post	-n kernel%{_alt_kernel}-smp-fs-shfs
%depmod %{_kernel_ver}smp

%postun -n kernel%{_alt_kernel}-smp-fs-shfs
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
%if %{with up} || %{without dist_kernel}
%files -n kernel%{_alt_kernel}-fs-shfs
%defattr(644,root,root,755)
%dir /lib/modules/%{_kernel_ver}/kernel/fs/shfs
/lib/modules/%{_kernel_ver}/kernel/fs/shfs/shfs.ko*
%endif

%if %{with smp} && %{with dist_kernel}
%files -n kernel%{_alt_kernel}-smp-fs-shfs
%defattr(644,root,root,755)
%dir /lib/modules/%{_kernel_ver}smp/kernel/fs/shfs
/lib/modules/%{_kernel_ver}smp/kernel/fs/shfs/shfs.ko*
%endif
%endif
