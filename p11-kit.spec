#
# Conditional build:
%bcond_without	apidocs		# API documentation (gtk-doc based)
%bcond_without	doc		# man pages
%bcond_without	systemd		# systemd support
%bcond_without	tests		# test suite
#
Summary:	Library and proxy module for properly loading and sharing PKCS#11 modules
Summary(pl.UTF-8):	Biblioteka i moduł proxy do właściwego wczytywania i współdzielenia modułów PKCS#11
Name:		p11-kit
Version:	0.26.5
Release:	1
License:	BSD
Group:		Libraries
#Source0Download: https://github.com/p11-glue/p11-kit/releases
Source0:	https://github.com/p11-glue/p11-kit/releases/download/%{version}/%{name}-%{version}.tar.xz
# Source0-md5:	308306e889850bff08fae74ae7897a21
URL:		https://p11-glue.github.io/p11-glue/p11-kit.html
%{?with_doc:BuildRequires:	docbook-style-xsl}
BuildRequires:	gettext-tools >= 0.19.8
%{?with_apidocs:BuildRequires:	gtk-doc >= 1.15}
BuildRequires:	libffi-devel >= 3.0.0
BuildRequires:	libtasn1-devel >= 2.14
%{?with_doc:BuildRequires:	libxslt-progs}
BuildRequires:	meson >= 0.51
BuildRequires:	ninja >= 1.5
BuildRequires:	pkgconfig >= 1:0.29
BuildRequires:	python3 >= 1:3.6
BuildRequires:	rpm-build >= 4.6
BuildRequires:	rpmbuild(macros) >= 2.042
%{?with_systemd:BuildRequires:	systemd-devel >= 1:209}
BuildRequires:	tar >= 1:1.22
BuildRequires:	xz
Requires(post,preun):	systemd-units >= 1:250.1
Requires:	filesystem >= 4.0-28
Requires:	libtasn1%{?_isa} >= 2.14
Requires:	systemd-units >= 1:250.1
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
Requires:	%{name}%{?_isa} = %{version}-%{release}
Obsoletes:	p11-kit-static < 0.9

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
Requires:	bash-completion >= 1:2.0
BuildArch:	noarch

%description -n bash-completion-p11-kit
Bash completion for p11-kit commands (p11-kit and trust).

%description -n bash-completion-p11-kit -l pl.UTF-8
Bashowe uzupełnianie parametrów poleceń p11-kit (p11-kit i trust).

%package -n zsh-completion-p11-kit
Summary:	Zsh completion for p11-kit commands
Summary(pl.UTF-8):	Zshowe uzupełnianie parametrów poleceń p11-kit
Group:		Applications/Shells
Requires:	%{name} = %{version}-%{release}
Requires:	zsh
BuildArch:	noarch

%description -n zsh-completion-p11-kit
Zsh completion for p11-kit commands (p11-kit and trust).

%description -n zsh-completion-p11-kit -l pl.UTF-8
Zshowe uzupełnianie parametrów poleceń p11-kit (p11-kit i trust).

%prep
%setup -q

%build
%meson \
	-Dbash_completion=enabled \
	-Dbashcompdir=%{bash_compdir} \
	-Dglib_prefix=%{_prefix} \
	-Dgtk_doc=%{__true_false apidocs} \
	-Dman=%{__true_false doc} \
	-Dsystemd=%{__enabled_disabled systemd} \
	-Dtest=%{__true_false tests} \
	-Dtrust_paths=/etc/certs/ca-certificates.crt \
	-Dzsh_completion=enabled \
	-Dzshcompdir=%{zsh_compdir}

%meson_build

%if %{with tests}
%meson_test
%endif

%install
rm -rf $RPM_BUILD_ROOT
%meson_install

install -d $RPM_BUILD_ROOT%{_sysconfdir}/pkcs11/modules

%{__mv} $RPM_BUILD_ROOT%{_sysconfdir}/pkcs11/pkcs11.conf{.example,}

# upstream installs a placeholder meant to be replaced by the distribution's
# update command
ln -sf %{_sbindir}/update-ca-certificates $RPM_BUILD_ROOT%{_libexecdir}/p11-kit/trust-extract-compat

%find_lang %{name}

%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/ldconfig
%systemd_user_post p11-kit-server.service p11-kit-server.socket

%preun
%systemd_user_preun p11-kit-server.service p11-kit-server.socket

%postun	-p /sbin/ldconfig

%files -f %{name}.lang
%defattr(644,root,root,755)
%doc AUTHORS COPYING ChangeLog NEWS README
%attr(755,root,root) %{_bindir}/p11-kit
%attr(755,root,root) %{_bindir}/trust
%if %{with doc}
%{_mandir}/man1/trust.1*
%{_mandir}/man5/pkcs11.conf.5*
%{_mandir}/man8/p11-kit.8*
%endif
%{_libdir}/libp11-kit.so.*.*.*
%ghost %{_libdir}/libp11-kit.so.0
%{_libdir}/p11-kit-proxy.so
%{_libdir}/pkcs11/p11-kit-client.so
%{_libdir}/pkcs11/p11-kit-trust.so
%dir %{_sysconfdir}/pkcs11
%dir %{_sysconfdir}/pkcs11/modules
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/pkcs11/pkcs11.conf
%dir %{_libexecdir}/p11-kit
%attr(755,root,root) %{_libexecdir}/p11-kit/p11-kit-remote
%attr(755,root,root) %{_libexecdir}/p11-kit/p11-kit-server
%attr(755,root,root) %{_libexecdir}/p11-kit/trust-extract-compat
%dir %{_datadir}/p11-kit
%dir %{_datadir}/p11-kit/modules
%{_datadir}/p11-kit/modules/p11-kit-trust.module
%if %{with systemd}
%{systemduserunitdir}/p11-kit-server.service
%{systemduserunitdir}/p11-kit-server.socket
%endif

%files devel
%defattr(644,root,root,755)
%{_libdir}/libp11-kit.so
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

%files -n zsh-completion-p11-kit
%defattr(644,root,root,755)
%{zsh_compdir}/_p11-kit
%{zsh_compdir}/_trust
