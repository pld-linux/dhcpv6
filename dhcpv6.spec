Summary:	DHCPv6 - DHCP server and client for IPv6
Summary(pl):	DHCPv6 - serwer i klient DHCP dla IPv6
Name:		dhcpv6
Version:	0.10
Release:	1
License:	GPL
Group:		Networking/Daemons
Source0:	http://dl.sourceforge.net/dhcp/dhcp-%{version}.tgz
Source1:	rfc3315.txt
Patch0:		%{name}-0.10-initscripts.patch
Patch1:		%{name}-0.10-change_resolv_conf.patch
URL:		http://dhcpv6.sourceforge.net/
Requires(post,preun):	/sbin/chkconfig
BuildRequires:	bison
BuildRequires:	flex
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
Ten pakiet jest implementacj� protoko�u Dynamic Host Configuration
Protocol (DHCP) dla sieci IPv6 zgodnie z RFC 3315: Dynamic Host
Configuration Protocol for IPv6 (DHCPv6). Zawiera demona serwera DHCP
- dhcp6s(8). Nale�y zainstalowa� ten pakiet, je�li potrzebujemy
obs�ugi dynamicznej konfiguracji adres�w i parametr�w sieci IPv6.
Wi�cej znajduje si� w manualach dhcp6s(8), dhcp6s.conf(5) oraz
dokumentacji w /usr/share/doc/dhcpv6* .

%prep
%setup -q -n dhcp-%{version}
%patch0 -p1
%patch1 -p1

%build
%configure \
	--prefix= \
	--mandir=%{_mandir}
%{__make}
cp -fp %{SOURCE1} docs

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_localstatedir}/lib/dhcpv6

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
Ten pakiet dostarcza klienta protoko�u DHCPv6 (RFC 3315) do obs�ugi
dynamicznej konfiguracji adres�w i parametr�w sieci iPv6. Wi�cej
znajduje si� w manualu dhcp6c(8), dhcp6c.conf(5) oraz dokumentacji w
/usr/share/doc/dhcpv6_client*

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

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc ReadMe docs/* dhcp6s.conf
%attr(754,root,root) %{_sbindir}/dhcp6s
%attr(755,root,root) %config /etc/rc.d/init.d/dhcp6s
%config(noreplace) /etc/sysconfig/dhcp6s
%{_mandir}/man8/dhcp6s.8*
%{_mandir}/man5/dhcp6s.conf.5*
%attr(754,root,root) %dir %{_localstatedir}/lib/dhcpv6

%files -n dhcpv6_client
%defattr(644,root,root,755)
%doc ReadMe dhcp6c.conf
%attr(750,root,root) /sbin/dhcp6c
%{_mandir}/man8/dhcp6c.8*
%{_mandir}/man5/dhcp6c.conf.5*
%attr(750,root,root) %dir %{_localstatedir}/lib/dhcpv6