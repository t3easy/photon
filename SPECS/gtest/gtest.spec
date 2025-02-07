Summary:        Google's C++ gtest framework
Name:           gtest
Version:        1.12.1
Release:        1%{?dist}
License:        ASL 2.0
URL:            https://github.com/google/googletest
Group:          Development/Tools
Vendor:         VMware, Inc.
Distribution:   Photon

Source0:        https://github.com/google/googletest/archive/googletest-%{version}.tar.gz
%define sha512  googletest=a9104dc6c53747e36e7dd7bb93dfce51a558bd31b487a9ef08def095518e1296da140e0db263e0644d9055dbd903c0cb69380cb2322941dbfb04780ef247df9c

BuildRequires:  autoconf
BuildRequires:  automake
BuildRequires:  cmake
BuildRequires:  make
BuildRequires:  gcc

%description
Google's C++ test framework that combines the GoogleTest and GoogleMock projects.
This package provides gtest shared libraries.

%package        devel
Summary:        libgtest headers
Group:          Development/Tools

%description    devel
This contains libgtest header files.

%package        static
Summary:        libgtest static lib
Group:          Development/Tools

%description    static
This contains libgtest static library.

%package -n     gmock
Summary:        Google's C++ gmock framework
Group:          Development/Tools

%description -n gmock
Google's C++ test framework that combines the GoogleTest and GoogleMock projects.
This package provides gmock shared libraries.

%package -n     gmock-devel
Summary:        libgmock headers
Group:          Development/Tools

%description -n gmock-devel
This contains libgmock header files.

%package -n     gmock-static
Summary:        libgtest static lib
Group:          Development/Tools

%description -n gmock-static
This contains libgmock static library.

%prep
%autosetup -p1 -n googletest-release-%{version}

%build
%cmake -DBUILD_SHARED_LIBS=OFF -DCMAKE_INSTALL_LIBDIR=%{_libdir}
%cmake_build

%cmake -DBUILD_SHARED_LIBS=ON -DCMAKE_INSTALL_LIBDIR=%{_libdir}
%cmake_build

%install
%cmake_install

mv %{__cmake_builddir}/lib/*.a %{buildroot}%{_libdir}
chmod 644 %{buildroot}%{_libdir}/*.a

install -vdm 755 %{buildroot}%{_usrsrc}/gtest/src/
install -vdm 755 %{buildroot}%{_usrsrc}/gmock/src/
cp googletest/src/* %{buildroot}%{_usrsrc}/gtest/src/
cp googlemock/src/* %{buildroot}%{_usrsrc}/gmock/src/
find %{buildroot} -name '*.la' -delete

%files
%defattr(-,root,root)
%{_libdir}/libgtest.so
%{_libdir}/libgtest_main.so

%files -n gmock
%{_libdir}/libgmock.so
%{_libdir}/libgmock_main.so

%files devel
%defattr(-,root,root)
%{_includedir}/gtest/*
%{_usrsrc}/gtest/
%{_libdir}/cmake/GTest/*.cmake
%{_libdir}/pkgconfig/*.pc
%{_libdir}/libgmock.so.*
%{_libdir}/libgmock_main.so.*
%{_libdir}/libgtest.so.*
%{_libdir}/libgtest_main.so.*

%files -n gmock-devel
%{_includedir}/gmock/*
%{_usrsrc}/gmock/

%files -n gmock-static
%defattr(-,root,root)
%{_libdir}/libgmock.a
%{_libdir}/libgmock_main.a

%files static
%defattr(-,root,root)
%{_libdir}/libgtest.a
%{_libdir}/libgtest_main.a

%changelog
* Mon Jul 11 2022 Gerrit Photon <photon-checkins@vmware.com> 1.12.1-1
- Automatic Version Bump
* Mon Jun 20 2022 Shreenidhi Shedi <sshedi@vmware.com> 1.11.0-2
- Use cmake macros for build
* Mon Apr 18 2022 Gerrit Photon <photon-checkins@vmware.com> 1.11.0-1
- Automatic Version Bump
* Mon Jun 22 2020 Gerrit Photon <photon-checkins@vmware.com> 1.10.0-1
- Automatic Version Bump
* Sun Sep 23 2018 Sharath George <anishs@vmware.com> 1.8.1-2
- Add gmock subpackage
* Wed Sep 12 2018 Anish Swaminathan <anishs@vmware.com> 1.8.1-1
- Update version to 1.8.1
* Thu May 04 2017 Anish Swaminathan <anishs@vmware.com> 1.8.0-2
- Add gtest sources in devel package
* Mon Apr 10 2017 Vinay Kulkarni <kulkarniv@vmware.com> 1.8.0-1
- Initial version of libgtest package for Photon.
