Summary:	GNOME VNC client
Name:		vinagre
Version:	3.14.0
Release:	1
License:	GPL v2+
Group:		X11/Applications
Source0:	http://download.gnome.org/sources/vinagre/3.14/%{name}-%{version}.tar.xz
# Source0-md5:	29640307d8f57623a915d286db516b9f
URL:		http://www.gnome.org/projects/vinagre/
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	avahi-glib-devel
BuildRequires:	avahi-ui-gtk3-devel
BuildRequires:	gtk-vnc-devel
BuildRequires:	intltool
BuildRequires:	itstool
BuildRequires:	libsecret-devel
BuildRequires:	perl-XML-Parser
BuildRequires:	pkg-config
BuildRequires:	telepathy-glib-devel
BuildRequires:	vte-devel
BuildRequires:	yelp-tools
Requires(post,postun):	/usr/bin/gtk-update-icon-cache
Requires(post,postun):	desktop-file-utils
Requires(post,postun):	glib-gio-gsettings
Requires(post,postun):	hicolor-icon-theme
Requires(post,postun):	shared-mime-info
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_libexecdir	%{_libdir}/vinagre

%description
Vinagre is a VNC client for the GNOME desktop environment.

%prep
%setup -q
# kill gnome common deps
%{__sed} -i -e 's/GNOME_COMPILE_WARNINGS.*//g'	\
    -i -e 's/GNOME_MAINTAINER_MODE_DEFINES//g'	\
    -i -e 's/GNOME_COMMON_INIT//g'		\
    -i -e 's/GNOME_CXX_WARNINGS.*//g'		\
    -i -e 's/GNOME_DEBUG_CHECK//g'		\
    -i -e '/APPSTREAM_XML/d' configure.ac
%{__sed} -i '/@APPSTREAM_XML_RULES@/d' Makefile.am

%build
%{__intltoolize}
%{__libtoolize}
%{__aclocal}
%{__autoconf}
%{__automake}
%configure \
	--disable-schemas-compile	\
	--disable-silent-rules		\
	--disable-spice
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%{__rm} -r $RPM_BUILD_ROOT%{_datadir}/GConf

%find_lang vinagre --with-gnome --with-omf

%clean
rm -rf $RPM_BUILD_ROOT

%post
%update_gsettings_cache
%update_mime_database
%update_icon_cache hicolor
%update_desktop_database

%postun
%update_gsettings_cache
%update_mime_database
%update_icon_cache hicolor
%update_desktop_database

%files -f vinagre.lang
%defattr(644,root,root,755)
%doc README NEWS COPYING AUTHORS
%attr(755,root,root) %{_bindir}/vinagre
%{_datadir}/dbus-1/services/org.freedesktop.Telepathy.Client.Vinagre.service
%{_datadir}/glib-2.0/schemas/org.gnome.Vinagre.gschema.xml
%{_datadir}/telepathy/clients/Vinagre.client
%dir %{_datadir}/vinagre
%{_datadir}/vinagre/vinagre-ui.xml
%{_datadir}/vinagre/vinagre.ui

%{_datadir}/mime/packages/vinagre-mime.xml
%{_desktopdir}/vinagre-file.desktop
%{_desktopdir}/vinagre.desktop
%{_iconsdir}/hicolor/*/mimetypes/*.png
%{_iconsdir}/hicolor/*/mimetypes/*.svg
%{_iconsdir}/hicolor/*/status/*.png

%{_datadir}/man/man1/vinagre.1*

