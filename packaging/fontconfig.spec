%global freetype_version 2.1.4

Name:           fontconfig
Version:        2.10.91
Release:        0
License:        MIT
Summary:        Font configuration and customization library
Url:            http://fontconfig.org
Group:          System/Libraries
Source:         %{name}-%{version}.tar.bz2
BuildRequires:  expat-devel
BuildRequires:  gawk
BuildRequires:  perl
BuildRequires:  pkgconfig(freetype2) >= %{freetype_version}
Requires(pre): /usr/bin/fc-cache, /usr/bin/mkdir /usr/bin/rm, /usr/bin/grep

%description
Fontconfig is designed to locate fonts within the
system and select them according to requirements specified by
applications.

%package devel
Summary:        Font configuration and customization library
Group:          Development/Libraries
Requires:       %{name} = %{version}
Requires:       fontconfig = %{version}
Requires:       freetype-devel >= %{freetype_version}
Requires:       pkg-config

%description devel
The fontconfig-devel package includes the header files,
and developer docs for the fontconfig package.

Install fontconfig-devel if you want to develop programs which
will use fontconfig.

%prep
%setup -q

%build
# We don't want to rebuild the docs, but we want to install the included ones.
export HASDOCBOOK=no

%reconfigure --disable-static \
    --with-expat=/usr \
    --with-expat-include=%{_includedir} \
    --with-expat-lib=%{_libdir} \
    --with-freetype-config=%{_bindir}/freetype-config \
    --with-add-fonts=%{_datadir}/fonts,/usr/share/app_fonts,/usr/share/fallback_fonts \
    --with-cache-dir=/var/cache/fontconfig \
    --with-confdir=/etc/fonts \
    --with-templatedir=%{_sysconfdir}/fonts/conf.avail \
    --disable-docs

make %{?_smp_mflags}

%check
make check

%install

%make_install

mkdir -p %{buildroot}%{_datadir}/fonts

%post
/sbin/ldconfig

umask 0022

mkdir -p /var/cache/fontconfig
# Remove stale caches
rm -f /var/cache/fontconfig/????????????????????????????????.cache-2
rm -f /var/cache/fontconfig/stamp

if [ -x /usr/bin/fc-cache ] && /usr/bin/fc-cache --version 2>&1 | grep -q %{version} ; then
HOME=/root /usr/bin/fc-cache -f
fi

%postun -p /sbin/ldconfig

%files
%license COPYING
%{_libdir}/libfontconfig.so.*
%{_bindir}/fc-*
%{_sysconfdir}/fonts/*
%dir %{_datadir}/fonts
%doc %{_sysconfdir}/fonts/conf.d/README
%config %{_sysconfdir}/fonts/conf.avail/*.conf
%config(noreplace) %{_sysconfdir}/fonts/conf.d/*.conf
%dir %{_localstatedir}/cache/fontconfig
/usr/share/xml/fontconfig/fonts.dtd

%files devel
%{_libdir}/libfontconfig.so
%{_libdir}/pkgconfig/*
%{_includedir}/fontconfig

