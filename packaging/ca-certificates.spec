BuildRequires:  openssl
BuildRequires:  pkgconfig(libtzplatform-config)
Name:           ca-certificates
License:        GPL-2.0+
Group:          Security/Certificate Management
Version:        1
Release:        0
Summary:        Utilities for system wide CA certificate installation
Source0:        update-ca-certificates
Source1:        update-ca-certificates.8
Source2:        GPL-2.0.txt
Source3:        certbundle.run
Source1001:     ca-certificates.manifest
Url:            http://gitorious.org/opensuse/ca-certificates
Recommends:     ca-certificates-mozilla
BuildArch:      noarch

%description
Utilities for system wide CA certificate installation

%package devel
Summary:  Devel package of ca-certificates which contains RPM macros
Group:    Development/Libraries
License:  GPL-2.0+
BuildRequires: %name = %version

%description devel
ca-certificates devel package which contains RPM macros
for ca-bundle and ssl certs directory

# sync ssletcdir with openssldir
%define ssletcdir %{_sysconfdir}/ssl

%define etccadir    %{ssletcdir}/certs
%define usrcadir    %{_datadir}/ca-certificates/certs
%define cabundle    /var/lib/ca-certificates/ca-bundle.pem
%define usrcabundle %{ssletcdir}/ca-bundle.pem

%prep
%setup -qcT
cp %{SOURCE1001} .
install -m 755 %{SOURCE0} .
install -m 644 %{SOURCE1} .
install -m 644 %{SOURCE2} COPYING

%build


%install
mkdir -p %{buildroot}/%{etccadir}
mkdir -p %{buildroot}/%{usrcadir}
mkdir -p %{buildroot}/%{_sbindir}
mkdir -p %{buildroot}/%{_mandir}/man8
mkdir -p %{buildroot}/etc/ca-certificates/update.d
mkdir -p %{buildroot}%{_prefix}/lib/ca-certificates/update.d
mkdir -p %{buildroot}/var/lib/ca-certificates
install -m 644 /dev/null %{buildroot}/etc/ca-certificates.conf
install -m 755 %{SOURCE3} %{buildroot}%{_prefix}/lib/ca-certificates/update.d
ln -s %{cabundle} %{buildroot}%{usrcabundle}

install -m 755 update-ca-certificates %{buildroot}/%{_sbindir}
install -m 644 update-ca-certificates.8 %{buildroot}/%{_mandir}/man8

mkdir -p %{buildroot}%{_sysconfdir}/rpm
%define macro_ca_certificates %{_sysconfdir}/rpm/macros.ca-certificates
touch %{buildroot}%{macro_ca_certificates}
echo "%TZ_SYS_CA_CERTS      %{etccadir}"    >> %{buildroot}%{macro_ca_certificates}
echo "%TZ_SYS_CA_CERTS_ORIG %{usrcadir}"    >> %{buildroot}%{macro_ca_certificates}
echo "%TZ_SYS_CA_BUNDLE     %{usrcabundle}" >> %{buildroot}%{macro_ca_certificates}
echo "%TZ_SYS_CA_BUNDLE_RW  %{cabundle}"    >> %{buildroot}%{macro_ca_certificates}

%files
%manifest %{name}.manifest
%defattr(-, root, root)
%license COPYING
%dir %{usrcadir}
%dir %attr(775, root, system) %{etccadir}
%dir /var/lib/ca-certificates
%{usrcabundle}

%files devel
%config %{macro_ca_certificates}
%ghost %config(noreplace) /etc/ca-certificates.conf
%dir /etc/ca-certificates
%dir /etc/ca-certificates/update.d
%dir %{_prefix}/lib/ca-certificates
%dir %{_prefix}/lib/ca-certificates/update.d
%{_prefix}/lib/ca-certificates/update.d/certbundle.run
%{_sbindir}/update-ca-certificates
%{_mandir}/man8/update-ca-certificates.8*
