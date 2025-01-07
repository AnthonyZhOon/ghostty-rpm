%bcond test 1
# Fedora 40 doesn't have the required simdutf version
%if 0%{?fedora} == 40
%bcond simdutf 0
%else
%bcond simdutf 1
%endif

# Need to disable build from stripping debug
%global debug_package %{nil}
%global project_id          com.mitchellh.ghostty
%global project_description %{expand:
Ghostty is a cross-platform, GPU-accelerated terminal emulator that aims to push 
the boundaries of what is possible with a terminal emulator by exposing modern, 
opt-in features that enable CLI tool developers to build more feature rich, 
interactive applications.}

%global pubkey RWQlAjJC23149WL2sEpT/l0QKy7hMIFhYdQOFy0Z7z7PbneUgvlsnYcV
%global build_flags %{shrink:
  %{?with_simdutf:-fsys=simdutf} \
   -Doptimize=ReleaseFast \
   -Dversion-string=%{version}
}

# Performance issues and debug build banner in safe
%global _zig_release_mode fast
%global _zig_cache_dir /tmp/zig-cache

Name:           ghostty
Version:        1.0.1+post
Release:        1%{?dist}
Summary:        A modern, feature-rich terminal emulator in Zig

License:        MIT AND OFL-1.1
URL:            https://ghostty.org

Source0:        https://github.com/ghostty-org/ghostty/releases/download/tip/%{name}-source.tar.gz
Source1:        https://github.com/ghostty-org/ghostty/releases/download/tip/%{name}-source.tar.gz.minisig

Conflicts:      ghostty
ExclusiveArch: %{zig_arches}
# Compile with zig, which bundles a C/C++ compiler
# Use pandoc to build docs, minisign to check signature
BuildRequires:  (zig >= 0.13.0 with zig < 0.14.0~)
BuildRequires:   pandoc
BuildRequires:   minisign
BuildRequires:   zig-rpm-macros

BuildRequires:  pkgconfig(fontconfig)
BuildRequires:  pkgconfig(freetype2)
BuildRequires:  pkgconfig(glib-2.0),
BuildRequires:  pkgconfig(gtk4)
BuildRequires:  pkgconfig(harfbuzz)
BuildRequires:  pkgconfig(libadwaita-1)
BuildRequires:  pkgconfig(libpng)
BuildRequires:  pkgconfig(oniguruma)
%if %{with simdutf}
BuildRequires: pkgconfig(simdutf) >= 5.2.8
%endif
BuildRequires:  pkgconfig(zlib-ng)


# Validate desktop vile and deduplicate files according to lints + guidelines
BuildRequires:  desktop-file-utils
BuildRequires:  fdupes

%if %{with test}
BuildRequires: hostname
%endif

Requires: %{name}-terminfo = %{version}-%{release}

# Embedded fonts
# see src/font/embedded.zig, most fonts are in source for tests and only
# JetBrainsMono, Noto Color Emoji, and Noto Color are in the application.
# Discovered with  `fc-query -f '%{fontversion}\n' ./CozetteVector.ttf | perl -E 'printf "%.3f\n", <>/65536.0'`
Provides:      bundled(font(CodeNewRoman)) = 2.000
Provides:      bundled(font(CozetteVector)) = 1.22.2
Provides:      bundled(font(GeistMono)) = 1.2.0
Provides:      bundled(font(Inconsolata)) = 3.001
Provides:      bundled(font(JetBrainsMonoNerdFont)) = 2.304
Provides:      bundled(font(JetBrainsMonoNoNF)) = 2.304
Provides:      bundled(font(JuliaMono)) = 0.055
# Version does not match known releases
Provides:      bundled(font(KawkabMono)) = 1.000 
Provides:      bundled(font(Lilex)) = 2.200 
Provides:      bundled(font(MonaspaceNeon)) = 1.000
Provides:      bundled(font(NotoColorEmoji)) = 2.034
Provides:      bundled(font(NotoEmoji)) = 1.002

# More C bindings are bundled in ./pkgs which are for now developed as part of ghostty however they can be linked statically
Provides:      bundled(glslang) = 14.2.0
%if %{without simdutf}
Provides:      bundled(simdutf) = 5.2.8
%endif
Provides:      bundled(spirv-cross) = 13.1.1

