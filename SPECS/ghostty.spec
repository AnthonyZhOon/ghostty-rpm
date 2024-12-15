Name:           ghostty
Version:        0.1.0
Release:        %autorelease
Summary:        A modern terminal emulator in Zig, source branch

License:        Unknown
URL:            https://mitchellh.com/ghostty
Source0:        %{name}-%{version}.tar.gz

# Compile with zig, which self-sources C/C++ compiling
# Use pandoc to build docs
BuildRequires:  zig >= 0.13.0, zig < 0.14.0, pandoc

# Dynamic linking dependencies
BuildRequires:  pkgconfig(fontconfig), pkgconfig(freetype2), pkgconfig(harfbuzz), pkgconfig(gtk4), 
# Choose zlib-ng over zlib-ng-compat as we don't require compatibility with 32-bit systems
BuildRequires:  pkgconfig(oniguruma), pkgconfig(glib-2.0), pkgconfig(libadwaita-1), pkgconfig(libpng), pkgconfig(zlib-ng)

# Testing requires hostname util
BuildRequires:  hostname

%description
Ghostty is a cross-platform, GPU-accelerated terminal emulator that aims to push
the boundaries of what is possible with a terminal emulator by exposing modern,
opt-in features that enable CLI tool developers to build more feature rich,
interactive applications.

# Is this okay? Ghostty uses sentry to create coredumps for debugging
%global debug_package %{nil}

%prep
%autosetup


%build
%define _build_flags --system "$(pwd)/.zig-cache/p" -Dcpu=baseline -Dtarget=native -Doptimize=ReleaseFast -Demit-docs -Dpie
# I want to move this into the prep step as the fetch is part of the sources ideally
ZIG_GLOBAL_CACHE_DIR="$(pwd)/.zig-cache" ./nix/build-support/fetch-zig-cache.sh
zig build %{_build_flags}

%check
zig build test %{_build_flags}

%install
# use install step of the build script
zig build install --prefix %{buildroot}%{_prefix} %{_build_flags}


%files

# Our application
%{_bindir}/%{name}

%docdir %{_datadir}/ghostty/doc

# It's okay to own this directory as it is created by ghostty
%{_datadir}/ghostty/*

%{_datadir}/fish/vendor_completions.d/ghostty.fish
%{_datadir}/bat/syntaxes/ghostty.sublime-syntax
%{_datadir}/zsh/site-functions/_ghostty
%{_datadir}/applications/com.mitchellh.ghostty.desktop

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

# %license add-license-file-here


%changelog
%autochangelog
