# To handle zig package management which requires a cache directory of its dependencies
# build step with `zig fetch <url>`. We can instead download the archive
# sources and do `zig fetch <path>` to populate the package cache offline
%bcond test 1
# Fedora 40 doesn't have the required simdutf version
%if 0%{?fedora} == 40
%bcond simdutf 0
%else
%bcond simdutf 1
%endif

# unbundled https://github.com/ghostty-org/ghostty/pull/4520
%global fontconfig_version 2.14.2
# unbundled https://github.com/ghostty-org/ghostty/pull/4205
%global harfbuzz_version 8.4.0
%global utfcpp_version 4.0.5
%global iterm2_color_commit e030599a6a6e19fcd1ea047c7714021170129d56
%global z2d_commit 4638bb02a9dc41cc2fb811f092811f6a951c752a
%global spirv_cross_commit 476f384eb7d9e48613c45179e502a15ab95b6b49
%global libvaxis_commit1 6d729a2dc3b934818dffe06d2ba3ce02841ed74b
%global libvaxis_commit2 dc0a228a5544988d4a920cfb40be9cd28db41423
%global sentry_version 0.7.8
%global glslang_version 14.2.0
# unbundled https://github.com/ghostty-org/ghostty/pull/4543
%global freetype_version 2.13.2
%global freetype_dash_version %{lua x = string.gsub(macros['freetype_version'], "%.", "-"); print(x)}
# unbundled https://github.com/ghostty-org/ghostty/pull/4534
%global oniguruma_version 6.9.9
%global highway_version 1.1.0
%global libxev_commit db6a52bafadf00360e675fefa7926e8e6c0e9931
%global imgui_commit e391fe2e66eb1c96b1624ae8444dc64c23146ef4
%global breakpad_commit b99f444ba5f6b98cac261cbb391d8766b34a5918
%global wuffs_version 0.4.0-alpha.8
%global ziglyph_commit b89d43d1e3fb01b6074bc1f7fc980324b04d26a5
%global zf_commit ed99ca18b02dda052e20ba467e90b623c04690dd
%global zigimg_commit 3a667bdb3d7f0955a5a51c8468eac83210c1439e
%global zg_version 0.13.2
# These aren't needed for compiling on linux however these are not marked as lazy
# thus required to be valid zig packages.
# Needed for build script switches in 1.0.1
%global zig_objc_commit 9b8ba849b0f58fe207ecd6ab7c147af55b17556e
%global zig_js_commit d0b8b0a57c52fbc89f9d9fecba75ca29da7dd7d1

%global pubkey RWQlAjJC23149WL2sEpT/l0QKy7hMIFhYdQOFy0Z7z7PbneUgvlsnYcV

# Performance issues and debug build banner in safe
%global _zig_release_mode fast
%global _zig_cache_dir %{builddir}/zig-cache

# zig-rpm-macros is broken for system integration
# fixed in zig-rpm-macros-0.13.0-4
%global build_flags %{shrink:
   --system %{_zig_cache_dir}/p \
  %{?with_simdutf:-fsys=simdutf} \
   -Dversion-string=%{version} \
#  -Dstrip=false is a merged PR but not available in v1.0.1
}

# macro to provide setup args for bundled dependency sources
%global setup_args %{lua for i = 10, 30 do print(" -a " .. i) end}

# Need to disable build from stripping debug
%global debug_package %{nil}
%global project_id          com.mitchellh.ghostty
%global project_description %{expand:
Ghostty is a cross-platform, GPU-accelerated terminal emulator that aims to push 
the boundaries of what is possible with a terminal emulator by exposing modern, 
opt-in features that enable CLI tool developers to build more feature rich, 
interactive applications.}


Name:           ghostty
Version:        1.0.1
Release:        %autorelease
Summary:        A modern, feature-rich terminal emulator in Zig

# unbundled dependencies only require the in-tree pkg/* directory and use system integration
# not requiring bundling the upstream source
#
# ghostty:                   MIT
# libvaxis:                  MIT
# libxev:                    MIT
# zig-objc:                  MIT
# zig-js:                    MIT
# z2d:                       MPL-2.0
# zf:                        MIT
# zigimg:                    MIT
# ziglyph:                   MIT
# zg:                        MIT
# iTerm2-Color-Schemes:      MIT
# pkg/fontconfig:            HPND AND LicenseRef-Fedora-Public-Domain AND Unicode-DFS-2016
# pkg/harfbuzz (unbundled):  MIT-Modern-Variant
# pkg/utfcpp:                BSL-1.0
# pkg/spirv-cross:           Apache-2.0
# pkg/sentry:                MIT
# pkg/glslang:               BSD-2-Clause AND BSD-3-Clause AND GPL-3.0-or-later AND Apache-2.0
# pkg/freetype:              (FTL OR GPL-2.0-or-later) AND BSD-3-Clause AND MIT AND MIT-Modern-Variant AND LicenseRef-Public-Domain AND Zlib)
# pkg/oniguruma (unbundled): BSD-2-Clause
# pkg/highway:               Apache-2.0
# pkg/cimgui:                MIT
# pkg/breakpad:              MIT AND BSD-2-Clause AND BSD-3-Clause AND BSD-4-Clause AND Apache-2.0 AND MIT AND curl AND APSL-2.0 AND ClArtistic AND Unicode-3.0 AND LicenseRef-Fedora-Public-Domain AND (GPL-2.0-or-later WITH Autoconf-exception-generic)
# pkg/wuffs:                 Apache-2.0 AND MIT
# vendor/glad                (WTFPL OR CC0-1.0) AND Apache-2.0    

