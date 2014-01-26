#
# Conditional build:
%bcond_without	apidocs		# do not build and package API docs
#
Summary:	Library and proxy module for properly loading and sharing PKCS#11 modules
Summary(pl.UTF-8):	Biblioteka i moduł proxy do właściwego wczytywania i współdzielenia modułów PKCS#11
Name:		p11-kit
# NOTE: 0.20.x is stable, 0.21.x unstable
Version:	0.20.2
Release:	1
License:	BSD
Group:		Libraries
Source0:	http://p11-glue.freedesktop.org/releases/%{name}-%{version}.tar.gz
# Source0-md5:	757b97ee4ac0ce598661a90cd784c4f1
URL:		http://p11-glue.freedesktop.org/p11-kit.html
BuildRequires:	gettext-devel
BuildRequires:	gtk-doc >= 1.15
BuildRequires:	libffi-devel >= 3.0.0
BuildRequires:	libtasn1-devel >= 2.14
BuildRequires:	pkgconfig
BuildRequires:	pkgconfig(libffi) >= 3.0.0
Requires:	filesystem >= 4.0-28
Requires:	libtasn1 >= 2.14
Suggests:	ca-certificates
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
P11-KIT provides a way to load and enumerate PKCS#11 modules. It also
provides a standard configuration setup for installing PKCS#11 modules
in such a way that they-re discoverable.

%description -l pl.UTF-8
P11-KIT zapewnia możliwość ładowania i numeracji modułów PKCS#11.
Zapewnia też ustandaryzowaną konfigurację do instalowania modułów
PKCS#11 w taki sposób, żeby były możliwe do wykrycia.

%package devel
Summary:	Header files for P11-KIT library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki P11-KIT
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Obsoletes:	p11-kit-static

%description devel
Header files for P11-KIT library.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki P11-KIT.

%package apidocs
Summary:	P11-KIT API documentation
Summary(pl.UTF-8):	Dokumentacja API biblioteki P11-KIT
Group:		Documentation
Requires:	gtk-doc-common

%description apidocs
API and internal documentation for P11-KIT library.

%description apidocs -l pl.UTF-8
Dokumentacja API biblioteki P11-KIT.

%prep
%setup -q

%build
%configure \
	%{!?with_apidocs:--disable-gtk-doc} \
	--disable-silent-rules \
	--with-html-dir=%{_gtkdocdir} \
	--with-trust-paths=/etc/certs/ca-certificates.crt
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_sysconfdir}/pkcs11/modules

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

# obsoleted by pkg-config
%{__rm} $RPM_BUILD_ROOT%{_libdir}/libp11-kit.la
# dlopened module
%{__rm} $RPM_BUILD_ROOT%{_libdir}/pkcs11/*.la

%{__mv} $RPM_BUILD_ROOT%{_sysconfdir}/pkcs11/pkcs11.conf{.example,}

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc AUTHORS COPYING ChangeLog NEWS README
%attr(755,root,root) %{_bindir}/p11-kit
%attr(755,root,root) %{_bindir}/trust
%attr(755,root,root) %{_libdir}/libp11-kit.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libp11-kit.so.0
%attr(755,root,root) %{_libdir}/p11-kit-proxy.so
%dir %{_sysconfdir}/pkcs11
%dir %{_sysconfdir}/pkcs11/modules
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/pkcs11/pkcs11.conf
%attr(755,root,root) %{_libdir}/pkcs11/p11-kit-trust.so
%dir %{_libdir}/p11-kit
%attr(755,root,root) %{_libdir}/p11-kit/trust-extract-compat
%dir %{_datadir}/p11-kit
%dir %{_datadir}/p11-kit/modules
%{_datadir}/p11-kit/modules/p11-kit-trust.module

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libp11-kit.so
%{_includedir}/p11-kit-1
%{_pkgconfigdir}/p11-kit-1.pc

%if %{with apidocs}
%files apidocs
%defattr(644,root,root,755)
%{_gtkdocdir}/p11-kit
%endif
