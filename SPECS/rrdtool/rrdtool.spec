Summary:	Round Robin Database Tool to store and display time-series data
Name:		rrdtool
Version:	1.8.0
Release:	1%{?dist}
License:	LGPLv2 or MPLv1.1
URL:		http://oss.oetiker.ch/rrdtool/
Group:		System Environment/Libraries
Vendor:		VMware, Inc.
Distribution:	Photon

Source0:	https://github.com/oetiker/rrdtool-1.x/releases/download/v1.6.0/%{name}-%{version}.tar.gz
%define sha512 rrdtool=8ae6f94d119e8d0e1ba7f2d0738f1ba008a4880d1022f1c0c5436f662d961fceec5c42e01c241493ece3d6f55c60fd7d1d264f93e678f3cf1251201dcde027c1

BuildRequires:	pkg-config
BuildRequires:	libpng-devel
BuildRequires:	pango-devel
BuildRequires:	libxml2-devel
BuildRequires:	pixman-devel
BuildRequires:	freetype2-devel
BuildRequires:	fontconfig-devel
BuildRequires:	cairo-devel
BuildRequires:	glib-devel
BuildRequires:	systemd

Requires:	systemd

%description
RRD is the Acronym for Round Robin Database. RRD is a system to store and
display time-series data.

%package	devel
Summary:	Header and development files
Requires:	%{name} = %{version}-%{release}
%description	devel
It contains the libraries and header files to create applications

%prep
%autosetup -p1

%build
%configure \
	--disable-tcl		\
	--disable-python 	\
	--disable-perl		\
	--disable-lua		\
	--disable-examples	\
    --with-systemdsystemunitdir=%{_unitdir} \
    --disable-docs 		\
	--disable-static

make %{?_smp_mflags}

%install
make DESTDIR=%{buildroot} install %{?_smp_mflags}
find %{buildroot} -name '*.la' -delete

#%%check
#make %{?_smp_mflags} -k check

%post
/sbin/ldconfig
%systemd_post rrdcached.service

%preun
%systemd_preun rrdcached.service

%postun
/sbin/ldconfig
%systemd_postun_with_restart rrdcached.service

%files
%defattr(-,root,root)
%{_bindir}/*
%{_libdir}/*.so*
%{_unitdir}/rrdcached.service
%{_unitdir}/rrdcached.socket
%exclude %{_datadir}/locale/*

%files devel
%defattr(-,root,root)
%{_includedir}/*
%{_libdir}/*.so
%{_libdir}/pkgconfig/*.pc

%changelog
* Tue Apr 19 2022 Gerrit Photon <photon-checkins@vmware.com> 1.8.0-1
- Automatic Version Bump
* Mon Jun 22 2020 Gerrit Photon <photon-checkins@vmware.com> 1.7.2-1
- Automatic Version Bump
* Mon Sep 10 2018 Keerthana K <keerthanak@vmware.com> 1.7.0-1
- Updated to version 1.7.0
* Wed Apr 5 2017 Dheeraj Shetty <dheerajs@vmware.com> 1.6.0-1
- Initial version
