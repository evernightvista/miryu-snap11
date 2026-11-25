# RPM spec for Miryu Snap11, a Windows 11 style snapping script for KWin 6.
#
# Build with:
#   rpmbuild -ba miryu-snap11.spec
# after placing miryu-snap11-45.0.0.tar.gz in ~/rpmbuild/SOURCES. The tarball
# holds a miryu-snap11-45.0.0/ directory with metadata.json, contents/, po/
# and LICENSE (tools/package.sh builds the same tree for the .kwinscript).
#
# Installs system-wide into the KWin scripts location, so every user gets it.

%global plugin_id org.miryugaming.snap11

Name:           miryu-snap11
Version:        45.0.0
Release:        1%{?dist}
Summary:        Windows 11 style window snapping for KWin

License:        MIT
URL:            https://github.com/evernightvista/miryu-snap11
Source0:        https://github.com/evernightvista/miryu-snap11/archive/refs/heads/main.zip

BuildArch:      noarch
BuildRequires:  gettext

%description
Miryu Snap11 brings Windows 11 style window snapping to KWin 6: a snap
layout bar that slides in at the top edge while a window is dragged, a live
drop preview, Snap Assist that fills the remaining zones with window
thumbnails, and layouts for halves, thirds and quarters.

%prep
%autosetup -n %{name}-main

%build
# Pure QML/GJS package: nothing to compile before %%install.

%install
dest=%{buildroot}%{_datadir}/kwin/scripts/%{plugin_id}
install -d "$dest"
cp -r metadata.json contents "$dest"/
install -pm 0644 LICENSE "$dest/LICENSE"
for po in po/*.po; do
    locale=$(basename "$po" .po)
    dir="$dest/contents/locale/$locale/LC_MESSAGES"
    install -d "$dir"
    msgfmt --check -o "$dir/%{plugin_id}.mo" "$po"
done
# Generate the per-locale file list. %%find_lang only scans standard
# %%{_datadir}/locale paths, but KWin scripts install translations under
# contents/locale/, so we build %%{name}.lang manually with find.
find %{buildroot}%{_datadir}/kwin/scripts/%{plugin_id}/contents/locale -type f -name '*.mo' -o -name '*.qm' \
    | sed "s|%{buildroot}||" > %{name}.lang

%files -f %{name}.lang
%{_datadir}/kwin/scripts/%{plugin_id}/metadata.json
%{_datadir}/kwin/scripts/%{plugin_id}/contents/config/
%{_datadir}/kwin/scripts/%{plugin_id}/contents/ui/
%{_datadir}/kwin/scripts/%{plugin_id}/LICENSE

%changelog
* Wed Nov 25 2026 KairikiFedora <13278297951@sina.cn> - 45.0.0-1
- Package Miryu Snap11 45.0.0 as a KWin script.
