%define major 1
%define libname %mklibname %{name}
%define devname %mklibname %{name} -d

# exclude unwanted cmake requires
%global __provides_exclude_from ^%{_datadir}/cmake/.*/Find.*cmake$

%bcond strict			1
%bcond unit_tests		1
%bcond unit_tests_install	0

Summary:	Language recognition library
Name:		belr
Version:	5.3.97
Release:	1
License:	GPLv3
Group:		System/Libraries
URL:		https://linphone.org/
Source0:	https://gitlab.linphone.org/BC/public/%{name}/-/archive/%{version}/%{name}-%{version}.tar.bz2
Patch0:		belr-5.3.6-fix-pkgconfig.patch
BuildRequires:	cmake
BuildRequires:  ninja
BuildRequires:	pkgconfig(udev)
BuildRequires:	cmake(bctoolbox)

%description
Belr aims at parsing any input formatted according to a language defined by
an ABNF grammar, such as the protocols standardised at IETF.

%files
%{_bindir}/%{name}-parse
%{_bindir}/%{name}-compiler
%if %{with unit_tests} && %{with unit_tests_install}
%{_bindir}/%{name}-tester
%{_datadir}/%{name}-tester/
%endif

#---------------------------------------------------------------------------

%package -n %{libname}
Summary:	Language recognition library
Group:		System/Libraries

%description -n %{libname}
Belr aims at parsing any input formatted according to a language defined by
an ABNF grammar, such as the protocols standardised at IETF.

%files -n %{libname}
%{_libdir}/lib%{name}.so.*
%{_datadir}/belr/grammars/belr-grammar-example.blr

#---------------------------------------------------------------------------

%package -n %{devname}
Summary:	Development files for %{name}
Group:		Development/C++
Requires:	%{libname} = %{version}-%{release}
Provides:	%{name}-devel = %{version}-%{release}

%description -n %{devname}
This package contains development files for %{name}

%files -n %{devname}
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
	-DENABLE_STRICT:BOOL=%{?with_strict:ON}%{?!with_strict:OFF} \
	-DENABLE_UNIT_TESTS:BOOL=%{?with_unit_tests:ON}%{?!with_unit_tests:OFF} \
	-DENABLE_TESTS:BOOL=%{?with_tests:ON}%{?!with_tests:OFF} \
	-G Ninja

%ninja_build

%install
%ninja_install -C build

# don't install unit tester
%if %{with unit_tests} && ! %{with unit_tests_install}
rm -f  %{buildroot}%{_bindir}/%{name}-tester
rm -fr %{buildroot}%{_datadir}/%{name}-tester/
%endif

%check
%if %{with unit_tests}
pushd build
ctest
popd
%endif

