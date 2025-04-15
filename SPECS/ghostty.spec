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

%global utfcpp_version 4.0.5
%global iterm2_color_commit db227d159adc265818f2e898da0f70ef8d7b580e
%global z2d_commit 4638bb02a9dc41cc2fb811f092811f6a951c752a
%global spirv_cross_commit 476f384eb7d9e48613c45179e502a15ab95b6b49
%global libvaxis_commit1 6d729a2dc3b934818dffe06d2ba3ce02841ed74b
%global libvaxis_commit2 dc0a228a5544988d4a920cfb40be9cd28db41423
%global glslang_version 14.2.0
%global highway_version 1.1.0
%global libxev_commit 31eed4e337fed7b0149319e5cdbb62b848c24fbd
%global imgui_commit e391fe2e66eb1c96b1624ae8444dc64c23146ef4
%global wuffs_version 0.4.0-alpha.9
%global ziglyph_commit b89d43d1e3fb01b6074bc1f7fc980324b04d26a5
%global zf_commit ed99ca18b02dda052e20ba467e90b623c04690dd
%global zigimg_commit 3a667bdb3d7f0955a5a51c8468eac83210c1439e
%global zig_gjobject_version 0.2.2
%global zg_version 0.13.2
%global zig_wayland_commit fbfe3b4ac0b472a27b1f1a67405436c58cbee12d 
%global wayland_commit 9cb3d7aa9dc995ffafdbdef7ab86a949d0fb0e7d
%global wayland_protocols_commit 258d8f88f2c8c25a830c6316f87d23ce1a0f12d9
%global plasma_wayland_protocols_commit db525e8f9da548cffa2ac77618dd0fbe7f511b86

%global pubkey RWQlAjJC23149WL2sEpT/l0QKy7hMIFhYdQOFy0Z7z7PbneUgvlsnYcV

# Performance issues and debug build banner in safe
%global _zig_release_mode fast
%global _zig_cache_dir %{_builddir}/zig-cache

%global deps_start 10
%global deps_end 29

# zig-rpm-macros is broken for system integration
# fixed in zig-rpm-macros-0.13.0-4
%global build_flags %{shrink:
   --system %{_zig_cache_dir}/p \
   %{?with_simdutf:-fsys=simdutf} \
   -Dgtk-wayland=true \
   -Dgtk-x11=true \
   -Dsentry=false \
   -Dstrip=false \
   -Dversion-string=%{version} \
}

# populates the zig cache with dependency %1 through %2
%define zig_extract() %{lua:
   for i = arg[1]//1, arg[2]//1 do 
      print(rpm.expand("\%zig_fetch \%{SOURCE" .. i .. "}") .. "\\n") 
   end
}
%global stub_package() %{expand:mkdir -p %{_zig_cache_dir}/p/%1}

%global project_id          com.mitchellh.ghostty
%global project_description %{expand:
Ghostty is a cross-platform, GPU-accelerated terminal emulator that aims to push 
the boundaries of what is possible with a terminal emulator by exposing modern, 
opt-in features that enable CLI tool developers to build more feature rich, 
interactive applications.}


Name:           ghostty
Version:        1.1.3
Release:        %autorelease
Summary:        A fast, feature-rich, and cross-platform terminal emulator in Zig

# Licenses for the dependencies themselves and in-tree bindings under pkg/ (both dependency and bindings)
# Unbundled dependencies are stubbed and do not contain source code compiled into the result
# These do not require their license added to a Fedora package
#
# ghostty:                    MIT
# libvaxis:                   MIT
# libxev:                     MIT
# plasma-wayland-protocols    LGPL-2.1-only
# wayland                     MIT
# wayland-protocols           MIT
# zig-gobject                 0BSD
# zig-wayland                 MIT
# z2d:                        MPL-2.0
# zf:                         MIT
# zigimg:                     MIT
# ziglyph:                    MIT
# zg:                         MIT
# iTerm2-Color-Schemes:       MIT
# pkg/utfcpp:                 BSL-1.0
# pkg/spirv-cross:            Apache-2.0
# pkg/glslang:                BSD-2-Clause AND BSD-3-Clause AND GPL-3.0-or-later AND Apache-2.0 AND MIT
# pkg/highway:                Apache-2.0 AND BSD-3-Clause
# pkg/cimgui:                 MIT
# pkg/wuffs:                  Apache-2.0 AND MIT
# vendor/glad                 (WTFPL OR CC0-1.0) AND Apache-2.0

