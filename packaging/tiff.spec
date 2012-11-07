Name:           tiff
Version:        4.0.2
Release:        0
License:        HPND
Summary:        Tools for Converting from and to the Tiff Format
Url:            http://www.remotesensing.org/libtiff
Group:          Productivity/Graphics/Convertors
Source:         tiff-%{version}.tar.bz2
Source3:        baselibs.conf
Patch2:         tiff-%{version}-seek.patch
Patch3:         tiff-%{version}-tiff2pdf-colors.patch
Patch9:         tiff-%{version}-dont-fancy-upsampling.patch
Patch10:        tiff-bigendian.patch
Patch11:        tiff-%{version}-CVE-2012-3401.patch
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
%patch2 -p1
%patch3 -p1
%patch9 -p1
%patch10 -p1
%patch11

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
%defattr(-,root,root)
%{_bindir}/*

%files -n libtiff
%doc COPYRIGHT
%{_libdir}/*.so.*

%files -n libtiff-devel
%{_includedir}/*
%{_libdir}/*.so
%{_libdir}/pkgconfig/*.pc

%changelog
