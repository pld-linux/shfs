#
# Conditional build:
# _without_dist_kernel          without distribution kernel
#
Summary:	(Secure) SHell FileSystem utilities
Summary(pl):	Narzêdzia obs³uguj±ce system plików przez ssh
Name:		shfs
Version:	0.32pre2
%define	rel	1
Release:	%{rel}
License:	GPL
Group:		Applications/System
Source0:	http://atrey.karlin.mff.cuni.cz/~qiq/src/shfs/shfs-0.32/%{name}-%{version}.tar.gz
# Source0-md5:	36e466c4e694700cc64b67ef13a4288b
Patch0:		%{name}-opt.patch
URL:		http://shfs.sourceforge.net/
%{!?_without_dist_kernel:BuildRequires:         kernel-headers}
BuildRequires:	%{kgcc_package}
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
Release:	%{rel}@%{_kernel_ver_str}
Group:		Base/Kernel
%{!?_without_dist_kernel:%requires_releq_kernel_up}
Requires(post,postun):	/sbin/depmod
Obsoletes:	kernel-misc-shfs

%description -n kernel-fs-shfs
SHell File System Linux kernel module.

%description -n kernel-fs-shfs -l pl
Modu³ j±dra Linuksa obs³uguj±cy pow³okowy system plików.

%package -n kernel-smp-fs-shfs
Summary:	SHell File System Linux SMP kernel module
Summary(pl):	Modu³ j±dra Linuksa SMP obs³uguj±cy pow³okowy system plików
Release:	%{rel}@%{_kernel_ver_str}
Group:		Base/Kernel
%{!?_without_dist_kernel:%requires_releq_kernel_smp}
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
%{__make} -C shfs \
	CC="%{kgcc} -D__SMP__" \
	OPT="%{rpmcflags}"

mv -f shfs/Linux-2.4/shfs.o shfs.smp.o

%{__make} clean -C shfs
%{__make} -C shfs \
	CC="%{kgcc}" \
	OPT="%{rpmcflags}"

%{__make} -C shfsmount \
	CC="%{__cc}" \
	OPT="%{rpmcflags}"

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT/lib/modules/%{_kernel_ver}smp/kernel/fs/shfs

%{__make} install \
	ROOT=$RPM_BUILD_ROOT \
	MODULESDIR=$RPM_BUILD_ROOT/lib/modules/%{_kernel_ver} \
	MAN_PAGE_DIR=%{_mandir}

install shfs.smp.o $RPM_BUILD_ROOT/lib/modules/%{_kernel_ver}smp/kernel/fs/shfs/shfs.o

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

%files
%defattr(644,root,root,755)
%doc COPYRIGHT Changelog TODO docs/html
%attr(755,root,root) %{_bindir}/*
/sbin/*
%{_mandir}/man8/*

%files -n kernel-fs-shfs
%defattr(644,root,root,755)
%attr(755,root,root) /lib/modules/%{_kernel_ver}/kernel/fs/shfs/*.o*

%files -n kernel-smp-fs-shfs
%defattr(644,root,root,755)
%attr(755,root,root) /lib/modules/%{_kernel_ver}smp/kernel/fs/shfs/*.o*
