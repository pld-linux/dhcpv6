Summary:	DHCPv6 - DHCP server and client for IPv6
Summary(pl.UTF-8):	DHCPv6 - serwer i klient DHCP dla IPv6
Name:		dhcpv6
Version:	1.0.15
Release:	1
Epoch:		1
License:	GPL v2+
Group:		Networking/Daemons
Source0:	https://fedorahosted.org/releases/d/h/dhcpv6/%{name}-%{version}.tar.gz
# Source0-md5:	2b0b5374cb2a0c460b62af3705cb29f7
Source1:	dhcp6s.init
Source2:	dhcp6c.init
Patch0:		%{name}-configure.patch
URL:		https://fedorahosted.org/dhcpv6/
BuildRequires:	autoconf >= 2.61
BuildRequires:	automake
BuildRequires:	bison
BuildRequires:	flex
BuildRequires:	libtool
BuildRequires:	rpmbuild(macros) >= 1.268
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Implements the Dynamic Host Configuration Protocol (DHCP) for Internet
Protocol version 6 (IPv6) networks in accordance with RFC 3315:
Dynamic Host Configuration Protocol for IPv6 (DHCPv6).

%description -l pl.UTF-8
Ten pakiet jest implementacją protokołu Dynamic Host Configuration
Protocol (DHCP) dla sieci IPv6 zgodnie z RFC 3315: Dynamic Host
Configuration Protocol for IPv6 (DHCPv6).

%package client
Summary:	DHCPv6 client
Summary(pl.UTF-8):	Klient DHCPv6
Group:		Applications/Networking
Requires(post,preun):	/sbin/chkconfig
Requires:	rc-scripts

%description client
Provides the client for the DHCPv6 protocol (RFC 3315) to support
dynamic configuration of IPv6 addresses and parameters.

%description client -l pl.UTF-8
Ten pakiet dostarcza klienta protokołu DHCPv6 (RFC 3315) do obsługi
dynamicznej konfiguracji adresów i parametrów sieci iPv6.

%package relay
Summary:	DHCPv6 relay agent
Summary(pl.UTF-8):	Agent przekazujący DHCPv6
Group:		Applications/Networking
Requires(post,preun):	/sbin/chkconfig
Requires:	rc-scripts

%description relay
dhcp6r acts as DHCPv6 relay agent forwarding DHCPv6 messages from
clients to servers and vice versa.

%description relay -l pl.UTF-8
dhcp6r służy jako agent przekazujący komunikaty DHCPv6 od klientów do
serwerów i z powrotem.

%package server
Summary:	DHCPv6 server daemon
Summary(pl.UTF-8):	Demon serwera DHCPv6
Group:		Applications/Networking
Requires(post,preun):	/sbin/chkconfig
Requires:	rc-scripts

%description server
dhcp6s is an implementation of the DHCPv6 server.

%description server -l pl.UTF-8
dhcp6s to implementacja serwera DHCPv6.

%package -n libdhcp6client
Summary:	The DHCPv6 client in a library for invocation by other programs
Summary(pl.UTF-8):	Klient DHCPv6 w postaci biblioteki do wykorzystania w innych programach
Group:		Libraries

%description -n libdhcp6client
Provides the client for the DHCPv6 protocol (RFC 3315) to support
dynamic configuration of IPv6 addresses and parameters, in a library
for invocation by other programs.

%description -n libdhcp6client -l pl.UTF-8
Ten pakiet zawiera klienta protokołu DHCPv6 (RFC 3315) do obsługi
dynamicznej konfiguracji adresów i parametrów IPv6 w postaci
biblioteki do wykorzystania w innych programach.

%package -n libdhcp6client-devel
Summary:	Header files for development with the DHCPv6 client library
Summary(pl.UTF-8):	Pliki nagłówkowe do programowania z użyciem biblioteki klienckiej DHCPv6
Group:		Development/Libraries
Requires:	libdhcp6client = %{epoch}:%{version}-%{release}

%description -n libdhcp6client-devel
Header files for development with the DHCPv6 client library.

%description -n libdhcp6client-devel -l pl.UTF-8
Pliki nagłówkowe do programowania z użyciem biblioteki klienckiej
DHCPv6.

%package -n libdhcp6client-static
Summary:	Static DHCPv6 client library
Summary(pl.UTF-8):	Statyczna biblioteka kliencka DHCPv6
Group:		Development/Libraries
Requires:	libdhcp6client-devel = %{epoch}:%{version}-%{release}

%description -n libdhcp6client-static
Static DHCPv6 client library.

%description -n libdhcp6client-static -l pl.UTF-8
Statyczna biblioteka kliencka DHCPv6.

%prep
%setup -q
%patch0 -p1

%build
%{__libtoolize}
%{__aclocal} -I m4
%{__autoconf}
%{__automake}
%configure

%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_localstatedir}/lib/dhcpv6,/etc/{rc.d/init.d,sysconfig}}

%{__make} install \
	INSTALL_USER=$(id -u) \
	INSTALL_GROUP=$(id -g) \
	DESTDIR=$RPM_BUILD_ROOT

install %{SOURCE1}	$RPM_BUILD_ROOT/etc/rc.d/init.d/dhcp6s
install %{SOURCE2}	$RPM_BUILD_ROOT/etc/rc.d/init.d/dhcp6c

%clean
rm -rf $RPM_BUILD_ROOT

%post client
/sbin/chkconfig --add dhcp6c
%service dhcp6c restart

%post relay
/sbin/chkconfig --add dhcp6r
%service dhcp6r restart

%post server
/sbin/chkconfig --add dhcp6s
%service dhcp6s restart

%preun client
if [ "$1" = "0" ]; then
	%service dhcp6c stop
	/sbin/chkconfig --del dhcp6c
fi

%preun relay
if [ "$1" = "0" ]; then
	%service dhcp6r stop
	/sbin/chkconfig --del dhcp6r
fi

%preun server
if [ "$1" = "0" ]; then
	%service dhcp6s stop
	/sbin/chkconfig --del dhcp6s
fi

%post	-n libdhcp6client -p /sbin/ldconfig
%postun	-n libdhcp6client -p /sbin/ldconfig

%files client
%defattr(644,root,root,755)
%attr(755,root,root) %{_sbindir}/dhcp6c
%attr(754,root,root) /etc/rc.d/init.d/dhcp6c
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/dhcp6c.conf
%{_mandir}/man8/dhcp6c.8*
%{_mandir}/man5/dhcp6c.conf.5*

%files relay
%defattr(644,root,root,755)
%attr(755,root,root) %{_sbindir}/dhcp6r
%attr(754,root,root) /etc/rc.d/init.d/dhcp6r
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) /etc/sysconfig/dhcp6r
%{_mandir}/man8/dhcp6r.8*

%files server
%defattr(644,root,root,755)
%doc AUTHORS README TODO
%attr(755,root,root) %{_sbindir}/dhcp6s
%attr(754,root,root) /etc/rc.d/init.d/dhcp6s
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) /etc/sysconfig/dhcp6s
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/dhcp6s.conf
%{_mandir}/man8/dhcp6s.8*
%{_mandir}/man5/dhcp6s.conf.5*
%attr(750,root,root) %dir %{_localstatedir}/lib/dhcpv6

%files -n libdhcp6client
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libdhcp6client-*.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libdhcp6client-*.so.2

%files -n libdhcp6client-devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libdhcp6client.so
%{_libdir}/libdhcp6client.la
%{_includedir}/dhcp6client
%{_pkgconfigdir}/libdhcp6client.pc

%files -n libdhcp6client-static
%defattr(644,root,root,755)
%{_libdir}/libdhcp6client.a
