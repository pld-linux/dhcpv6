# TODO:
# - obsoletes when renaming a package
# - subpackage for relay daemon
# - use %%service
Summary:	DHCPv6 - DHCP server and client for IPv6
Summary(pl.UTF-8):	DHCPv6 - serwer i klient DHCP dla IPv6
Name:		dhcpv6
Version:	1.0.3
Release:	0.9
Epoch:		1
License:	GPL
Group:		Networking/Daemons
Source0:	http://dcantrel.fedorapeople.org/dhcpv6/%{name}-%{version}.tar.gz
# Source0-md5:	7af9760efa2cb2796f75e9911c569054
Source1:	dhcp6s.init
Source2:	dhcp6c.init
Patch0:		%{name}-configure.patch
URL:		http://dhcpv6.sourceforge.net/
BuildRequires:	autoconf
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

%description -l pl.UTF-8
Ten pakiet jest implementacją protokołu Dynamic Host Configuration
Protocol (DHCP) dla sieci IPv6 zgodnie z RFC 3315: Dynamic Host
Configuration Protocol for IPv6 (DHCPv6). Zawiera demona serwera DHCP
- dhcp6s(8). Należy zainstalować ten pakiet, jeśli potrzebujemy
  obsługi dynamicznej konfiguracji adresów i parametrów sieci IPv6.
  Więcej znajduje się w manualach dhcp6s(8), dhcp6s.conf(5) oraz
  dokumentacji w /usr/share/doc/dhcpv6* .

%package -n dhcpv6-client
Summary:	DHCPv6 client
Summary(pl.UTF-8):	Klient DHCPv6
Group:		Applications/Networking
Requires:	rc-scripts

%description -n dhcpv6-client
Provides the client for the DHCPv6 protocol (RFC 3315) to support
dynamic configuration of IPv6 addresses and parameters. See man
dhcp6c(8), dhcp6c.conf(5), and the documentation in
/usr/share/doc/dhcpv6_client* .

%description -n dhcpv6-client -l pl.UTF-8
Ten pakiet dostarcza klienta protokołu DHCPv6 (RFC 3315) do obsługi
dynamicznej konfiguracji adresów i parametrów sieci iPv6. Więcej
znajduje się w manualu dhcp6c(8), dhcp6c.conf(5) oraz dokumentacji w
/usr/share/doc/dhcpv6_client*

%package -n libdhcp6client
Summary:	The DHCPv6 client in a library for invocation by other programs
Summary(pl.UTF-8):	Klient DHCPv6 w postaci biblioteki do wykorzystania w innych programach
Group:		Development/Libraries

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

%post
/sbin/chkconfig --add dhcp6s

%preun
if [ "$1" = "0" ]; then
	/etc/rc.d/init.d/dhcp6s stop >/dev/null 2>&1
	/sbin/chkconfig --del dhcp6s
fi

%postun
if [ "$1" -ge "1" ]; then
	/etc/rc.d/init.d/dhcp6s restart >/dev/null 2>&1
fi

%files
%defattr(644,root,root,755)
%doc AUTHORS README TODO docs/*
%attr(755,root,root) %{_sbindir}/dhcp6r
%attr(755,root,root) %{_sbindir}/dhcp6s
%attr(754,root,root) /etc/rc.d/init.d/dhcp6r
%attr(754,root,root) /etc/rc.d/init.d/dhcp6s
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) /etc/sysconfig/dhcp6r
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) /etc/sysconfig/dhcp6s
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/dhcp6s.conf
%attr(750,root,root) %dir %{_localstatedir}/lib/dhcpv6
%{_mandir}/man8/dhcp6r.8*
%{_mandir}/man8/dhcp6s.8*
%{_mandir}/man5/dhcp6s.conf.5*

%files -n dhcpv6-client
%defattr(644,root,root,755)
%attr(755,root,root) /%{_sbindir}/dhcp6c
%attr(754,root,root) /etc/rc.d/init.d/dhcp6c
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/dhcp6c.conf
%{_mandir}/man8/dhcp6c.8*
%{_mandir}/man5/dhcp6c.conf.5*

%files -n libdhcp6client
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libdhcp6client-*.so.*

%files -n libdhcp6client-devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libdhcp6client.so
%{_libdir}/libdhcp6client.la
%{_includedir}/*
%{_pkgconfigdir}/libdhcp6client.pc

%files -n libdhcp6client-static
%defattr(644,root,root,755)
%{_libdir}/libdhcp6client.a
