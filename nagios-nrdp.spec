# TODO
# - send_nrdp  is crap, it never reports any errors back
%define		pkg	nrdp
%define		php_min_version 5.1.0
Summary:	Nagios Remote Data Processor (NDRP)
Name:		nagios-%{pkg}
Version:	1.2
Release:	0.6
License:	GPL v2 (server), BSD (send_nrdp)
Group:		Applications/WWW
Source0:	http://assets.nagios.com/downloads/nrdp/nrdp.zip
# Source0-md5:	e67bb3c660b22d80abd8a06a4853d814
Patch0:		config.patch
URL:		http://exchange.nagios.org/directory/Addons/Passive-Checks/NRDP--2D-Nagios-Remote-Data-Processor/details
BuildRequires:	rpmbuild(macros) >= 1.553
Requires:	nagios
Requires:	nagios-cgi
Requires:	php(core) >= %{php_min_version}
Requires:	php(date)
Requires:	php(simplexml)
Requires:	php(xml)
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_webapps	/etc/webapps
%define		_sysconfdir	%{_webapps}/nagios
%define		_appdir		%{_datadir}/nagios/%{pkg}

# bad depsolver
%define		_noautopear	pear
# put it together for rpmbuild
%define		_noautoreq	%{?_noautophp} %{?_noautopear}

%description
Nagios Remote Data Processor (NDRP) is a flexible data transport
mechanism and processor for Nagios. It is designed with a simple and
powerful architecture that allows for it to be easily extended and
customized to fit individual users' needs. It uses standard ports
protocols (HTTP(S) and XML) and can be implemented as a replacement
for NSCA.

%package client
Summary:	NRDP Host and Service Check Client
Group:		Networking
Requires:	php(core) >= %{php_min_version}
Requires:	php(date)

%description client
Client to send results to Nagios Remote Data Processor (NDRP) server.

%prep
%setup -qc
mv %{pkg}/* .
%patch0 -p1
%undos clients/send_nrdp.php

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_sysconfdir},%{_appdir},/var/lib/nagios/%{pkg},%{_bindir}}
cp -a server/* /$RPM_BUILD_ROOT%{_appdir}

mv $RPM_BUILD_ROOT{%{_appdir}/config.inc.php,%{_sysconfdir}/%{pkg}.php}
ln -s %{_sysconfdir}/%{pkg}.php $RPM_BUILD_ROOT%{_appdir}/config.inc.php

install -p clients/send_nrdp.php $RPM_BUILD_ROOT%{_bindir}/send_nrdp

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc CHANGES.TXT INSTALL.TXT LICENSE.TXT
%attr(640,root,http) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/%{pkg}.php
%{_appdir}

# tmp dir for data exchange nagios/webserver
%attr(2770,root,nagcmd) %dir /var/lib/nagios/%{pkg}

%files client
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/send_nrdp
