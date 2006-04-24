Name: ices
Version: 2.0.1
Release: 2%{?dist}
Summary: Source streaming for Icecast
Group: System Environment/Daemons
License: GPL
URL: http://www.icecast.org
Source0: http://downloads.us.xiph.org/releases/ices/ices-2.0.1.tar.bz2
Source1: ices.init
Source2: ices.logrotate
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires: libxml2-devel, libshout-devel >= 2.0, libvorbis-devel,
BuildRequires: alsa-lib-devel, pkgconfig, zlib-devel, libogg-devel
BuildRequires: libtheora-devel, speex-devel
Requires: streaming-server
Requires(post): /sbin/chkconfig
Requires(post): /sbin/service
Requires(preun): /sbin/chkconfig
Requires(preun): /sbin/service

%description
IceS is a source client for a streaming server. The purpose of this client is
to provide an audio stream to a streaming server such that one or more
listeners can access the stream. With this layout, this source client can be
situated remotely from the icecast server.

The primary example of a streaming server used is Icecast 2, although others
could be used if certain conditions are met.

%prep
%setup -q
perl -pi -e 's|<background>0</background>|<background>1</background>|' conf/*.xml

%build
%configure \
	--with-ogg \
	--with-vorbis

%{__make} %{?_smp_mflags}

%install
rm -rf %{buildroot}

install -D -m 755 src/ices %{buildroot}%{_bindir}/ices
install -D -m 644 conf/ices-playlist.xml %{buildroot}%{_sysconfdir}/ices.conf
install -D -m 755 %{SOURCE1} %{buildroot}%{_initrddir}/ices
install -D -m 644 %{SOURCE2} %{buildroot}%{_sysconfdir}/logrotate.d/ices
install -d -m 755 %{buildroot}%{_var}/log/ices

%clean 
rm -rf %{buildroot}

%pre
/usr/sbin/useradd -c "IceS Shoutcast source" \
        -s /sbin/nologin -r -d /dev/null ices 2> /dev/null || :

%post
if [ $1 = 1 ]; then
   /sbin/chkconfig --add ices
fi

%preun
if [ $1 = 0 ]; then
        /sbin/service ices stop >/dev/null 2>&1
        /sbin/chkconfig --del ices
fi

%postun
if [ "$1" -ge "1" ]; then
        /sbin/service ices condrestart >/dev/null 2>&1
fi

%files
%defattr(-,root,root)
%doc AUTHORS COPYING README TODO doc/*.html doc/*.css conf/*.xml
%{_bindir}/ices
%config(noreplace) %{_sysconfdir}/ices.conf
%config %{_sysconfdir}/logrotate.d/ices
%{_initrddir}/ices
%attr(0770,root,ices) %{_var}/log/ices

%changelog
* Tue Mar 28 2006 Andreas Thienemann <andreas@bawue.net> 2.0.1-2
- Cleaned up the specfile for FE

* Thu Nov 17 2005 Matt Domsch <Matt_Domsch@dell.com> 2.0.1-1
- add dist tag
- rebuild for FC4

* Mon Jan 31 2005 Ignacio Vazquez-Abrams <ivazquez@ivazquez.net> 0:2.0.1-0.iva.0
- Upstream update

* Fri Jan  7 2005 Ignacio Vazquez-Abrams <ivazquez@ivazquez.net> 0:2.0.0-0.iva.0
- Retooled for Fedora Core 3
