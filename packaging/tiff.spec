Name:           tiff
Version:        4.0.3
Release:        0
License:        libtiff
Summary:        Tools for Converting from and to the Tiff Format
Url:            http://www.remotesensing.org/libtiff
Group:          Productivity/Graphics/Convertors
Source:         tiff-%{version}.tar.bz2
Source3:        baselibs.conf
Source1001: 	tiff.manifest
BuildRequires:  gcc-c++
BuildRequires:  libjpeg8-devel
BuildRequires:  libtool
BuildRequires:  lzma-devel
BuildRequires:  pkg-config
BuildRequires:  pkgconfig(zlib)
BuildRoot:      %{_tmppath}/%{name}-%{version}-build

%description
This package contains the library and support programs for the TIFF
image format.

%package -n libtiff
Summary:        The Tiff Library (with JPEG and compression support)
Group:          System/Libraries

%description -n libtiff
This package includes the tiff libraries. To link a program with
libtiff, you will have to add -ljpeg and -lz to include the necessary
libjpeg and libz in the linking process.

%package -n libtiff-devel
Summary:        Development Tools for Programs which will use the libtiff Library
Group:          Development/Libraries/C and C++
Requires:       glibc-devel
Requires:       libstdc++-devel
Requires:       libtiff = %{version}

%description -n libtiff-devel
This package contains the header files and static libraries for
developing programs which will manipulate TIFF format image files using
the libtiff library.

%prep
%setup -q
cp %{SOURCE1001} .

%build
%configure --disable-static --with-pic
make %{?_smp_mflags}

%install
mkdir -p %{buildroot}/{%{_mandir}/{man1,man3},usr/{bin,lib,include}}
%make_install
for f in `find %{buildroot}/%{_mandir} -type f -print ` ; do
  if [ `wc -l <$f` -eq 1 ] && grep -q "^\.so " $f ; then
    linkto=`sed -e "s|^\.so ||" $f`
    [ -f "`dirname $f`/$linkto" ] && ln -sf "$linkto" $f
  fi
done

rm -rf %{buildroot}%{_datadir}/doc/tiff*
rm -f %{buildroot}/%{_libdir}/*.la
find html -name "Makefile*" | xargs rm


%docs_package

%post -n libtiff -p /sbin/ldconfig

%postun -n libtiff -p /sbin/ldconfig

%files
%manifest %{name}.manifest
%defattr(-,root,root)
%{_bindir}/*

%files -n libtiff
%manifest %{name}.manifest
%license COPYRIGHT
%{_libdir}/*.so.*

%files -n libtiff-devel
%manifest %{name}.manifest
%{_includedir}/*
%{_libdir}/*.so
%{_libdir}/pkgconfig/*.pc

