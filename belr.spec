%define major 1
%define libname %mklibname %{name} %{major}
%define develname %mklibname %{name} -d

Summary:	Language recognition library
Name:		belr
Version:	0.1.3
Release:	1
License:	GPLv3
Group:		System/Libraries
URL:		https://linphone.org/
Source0:	https://linphone.org/releases/sources/belr/belr-%{version}.tar.gz
Source1:	https://linphone.org/releases/sources/belr/belr-%{version}.tar.gz.md5
# (wally) from OpenSUSE to install pkgconfig .pc file
Patch0:		belr-fix-pkgconfig.patch
# (wally) alow overriding cmake config file location from cmd line
Patch1:         belr-0.1.3-cmake-config-location.patch
BuildRequires:	cmake
BuildRequires:	pkgconfig(udev)
BuildRequires:	pkgconfig(bctoolbox)
BuildRequires:	bctoolbox-static-devel
%description
Belr aims at parsing any input formatted according to a language defined by
an ABNF grammar, such as the protocols standardised at IETF.

%package -n	%{libname}
Summary:	Language recognition library
Group:		System/Libraries

%description -n	%{libname}
Belr aims at parsing any input formatted according to a language defined by
an ABNF grammar, such as the protocols standardised at IETF.

%package -n	%{develname}
Summary:	Development files for %{name}
Group:		Development/C++
Requires:	%{libname} = %{version}-%{release}
Provides:	%{name}-devel = %{version}-%{release}

%description -n	%{develname}
This package contains development files for %{name}

%prep
%setup -qn %{name}-%{version}-0
sed -i -e 's,\r$,,' CMakeLists.txt
%apply_patches

%build
%cmake \
  -DENABLE_STATIC:BOOL=NO \
  -DENABLE_STRICT:BOOL=NO \
  -DCONFIG_PACKAGE_LOCATION:PATH=%{_libdir}/cmake/Belr
%make

%install
%makeinstall_std -C build

find %{buildroot} -name "*.la" -delete

%files
%doc README.md COPYING
%{_bindir}/belr-parse

%files -n %{libname}
%doc AUTHORS NEWS README.md COPYING
%{_libdir}/lib%{name}.so.*

%files -n %{develname}
%{_includedir}/%{name}/
%{_libdir}/lib%{name}.so
%{_libdir}/cmake/Belr/
%{_libdir}/pkgconfig/%{name}.pc

