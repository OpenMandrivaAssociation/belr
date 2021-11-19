%define major 1
%define libname %mklibname %{name} %{major}
%define develname %mklibname %{name} -d

Summary:	Language recognition library
Name:		belr
Version:	5.0.51
Release:	1
License:	GPLv3
Group:		System/Libraries
URL:		https://linphone.org/
Source0:	https://gitlab.linphone.org/BC/public/%{name}/-/archive/%{version}/%{name}-%{version}.tar.bz2
# (wally) from OpenSUSE to install pkgconfig .pc file
Patch0:		belr-fix-pkgconfig.patch
BuildRequires:	cmake
BuildRequires:	pkgconfig(udev)
BuildRequires:	bctoolbox-static-devel
BuildRequires:  ninja

%description
Belr aims at parsing any input formatted according to a language defined by
an ABNF grammar, such as the protocols standardised at IETF.

%files
%{_bindir}/belr-parse
%{_bindir}/belr-compiler

#---------------------------------------------------------------------------

%package -n %{libname}
Summary:	Language recognition library
Group:		System/Libraries

%description -n %{libname}
Belr aims at parsing any input formatted according to a language defined by
an ABNF grammar, such as the protocols standardised at IETF.

%files -n %{libname}
%{_libdir}/lib%{name}.so.*

#---------------------------------------------------------------------------

%package -n %{develname}
Summary:	Development files for %{name}
Group:		Development/C++
Requires:	%{libname} = %{version}-%{release}
Provides:	%{name}-devel = %{version}-%{release}

%description -n %{develname}
This package contains development files for %{name}

%files -n %{develname}
%doc README.md
%{_includedir}/%{name}/
%{_libdir}/lib%{name}.so
%{_libdir}/cmake/?elr/
%{_libdir}/pkgconfig/%{name}.pc

#---------------------------------------------------------------------------

%prep
%autosetup -p1
sed -i -e 's,\r$,,' CMakeLists.txt

%build
%cmake \
  -DENABLE_STATIC:BOOL=NO \
  -DENABLE_STRICT:BOOL=NO \
  -DENABLE_UNIT_TESTS=NO \
  -DENABLE_TESTS:BOOL=NO \
  -G Ninja

%ninja_build

%install
%ninja_install -C build

find %{buildroot} -name "*.la" -delete
