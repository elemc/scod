%define daemon_name scodd
%define qtclient qtscod
%define gtkclient gtkscod

Name:           scod
Version:        0.1.git20110929
Release:        1%{?dist}
Summary:        SCOD is a applications for easy enable device kernel modules

Group:          Applications/System
License:        GPLv3
URL:            www.russianfedora.ru
Source0:        http://github.com/elemc/scod/%{name}-%{version}.tar.bz2
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildArch:	noarch

%description
SCOD us a daemon and clients for easy operate with (a)kmod packages contained kernel modules
for various device.

%package daemon
Summary:		SCOD daemon, service for listen new devices
Group:			System Environment/Daemons
Requires:		dbus, python, pyudev
Requires(post):		systemd-units
Requires(preun):	systemd-units
Requires(postun):	systemd-units

%description daemon
SCOD daemon is a service for listen and notification about new and existing device

%package client-qt
Summary:	SCOD Qt client
Group:		Applications/System
Requires:	dbus, PyQt4, scod-daemon
BuildRequires:	PyQt4-devel

%description client-qt
Qt frontend for SCOD

%prep
%setup -q

%build
make %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT/usr SYSCONFDIR=$RPM_BUILD_ROOT/etc UNITDIR=$RPM_BUILD_ROOT/%{_unitdir}
pushd qtscod
      make install DESTDIR=$RPM_BUILD_ROOT/usr
popd

%clean
rm -rf $RPM_BUILD_ROOT

%files daemon
%{_bindir}/%{daemon_name}
%{_datadir}/%{daemon_name}/*.py*
%config %{_sysconfdir}/%{daemon_name}/devices.conf
%config %{_sysconfdir}/dbus-1/system.d/%{daemon_name}.conf
%{_unitdir}/%{daemon_name}.service
%doc README

%files client-qt
%{_bindir}/%{qtclient}
%{_datadir}/%{qtclient}/*.py*
%{_datadir}/%{qtclient}/src/*.py*
%{_datadir}/%{qtclient}/ui/*.py*
%{_datadir}/%{qtclient}/lang/*
%doc README

%post daemon
if [ $1 -eq 1 ] ; then 
    # Initial installation 
    /bin/systemctl daemon-reload >/dev/null 2>&1 || :
fi

%preun daemon
if [ $1 -eq 0 ] ; then
    # Package removal, not upgrade
    /bin/systemctl --no-reload disable scodd.service > /dev/null 2>&1 || :
    /bin/systemctl stop scodd.service > /dev/null 2>&1 || :
fi

%postun daemon
/bin/systemctl daemon-reload >/dev/null 2>&1 || :
if [ $1 -ge 1 ] ; then
    # Package upgrade, not uninstall
    /bin/systemctl try-restart scodd.service >/dev/null 2>&1 || :
fi

%changelog
* Sat Mar 12 2011 Alexei Panov <elemc AT atisserv DOT ru> - 0.1.git20110312-1
- Initial build