## unbundled
# pkg/breakpad:               MIT AND BSD-2-Clause AND BSD-3-Clause AND BSD-4-Clause AND Apache-2.0 AND MIT AND curl AND APSL-2.0 AND ClArtistic AND Unicode-3.0 AND LicenseRef-Fedora-Public-Domain AND (GPL-2.0-or-later WITH Autoconf-exception-generic)
# pkg/fontconfig:             MIT-Modern-Variant AND MIT AND HPND AND LicenseRef-Fedora-Public-Domain AND Unicode-DFS-2016
# pkg/freetype:               (FTL OR GPL-2.0-or-later) AND (MIT or Apache-2.0)AND Zlib
# pkg/gtk4-layer-shell        MIT
# pkg/harfbuzz:               MIT-Modern-Variant
# pkg/libintl:                LGPL-2.1-only
# pkg/oniguruma:              BSD-2-Clause
# pkg/sentry:                 MIT
# zig-js:                     MIT
# zig-objc:                   MIT

# CodeNewRoman                OFL-1.1
# GeistMono                   OFL-1.1
# Inconsolata                 OFL-1.1
# JetBrainsMono               OFL-1.1
# JuliaMono                   OFL-1.1
# KawkabMono                  OFL-1.1
# Lilex                       OFL-1.1
# MonaspaceNeon               OFL-1.1
# NotoEmoji                   OFL-1.1
# CozetteVector               MIT
# NerdFont                    MIT AND OFL-1.1

License:        MIT AND 0BSD AND Apache-2.0 AND BSD-2-Clause AND BSD-3-Clause AND BSL-1.0 AND GPL-3.0-or-later AND LGPL-2.1-only AND MPL-2.0 AND OFL-1.1 AND (WTFPL OR CC0-1.0)
URL:            https://ghostty.org

Source0:        https://release.files.ghostty.org/%{version}/ghostty-%{version}.tar.gz
Source1:        https://release.files.ghostty.org/%{version}/ghostty-%{version}.tar.gz.minisig

# Take these archives from recursively searching URLs in build.zig.zon files, and build errors when not included
Source10:       https://github.com/nemtrif/utfcpp/archive/refs/tags/v%{utfcpp_version}/utfcpp-%{utfcpp_version}.tar.gz
Source11:       https://github.com/mbadolato/iTerm2-Color-Schemes/archive/%{iterm2_color_commit}/iTerm2-Color-Schemes-%{iterm2_color_commit}.tar.gz
Source12:       https://github.com/vancluever/z2d/archive/%{z2d_commit}/z2d-%{z2d_commit}.tar.gz
Source13:       https://github.com/KhronosGroup/SPIRV-Cross/archive/%{spirv_cross_commit}/SPIRV-Cross-%{spirv_cross_commit}.tar.gz
# zf requires a different version of libvaxis than ghostty
Source14:       https://github.com/rockorager/libvaxis/archive/%{libvaxis_commit1}/libvaxis-%{libvaxis_commit1}.tar.gz
Source15:       https://github.com/rockorager/libvaxis/archive/%{libvaxis_commit2}/libvaxis-%{libvaxis_commit2}.tar.gz
# sentry is only used for catching error dumps and not for uploading
Source16:       https://github.com/KhronosGroup/glslang/archive/refs/tags/%{glslang_version}/glslang-%{glslang_version}.tar.gz
Source17:       https://github.com/google/highway/archive/refs/tags/%{highway_version}/highway-%{highway_version}.tar.gz
Source18:       https://github.com/mitchellh/libxev/archive/%{libxev_commit}/libxev-%{libxev_commit}.tar.gz
Source19:       https://github.com/ocornut/imgui/archive/%{imgui_commit}/imgui-%{imgui_commit}.tar.gz
Source20:       https://github.com/google/wuffs/archive/refs/tags/v%{wuffs_version}/wuffs-%{wuffs_version}.tar.gz
Source21:       https://deps.files.ghostty.org/ziglyph-%{ziglyph_commit}.tar.gz
Source22:       https://github.com/natecraddock/zf/archive/%{zf_commit}/zf-%{zf_commit}.tar.gz
Source23:       https://github.com/zigimg/zigimg/archive/%{zigimg_commit}/zigimg-%{zigimg_commit}.tar.gz
Source24:       https://codeberg.org/atman/zg/archive/v%{zg_version}.tar.gz
Source25:       https://codeberg.org/ifreund/zig-wayland/archive/%{zig_wayland_commit}.tar.gz
Source26:       https://gitlab.freedesktop.org/wayland/wayland/-/archive/%{wayland_commit}/wayland-%{wayland_commit}.tar.gz
Source27:       https://gitlab.freedesktop.org/wayland/wayland-protocols/-/archive/%{wayland_protocols_commit}/wayland-protocols-%{wayland_protocols_commit}.tar.gz
Source28:       https://github.com/KDE/plasma-wayland-protocols/archive/%{plasma_wayland_protocols_commit}/plasma-wayland-protocols-%{plasma_wayland_protocols_commit}.tar.gz
Source29:       https://github.com/ianprime0509/zig-gobject/releases/download/v%{zig_gjobject_version}/bindings-gnome47.tar.zst

