%global commit 9a40240c5ce3ac800aab83cb49f7f6dd00619b38
%global shortcommit %(c=%{commit}; echo ${c:0:7})

Name: meka
Version: 0.80
Release: 0.26.20191213git%{?dist}
Summary: Sega 8-bit emulator with debugging/hacking tools

License: MEKA and non-commercial
URL: http://www.smspower.org/meka/      
Source0: https://github.com/ocornut/%{name}/archive/%{commit}/%{name}-%{version}-%{shortcommit}.tar.gz
Source1: %{name}.sh
Source2: %{name}.desktop

# This is package contains ix86 asm code
ExclusiveArch: i686 x86_64

BuildRequires: gcc-c++
BuildRequires: allegro5-devel
BuildRequires: allegro5-addon-audio-devel
BuildRequires: allegro5-addon-image-devel
BuildRequires: allegro5-addon-ttf-devel
BuildRequires: libpng-devel
BuildRequires: ImageMagick
BuildRequires: desktop-file-utils
Requires: hicolor-icon-theme
Requires: grimmer-proggy-tinysz-fonts
Requires: grimmer-proggy-squaresz-fonts

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

# Fix end-of-line-encoding
sed -i 's/\r//' *.txt

# Fix char encondigs
for i in *.txt; do
  iconv --from=ISO-8859-1 --to=UTF-8 $i > $i.utf8
  mv $i.utf8 $i
done

# Fix linking with allegro5
sed -i 's/pkg-config --cflags --libs allegro-5.0 allegro_image-5.0 allegro_audio-5.0 allegro_font-5.0 allegro_primitives-5.0 allegro_ttf-5.0/pkg-config --cflags --libs allegro-5 allegro_image-5 allegro_audio-5 allegro_font-5 allegro_primitives-5 allegro_ttf-5/' srcs/Makefile


%build
cd srcs
%set_build_flags
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

rm %{buildroot}%{_datadir}/%{name}/Data/fonts/ProggySquareSZ.ttf
ln -s %{_datadir}/fonts/grimmer-proggy-squaresz/ProggySquareSZ.ttf \
    %{buildroot}%{_datadir}/%{name}/Data/fonts/ProggySquareSZ.ttf


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
* Wed Jan 29 2025 RPM Fusion Release Engineering <sergiomb@rpmfusion.org> - 0.80-0.26.20191213git
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Sat Aug 03 2024 RPM Fusion Release Engineering <sergiomb@rpmfusion.org> - 0.80-0.25.20191213git
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Sun Feb 04 2024 RPM Fusion Release Engineering <sergiomb@rpmfusion.org> - 0.80-0.24.20191213git
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Thu Aug 03 2023 RPM Fusion Release Engineering <sergiomb@rpmfusion.org> - 0.80-0.23.20191213git
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Mon Aug 08 2022 RPM Fusion Release Engineering <sergiomb@rpmfusion.org> - 0.80-0.22.20191213git
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild and ffmpeg
  5.1

* Thu Feb 10 2022 RPM Fusion Release Engineering <sergiomb@rpmfusion.org> - 0.80-0.21.20191213git
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Wed Aug 04 2021 RPM Fusion Release Engineering <leigh123linux@gmail.com> - 0.80-0.20.20191213git
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Thu Feb 04 2021 RPM Fusion Release Engineering <leigh123linux@gmail.com> - 0.80-0.19.20191213git
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Wed Aug 19 2020 RPM Fusion Release Engineering <leigh123linux@gmail.com> - 0.80-0.18.20191213git
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Wed Feb 05 2020 RPM Fusion Release Engineering <leigh123linux@gmail.com> - 0.80-0.17.20191213git
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Sat Dec 14 2019 Andrea Musuruane <musuruan@gmail.com> - 0.80-0.16.20191213git
- Updated to a new upstream preview of version 0.80
- Spec file clean up

* Sat Aug 10 2019 RPM Fusion Release Engineering <leigh123linux@gmail.com> - 0.80-0.15.20150506git
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Tue Mar 05 2019 RPM Fusion Release Engineering <leigh123linux@gmail.com> - 0.80-0.14.20150506git
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Sun Aug 19 2018 RPM Fusion Release Engineering <leigh123linux@gmail.com> - 0.80-0.13.20150506git
- Rebuilt for Fedora 29 Mass Rebuild binutils issue

* Fri Jul 27 2018 RPM Fusion Release Engineering <sergio@serjux.com> - 0.80-0.12.20150506git
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Fri Mar 02 2018 RPM Fusion Release Engineering <leigh123linux@googlemail.com> - 0.80-0.11.20150506git
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Aug 31 2017 RPM Fusion Release Engineering <kwizart@rpmfusion.org> - 0.80-0.10.20150506git
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sun Mar 26 2017 RPM Fusion Release Engineering <kwizart@rpmfusion.org> - 0.80-0.9.20150506git
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

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
