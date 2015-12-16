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
Requires:       openssl
Requires:       smack
Requires:       coreutils
Requires(post): /usr/bin/rm
Recommends:     ca-certificates-mozilla
BuildArch:      noarch

%description
Utilities for system wide CA certificate installation

%package devel
Summary:  Devel package of ca-certificates which contains RPM macros
Group:    Development/Libraries
License:  GPL-2.0+
Requires: %name = %version

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
install -D -m 644 /dev/null %{buildroot}/%{cabundle}
install -m 644 /dev/null %{buildroot}/etc/ca-certificates.conf
install -m 755 %{SOURCE3} %{buildroot}%{_prefix}/lib/ca-certificates/update.d
ln -s %{cabundle} %{buildroot}%{usrcabundle}

install -m 755 update-ca-certificates %{buildroot}/%{_sbindir}
install -m 644 update-ca-certificates.8 %{buildroot}/%{_mandir}/man8
install -m 644 /dev/null %{buildroot}/var/lib/ca-certificates/ca-bundle.pem

mkdir -p %{buildroot}%{_sysconfdir}/rpm
%define macro_ca_certificates %{_sysconfdir}/rpm/macros.ca-certificates
touch %{buildroot}%{macro_ca_certificates}
echo "%TZ_SYS_CA_CERTS      %{etccadir}"    >> %{buildroot}%{macro_ca_certificates}
echo "%TZ_SYS_CA_CERTS_ORIG %{usrcadir}"    >> %{buildroot}%{macro_ca_certificates}
echo "%TZ_SYS_CA_BUNDLE     %{usrcabundle}" >> %{buildroot}%{macro_ca_certificates}
echo "%TZ_SYS_CA_BUNDLE_RW  %{cabundle}"    >> %{buildroot}%{macro_ca_certificates}

%post
# this is just needed for those updating Factory,
# can be removed before 11.3
if [ "$1" -ge 1 ]; then
  rm -f /etc/ca-certificates/update.d/certbundle.run
fi
# force rebuilding all certificate stores.
# This also makes sure we update the hash links in /etc/ssl/certs
# as openssl changed the hash format between 0.9.8 and 1.0
update-ca-certificates -f || true

chown root:system %{etccadir}
chmod 775 %{etccadir}
chsmack -a "System::Shared" %{etccadir}
chsmack -t %{etccadir}

%files
%manifest %{name}.manifest
%defattr(-, root, root)
%dir %{usrcadir}
%dir %{etccadir}
%license COPYING
%ghost %config(noreplace) /etc/ca-certificates.conf
%{usrcabundle}
%ghost %{cabundle}
%dir /etc/ca-certificates
%dir /etc/ca-certificates/update.d
%dir %{_prefix}/lib/ca-certificates
%dir %{_prefix}/lib/ca-certificates/update.d
%dir /var/lib/ca-certificates
%{_prefix}/lib/ca-certificates/update.d/certbundle.run
%{_sbindir}/update-ca-certificates
%{_mandir}/man8/update-ca-certificates.8*
%ghost %{cabundle}

%files devel
%config %{macro_ca_certificates}
