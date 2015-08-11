%global freetype_version 2.1.4

Name:           fontconfig
Version:        2.11.1
Release:        0
License:        MIT
Summary:        Font configuration and customization library
Url:            http://fontconfig.org
Group:          Graphics & UI Framework/Fonts
Source:         %{name}-%{version}.tar.bz2
Source1001:     fontconfig.manifest
BuildRequires:  expat-devel
BuildRequires:  gawk
BuildRequires:  perl
BuildRequires:  gperf
BuildRequires:  pkgconfig(freetype2) >= %{freetype_version}
Requires(pre):  /usr/bin/fc-cache, /usr/bin/mkdir /usr/bin/rm, /usr/bin/grep, /usr/bin/chsmack

%description
Fontconfig is designed to locate fonts within the
system and select them according to requirements specified by
applications.

%package devel
Summary:        Font configuration and customization library
Group:          Graphics & UI Framework/Fonts
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
cp %{SOURCE1001} .

%build
# We don't want to rebuild the docs, but we want to install the included ones.
export HASDOCBOOK=no
%autogen --disable-static \
    --with-expat=/usr \
    --with-expat-include=%{_includedir} \
    --with-expat-lib=%{_libdir} \
    --with-freetype-config=%{_bindir}/freetype-config \
    --with-add-fonts=%{_datadir}/fonts,/usr/share/app_fonts,/usr/share/fallback_fonts \
    --with-cache-dir=/var/cache/fontconfig \
    --with-confdir=/etc/fonts \
    --with-templatedir=%{_sysconfdir}/fonts/conf.avail \
    --disable-docs

%__make %{?_smp_mflags}

%check
%__make check

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

chsmack -a System::Shared -t /var/cache/fontconfig

if [ -x /usr/bin/fc-cache ] && /usr/bin/fc-cache --version 2>&1 | grep -q %{version} ; then
HOME=/root /usr/bin/fc-cache -f
fi

%postun -p /sbin/ldconfig

%files
%manifest %{name}.manifest
%license COPYING
%{_libdir}/libfontconfig.so.*
%{_bindir}/fc-*
%{_sysconfdir}/fonts/*
%dir %{_datadir}/fonts
%doc %{_sysconfdir}/fonts/conf.d/README
%config %{_sysconfdir}/fonts/conf.avail/*.conf
%config(noreplace) %{_sysconfdir}/fonts/conf.d/*.conf
%dir %{_localstatedir}/cache/fontconfig
%{_datadir}/xml/fontconfig/fonts.dtd

%files devel
%manifest %{name}.manifest
%{_libdir}/libfontconfig.so
%{_libdir}/pkgconfig/*
%{_includedir}/fontconfig