# https://deps.files.ghostty.org/ziglyph-b89d43d1e3fb01b6074bc1f7fc980324b04d26a5.tar.gz
Provides:      bundled(zig(dude_the_builder/ziglyph)) = 0.13.0~gitb89d43d1e3fb01b6074bc1f7fc980324b04d26a5 
# https://github.com/mitchellh/libxev/archive/db6a52bafadf00360e675fefa7926e8e6c0e9931.tar.gz
Provides:      bundled(zig(mitchellh/libxev)) = 0~gitdb6a52bafadf00360e675fefa7926e8e6c0e9931 
# https://github.com/mitchellh/mach-glfw/archive/37c2995f31abcf7e8378fba68ddcf4a3faa02de0.tar.gz
Provides:      bundled(zig(mitchellh/mach-glfw)) = 0~git37c2995f31abcf7e8378fba68ddcf4a3faa02de0 
# https://github.com/mitchellh/zig-js/archive/d0b8b0a57c52fbc89f9d9fecba75ca29da7dd7d1.tar.gz
Provides:      bundled(zig(mitchellh/zig-js)) = 0~gitd0b8b0a57c52fbc89f9d9fecba75ca29da7dd7d1 
# https://github.com/mitchellh/zig-objc/archive/9b8ba849b0f58fe207ecd6ab7c147af55b17556e.tar.gz
Provides:      bundled(zig(mitchellh/zig-objc)) = 0~git9b8ba849b0f58fe207ecd6ab7c147af55b17556e 
# git+https://github.com/natecraddock/zf/?ref=main#ed99ca18b02dda052e20ba467e90b623c04690dd
Provides:      bundled(zig(natecraddock/zf)) = 0~gited99ca18b02dda052e20ba467e90b623c04690dd 
# git+https://github.com/rockorager/libvaxis/?ref=main#6d729a2dc3b934818dffe06d2ba3ce02841ed74b
Provides:      bundled(zig(rockorager/libvaxis)) = 0~git6d729a2dc3b934818dffe06d2ba3ce02841ed74b 
# git+https://github.com/vancluever/z2d?ref=v0.4.0#4638bb02a9dc41cc2fb811f092811f6a951c752a
Provides:      bundled(zig(vancluever/z2d)) = 0.4.0 

%description
%{project_description}

%package terminfo
Summary:       Terminfo for ghostty (xterm-ghostty)
BuildArch:     noarch
License:       MIT

Requires:      ncurses-base

%description terminfo
%{project_description}

Terminfo files for %{name}

%prep
# Check source signature with minisign pubkey at https://github.com/ghostty-org/ghostty/blob/main/PACKAGING.md
minisign -Vm %{SOURCE0} -x %{SOURCE1} -P %{pubkey}
%setup -q -n ghostty-source

ZIG_GLOBAL_CACHE_DIR=%{_zig_cache_dir} ./nix/build-support/fetch-zig-cache.sh # _REQUIRES_NETWORK


%build
# I want to move this into the prep step as the fetch is part of the sources ideally
%{zig_build} %{build_flags}


%install
# use install step of the build script
%{zig_install} %{build_flags}
%fdupes %{buildroot}/${_datadir}

%check
desktop-file-validate %{buildroot}/%{_datadir}/applications/%{project_id}.desktop
%{buildroot}/%{_bindir}/%{name} --version

%if %{with test}
# These are currently unit tests for individual features in ghostty
zig build test %{build_flags}
%endif

%files
%{_bindir}/%{name}
%license LICENSE
# Owned directory containing themes, shell integration and docs
%{_datadir}/%{name}/
%{_datadir}/applications/%{project_id}.desktop
# KDE integration
%{_datadir}/kio/servicemenus/%{project_id}.desktop

%{_datadir}/icons/hicolor/*/apps/%{project_id}.png
%{_mandir}/man{1,5}/%{name}.{1,5}*

# Shell completions
%{_datadir}/bash-completion/completions/%{name}.bash
%{_datadir}/fish/vendor_completions.d/%{name}.fish
%{_datadir}/zsh/site-functions/_%{name}
%{_datadir}/bat/syntaxes/%{name}.sublime-syntax

# Consider separating and depending on vim/nvim
%{_datadir}/nvim/site/{ftdetect,ftplugin,syntax}/%{name}.vim
%{_datadir}/vim/vimfiles/{ftdetect,ftplugin,syntax}/%{name}.vim
%docdir %{_datadir}/%{name}/doc

%files terminfo
%license LICENSE
%{_datadir}/terminfo/g/%{name}
%{_datadir}/terminfo/%{name}.term{cap,info}
%{_datadir}/terminfo/x/xterm-%{name}


%changelog
%autochangelog
