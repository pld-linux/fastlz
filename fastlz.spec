#
# Conditional build:
%bcond_without	tests		# build without tests

%define	rel	1
%define	rdate   20070619
%define	svnrev 12
Summary:	Portable real-time compression library
Name:		fastlz
Version:	0.1.0
Release:	0.r%{svnrev}.%{rdate}.%{rel}
License:	MIT
Group:		Libraries
# svn export -r 12 http://fastlz.googlecode.com/svn/trunk/ fastlz-12
# tar cjf fastlz-12.tar.bz2 fastlz-12
Source0:	http://pkgs.fedoraproject.org/repo/pkgs/fastlz/%{name}-%{svnrev}.tar.bz2/592bdf20af83c0124f19b55d0346f266/%{name}-%{svnrev}.tar.bz2
# Source0-md5:	592bdf20af83c0124f19b55d0346f266
URL:		http://fastlz.org/
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define abi    0

%description
FastLZ is a lossless data compression library designed for real-time
compression and decompression. It favors speed over compression ratio.
Decompression requires no memory. Decompression algorithm is very
simple, and thus extremely fast.

%package devel
Summary:	Header files and development libraries for %{name}
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description devel
This package contains the header files and development libraries for
%{name}.

%prep
%setup -q -n %{name}-%{svnrev}

%build
# Build the shared library
%{__cc} %{rpmcflags} -fPIC -c fastlz.c  -o fastlz.o
%{__cc} %{rpmcflags} -fPIC -shared -Wl,-soname -Wl,lib%{name}.so.%{abi} -o lib%{name}.so.%{abi} fastlz.o
ln -s lib%{name}.so.%{abi} lib%{name}.so

# Build the commands for test
%{__cc} %{rpmcflags} -fPIC 6pack.c   -L. -l%{name} -o 6pack
%{__cc} %{rpmcflags} -fPIC 6unpack.c -L. -l%{name} -o 6unpack

%if %{with tests}
export LD_LIBRARY_PATH=$PWD
cp %{name}.c tmpin
./6pack -v
./6unpack -v

: Compress
./6pack -1 tmpin tmpout1
./6pack -2 tmpin tmpout2

: Uncompress 1
rm tmpin
./6unpack tmpout1
diff %{name}.c tmpin

: Uncompress 2
rm tmpin
./6unpack tmpout2
diff %{name}.c tmpin
%endif

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_libdir},%{_includedir}}

install -p lib%{name}.so.%{abi} $RPM_BUILD_ROOT%{_libdir}
ln -s lib%{name}.so.%{abi} $RPM_BUILD_ROOT%{_libdir}/lib%{name}.so
cp -p %{name}.h $RPM_BUILD_ROOT%{_includedir}

# Don't install the commands, as we obviously don't need more compression tools

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc LICENSE
%attr(755,root,root) %{_libdir}/libfastlz.so.0

%files devel
%defattr(644,root,root,755)
%{_libdir}/libfastlz.so
%{_includedir}/fastlz.h
