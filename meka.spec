%global commit f55fcdd96f1ad43f01d2645f4cd7fe0b9c5c6870
%global shortcommit %(c=%{commit}; echo ${c:0:7})

Name: meka
Version: 0.80
Release: 0.8.20150506git%{?dist}
Summary: Sega 8-bit emulator with debugging/hacking tools

License: MEKA and non-commercial
URL: http://www.smspower.org/meka/      
Source0: https://github.com/ocornut/%{name}/archive/%{commit}/%{name}-%{version}-%{shortcommit}.tar.gz
Source1: %{name}.sh
Source2: %{name}.desktop

# This is package contains ix86 asm code
ExclusiveArch: i686 x86_64

BuildRequires: allegro5-devel
BuildRequires: allegro5-addon-audio-devel
BuildRequires: allegro5-addon-image-devel
BuildRequires: allegro5-addon-ttf-devel
BuildRequires: libpng-devel
BuildRequires: ImageMagick
BuildRequires: desktop-file-utils
Requires: hicolor-icon-theme
Requires: grimmer-proggy-tinysz-fonts

%description
MEKA is a multi machine emulator, originally started as a Sega Master System
emulator, and generally very oriented toward Z80-based Sega 8-bit systems.
MEKA officially emulates the following systems:

 - Sega Game 1000        / SG-1000  / Japan, Oceania
 - Sega Computer 3000    / SC-3000  / Japan, Oceania, Europe
 - Super Control Station / SF-7000  / Japan, Oceania, Europe
 - Sega Mark III         / MK3      / Japan
    + FM Unit Extension  / MK3+FM   / Japan
 - Sega Master System    / SMS      / World Wide
 - Sega Game Gear        / GG       / World Wide
 - ColecoVision          / COLECO   / America, Europe
 - Othello Multivision   / OMV      / Japan

You can play other systems on it only if you are smart enough to figure how.
And if you are, I doubt you will want to play Nintendo games. So forget it.

%prep
%setup -q -n %{name}-%{commit}/%{name}

# Remove boundled libs
rm -rf libs

# Fix end-of-line-encoding
sed -i 's/\r//' *.txt

# Fix char encondigs
for i in *.txt; do
  iconv --from=ISO-8859-1 --to=UTF-8 $i > $i.utf8
  mv $i.utf8 $i
done

# Fix linking
sed -i 's/allegro_primitives-5.0`/allegro_primitives-5.0 allegro_ttf-5.0`/' srcs/Makefile

# Compile for unix
sed -i 's/SYSTEM = macosx/# SYSTEM = macosx/' srcs/Makefile
sed -i 's/# SYSTEM = unix/SYSTEM = unix/' srcs/Makefile


%build
cd srcs
export CFLAGS="%{optflags}"
# make doesn't compile with %%{?_smp_mflags}
make


%install
install -d %{buildroot}/%{_bindir}
install -m 755 %{SOURCE1} %{buildroot}/%{_bindir}/meka
install -d %{buildroot}/%{_libexecdir}/meka
install -m 755 meka %{buildroot}/%{_libexecdir}/meka
install -d %{buildroot}/%{_datadir}/meka
install -m 644 meka.{blt,dat,inp,msg,nam,pat,thm} %{buildroot}/%{_datadir}/meka
cp -aR {Data,Themes} %{buildroot}/%{_datadir}/meka

# install desktop file
mkdir -p %{buildroot}%{_datadir}/applications
desktop-file-install \
  --dir %{buildroot}%{_datadir}/applications \
  %{SOURCE2}

# install icons
mkdir -p %{buildroot}%{_datadir}/icons/hicolor/{16x16,32x32}/apps
convert -delete 1 srcs/mekaw.ico \
  %{buildroot}%{_datadir}/icons/hicolor/16x16/apps/%{name}.png
convert -delete 0 srcs/mekaw.ico \
  %{buildroot}%{_datadir}/icons/hicolor/32x32/apps/%{name}.png

# symlink system fonts
rm %{buildroot}%{_datadir}/%{name}/Data/fonts/ProggyTinySZ.ttf
ln -s %{_datadir}/fonts/grimmer-proggy-tinysz/ProggyTinySZ.ttf \
    %{buildroot}%{_datadir}/%{name}/Data/fonts/ProggyTinySZ.ttf


%post
touch --no-create %{_datadir}/icons/hicolor &>/dev/null || :


%postun
if [ $1 -eq 0 ] ; then
    touch --no-create %{_datadir}/icons/hicolor &>/dev/null
    gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :
fi


%posttrans
gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :


%files
%{_bindir}/meka
%{_libexecdir}/meka
%{_datadir}/meka
%{_datadir}/applications/%{name}.desktop
%{_datadir}/icons/hicolor/16x16/apps/%{name}.png
%{_datadir}/icons/hicolor/32x32/apps/%{name}.png
%doc changes.txt compat.txt debugger.txt history.txt meka.txt multi.txt
%doc sources.txt tech.txt TODO.txt


%changelog
* Thu Jun 02 2016 Andrea Musuruane <musuruan@gmail.com> - 0.80-0.8.20150506git
- Updated to a new upstream preview of version 0.80
- Using new upstream repository

* Sun Oct 05 2014 Andrea Musuruane <musuruan@gmail.com> - 0.80-0.7.20141005svn
- Updated to a new upstream preview of version 0.80
- Made a patch to fix format strings
- Dropped cleaning at the beginning of %%install
- Spec file clean up

* Sun Aug 31 2014 Sérgio Basto <sergio@serjux.com> - 0.80-0.6.20130725svn
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Tue Oct 01 2013 Nicolas Chauvet <kwizart@gmail.com> - 0.80-0.5.20130725svn
- Rebuilt

* Mon Sep 30 2013 Nicolas Chauvet <kwizart@gmail.com> - 0.80-0.4.20130725svn
- Rebuilt

* Sun Aug 18 2013 Andrea Musuruane <musuruan@gmail.com> 0.80-0.3.20130725svn
- Updated to a new upstream preview of version 0.80
- Fixed startup script
- Used unversioned docdir

* Mon Dec 17 2012 Andrea Musuruane <musuruan@gmail.com> 0.80-0.2.20120503svn
- Fixed supported archs (BZ #2611)

* Sat May 05 2012 Andrea Musuruane <musuruan@gmail.com> 0.80-0.1.20120503svn
- Updated to an upstream preview of version 0.80
- Minor clean up for rpm >= 4.9

* Thu Feb 09 2012 Nicolas Chauvet <kwizart@gmail.com> - 0.73-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Sat Dec 11 2010 Andrea Musuruane <musuruan@gmail.com> 0.73-4
- Fixed license

* Sat Dec 04 2010 Andrea Musuruane <musuruan@gmail.com> 0.73-3
- Changed summary
- Removed pre-built lib files
- Fixed execstack patch
- Fixed consistent use of macros
- Minor changes

* Sat Nov 20 2010 Andrea Musuruane <musuruan@gmail.com> 0.73-2
- Added a patch to compile with gcc4.5

* Sun Jun 13 2010 Andrea Musuruane <musuruan@gmail.com> 0.73-1
- New upstream release

* Thu Jul 30 2009 Andrea Musuruane <musuruan@gmail.com> 0.73-0.1.20080619
- First release