# CodeNewRoman              OFL-1.1
# GeistMono                 OFL-1.1
# Inconsolata               OFL-1.1
# JetBrainsMono             OFL-1.1
# JuliaMono                 OFL-1.1
# KawkabMono                OFL-1.1
# Lilex                     OFL-1.1
# MonaspaceNeon             OFL-1.1
# NotoEmoji                 OFL-1.1
# CozetteVector             MIT
# NerdFont                  MIT AND OFL-1.1
License:        MIT AND (GPL-2.0-or-later WITH Autoconf-exception-generic) AND (WTFPL OR CC0-1.0) AND APSL-2.0 AND Apache-2.0 AND BSD-2-Clause AND BSD-3-Clause AND BSD-4-Clause AND BSL-1.0 AND ClArtistic AND GPL-3.0-or-later AND HPND AND LicenseRef-Fedora-Public-Domain AND MPL-2.0 AND OFL-1.1 AND OFL-1.1 AND Unicode-3.0 AND Unicode-DFS-2016 AND curl

URL:            https://ghostty.org
Source0:        https://release.files.ghostty.org/%{version}/%{name}-%{version}.tar.gz
Source1:        https://release.files.ghostty.org/%{version}/%{name}-%{version}.tar.gz.minisig

# Take these archives from recursively searching URLs in build.zig.zon files
Source10:       https://github.com/nemtrif/utfcpp/archive/refs/tags/v%{utfcpp_version}/utfcpp-%{utfcpp_version}.tar.gz
Source11:       https://github.com/mbadolato/iTerm2-Color-Schemes/archive/%{iterm2_color_commit}/iTerm2-Color-Schemes-%{iterm2_color_commit}.tar.gz
Source12:       https://github.com/vancluever/z2d/archive/%{z2d_commit}/z2d-%{z2d_commit}.tar.gz
Source13:       https://github.com/KhronosGroup/SPIRV-Cross/archive/%{spirv_cross_commit}/SPIRV-Cross-%{spirv_cross_commit}.tar.gz
# zf requires a different version of libvaxis than ghostty
Source14:       https://github.com/rockorager/libvaxis/archive/%{libvaxis_commit1}/libvaxis-%{libvaxis_commit1}.tar.gz
Source15:       https://github.com/rockorager/libvaxis/archive/%{libvaxis_commit2}/libvaxis-%{libvaxis_commit2}.tar.gz
# sentry is only used for catching errors and not for uploading
# PR to disable it https://github.com/ghostty-org/ghostty/pull/3934
Source16:       https://github.com/getsentry/sentry-native/archive/refs/tags/%{sentry_version}/sentry-native-%{sentry_version}.tar.gz
Source17:       https://github.com/KhronosGroup/glslang/archive/refs/tags/%{glslang_version}/glslang-%{glslang_version}.tar.gz
Source18:       https://github.com/google/highway/archive/refs/tags/%{highway_version}/highway-%{highway_version}.tar.gz
Source19:       https://github.com/mitchellh/libxev/archive/%{libxev_commit}/libxev-%{libxev_commit}.tar.gz
Source20:       https://github.com/ocornut/imgui/archive/%{imgui_commit}/imgui-%{imgui_commit}.tar.gz
Source21:       https://github.com/getsentry/breakpad/archive/%{breakpad_commit}/sentry-breakpad-%{breakpad_commit}.tar.gz
Source22:       https://github.com/google/wuffs/archive/refs/tags/v%{wuffs_version}/wuffs-%{wuffs_version}.tar.gz
Source23:       https://deps.files.ghostty.org/ziglyph-%{ziglyph_commit}.tar.gz
Source24:       https://github.com/natecraddock/zf/archive/%{zf_commit}/zf-%{zf_commit}.tar.gz
Source25:       https://github.com/zigimg/zigimg/archive/%{zigimg_commit}/zigimg-%{zigimg_commit}.tar.gz
Source26:       https://codeberg.org/atman/zg/archive/v%{zg_version}.tar.gz#/zg-%{zg_version}.tar.gz
Source27:       https://github.com/mitchellh/zig-objc/archive/%{zig_objc_commit}/zig-objc-%{zig_objc_commit}.tar.gz
Source28:       https://github.com/mitchellh/zig-js/archive/%{zig_js_commit}/zig-js-%{zig_js_commit}.tar.gz

