Summary:	DHCPv6 - DHCP server and client for IPv6
Name:		dhcpv6
Version:	0.10
Release:	1
License:	GPL
Group:		Networking/Daemons
URL:		http://dhcpv6.sourceforge.net/
Source0:	ftp://ftp.sourceforge.net/pub/sourceforge/d/dh/dhcp/dhcp-%{version}.tgz
Source1:	rfc3315.txt
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)
Patch0:		%{name}-0.10-initscripts.patch
Patch1:		%{name}-0.10-change_resolv_conf.patch
Requires:	/sbin/chkconfig
Requires:	/sbin/service
BuildRequires:	flex, bison

%description
Implements the Dynamic Host Configuration Protocol (DHCP) for Internet
Protocol version 6 (IPv6) networks in accordance with RFC 3315 :
Dynamic Host Configuration Protocol for IPv6 (DHCPv6). Consists of
dhcp6s(8), the server DHCP daemon. Install this if you want to support
dynamic configuration of IPv6 addresses and parameters on your IPv6
network. See man dhcp6s(8), dhcp6s.conf(5), and the documentation in
/usr/share/dhcpv6* .

%prep
%setup -q -n dhcp-%{version}
%patch0 -p1 -b .initscripts
%patch1 -p1 -b .change_resolv_conf

%build
%configure \
	--prefix=\
	--mandir=%{_mandir}
%{__make}
cp -fp %{SOURCE1} docs

%install
rm -rf $RPM_BUILD_ROOT
rm -rf %{buildroot}
%{__make} install DESTDIR=%{buildroot}
install -d %{buildroot}%{_localstatedir}/lib/dhcpv6

%package -n dhcpv6_client
Summary:  DHCPv6 client
Requires: initscripts >= 7.73
Group: System Environment/Base

%description -n dhcpv6_client
Provides the client for the DHCPv6 protocol (RFC 3315) to support
dynamic configuration of IPv6 addresses and parameters. See man
dhcp6c(8), dhcp6c.conf(5), and the documentation in
/usr/share/dhcpv6_client* .

%post
chkconfig --add dhcp6s

%preun
if [ $1 = 0 ]; then
  service dhcp6s stop > /dev/null 2>&1
  chkconfig --del dhcp6s
fi

%postun
if [ "$1" -ge "1" ]; then
  service dhcp6s condrestart >/dev/null 2>&1
fi

%clean
rm -rf %{buildroot}

%files
%defattr(644,root,root,755)
%attr(754,root,root) %{_sbindir}/dhcp6s
%attr(755,root,root) %config /etc/rc.d/init.d/dhcp6s
%config(noreplace) /etc/sysconfig/dhcp6s
%{_mandir}/man8/dhcp6s.8.gz
%{_mandir}/man5/dhcp6s.conf.5.gz
%attr(754,root,root) %dir %{_localstatedir}/lib/dhcpv6

%doc ReadMe docs/* dhcp6s.conf

%files -n dhcpv6_client
%defattr(644,root,root,755)
%attr(750,root,root) /sbin/dhcp6c
%{_mandir}/man8/dhcp6c.8.gz
%{_mandir}/man5/dhcp6c.conf.5.gz
%doc ReadMe dhcp6c.conf
%attr(750,root,root) %dir %{_localstatedir}/lib/dhcpv6
