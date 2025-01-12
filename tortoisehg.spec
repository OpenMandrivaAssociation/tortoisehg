Name:		tortoisehg
Version:	3.0.1
Release:	2
Summary:	Mercurial GUI command line tool hgtk
Group:		Development/Other
License:	GPLv2
# - few files are however under the more permissive GPLv2+
URL:		https://tortoisehg.bitbucket.org/
#Source0:	http://bitbucket.org/tortoisehg/targz/downloads/tortoisehg-%{version}.tar.bz2
Source0:	http://bitbucket.org/tortoisehg/stable/get/%{name}-%{version}.tar.gz
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
# This package _is_ noarch, but that isn't possible because the nautilus
# subpackage has to be arch-specific:
BuildArch:	noarch
#Requires:	mercurial >= 3.0

BuildRequires:  python-devel, gettext, python-sphinx, python-qt4-devel
Requires:       python-iniparse, mercurial >= 2.9, gnome-python-gconf
Requires:       pygtk2, gnome-python-gtkspell, python-qt4-qscintilla

%description
This package contains the hgtk command line tool, which provides a graphical
user interface to the Mercurial distributed revision control system. 

%package        nautilus
Summary:        Mercurial GUI plugin to Nautilus file manager 
Group:          Development/Other
Requires:       %{name} = %{version}-%{release}, nautilus-python

%description    nautilus
This package contains the TortoiseHg Gnome/Nautilus extension, which makes the
Mercurial distributed revision control system available in the file manager
with a graphical interface. 

Note that the nautilus extension has been deprecated upstream.

%prep
%setup -q

# Fedora Nautilus python extensions lives in lib64 on x86_64 (https://bugzilla.redhat.com/show_bug.cgi?id=509633) ...
%{__sed} -i "s,lib/nautilus,%{_lib}/nautilus,g" setup.py

cat > tortoisehg/util/config.py << EOT
bin_path     = "%{_bindir}"
license_path = "%{_docdir}/%{name}-%{version}/COPYING.txt"
locale_path  = "%{_datadir}/locale"
icon_path    = "%{_datadir}/pixmaps/tortoisehg/icons"
nofork       = True
EOT

%build
%{__python} setup.py build

(cd doc && make html)
rm doc/build/html/.buildinfo

%install
%{__python} setup.py install -O1 --skip-build --root $RPM_BUILD_ROOT

#install -m 644 -D contrib/_hgtk $RPM_BUILD_ROOT/%{_datadir}/zsh/site-functions/_hgtk

%find_lang %{name}

%clean

%files -f %{name}.lang
%doc COPYING.txt doc/build/html/
%{_bindir}/thg
%{python_sitelib}/tortoisehg/
%{python_sitelib}/tortoisehg-*.egg-info
%{_datadir}/pixmaps/tortoisehg/

# /usr/share/zsh/site-functions/ is owned by zsh package which we don't want to
# require. We also don't want to create a sub-package just for this dependency.
# Instead we just claim ownership of the zsh top folder ...
#%{_datadir}/zsh

%files nautilus
#{_libdir}/nautilus/extensions-2.0/python/nautilus-thg.py
%{_datadir}/nautilus-python/extensions/nautilus-thg.py

%changelog
