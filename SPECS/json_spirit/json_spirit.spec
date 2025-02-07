Summary:    A C++ JSON Parser/Generator
Name:       json_spirit
Version:    4.08
Release:    3%{?dist}
License:    MIT
URL:        https://www.codeproject.com/Articles/20027/JSON-Spirit-A-C-JSON-Parser-Generator-Implemented
Group:      Development/Tools
Vendor:     VMware, Inc.
Distribution:   Photon

Source0:    https://www.codeproject.com/KB/recipes/JSON_Spirit/json_spirit_v4.08.zip
%define sha512 %{name}=be13b0cb8471456bd6eb63fb890c9a411dd080750c234418ee23f4c9a20a4f62f8c14e2f18f2d905a88daa93ddec0378043ac7fba1ad975f210a2d4f4d973fe8

BuildRequires:  autoconf
BuildRequires:  automake
BuildRequires:  boost
BuildRequires:  boost-devel
BuildRequires:  cmake
BuildRequires:  make
BuildRequires:  gcc
BuildRequires:  unzip

Requires:       boost

%description
JSON Spirit is a C++ library that reads and writes JSON files or streams. It
is written using the Boost Spirit parser generator.

%package devel
Summary:        %{name} devel
Group:          Development/Tools
%description devel
This contains development tools and libraries for %{name}.

%prep
%autosetup -p1 -n %{name}_v%{version}

%build
# Build static lib
CPPFLAGS="-std=c++98"
%cmake \
    -DBUILD_SHARED_LIBS=OFF \
    -DCMAKE_INSTALL_LIBDIR=%{_libdir} \
    -DCMAKE_BUILD_TYPE=Debug

%cmake_build

sed -i s/"json_spirit STATIC"/"json_spirit SHARED"/g %{name}/CMakeLists.txt

CPPFLAGS="-std=c++98 -fPIC"
%cmake \
    -DBUILD_SHARED_LIBS=ON \
    -DCMAKE_INSTALL_LIBDIR=%{_libdir} \
    -DCMAKE_BUILD_TYPE=Debug

%cmake_build

%install
%cmake_install
install -v -D %{__cmake_builddir}/%{name}/libjson_spirit.so -t %{buildroot}%{_libdir}

%if 0%{?with_check}
%check
#Test waits for key press in the end.
cd %{__cmake_builddir}
json_test/json_test <<< "key_press\n"
%endif

%files
%defattr(-,root,root)
%{_libdir}/libjson_spirit.so*

%files devel
%defattr(-,root,root)
%{_includedir}/%{name}*
%{_libdir}/libjson_spirit.a

%changelog
* Sun Nov 25 2018 Ashwin H <ashwinh@vmware.com> 4.08-3
- Add %check
* Thu Jun 1  2017 Bo Gan <ganb@vmware.com> 4.08-2
- Fix file paths
* Sat Mar 25 2017 Vinay Kulkarni <kulkarniv@vmware.com> 4.08-1
- Initial version of json_spirit for Photon.
