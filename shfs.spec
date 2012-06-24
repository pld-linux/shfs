Summary:	(Secure) SHell FileSystem Linux kernel module
Summary(pl):	Modu� j�dra wspieraj�cy system plik�w przez ssh
Name:		shfs
Version:	0.32pre1
Release:	0.1
License:	GPL
Group:		Applications/Mail
# Source0-md5:	eb4840e893da72f6169796b020a77769
Source0:	http://atrey.karlin.mff.cuni.cz/~qiq/src/shfs/%{name}-%{version}.tar.gz
Requires:	kernel-headers
URL:		http://shfs.sourceforge.net/
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
SHFS is a simple and easy to use Linux kernel (2.4) module which allows you to
mount remote filesystems using plain shell (ssh/rsh) connection. It supports
some nice features like number of different caches for access speedup, target
system optimisations, etc.

%description -l pl
SHFS to prosty i bezpieczny pomys�, aby zaimplementowa� modu� systemu plik�w
bazuj�cy na po��czaniu przez ssh (secure shell).

%prep
%setup -q

%build
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
%{__make} install ROOT="$RPM_BUILD_ROOT"

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%{_bindir}/*
/sbin/*
# the line above MUST be better!
/lib/modules/2.4.20/kernel/fs/shfs/*
