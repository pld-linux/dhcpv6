# TODO:
# - test it
# - pld has rc-scripts not initscripts
# - obsoletes when renaming a package
# - subpackage for relay daemon
# - use %%service
Summary:	DHCPv6 - DHCP server and client for IPv6
Summary(pl.UTF-8):	DHCPv6 - serwer i klient DHCP dla IPv6
Name:		dhcpv6
Version:	0.10
Release:	0.8
Epoch:		1
License:	GPL
Group:		Networking/Daemons
Source0:	http://dl.sourceforge.net/dhcpv6/dhcp-%{version}.tgz
# Source0-md5:	72b802d6c89e15e5cf6b0aecf46613f2
Source1:	dhcp6s.init
Source2:	dhcp6c.init
Source3:	libdhcp6client.pc
Patch0:		%{name}-redhat.patch
Patch1:		%{name}-relay.patch
Patch2:		%{name}-man.patch
Patch3:		%{name}-gethwid.patch
Patch4:		%{name}-no-strlcat.patch
Patch5:		%{name}-libdhcp6client.patch
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
Requires:	initscripts >= 7.73

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
Group:		Development/Libraries

%description -n libdhcp6client
Provides the client for the DHCPv6 protocol (RFC 3315) to support
dynamic configuration of IPv6 addresses and parameters, in a library
for invocation by other programs.

%package -n libdhcp6client-devel
Summary:	Header files for development with the DHCPv6 client library
Group:		Development/Libraries

%description -n libdhcp6client-devel
Header files for development with the DHCPv6 client library.

%package -n libdhcp6client-static
Summary:	Static DHCPv6 client library
Group:		Development/Libraries

%description -n libdhcp6client-static
Static DHCPv6 client library.

%prep
%setup -q -n dhcp-%{version}
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1
%patch5 -p1

# these things are part of glibc
rm -f ifaddrs.c ifaddrs.h queue.h

# we don't need these things
rm -f strlcat.c

sed 's/@DHCPV6_VERSION@/'%{version}'/' < %{SOURCE3} > libdhcp6client.pc

%build
%{__autoconf}
%configure \
	 \

%{__make}
%{__make} -C libdhcp6client

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_localstatedir}/lib/dhcpv6,/etc/{rc.d/init.d,sysconfig}}

%{__make} install \
	INSTALL_USER=$(id -u) \
	INSTALL_GROUP=$(id -g) \
	DESTDIR=$RPM_BUILD_ROOT

%{__make} -C libdhcp6client install \
	INSTALL_USER=$(id -u) \
	INSTALL_GROUP=$(id -g) \
	DESTDIR=$RPM_BUILD_ROOT \
	LIBDIR="%{_libdir}" \
	PKGCFGDIR="%{_pkgconfigdir}"

install dhcp6c.conf dhcp6s.conf server6_addr.conf $RPM_BUILD_ROOT%{_sysconfdir}
install dhcp6c.sysconfig $RPM_BUILD_ROOT/etc/sysconfig/dhcp6c
install dhcp6r.sysconfig $RPM_BUILD_ROOT/etc/sysconfig/dhcp6r
install dhcp6s.sysconfig $RPM_BUILD_ROOT/etc/sysconfig/dhcp6s

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
	/etc/rc.d/init.d/dhcp6s restart >/dev/null 2>&1
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


%files -n dhcpv6-client
%defattr(644,root,root,755)
%doc ReadMe dhcp6c.conf
%attr(755,root,root) /sbin/dhcp6c
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) /etc/sysconfig/dhcp6c
%attr(754,root,root) /etc/rc.d/init.d/dhcp6c
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/dhcp6c.conf
%{_mandir}/man8/dhcp6c.8*
%{_mandir}/man5/dhcp6c.conf.5*

%files -n libdhcp6client
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libdhcp6client-%{version}.so.*

%files -n libdhcp6client-devel
%defattr(644,root,root,755)
%{_includedir}/*
%{_pkgconfigdir}/libdhcp6client.pc
%attr(755,root,root) %{_libdir}/libdhcp6client.so

%files -n libdhcp6client-static
%defattr(644,root,root,755)
%{_libdir}/libdhcp6client.a