# Required in 1.0.1, future releases have a merged PR to build using system -devel for fontconfig and freetype sources
Source29:       https://deps.files.ghostty.org/fontconfig-%{fontconfig_version}.tar.gz
# unbundling in process https://github.com/ghostty-org/ghostty/pull/4205
Source30:       https://github.com/freetype/freetype/archive/refs/tags/VER-%{freetype_dash_version}.tar.gz#/freetype2-%{freetype_dash_version}.tar.gz

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


Provides:      bundled(libvaxis) = 0~git6d729a2dc3b934818dffe06d2ba3ce02841ed74b 
Provides:      bundled(ziglyph) = 0~gitb89d43d1e3fb01b6074bc1f7fc980324b04d26a5 
Provides:      bundled(libxev) = 0~gitdb6a52bafadf00360e675fefa7926e8e6c0e9931 
Provides:      bundled(mach-glfw) = 0~git37c2995f31abcf7e8378fba68ddcf4a3faa02de0 
Provides:      bundled(zig-js) = 0~gitd0b8b0a57c52fbc89f9d9fecba75ca29da7dd7d1 
Provides:      bundled(zig-objc) = 0~git9b8ba849b0f58fe207ecd6ab7c147af55b17556e 
Provides:      bundled(zf) = 0~gited99ca18b02dda052e20ba467e90b623c04690dd 
Provides:      bundled(z2d) = 0.4.0 

%description
%{project_description}

%package terminfo
Summary:       Terminfo for ghostty (xterm-ghostty)
BuildArch:     noarch
License:        MIT AND MIT-Modern-Variant AND Zlib AND curl AND MPL-2.0 AND HPND AND LicenseRef-Fedora-Public-Domain AND Unicode-DFS-2016 AND Unicode-3.0 AND BSL-1.0 AND Apache-2.0 AND BSD-2-Clause AND BSD-3-Clause AND BSD-4-Clause AND (FTL OR GPL-2.0-or-later) AND APSL-2.0 AND ClArtistic AND GPL-3.0-or-later AND (GPL-2.0-or-later WITH Autoconf-exception-generic) AND OFL-1.1 AND (WTFPL OR CC0-1.0)

Requires:      ncurses-base

%description terminfo
%{project_description}

Terminfo files for %{name}

%prep
# Check source signature with minisign pubkey at https://github.com/ghostty-org/ghostty/blob/main/PACKAGING.md
minisign -Vm %{SOURCE0} -x %{SOURCE1} -P %{pubkey}
%setup -q %{setup_args}
# Put all packages in the cache using directory names after extracting archives

%zig_fetch utfcpp-%{utfcpp_version}
%zig_fetch iTerm2-Color-Schemes-%{iterm2_color_commit}
%zig_fetch z2d-%{z2d_commit}
%zig_fetch SPIRV-Cross-%{spirv_cross_commit}
%zig_fetch libvaxis-%{libvaxis_commit1}
%zig_fetch libvaxis-%{libvaxis_commit2}
%zig_fetch sentry-native-%{sentry_version}
%zig_fetch glslang-%{glslang_version}
%zig_fetch highway-%{highway_version}
%zig_fetch libxev-%{libxev_commit}
%zig_fetch imgui-%{imgui_commit}
%zig_fetch breakpad-%{breakpad_commit}
%zig_fetch wuffs-%{wuffs_version}
%zig_fetch ziglyph
%zig_fetch zf-%{zf_commit}
%zig_fetch zigimg-%{zigimg_commit}
%zig_fetch zg
%zig_fetch zig-objc-%{zig_objc_commit}
%zig_fetch zig-js-%{zig_js_commit}

# Change to stubs after 1.0.1
%zig_fetch fontconfig-%{fontconfig_version}
%zig_fetch freetype-VER-%{freetype_dash_version}

# stubbing some packages that don't need bundled sources
#	harfbuzz
mkdir -p %{_zig_cache_dir}/p/1220b8588f106c996af10249bfa092c6fb2f35fbacb1505ef477a0b04a7dd1063122
#	oniguruma
mkdir -p %{_zig_cache_dir}/p/1220c15e72eadd0d9085a8af134904d9a0f5dfcbed5f606ad60edc60ebeccd9706bb 
#   libxml2
mkdir -p %{_zig_cache_dir}/p/122032442d95c3b428ae8e526017fad881e7dc78eab4d558e9a58a80bfbd65a64f7d
#   libpng
mkdir -p %{_zig_cache_dir}/p/1220aa013f0c83da3fb64ea6d327f9173fa008d10e28bc9349eac3463457723b1c66
#   zlib
mkdir -p %{_zig_cache_dir}/p/1220fed0c74e1019b3ee29edae2051788b080cd96e90d56836eea857b0b966742efb


# ZIG_GLOBAL_CACHE_DIR="%{_zig_cache_dir}" ./nix/build-support/fetch-zig-cache.sh # _REQUIRES_NETWORK

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
%{zig_test} %{build_flags}
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
