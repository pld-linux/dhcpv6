# TODO:
# - new .sysconfig files
# - test it
Summary:	DHCPv6 - DHCP server and client for IPv6
Summary(pl):	DHCPv6 - serwer i klient DHCP dla IPv6
Name:		dhcpv6
Version:	0.10
Release:	0.6
Epoch:		1
License:	GPL
Group:		Networking/Daemons
Source0:	http://dl.sourceforge.net/dhcpv6/dhcp-%{version}.tgz
# Source0-md5:	72b802d6c89e15e5cf6b0aecf46613f2
Source1:	dhcp6s.init
Source2:	dhcp6c.init
Patch0:		%{name}-initscripts.patch
Patch1:		%{name}-DESTDIR.patch
Patch2:		%{name}-Makefile.patch
URL:		http://dhcpv6.sourceforge.net/
BuildRequires:	bison
BuildRequires:	flex
Requires(post,preun):	/sbin/chkconfig
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Implements the Dynamic Host Configuration Protocol (DHCP) for Internet
Protocol version 6 (IPv6) networks in accordance with RFC 3315 :
Dynamic Host Configuration Protocol for IPv6 (DHCPv6). Consists of
dhcp6s(8), the server DHCP daemon. Install this if you want to support
dynamic configuration of IPv6 addresses and parameters on your IPv6
network. See man dhcp6s(8), dhcp6s.conf(5), and the documentation in
/usr/share/doc/dhcpv6* .

%description -l pl
Ten pakiet jest implementacj± protoko³u Dynamic Host Configuration
Protocol (DHCP) dla sieci IPv6 zgodnie z RFC 3315: Dynamic Host
Configuration Protocol for IPv6 (DHCPv6). Zawiera demona serwera DHCP
- dhcp6s(8). Nale¿y zainstalowaæ ten pakiet, je¶li potrzebujemy
obs³ugi dynamicznej konfiguracji adresów i parametrów sieci IPv6.
Wiêcej znajduje siê w manualach dhcp6s(8), dhcp6s.conf(5) oraz
dokumentacji w /usr/share/doc/dhcpv6* .

%package -n dhcpv6_client
Summary:	DHCPv6 client
Summary(pl):	Klient DHCPv6
Group:		Applications/Networking
Requires:	initscripts >= 7.73

%description -n dhcpv6_client
Provides the client for the DHCPv6 protocol (RFC 3315) to support
dynamic configuration of IPv6 addresses and parameters. See man
dhcp6c(8), dhcp6c.conf(5), and the documentation in
/usr/share/doc/dhcpv6_client* .

%description -n dhcpv6_client -l pl
Ten pakiet dostarcza klienta protoko³u DHCPv6 (RFC 3315) do obs³ugi
dynamicznej konfiguracji adresów i parametrów sieci iPv6. Wiêcej
znajduje siê w manualu dhcp6c(8), dhcp6c.conf(5) oraz dokumentacji w
/usr/share/doc/dhcpv6_client*

%prep
%setup -q -n dhcp-%{version}
%patch0 -p1
%patch1 -p1
%patch2 -p1

%build
%configure \
	--prefix= \
	--mandir=%{_mandir}

%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_localstatedir}/lib/dhcpv6,/etc/rc.d/init.d}

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

install	dhcp6relay.8	$RPM_BUILD_ROOT%{_mandir}/man8
install %{SOURCE1}	$RPM_BUILD_ROOT/etc/rc.d/init.d/dhcp6s
install %{SOURCE2}	$RPM_BUILD_ROOT/etc/rc.d/init.d/dhcp6c

%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/chkconfig --add dhcp6s

%preun
if [ "$1" = "0" ]; then
	/etc/rc.d/init.d/dhcp6s stop >/dev/null 2>&1
	/sbin/chkconfig --del dhcp6s
fi

%postun
if [ "$1" -ge "1" ]; then
	/etc/rc.d/init.d/dhcp6s condrestart >/dev/null 2>&1
fi

%files
%defattr(644,root,root,755)
%doc ReadMe docs/*
%attr(755,root,root) %{_sbindir}/dhcp6s
%attr(754,root,root) /etc/rc.d/init.d/dhcp6s
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) /etc/sysconfig/dhcp6s
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/dhcp6s.conf
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/server6_addr.conf
%attr(750,root,root) %dir %{_localstatedir}/lib/dhcpv6
%{_mandir}/man8/dhcp6s.8*
%{_mandir}/man8/dhcp6relay.8*
%{_mandir}/man5/dhcp6s.conf.5*


%files -n dhcpv6_client
%defattr(644,root,root,755)
%doc ReadMe dhcp6c.conf
%attr(755,root,root) %{_sbindir}/dhcp6c
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) /etc/sysconfig/dhcp6c
%attr(754,root,root) /etc/rc.d/init.d/dhcp6c
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/dhcp6c.conf
%{_mandir}/man8/dhcp6c.8*
%{_mandir}/man5/dhcp6c.conf.5*
