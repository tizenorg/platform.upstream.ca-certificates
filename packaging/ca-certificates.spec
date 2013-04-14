BuildRequires:  openssl
Name:           ca-certificates
%define ssletcdir %{_sysconfdir}/ssl
%define etccadir  %{ssletcdir}/certs
%define cabundle  /var/lib/ca-certificates/ca-bundle.pem
%define usrcadir  %{_datadir}/ca-certificates
License:        GPL-2.0+
Group:          Productivity/Networking/Security
Version:        1
Release:        0
Summary:        Utilities for system wide CA certificate installation
Source0:        update-ca-certificates
Source1:        update-ca-certificates.8
Source2:        GPL-2.0.txt
Source3:        certbundle.run
Url:            http://gitorious.org/opensuse/ca-certificates
Requires:       openssl
Requires(post): /usr/bin/rm
Requires(post): openssl-misc
Recommends:     ca-certificates-mozilla
BuildArch:      noarch


%description
Utilities for system wide CA certificate installation

%prep
%setup -qcT
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
ln -s %{cabundle} %{buildroot}%{ssletcdir}/ca-bundle.pem

install -m 755 update-ca-certificates %{buildroot}/%{_sbindir}
install -m 644 update-ca-certificates.8 %{buildroot}/%{_mandir}/man8
install -m 644 /dev/null %{buildroot}/var/lib/ca-certificates/ca-bundle.pem

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


%files
%defattr(-, root, root)
%dir %{usrcadir}
%dir %{etccadir}
%license COPYING
%ghost %config(noreplace) /etc/ca-certificates.conf
%{ssletcdir}/ca-bundle.pem
%ghost %{cabundle}
%dir /etc/ca-certificates
%dir /etc/ca-certificates/update.d
%dir %{_prefix}/lib/ca-certificates
%dir %{_prefix}/lib/ca-certificates/update.d
%dir /var/lib/ca-certificates
%{_prefix}/lib/ca-certificates/update.d/certbundle.run
%{_sbindir}/update-ca-certificates
%{_mandir}/man8/update-ca-certificates.8*
%ghost /var/lib/ca-certificates/ca-bundle.pem


%changelog
