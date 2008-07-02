#
# Conditional build:
%bcond_without	dist_kernel	# without distribution kernel
%bcond_without	kernel		# don't build kernel modules
%bcond_with	verbose		# verbose build (V=1)
%bcond_without	userspace	# don't build userspace tools

%if %{without kernel}
%undefine	with_dist_kernel
%endif
%if "%{_alt_kernel}" != "%{nil}"
%undefine	with_userspace
%endif
%if %{without userspace}
# nothing to be placed to debuginfo package
%define		_enable_debug_packages	0
%endif

%define		rel		66
%define		pname	shfs
Summary:	(Secure) SHell FileSystem utilities
Summary(pl.UTF-8):	Narzędzia obsługujące system plików przez ssh
Name:		%{pname}%{_alt_kernel}
Version:	0.35
Release:	%{rel}
License:	GPL v2
Group:		Applications/System
Source0:	http://dl.sourceforge.net/shfs/%{pname}-%{version}.tar.gz
# Source0-md5:	016f49d71bc32eee2b5d11fc1600cfbe
Patch0:		%{pname}-opt.patch
Patch1:		%{pname}-df.patch
Patch2:		%{pname}-space_chars.patch
Patch3:		%{pname}-uidgid32.patch
Patch4:		%{pname}-gcc4.patch
Patch5:		%{pname}-inode_oops.patch
Patch6:		%{pname}-d_entry.patch
Patch7:		%{pname}-shfs_get_sb.patch
Patch8:		%{pname}-2.6.19.patch
Patch9:		%{pname}-kmem_cache.patch
URL:		http://shfs.sourceforge.net/
%if %{with kernel}
%{?with_dist_kernel:BuildRequires:	kernel%{_alt_kernel}-module-build >= 3:2.6.20.2}
BuildRequires:	rpmbuild(macros) >= 1.379
%endif
Obsoletes:	shfsmount
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
SHFS is a simple and easy to use Linux kernel 2.4.10+ and 2.6 module
which allows you to mount remote filesystems using plain shell
(ssh/rsh) connection. It supports some nice features like number of
different caches for access speedup, target system optimisations, etc.

This package contains utilities for SHFS.

%description -l pl.UTF-8
SHFS to prosty i łatwy w użyciu moduł jądra Linuksa 2.4.10+ i 2.6
pozwalający montować zdalne systemy plików przy użyciu zwykłego
połączenia ze zdalną powłoką (ssh lub rsh). Obsługuje pewne miłe
cechy, takie jak różne sposoby buforowania dla przyspieszenia dostępu,
optymalizacje pod kątem zdalnego systemu itp.

Ten pakiet zawiera programy narzędziowe dla SHFS.

%package -n kernel%{_alt_kernel}-fs-shfs
Summary:	SHell File System Linux kernel module
Summary(pl.UTF-8):	Moduł jądra Linuksa obsługujący powłokowy system plików
Release:	%{rel}@%{_kernel_ver_str}
Group:		Base/Kernel
Requires(post,postun):	/sbin/depmod
%if %{with dist_kernel}
%requires_releq_kernel
Requires(postun):	%releq_kernel
%endif
Provides:	kernel(shfs)
%if "%{_alt_kernel}" == "%{nil}"
Obsoletes:	kernel-misc-shfs
%endif

%description -n kernel%{_alt_kernel}-fs-shfs
SHell File System Linux kernel module.

%description -n kernel%{_alt_kernel}-fs-shfs -l pl.UTF-8
Moduł jądra Linuksa obsługujący powłokowy system plików.

%prep
%setup -q -n %{pname}-%{version}
%patch0 -p1
%patch1 -p0
%patch2 -p1
%patch3 -p1
%patch4 -p1
%patch5 -p1
%patch6 -p1
%patch7 -p1
%patch8 -p1
%patch9 -p1

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
%files -n kernel%{_alt_kernel}-fs-shfs
%defattr(644,root,root,755)
%dir /lib/modules/%{_kernel_ver}/kernel/fs/shfs
/lib/modules/%{_kernel_ver}/kernel/fs/shfs/shfs.ko*
%endif
