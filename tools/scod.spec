Name:           scod
Version:        0.1.git20110312
Release:        1%{?dist}
Summary:        SCOD is a applications for easy enable device kernel modules

Group:          Applications/System
License:        GPLv3
URL:            www.russianfedora.ru
Source0:        http://github.com/elemc/scod/%{name}-%{version}.tar.bz2
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

#BuildRequires:  PyQt4-devel
#Requires:       dbus, pyudev

BuildArch:	noarch

%description
SCOD us a daemon and clients for easy operate with (a)kmod packages contained kernel modules
for various device.

%package daemon
Summary:	SCOD daemon, service for listen new devices
Group:		System Environment/Daemons
Requires:	dbus, python, pyudev

%description daemon
SCOD daemon is a service for listen and notification about new and existing device

%prep
%setup -q

%build
make %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT/usr SYSCONFDIR=$RPM_BUILD_ROOT/etc

%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root,-)
%doc README

%files daemon
%{_bindir}/%{name}
%{_datadir}/%{name}/*.py
%config %{_sysconfdir}/%{name}/devices.conf
%config %{_syscofndir}/dbus-1/system.d/%{name}.conf


%changelog
* Sat Mar 12 2011 Alexei Panov <elemc AT atisserv DOT ru> - 0.1.git20110312-1
- Initial build
