#sbs-git:slp/pkgs/f/fontconfig fontconfig 2.6.0 70f07428c05d43eef8009f4dfbe28723b040e865
%global freetype_version 2.1.4

Name:       fontconfig
Summary:    Font configuration and customization library
Version:    2.9.0
Release:    6
Group:      System/Libraries
License:    MIT
URL:        http://fontconfig.org
Source0:    http://fontconfig.org/release/fontconfig-%{version}.tar.gz
Source1001: packaging/fontconfig.manifest
Requires(pre): /usr/bin/fc-cache, /bin/mkdir /bin/rm, /bin/grep
Requires(post): /sbin/ldconfig
Requires(postun): /sbin/ldconfig
BuildRequires:  pkgconfig(freetype2) >= %{freetype_version}
BuildRequires:  gawk
BuildRequires:  expat-devel
BuildRequires:  perl

%description
Fontconfig is designed to locate fonts within the
system and select them according to requirements specified by
applications.

%package devel
Summary:    Font configuration and customization library
Group:      Development/Libraries
Requires:   %{name} = %{version}-%{release}
Requires:   fontconfig = %{version}-%{release}
Requires:   freetype-devel >= %{freetype_version}
Requires:   pkgconfig

%description devel
The fontconfig-devel package includes the header files,
and developer docs for the fontconfig package.

Install fontconfig-devel if you want to develop programs which
will use fontconfig.

%prep
%setup -q -n %{name}-%{version}

%build
cp %{SOURCE1001} .
# We don't want to rebuild the docs, but we want to install the included ones.
export HASDOCBOOK=no

%reconfigure --disable-static \
    --with-expat=/usr \
    --with-expat-include=%{_includedir} \
    --with-expat-lib=%{_libdir} \
    --with-freetype-config=%{_bindir}/freetype-config \
    --with-add-fonts=/opt/share/fonts,/usr/share/app_fonts,/usr/share/fallback_fonts \
    --with-cache-dir=/var/cache/fontconfig \
    --with-confdir=/usr/etc/fonts \
    --disable-docs

make %{?jobs:-j%jobs}

make check
%install
rm -rf %{buildroot}

%make_install

#install -m 0644 %{SOURCE1} $RPM_BUILD_ROOT%{_sysconfdir}/fonts/conf.d
#install -m 0644 %{SOURCE2} $RPM_BUILD_ROOT%{_sysconfdir}/fonts/conf.avail
#install -m 0644 %{SOURCE3} $RPM_BUILD_ROOT%{_sysconfdir}/fonts/conf.avail
#ln -s ../conf.avail/25-unhint-nonlatin.conf $RPM_BUILD_ROOT%{_sysconfdir}/fonts/conf.d
#ln -s ../conf.avail/10-autohint.conf $RPM_BUILD_ROOT%{_sysconfdir}/fonts/conf.d
#ln -s ../conf.avail/10-antialias.conf $RPM_BUILD_ROOT%{_sysconfdir}/fonts/conf.d
#ln -s ../conf.avail/10-hinted.conf $RPM_BUILD_ROOT%{_sysconfdir}/fonts/conf.d

# move installed doc files back to build directory to package themm
# in the right place
#mv $RPM_BUILD_ROOT%{_docdir}/fontconfig/* .
#rmdir $RPM_BUILD_ROOT%{_docdir}/fontconfig/

# All font packages depend on this package, so we create
# and own /usr/share/fonts
mkdir -p $RPM_BUILD_ROOT%{_datadir}/fonts

# Remove unpackaged files. no need when configure --disable-static
#rm $RPM_BUILD_ROOT%{_libdir}/*.la
#rm $RPM_BUILD_ROOT%{_libdir}/*.a

%post
/sbin/ldconfig

umask 0022

mkdir -p /var/cache/fontconfig
# Remove stale caches
rm -f /var/cache/fontconfig/????????????????????????????????.cache-2
rm -f /var/cache/fontconfig/stamp

# remove 49-sansserif.conf to fix bmc #9024
#rm -rf /usr/%{_sysconfdir}/fonts/conf.d/49-sansserif.conf

# Force regeneration of all fontconfig cache files
# The check for existance is needed on dual-arch installs (the second
#  copy of fontconfig might install the binary instead of the first)
# The HOME setting is to avoid problems if HOME hasn't been reset
if [ -x /usr/bin/fc-cache ] && /usr/bin/fc-cache --version 2>&1 | grep -q %{version} ; then
HOME=/root /usr/bin/fc-cache -f
fi

%postun -p /sbin/ldconfig

%files
%manifest fontconfig.manifest
%defattr(-,root,root,-)
%defattr(-, root, root)
%doc README AUTHORS COPYING
%{_libdir}/libfontconfig.so.*
%{_bindir}/fc-*
/usr/%{_sysconfdir}/fonts/*
%dir /usr/%{_sysconfdir}/fonts/conf.avail
%dir %{_datadir}/fonts
%doc /usr/%{_sysconfdir}/fonts/conf.d/README
%config /usr/%{_sysconfdir}/fonts/conf.avail/*.conf
%config(noreplace) /usr/%{_sysconfdir}/fonts/conf.d/*.conf
%dir /var/cache/fontconfig

%files devel
%manifest fontconfig.manifest
%defattr(-,root,root,-)
%defattr(-, root, root)
%{_libdir}/libfontconfig.so
%{_libdir}/pkgconfig/*
%{_includedir}/fontconfig