ExclusiveArch: %{zig_arches}
# Compile with zig, which bundles a C/C++ compiler
# Use pandoc to build docs, minisign to check signature
BuildRequires:  (zig >= 0.13.0 with zig < 0.14.0~)
BuildRequires:  pandoc
BuildRequires:  minisign
BuildRequires:  zig-rpm-macros
BuildRequires:  zig-srpm-macros

BuildRequires:  pkgconfig(fontconfig)
BuildRequires:  pkgconfig(freetype2)
BuildRequires:  pkgconfig(glib-2.0)
BuildRequires:  pkgconfig(gtk4)
BuildRequires:  pkgconfig(harfbuzz)
BuildRequires:  pkgconfig(libadwaita-1)
BuildRequires:  pkgconfig(libpng)
BuildRequires:  pkgconfig(oniguruma)
%if %{with simdutf}
BuildRequires:  pkgconfig(simdutf) >= 5.2.8
%endif
BuildRequires:  pkgconfig(zlib-ng)


# Validate desktop vile and deduplicate files according to lints + guidelines
BuildRequires:  desktop-file-utils
BuildRequires:  fdupes

%if %{with test}
BuildRequires:  hostname
%endif

Requires:       %{name}-terminfo = %{version}-%{release}
Requires:       hicolor-icon-theme
# System-wide add-ons for other applications
# Can become reverse-dependencies later
Suggests:       %{name}-syntax-vim = %{version}-%{release}
Suggests:       %{name}-nautilus = %{version}-%{release}
Suggests:       %{name}-dolphin = %{version}-%{release}
# Embedded fonts
# see src/font/embedded.zig, most fonts are in source for tests and only
# JetBrainsMono, Noto Color Emoji, and Noto Color are in the application.
# Discovered with  `fc-query -f '%{fontversion}\n' ./CozetteVector.ttf | perl -E 'printf "%.3f\n", <>/65536.0'`
Provides:       bundled(font(CodeNewRoman)) = 2.000
Provides:       bundled(font(CozetteVector)) = 1.22.2
Provides:       bundled(font(GeistMono)) = 1.2.0
Provides:       bundled(font(Inconsolata)) = 3.001
Provides:       bundled(font(JetBrainsMonoNerdFont)) = 2.304
Provides:       bundled(font(JetBrainsMonoNoNF)) = 2.304
Provides:       bundled(font(JuliaMono)) = 0.055
# Version does not match known releases
Provides:       bundled(font(KawkabMono)) = 1.000 
Provides:       bundled(font(Lilex)) = 2.200 
Provides:       bundled(font(MonaspaceNeon)) = 1.000
Provides:       bundled(font(NotoColorEmoji)) = 2.034
Provides:       bundled(font(NotoEmoji)) = 1.002

# Statically linked dependencies
Provides:       bundled(glslang) = 14.2.0
Provides:       bundled(libvaxis) = 0~git6d729a2dc3b934818dffe06d2ba3ce02841ed74b
Provides:       bundled(libxev) = 0~gitdb6a52bafadf00360e675fefa7926e8e6c0e9931
Provides:       bundled(mach-glfw) = 0~git37c2995f31abcf7e8378fba68ddcf4a3faa02de0
%if %{without simdutf}
Provides:       bundled(simdutf) = 5.2.8
%endif
Provides:       bundled(spirv-cross) = 13.1.1
Provides:       bundled(wayland) = 0~git%{wayland_commit}
Provides:       bundled(wayland-protocols) = 0~git%{wayland_protocols_commit}
Provides:       bundled(plasma-wayland-protocols) = 0~git%{plasma_wayland_protocols_commit}
Provides:       bundled(z2d) = 0.4.0
Provides:       bundled(zf) = 0~gited99ca18b02dda052e20ba467e90b623c04690dd
Provides:       bundled(zg) = %{zg_version}
Provides:       bundled(zig-gobject) = %{zig_gjobject_version}
Provides:       bundled(ziglyph) = 0~gitb89d43d1e3fb01b6074bc1f7fc980324b04d26a5
Provides:       bundled(zig-wayland) = 0~git%{zig_wayland_commit}

%description
%{project_description}

%package terminfo
Summary:       Terminfo for ghostty terminal
BuildArch:     noarch

Requires:      ncurses-base
Supplements:   %{name}

%description terminfo
%{project_description}

Terminfo files for %{name} terminal

%package nautilus
Summary:       Nautilus extension for %{name}
BuildArch:     noarch

Requires:      nautilus-python
Requires:      %{name} = %{version}-%{release}
Supplements:   %{name}

%description nautilus
Provides the 'Open in Ghostty' action to start the terminal.

%package dolphin
Summary:       Dolphin service menu add-on for %{name}
BuildArch:     noarch

