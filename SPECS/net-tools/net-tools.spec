Summary:    Networking Tools
Name:       net-tools
Version:    1.60
Release:    13%{?dist}
License:    GPLv2+
URL:        http://net-tools.sourceforge.net
Group:      System Environment/Base
Vendor:     VMware, Inc.
Distribution:   Photon

Source0:    http://www.tazenda.demon.co.uk/phil/net-tools/%{name}-%{version}.tar.bz2
%define sha512  %{name}=8e1ae9bca726ad7d795a06c58388f9e11c1d617d94eebb9ed18bd11e5f34c6541e1ffe631706c407996db86e78df6e5cf1968a2d90b242b473596fda3b6d1eae

Patch0:     Bug-632660-netstat.c-long_udp6_addr.patch
Patch1:     CVS-20020730-route.c_opts_64.patch
Patch2:     CVS-20030911-nameif.c_sync.patch
Patch3:     CVS-20031011-hostname.c_sync.patch
Patch4:     CVS-20051204-arp.c_sync.patch
Patch5:     CVS-20051204-slttach.c_sync.patch
Patch6:     CVS-20060927-mii-tool.c_sync.patch
Patch7:     CVS-20061011-includes_sync.patch
Patch8:     CVS-20061011-ipmaddr.c_buffer_overflow.patch
Patch9:     CVS-20070316-netstat.c_sync.patch
Patch10:    CVS-20071202-rarp.c_sync.patch
Patch11:    CVS-20081002-ifconfig.c_sync.patch
Patch12:    CVS-20081003-statistics.c_sync.patch
Patch13:    CVS-lib_sync.patch
Patch14:    CVS-20081003-config.in_sync.patch
Patch15:    CVS-20081002-manpages_sync.patch
Patch16:    netstat.c-assorted_changes.patch
Patch17:    Bug-254243-netstat.c-wide-opt.patch
Patch18:    netstat.c-local_changes.patch
Patch19:    translations.patch
Patch20:    lib_local_changes.patch
Patch21:    local-manpages.patch
Patch22:    Bug-345331-socket_overflow.patch
Patch23:    Bug-569509-iface_overflow.patch
Patch24:    Add_missing_headers.patch
Patch25:    proper-uts-check.patch
Patch26:    fix-fprintf.patch
Patch27:    Bug-747006-inet6_sr.c-buffer-overflows.patch
Patch28:    Bug-561161-statistics.c-long_numbers.patch
Patch29:    Bug-508110-inet6.c-initialize_fields.patch
Patch30:    Ubuntu_unit_conversion.patch

Obsoletes:  inetutils

Conflicts:      toybox < 0.8.2-2

%description
The Net-tools package is a collection of programs for controlling the network subsystem of the Linux kernel.

%prep
%autosetup -p1

%build
# make doesn't support _smp_mflags
yes "" | make config

sed -i -e 's|HAVE_IP_TOOLS 0|HAVE_IP_TOOLS 1|g' \
       -e 's|HAVE_AFINET6 0|HAVE_AFINET6 1|g' \
       -e 's|HAVE_MII 0|HAVE_MII 1|g' config.h

sed -i -e 's|#define HAVE_HWSTRIP 1|#define HAVE_HWSTRIP 0|g' \
       -e 's|#define HAVE_HWTR 1|#define HAVE_HWTR 0|g' config.h

sed -i -e 's|# HAVE_IP_TOOLS=0|HAVE_IP_TOOLS=1|g' \
       -e 's|# HAVE_AFINET6=0|HAVE_AFINET6=1|g' \
       -e 's|# HAVE_MII=0|HAVE_MII=1|g' config.make

sed -i 's|#include <netinet/ip.h>|//#include <netinet/ip.h>|g' iptunnel.c

# make doesn't support _smp_mflags
make

%install
# make doesn't support _smp_mflags
make BASEDIR=%{buildroot}%{_usr} installbin
# make doesn't support _smp_mflags
make BASEDIR=%{buildroot} installdata

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%clean
rm -rf %{buildroot}/*

%files
%defattr(-,root,root)
%{_bindir}/*
%{_sbindir}/*
%{_mandir}/man1/*
%{_mandir}/man5/*
%{_mandir}/man8/*

%changelog
* Wed Feb 23 2022 Shreenidhi Shedi <sshedi@vmware.com> 1.60-13
- Fix binary path
* Thu Apr 16 2020 Alexey Makhalov <amakhalov@vmware.com> 1.60-12
- Do not conflict with toybox >= 0.8.2-2
* Mon Oct 02 2017 Alexey Makhalov <amakhalov@vmware.com> 1.60-11
- Added conflicts toybox
* Wed Dec 14 2016 Alexey Makhalov <amakhalov@vmware.com> 1.60-10
- Fix compilation issue with linux-4.9
* Wed Nov 16 2016 Alexey Makhalov <amakhalov@vmware.com> 1.60-9
- Remove iputils deps.
* Tue Oct 04 2016 ChangLee <changLee@vmware.com> 1.60-8
- Modified %check
* Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> 1.60-7
- GA - Bump release of all rpms
* Thu Feb 4 2016 Alexey Makhalov <amakhalov@vmware.com> 1.60-6
- Apply all patches from 1.60-26ubuntu1.
* Fri Jan 22 2016 Alexey Makhalov <amakhalov@vmware.com> 1.60-5
- Added net-tools-1.60-manydevs.patch
* Fri Nov 6 2015 Alexey Makhalov <amakhalov@vmware.com> 1.60-4
- Added ipv6 support. Include hostname and dnshostname.
* Thu Oct 22 2015 Harish Udaiya Kumar <hudaiyakumar@vmware.com> 1.60-3
- Added changes to replace inetutils with net-tools
* Thu Jul 30 2015 Divya Thaluru <dthaluru@vmware.com> 1.60-2
- Disable building with parallel threads
* Mon Jul 13 2015 Divya Thaluru <dthaluru@vmware.com> 1.60-1
- Initial build. First version
