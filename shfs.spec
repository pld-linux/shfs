Summary:	(Secure) SHell FileSystem Linux kernel module
Summary(pl):	Modu³ j±dra wspieraj±cy system plików przez ssh
Name:		shfs
Version:	0.32pre1
Release:	3
License:	GPL
Group:		Applications/Mail
# Source0-md5:	eb4840e893da72f6169796b020a77769
Source0:	http://atrey.karlin.mff.cuni.cz/~qiq/src/shfs/%{name}-%{version}.tar.gz
Requires:	kernel-headers
Requires(post,postun):	/sbin/depmod
BuildRequires:	%{kgcc_package}
BuildRequires:	rpmbuild(macros) >= 1.118
URL:		http://shfs.sourceforge.net/
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
SHFS is a simple and easy to use Linux kernel (2.4) module which
allows you to mount remote filesystems using plain shell (ssh/rsh)
connection. It supports some nice features like number of different
caches for access speedup, target system optimisations, etc.

%description -l pl
SHFS to prosty i bezpieczny pomys³, aby zaimplementowaæ modu³ systemu
plików bazuj±cy na po³±czaniu przez ssh (secure shell).

%package -n shfs-kernel
Summary:	SHFS Linux kernel module
Summary(pl):	Modu³ j±dra wspieraj±cy system plików przez ssh	
#Release:	%{version}_%{release}@%{_kernel_ver_str}
Release:	%{release}@%{_kernel_ver_str}
Group:		Base/Kernel
Requires(post,postun):	/sbin/depmod

%description -n shfs-kernel
Linux kernel module for SHFS

%description -n shfs-kernel -l pl
Modu³ j±dra obs³uguj±cy SHFS

%prep
%setup -q

%build
%{__make} CC="%{kgcc}"

%install
rm -rf $RPM_BUILD_ROOT
%{__make} install ROOT="$RPM_BUILD_ROOT"
install -d $RPM_BUILD_ROOT/%{_mandir}/man8
install docs/manpages/*.8 $RPM_BUILD_ROOT/%{_mandir}/man8

%clean
rm -rf $RPM_BUILD_ROOT

%post -n shfs-kernel
%depmod %{_kernel_ver}

%postun -n shfs-kernel
%depmod %{_kernel_ver}

%files
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/*
/sbin/*
%{_mandir}/man8/*

%files -n shfs-kernel
%defattr(644,root,root,755)
%attr(755,root,root) /lib/modules/*/kernel/fs/shfs/*.o.gz
