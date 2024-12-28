%bcond test 1
# Fedora 40 doesn't have the required simdutf version
%if 0%{?fedora} == 40
%bcond simdutf 0
%else
%bcond simdutf 1
%endif

%global debug_package %{nil}
%global project_id    com.mitchellh.ghostty
Name:           ghostty
Version:        1.0.0
Release:        2%{?dist}
Summary:        A modern, feature-rich terminal emulator in Zig

License:        MIT AND OFL-1.1
URL:            https://ghostty.org
Source0:        https://release.files.ghostty.org/VERSION/ghostty-source.tar.gz
Source1:        https://release.files.ghostty.org/VERSION/ghostty-source.tar.gz.minisig


# Compile with zig, which bundles a C/C++ compiler
# Use pandoc to build docs, minisign to check signature
BuildRequires:  zig >= 0.13.0, zig < 0.14.0, pandoc, minisign

# Choose zlib-ng over zlib-ng-compat as we don't require compatibility with 32-bit systems
BuildRequires:  pkgconfig(fontconfig), pkgconfig(freetype2), pkgconfig(harfbuzz)
BuildRequires:  pkgconfig(gtk4), pkgconfig(oniguruma), pkgconfig(glib-2.0),
BuildRequires:  pkgconfig(libadwaita-1), pkgconfig(libpng), pkgconfig(zlib-ng)


%if %{with simdutf}
BuildRequires: pkgconfig(simdutf) >= 4.0.9
%endif

# Deduplicate installed files using fdupes, validate .desktop spec compliance
BuildRequires:  fdupes, desktop-file-utils

# Testing requires hostname util
%if %{with test}
BuildRequires: hostname
%endif

%description
Ghostty is a cross-platform, GPU-accelerated terminal emulator that aims to push
the boundaries of what is possible with a terminal emulator by exposing modern,
opt-in features that enable CLI tool developers to build more feature rich,
interactive applications.


%prep
# Check source signature with minisign pubkey at https://github.com/ghostty-org/ghostty/blob/main/PACKAGING.md
%global pubkey RWQlAjJC23149WL2sEpT/l0QKy7hMIFhYdQOFy0Z7z7PbneUgvlsnYcV
minisign -Vm %{SOURCE0} -x %{SOURCE1} -P %{pubkey}
%setup -q -n ghostty-source

ZIG_GLOBAL_CACHE_DIR="/tmp/offline-cache" ./nix/build-support/fetch-zig-cache.sh # _REQUIRES_NETWORK


%build
%global _build_flags %{?with_simdutf:-fsys=simdutf} --system "/tmp/offline-cache/p" -Dcpu=baseline -Dtarget=native -Doptimize=ReleaseFast -Demit-docs -Dpie
# I want to move this into the prep step as the fetch is part of the sources ideally
zig build %{_build_flags}


%install
# use install step of the build script
zig build install --prefix %{buildroot}/%{_prefix} %{_build_flags}
%fdupes %{buildroot}/${_datadir}

%check
desktop-file-validate %{buildroot}/%{_datadir}/applications/%{project_id}.desktop

%if %{with test}
zig build test %{_build_flags}
%endif

%files
%{_bindir}/%{name}
%license LICENSE
# It's okay to own this directory as it is created by ghostty
%{_datadir}/%{name}/

# Shell integrations
%{_datadir}/bash-completion/completions/%{name}.bash
%{_datadir}/fish/vendor_completions.d/%{name}.fish
%{_datadir}/zsh/site-functions/_%{name}
%{_datadir}/bat/syntaxes/%{name}.sublime-syntax
%{_datadir}/applications/%{project_id}.desktop

%{_datadir}/icons/hicolor/*/apps/%{project_id}.png
 
%{_mandir}/man{1,5}/%{name}.{1,5}*

%{_datadir}/nvim/site/{ftdetect,ftplugin,syntax}/%{name}.vim

%{_datadir}/vim/vimfiles/{ftdetect,ftplugin,syntax}/ghostty.vim

%{_datadir}/terminfo/g/%{name}
%{_datadir}/terminfo/%{name}.term{cap,info}
%{_datadir}/terminfo/x/xterm-%{name}

# KDE integration
%{_datadir}/kio/servicemenus/%{project_id}.desktop

%docdir %{_datadir}/%{name}/doc


%changelog
%autochangelog
