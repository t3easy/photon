%global debug_package %{nil}

Summary:    Photon OS Installer
Name:       photon-os-installer
Version:    2.0
Release:    2%{?dist}
License:    Apache 2.0 and GPL 2.0
Group:      System Environment/Base
Vendor:     VMware, Inc.
Distribution:   Photon
URL:        https://github.com/vmware/photon-os-installer

Source0:    %{name}-%{version}.tar.gz
%define sha1 %{name}=0f1164e8eef1fa76990346f22d281e36964404f5

Patch0:     error_screen_selectdisk.patch
Patch1:     fix-installroot-commands.patch

BuildRequires: python3-devel
BuildRequires: python3-pyinstaller
BuildRequires: python3-requests
BuildRequires: python3-cracklib
BuildRequires: python3-curses

Requires:      zlib
Requires:      glibc

%description
This is to create rpm for installer code

%prep
%autosetup -p1

%build
pyinstaller --onefile photon-installer.spec

%install
mkdir -p %{buildroot}%{_bindir}
cp dist/photon-installer %{buildroot}%{_bindir}

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
%{_bindir}/photon-installer

%changelog
* Wed Dec 22 2021 Shreenidhi Shedi <sshedi@vmware.com> 2.0-2
- Fix tdnf installroot commands
* Sat Dec 18 2021 Shreenidhi Shedi <sshedi@vmware.com> 2.0-1
- Bump version as a part of requests & chardet upgrade
* Tue Jun 01 2021 Piyush Gupta <gpiyush@vmware.com> 1.0-7
- Support for xen block device.
* Thu Mar 04 2021 Piyush Gupta <gpiyush@vmware.com> 1.0-6
- User specified mount media.
* Tue Feb 23 2021 Piyush Gupta <gpiyush@vmware.com> 1.0-5
- Added --releasever to tdnf install command
* Fri Feb 19 2021 Piyush Gupta <gpiyush@vmware.com> 1.0-4
- Listing block devices after user accepts license.
* Fri Jan 15 2021 Piyush Gupta <gpiyush@vmware.com> 1.0-3
- Generating PRNGs through secrets module.
* Wed Dec 16 2020 Prashant S Chauhan <psinghchauha@vmware.com> 1.0-2
- Add support for insecure_installation so that rpms can be
- served from untrusted https url
* Thu Aug 06 2020 Piyush Gupta <gpiyush@vmware.com> 1.0-1
- Initial photon installer for Photon OS.
