#
# Conditional build:
%bcond_without	apidocs		# do not build and package API docs
#
Summary:	Library and proxy module for properly loading and sharing PKCS#11 modules
Summary(pl.UTF-8):	Biblioteka i moduł proxy do właściwego wczytywania i współdzielenia modułów PKCS#11
Name:		p11-kit
# NOTE: 0.22.x is stable, 0.23.x used to be unstable  ...but current stable gnutls requires 0.23.x and 0.23.11+ is declared stable in NEWS
Version:	0.23.22
Release:	1
License:	BSD
Group:		Libraries
#Source0Download: https://github.com/p11-glue/p11-kit/releases
Source0:	https://github.com/p11-glue/p11-kit/releases/download/%{version}/%{name}-%{version}.tar.xz
# Source0-md5:	03f93a4eb62127b5d40e345c624a0665
URL:		https://p11-glue.github.io/p11-glue/p11-kit.html
BuildRequires:	gettext-tools >= 0.19.8
BuildRequires:	gtk-doc >= 1.15
BuildRequires:	libffi-devel >= 3.0.0
BuildRequires:	libtasn1-devel >= 2.14
BuildRequires:	pkgconfig >= 1:0.29
BuildRequires:	pkgconfig(libffi) >= 3.0.0
BuildRequires:	rpm-build >= 4.6
BuildRequires:	rpmbuild(macros) >= 1.673
BuildRequires:	systemd-devel >= 1:209
BuildRequires:	tar >= 1:1.22
BuildRequires:	xz
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
BuildArch:	noarch

%description apidocs
API and internal documentation for P11-KIT library.

%description apidocs -l pl.UTF-8
Dokumentacja API biblioteki P11-KIT.

%package -n bash-completion-p11-kit
Summary:	Bash completion for p11-kit commands
Summary(pl.UTF-8):	Bashowe uzupełnianie parametrów poleceń p11-kit
Group:		Applications/Shells
Requires:	%{name} = %{version}-%{release}
Requires:	bash-completion >= 2.0
BuildArch:	noarch

%description -n bash-completion-p11-kit
Bash completion for p11-kit commands (p11-kit and trust).

%description -n bash-completion-p11-kit -l pl.UTF-8
Bashowe uzupełnianie parametrów poleceń p11-kit (p11-kit i trust).

%prep
%setup -q

%build
%configure \
	bashcompdir=%{bash_compdir} \
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
%attr(755,root,root) %{_libdir}/pkcs11/p11-kit-client.so
%attr(755,root,root) %{_libdir}/pkcs11/p11-kit-trust.so
%dir %{_libexecdir}/p11-kit
%attr(755,root,root) %{_libexecdir}/p11-kit/p11-kit-remote
%attr(755,root,root) %{_libexecdir}/p11-kit/p11-kit-server
%attr(755,root,root) %{_libexecdir}/p11-kit/trust-extract-compat
%dir %{_datadir}/p11-kit
%dir %{_datadir}/p11-kit/modules
%{_datadir}/p11-kit/modules/p11-kit-trust.module
%{systemduserunitdir}/p11-kit-server.service
%{systemduserunitdir}/p11-kit-server.socket

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

%files -n bash-completion-p11-kit
%defattr(644,root,root,755)
%{bash_compdir}/p11-kit
%{bash_compdir}/trust
