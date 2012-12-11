###

Name:		tortoisehg
Version:	2.5
Release:	%mkrel 1
Summary:	Mercurial GUI command line tool hgtk
Group:		Development/Other
License:	GPLv2
# - few files are however under the more permissive GPLv2+
URL:		http://tortoisehg.bitbucket.org/
#Source0:	http://bitbucket.org/tortoisehg/targz/downloads/tortoisehg-%{version}.tar.bz2
Source0:	http://bitbucket.org/tortoisehg/stable/get/%{name}-%{version}.tar.gz
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
# This package _is_ noarch, but that isn't possible because the nautilus
# subpackage has to be arch-specific:
BuildArch:	noarch

BuildRequires:  python-devel, gettext, python-sphinx, python-qt4-devel
Requires:       python-iniparse, mercurial >= 1.6, gnome-python-gconf
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
rm -rf $RPM_BUILD_ROOT

%{__python} setup.py install -O1 --skip-build --root $RPM_BUILD_ROOT

#install -m 644 -D contrib/_hgtk $RPM_BUILD_ROOT/%{_datadir}/zsh/site-functions/_hgtk

%find_lang %{name}

%clean
rm -rf $RPM_BUILD_ROOT

%files -f %{name}.lang

%defattr(-,root,root,-)
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
%defattr(-,root,root,-)
#{_libdir}/nautilus/extensions-2.0/python/nautilus-thg.py
%{_datadir}/nautilus-python/extensions/nautilus-thg.py


%changelog
* Fri Sep 14 2012 Sergey Zhemoitel <serg@mandriva.org> 2.5-1mdv2012.0
+ Revision: 816942
- Update to 2.5

* Thu Aug 02 2012 Sergey Zhemoitel <serg@mandriva.org> 2.4.2-1
+ Revision: 811562
- Update to 2.4.2

* Wed Jun 13 2012 Sergey Zhemoitel <serg@mandriva.org> 2.4.1-1
+ Revision: 805373
- update to 2.4.1

* Fri May 11 2012 Sergey Zhemoitel <serg@mandriva.org> 2.4-1
+ Revision: 798366
- update to 2.4

* Wed Apr 25 2012 Sergey Zhemoitel <serg@mandriva.org> 2.3.2-1
+ Revision: 793300
- update release to 2.3.2

* Mon Mar 05 2012 Sergey Zhemoitel <serg@mandriva.org> 2.3.1-1
+ Revision: 782188
- add new version 2.3.1

* Tue Jan 03 2012 Sergey Zhemoitel <serg@mandriva.org> 2.2.2-1
+ Revision: 748902
- new release 2.2.2

* Sun Dec 11 2011 Sergey Zhemoitel <serg@mandriva.org> 2.2.1-1
+ Revision: 740235
- add new release 2.2.1

* Mon Nov 07 2011 Sergey Zhemoitel <serg@mandriva.org> 2.2-1
+ Revision: 726450
- new version 2.2 with mercurial 2.0

* Sun Nov 06 2011 Sergey Zhemoitel <serg@mandriva.org> 2.1.4-2
+ Revision: 723080
- add new release 2.1.4

* Thu Sep 22 2011 Sergey Zhemoitel <serg@mandriva.org> 2.1.3-2
+ Revision: 700963
+ rebuild (emptylog)

* Mon Aug 29 2011 Sergey Zhemoitel <serg@mandriva.org> 2.1.3-1
+ Revision: 697336
- new release 2.1.3

* Sun Aug 14 2011 Sergey Zhemoitel <serg@mandriva.org> 2.1.2-1
+ Revision: 694431
- new release 2.1.2

* Sun Aug 14 2011 Sergey Zhemoitel <serg@mandriva.org> 2.1-1
+ Revision: 694430
- fix spec
- new version 2.1.1
- imported package tortoisehg
- Update to new release 2.0.4
- imported package tortoisehg
- imported package tortoisehg

