Summary:        Extremely fast compression.
Name:           lz4
Version:        1.9.3
Release:        1%{?dist}
License:        BSD 2-Clause and GPLv2
URL:            http://lz4.github.io/lz4/
Group:          Applications
Vendor:         VMware, Inc.
Distribution:   Photon

Source0:        https://github.com/lz4/lz4/archive/v%{version}/%{name}-%{version}.tar.gz
%define sha1    %{name}=5a19554ef404a609123b756ddcbbb677df838f05

%description
LZ4 is lossless compression algorithm, providing compression speed at 400 MB/s per core, scalable with multi-cores CPU.
It features an extremely fast decoder, with speed in multiple GB/s per core, typically reaching RAM speed limits on multi-core systems.

%package devel
Summary:    Libraries and header files for lz4
Requires:   %{name} = %{version}-%{release}
%description devel
Static libraries and header files for the support library for lz4.

%prep
%autosetup -p1

%build
make %{?_smp_mflags} all

%install
[ %{buildroot} != "/" ] && rm -rf %{buildroot}/*
make install DESTDIR=%{buildroot} LIBDIR=%{_libdir} PREFIX=%{_prefix} %{?_smp_mflags}

%ldconfig_scriptlets

%files
%defattr(-,root,root)
%{_bindir}/*
%{_libdir}/liblz4.so.*
%{_datadir}/*
%{_mandir}/man1/*

%files devel
%defattr(-,root,root)
%{_libdir}/liblz4.so
%{_libdir}/*.a
%{_libdir}/pkgconfig/*
%{_includedir}/*

%changelog
* Tue Apr 13 2021 Gerrit Photon <photon-checkins@vmware.com> 1.9.3-1
- Automatic Version Bump
* Mon Jun 22 2020 Gerrit Photon <photon-checkins@vmware.com> 1.9.2-1
- Automatic Version Bump
* Wed Sep 05 2018 Srivatsa S. Bhat <srivatsa@csail.mit.edu> 1.8.2-1
- Update to version 1.8.2
* Wed Mar 29 2017 Michelle Wang <michellew@vmware.com> 1.7.5-1
- Update lz4 package to 1.7.5.
* Thu Dec 01 2016 Xiaolin Li <xiaolinl@vmware.com> 1.7.4-1
- Add lz4 package.
