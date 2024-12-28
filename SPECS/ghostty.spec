Name:           ghostty
Version:        1.0.0
Release:        %autorelease
Summary:        A modern, feature-rich terminal emulator in Zig

License:        MIT
URL:            https://mitchellh.com/ghostty
Source0:        https://release.files.ghostty.org/VERSION/ghostty-source.tar.gz
Source1:        https://release.files.ghostty.org/VERSION/ghostty-source.tar.gz.minisig

%bcond_with use_system_simdutf
%bcond_without fetch_zig_packages

# Compile with zig, which self-sources C/C++ compiling
# Use pandoc to build docs, minisig to checks signature
BuildRequires:  zig >= 0.13.0, zig < 0.14.0, pandoc, minisign

# Dynamic linking dependencies
BuildRequires:  pkgconfig(fontconfig), pkgconfig(freetype2), pkgconfig(harfbuzz), pkgconfig(gtk4), 
# Choose zlib-ng over zlib-ng-compat as we don't require compatibility with 32-bit systems
BuildRequires:  pkgconfig(oniguruma), pkgconfig(glib-2.0), pkgconfig(libadwaita-1), pkgconfig(libpng), pkgconfig(zlib-ng)


%if %{with use_system_simdutf}
BuildRequires: pkgconfig(simdutf) >= 4.0.9
%endif

# Testing requires hostname util
BuildRequires:  hostname
# Deduplicate installed files using fdupes, validate .desktop spec compliance
BuildRequires:  fdupes, desktop-file-utils


%description
Ghostty is a cross-platform, GPU-accelerated terminal emulator that aims to push
the boundaries of what is possible with a terminal emulator by exposing modern,
opt-in features that enable CLI tool developers to build more feature rich,
interactive applications.

# Is this okay? Ghostty uses sentry to create coredumps for debugging
%global debug_package %{nil}

%prep
# Check source signature with minisign pubkey at https://github.com/ghostty-org/ghostty/blob/main/PACKAGING.md
%global pubkey RWQlAjJC23149WL2sEpT/l0QKy7hMIFhYdQOFy0Z7z7PbneUgvlsnYcV
minisign -Vm %{SOURCE0} -x %{SOURCE1} -P %{pubkey}
%setup -q -n ghostty-source

%if %{with fetch_zig_packages}
ZIG_GLOBAL_CACHE_DIR="/tmp/zig-cache" ./nix/build-support/fetch-zig-cache.sh # _REQUIRES_NETWORK
%endif


%build
%if %{with use_system_simdutf}
%global _build_flags -fsys=simdutf --system "/tmp/zig-cache/p" -Dcpu=baseline -Dtarget=native -Doptimize=ReleaseFast -Demit-docs -Dpie
%else
%global _build_flags --system "/tmp/zig-cache/p" -Dcpu=baseline -Dtarget=native -Doptimize=ReleaseFast -Demit-docs -Dpie

%endif
# I want to move this into the prep step as the fetch is part of the sources ideally
zig build %{_build_flags}


%check
desktop-file-validate %{buildroot}/%{_datadir}/applications/com.mitchellh.ghostty.desktop
zig build test %{_build_flags}


%install
# use install step of the build script
zig build install --prefix %{buildroot}/%{_prefix} %{_build_flags}

# Symlink duplicate files to save space https://en.opensuse.org/openSUSE:Packaging_Conventions_RPM_Macros#%fdupes
%fdupes %{buildroot}/${_datadir}


%files

# Our application
%{_bindir}/%{name}

%docdir %{_datadir}/ghostty/doc

# It's okay to own this directory as it is created by ghostty
%{_datadir}/ghostty/*

# Shell integrations
%{_datadir}/bash-completion/completions/ghostty.bash
%{_datadir}/fish/vendor_completions.d/ghostty.fish
%{_datadir}/bat/syntaxes/ghostty.sublime-syntax
%{_datadir}/zsh/site-functions/_ghostty
%{_datadir}/applications/com.mitchellh.ghostty.desktop

# Icons
%{_datadir}/icons/hicolor/128x128/apps/com.mitchellh.ghostty.png
%{_datadir}/icons/hicolor/128x128@2/apps/com.mitchellh.ghostty.png
%{_datadir}/icons/hicolor/16x16/apps/com.mitchellh.ghostty.png
%{_datadir}/icons/hicolor/16x16@2/apps/com.mitchellh.ghostty.png
%{_datadir}/icons/hicolor/256x256/apps/com.mitchellh.ghostty.png
%{_datadir}/icons/hicolor/256x256@2/apps/com.mitchellh.ghostty.png
%{_datadir}/icons/hicolor/32x32/apps/com.mitchellh.ghostty.png
%{_datadir}/icons/hicolor/32x32@2/apps/com.mitchellh.ghostty.png
%{_datadir}/icons/hicolor/512x512/apps/com.mitchellh.ghostty.png
 
%{_mandir}/man1/ghostty.1*
%{_mandir}/man5/ghostty.5*

%{_datadir}/nvim/site/ftdetect/ghostty.vim
%{_datadir}/nvim/site/ftplugin/ghostty.vim
%{_datadir}/nvim/site/syntax/ghostty.vim

%{_datadir}/vim/vimfiles/ftdetect/ghostty.vim
%{_datadir}/vim/vimfiles/ftplugin/ghostty.vim
%{_datadir}/vim/vimfiles/syntax/ghostty.vim

%{_datadir}/terminfo/g/ghostty
%{_datadir}/terminfo/ghostty.termcap
%{_datadir}/terminfo/ghostty.terminfo
%{_datadir}/terminfo/x/xterm-ghostty

# KDE integration
%{_datadir}/kio/servicemenus/com.mitchellh.ghostty.desktop

%license LICENSE


%changelog
%autochangelog
