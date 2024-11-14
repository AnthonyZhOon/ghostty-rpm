Name:           ghostty
Version:        0.0.1
Release:        1%{?dist}
Summary:        A modern terminal emulator in Zig, source branch

License:        Unknown
URL:            https://mitchellh.com/ghostty
Source0:        %{name}-%{version}.tar.gz

BuildRequires:  zig >= 0.13.0, zig < 0.14.0, pandoc
Requires:       bzip2, fontconfig, freetype, gtk4, harfbuzz, pixman

%global debug_package %{nil}

%description
Ghostty is a cross-platform, GPU-accelerated terminal emulator that aims to push
the boundaries of what is possible with a terminal emulator by exposing modern,
opt-in features that enable CLI tool developers to build more feature rich,
interactive applications.

%prep
%autosetup


%build
ZIG_GLOBAL_CACHE_DIR="$(pwd)/.zig-cache" ./nix/build-support/fetch-zig-cache.sh
zig build --system "$(pwd)/.zig-cache/p" -fno-sys=oniguruma -Dcpu=baseline -Doptimize=ReleaseFast -Demit-docs -Dpie

%install
mkdir -p %{buildroot}%{_bindir}
mkdir -p %{buildroot}%{_datadir}
cp -r zig-out/bin/* %{buildroot}%{_bindir}
cp -r zig-out/share/* %{buildroot}%{_datadir}

%files

# Our application
%{_bindir}/%{name}

# Themes and shell integration
%docdir %{_datadir}/ghostty/doc

# It's okay to own this directory
%{_datadir}/ghostty/*

# Executable files
%defattr(0755, root, root) 
%{_datadir}/ghostty/shell-integration/bash/bash-preexec.sh
%{_datadir}/ghostty/shell-integration/bash/ghostty.bash
%{_datadir}/ghostty/shell-integration/elvish/lib/ghostty-integration.elv
%{_datadir}/ghostty/shell-integration/fish/vendor_conf.d/ghostty-shell-integration.fish
%{_datadir}/ghostty/shell-integration/zsh/ghostty-integration
%defattr(644, root, root)

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
 
%{_datadir}/man/man1/ghostty.1.gz
%{_datadir}/man/man5/ghostty.5.gz

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

# %license add-license-file-here



%changelog
* Thu Nov 14 2024 Anthony <anthony.zh.oon@gmail.com> Working on smooth 0.0.1-1
- 