Requires:      kf6-filesystem
Requires:      %{name} = %{version}-%{release}
Supplements:   %{name}

%description dolphin
Provides the 'Open in Ghostty' menu to start the terminal.

%package syntax-vim
Summary:       Vim syntax plugin for highlighting %{name}'s files
BuildArch:     noarch

Requires:      vim-filesystem
Requires:      %{name} = %{version}-%{release}
Supplements:   %{name}

%description syntax-vim
Provides vim syntax and filetype plugins to highlight Ghostty config and theme files

%prep
# Check source signature with minisign pubkey at https://github.com/ghostty-org/ghostty/blob/main/PACKAGING.md
minisign -Vm %{SOURCE0} -x %{SOURCE1} -P %{pubkey}
%setup -q
# Fill zig_cache with dependency sources
# zig will identify fetched dependencies at build time.
%zig_extract %deps_start %deps_end

# stubbing some packages that don't need bundled sources
# Find hash by building without fetch which compares against build.zig.zon hash
# freetype
%stub_package '1220b81f6ecfb3fd222f76cf9106fecfa6554ab07ec7fdc4124b9bb063ae2adf969d'
# fontconfig
%stub_package '12201149afb3326c56c05bb0a577f54f76ac20deece63aa2f5cd6ff31a4fa4fcb3b7'
# harfbuzz
%stub_package '1220b8588f106c996af10249bfa092c6fb2f35fbacb1505ef477a0b04a7dd1063122'
# libxml2
%stub_package '122032442d95c3b428ae8e526017fad881e7dc78eab4d558e9a58a80bfbd65a64f7d'
# libpng
%stub_package '1220aa013f0c83da3fb64ea6d327f9173fa008d10e28bc9349eac3463457723b1c66'
# oniguruma
%stub_package '1220c15e72eadd0d9085a8af134904d9a0f5dfcbed5f606ad60edc60ebeccd9706bb'
# pixels (wuffs test)
%stub_package '12207ff340169c7d40c570b4b6a97db614fe47e0d83b5801a932dcd44917424c8806'
# zlib
%stub_package '1220fed0c74e1019b3ee29edae2051788b080cd96e90d56836eea857b0b966742efb'
# sentry
%stub_package '1220446be831adcca918167647c06c7b825849fa3fba5f22da394667974537a9c77e'
# breakpad
%stub_package '12207fd37bb8251919c112dcdd8f616a491857b34a451f7e4486490077206dc2a1ea'
# zig_js
%stub_package '12205a66d423259567764fa0fc60c82be35365c21aeb76c5a7dc99698401f4f6fefc'
# zig_objc
%stub_package '1220e17e64ef0ef561b3e4b9f3a96a2494285f2ec31c097721bf8c8677ec4415c634'

%build
%{zig_build} %{build_flags}


%install
%{zig_install} %{build_flags}
%fdupes %{buildroot}/${_datadir}

# remove unused files
# Not supported by hicolor-icon-theme
rm %{buildroot}/%{_datadir}/icons/hicolor/1024x1024/apps/%{project_id}.png
# Does not support system-wide configuration
rm %{buildroot}/%{_datadir}/bat/syntaxes/%{name}.sublime-syntax
# It seems inappropriate to modify the /usr/share/nvim/runtime dir 
# and the neovim package does not support a -filesystem package
# installing under /usr/share/nvim/site will not enable the plugins without
# adding to the nvim runtimepath variable. So not packaged
rm %{buildroot}/%{_datadir}/nvim/site/{ftdetect,ftplugin,syntax,compiler}/%{name}.vim
# Avoid conflict with ncurses-term packaging this terminfo file
rm %{buildroot}/%{_datadir}/terminfo/g/ghostty


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


%{_datadir}/icons/hicolor/*/apps/%{project_id}.png
%{_mandir}/man{1,5}/%{name}.{1,5}*

# Shell completions
%{bash_completions_dir}/%{name}.bash
%{fish_completions_dir}/%{name}.fish
%{zsh_completions_dir}/_%{name}

%docdir %{_datadir}/%{name}/doc
%doc README.md

%files terminfo
%license LICENSE
# the terminfo/x/xterm-ghostty or terminfo/g/ghostty file is used as a sentinel to discover the GHOSTTY_RESOURCES_DIR automatically
%{_datadir}/terminfo/x/xterm-%{name}

%files nautilus
%license LICENSE
%{_datadir}/nautilus-python/extensions/%{name}.py

%files syntax-vim
%license LICENSE
%{_datadir}/vim/vimfiles/{ftdetect,ftplugin,syntax,compiler}/%{name}.vim

%files dolphin
%license LICENSE
%attr(644, -, -)
%{_datadir}/kio/servicemenus/%{project_id}.desktop

%changelog
%autochangelog
