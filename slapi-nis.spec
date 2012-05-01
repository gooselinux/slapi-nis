%if 0%{?fedora} >= 14 || 0%{?rhel} >= 6
%define ldap_impl openldap
%else
%define ldap_impl mozldap
%endif

Name:		slapi-nis
Version:	0.23
Release:	1%{?dist}
Summary:	NIS Server and Schema Compatibility plugins for Directory Server
Group:		System Environment/Daemons
License:	GPLv2
URL:		http://slapi-nis.fedorahosted.org/
Source0:	https://fedorahosted.org/releases/s/l/slapi-nis/slapi-nis-%{version}.tar.gz
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires:	389-ds-base-devel, %{ldap_impl}-devel, tcp_wrappers-devel
BuildRequires:	nspr-devel, nss-devel

%description
This package provides two plugins for Red Hat and 389 Directory Server.

The NIS Server plugin allows the directory server to act as a NIS server
for clients, dynamically generating and updating NIS maps according to
its configuration and the contents of the DIT, and serving the results to
clients using the NIS protocol as if it were an ordinary NIS server.

The Schema Compatibility plugin allows the directory server to provide an
alternate view of entries stored in part of the DIT, optionally adding,
dropping, or renaming attribute values, and optionally retrieving values
for attributes from multiple entries in the tree.

%prep
%setup -q

%build
%configure --disable-static --with-tcp-wrappers --with-ldap=%{ldap_impl}
make %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT
rm $RPM_BUILD_ROOT/%{_libdir}/dirsrv/plugins/*.la

%if 0
# ns-slapd doesn't want to start in koji, so no tests get run
%check
make check
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)
%doc COPYING NEWS README STATUS doc/*.txt doc/examples/*.ldif
%{_libdir}/dirsrv/plugins/*.so
%{_sbindir}/nisserver-plugin-defs

%changelog
* Thu Mar 31 2011 Nalin Dahyabhai <nalin@redhat.com> - 0.23-1
- speed up building compat entries with attributes with thousands of literal
  values (#692690)

* Thu Jan  6 2011 Nalin Dahyabhai <nalin@redhat.com> - 0.22-1
- fix a number of scanner-uncovered defects

* Thu Jan  6 2011 Nalin Dahyabhai <nalin@redhat.com> - 0.21-2
- make sure we always pull in nss-devel and nspr-devel, and the right
  ldap toolkit for the Fedora or RHEL version

* Tue Nov 18 2010 Nalin Dahyabhai <nalin@redhat.com> - 0.21-1
- update to 0.21
  - schema-compat: don't look at standalone compat containers for a search,
    since we'll already have looked at the group container

* Tue Nov 18 2010 Nalin Dahyabhai <nalin@redhat.com> - 0.20-1
- update to 0.20
  - add a deref_f function

* Mon Nov 17 2010 Nalin Dahyabhai <nalin@redhat.com> - 0.19-1
- fix a brown-paper-bag crash

* Mon Nov 17 2010 Nalin Dahyabhai <nalin@redhat.com> - 0.18-1
- update to 0.18
  - add a deref_rf function
  - schema-compat: don't respond to search requests for which there's no backend
  - schema-compat: add the ability to do standalone compat containers

* Wed Nov 17 2010 Nalin Dahyabhai <nalin@redhat.com> - 0.17-6
- revert that last change, it's unnecessary

* Thu Nov 11 2010 Nalin Dahyabhai <nalin@redhat.com> - 0.17-5
- build against either 389-ds-base or redhat-ds-base, whichever is probably
  more appropriate here

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.17-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Jul 15 2009 Nalin Dahyabhai <nalin@redhat.com> - 0.17-3
- change buildreq from fedora-ds-base-devel to 389-ds-base-devel, which
  should avoid multilib conflicts from installing both arches of the new
  package (#511504)

* Tue Jul 14 2009 Nalin Dahyabhai <nalin@redhat.com> - 0.17-2
- fixup changelog entries that resemble possible macro invocations

* Thu May 14 2009 Nalin Dahyabhai <nalin@redhat.com> - 0.17-1
- actually send portmap registrations to the right server

* Thu May 14 2009 Nalin Dahyabhai <nalin@redhat.com> - 0.16-1
- fix NIS server startup problem when no port is explicitly configured and
  we're using portmap instead of rpcbind (#500903)

* Fri May  8 2009 Nalin Dahyabhai <nalin@redhat.com> - 0.15-1
- fix %%deref and %%referred to fail rather than return a valid-but-empty
  result when they fail to evaluate (reported by Rob Crittenden)

* Wed May  6 2009 Nalin Dahyabhai <nalin@redhat.com> - 0.14-1
- correctly handle being loaded but disabled (#499404)

* Thu Apr 30 2009 Nalin Dahyabhai <nalin@redhat.com> - 0.13-1
- update to 0.13, reworking %%link() to correct some bugs (#498432)

* Thu Apr 30 2009 Nalin Dahyabhai <nalin@redhat.com> - 0.12-1
- correct test suite failures that 0.11 started triggering

* Tue Apr 28 2009 Nalin Dahyabhai <nalin@redhat.com> - 0.11-1
- update to 0.11 (#497904)

* Wed Mar  4 2009 Nalin Dahyabhai <nalin@redhat.com> - 0.10-1
- update to 0.10

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Tue Dec  9 2008 Nalin Dahyabhai <nalin@redhat.com> - 0.8.5-2
- make the example nsslapd-pluginpath values the same on 32- and 64-bit
  systems, because we can depend on the directory server "knowing" which
  directory to search for the plugins

* Mon Dec  8 2008 Nalin Dahyabhai <nalin@redhat.com> - 0.8.5-1
- update to 0.8.5 to suppress duplicate values for attributes in the schema
  compatibility plugin

* Thu Dec  4 2008 Nalin Dahyabhai <nalin@redhat.com> - 0.8.4-1
- update to 0.8.4 to fix:
  - problems updating references, particularly those for %%referred() (#474478)
  - inability to notice internal add/modify/modrdn/delete operations (really
    this time) (#474426)

* Wed Dec  3 2008 Nalin Dahyabhai <nalin@redhat.com> - 0.8.3-1
- update to 0.8.3 to also notice and reflect changes caused by internal
  add/modify/modrdn/delete operations
 
* Wed Nov 19 2008 Nalin Dahyabhai <nalin@redhat.com> - 0.8.2-1
- update to 0.8.2 to remove a redundant read lock in the schema-compat plugin

* Fri Nov  7 2008 Nalin Dahyabhai <nalin@redhat.com> - 0.9-1
- update to 0.9

* Fri Oct  3 2008 Nalin Dahyabhai <nalin@redhat.com> - 0.8.1-1
- update to 0.8.1 to fix a heap corruption (Rich Megginson)

* Wed Aug  6 2008 Nalin Dahyabhai <nalin@redhat.com> - 0.8-1
- update to 0.8

* Wed Aug  6 2008 Nalin Dahyabhai <nalin@redhat.com> - 0.7-1
- update to 0.7

* Wed Jul 23 2008 Nalin Dahyabhai <nalin@redhat.com> - 0.6-1
- rebuild (and make rpmlint happy)

* Wed Jul  9 2008 Nalin Dahyabhai <nalin@redhat.com> - 0.2-1
- initial package
