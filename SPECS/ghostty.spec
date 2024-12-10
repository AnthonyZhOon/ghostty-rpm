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

%global debug_package %{nil}

%description
Ghostty is a cross-platform, GPU-accelerated terminal emulator that aims to push
the boundaries of what is possible with a terminal emulator by exposing modern,
opt-in features that enable CLI tool developers to build more feature rich,
interactive applications.

%prep
%autosetup


%build
# I want to move this into a source step
ZIG_GLOBAL_CACHE_DIR="$(pwd)/.zig-cache" ./nix/build-support/fetch-zig-cache.sh
zig build --system "$(pwd)/.zig-cache/p" -Dcpu=baseline -Dtarget=native -Doptimize=ReleaseFast -Demit-docs -Dpie

%install
# use install step of the build script
zig build --prefix %{buildroot}%{_prefix} --system "$(pwd)/.zig-cache/p" -Dcpu=baseline -Dtarget=native -Doptimize=ReleaseFast -Demit-docs -Dpie


%files

# Our application
%{_bindir}/%{name}

%docdir %{_datadir}/ghostty/doc

# It's okay to own this directory as it is created by ghostty
%{_datadir}/ghostty/*

%{_datadir}/fish/vendor_completions.d/ghostty.fish
%{_datadir}/bat/syntaxes/ghostty.sublime-syntax
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
