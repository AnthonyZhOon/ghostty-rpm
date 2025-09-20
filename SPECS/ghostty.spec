# To handle zig package management which requires a cache directory of its dependencies
# build step with `zig fetch <url>`. We can instead download the archive
# sources and do `zig fetch <path>` to populate the package cache offline
%bcond test 1
%undefine _missing_build_ids_terminate_build

# The github short commit of the source code
%global short_commit 74b204b

%global utfcpp_version 4.0.5
%global iterm2_color_commit b314fc540434cc037c2811fc048d32854b5b78c3
%global z2d_version 0.8.1
%global spirv_cross_commit 476f384eb7d9e48613c45179e502a15ab95b6b49
%global libvaxis_commit1 1f41c121e8fc153d9ce8c6eb64b2bbab68ad7d23
%global libvaxis_commit2 dc0a228a5544988d4a920cfb40be9cd28db41423
%global ghostty_gobject_version 0.15.1-2025-09-04-48-1
%global glslang_version 14.2.0
%global highway_commit 66486a10623fa0d72fe91260f96c892e41aceb06
%global libxev_commit 7f803181b158a10fec8619f793e3b4df515566cb
%global imgui_commit e391fe2e66eb1c96b1624ae8444dc64c23146ef4
%global wuffs_version 0.4.0-alpha.9
%global ziglyph_commit b89d43d1e3fb01b6074bc1f7fc980324b04d26a5
%global zf_commit 7aacbe6d155d64d15937ca95ca6c014905eb531f
%global zigimg_commit 31268548fe3276c0e95f318a6c0d2ab10565b58d
%global zg_commit 4a002763419a34d61dcbb1f415821b83b9bf8ddc
%global zig_wayland_commit f3c5d503e540ada8cbcb056420de240af0c094f7 
%global wayland_commit 9cb3d7aa9dc995ffafdbdef7ab86a949d0fb0e7d
%global wayland_protocols_commit 258d8f88f2c8c25a830c6316f87d23ce1a0f12d9
%global plasma_wayland_protocols_commit db525e8f9da548cffa2ac77618dd0fbe7f511b86
%global jetbrains_mono_version 2.304
%global nerdfont_symbols_only_version 3.4.0

%global pubkey RWQlAjJC23149WL2sEpT/l0QKy7hMIFhYdQOFy0Z7z7PbneUgvlsnYcV

# Performance issues and debug build banner in safe
%global _zig_release_mode fast
%global _zig_cache_dir %{_builddir}/zig-cache

%global deps_start 10
%global deps_end 32

# zig-rpm-macros is broken for system integration
# fixed in zig-rpm-macros-0.13.0-4
%global build_flags %{shrink:
   --system %{_zig_cache_dir}/p \
   -fsys=simdutf \
   -Dgtk-wayland=true \
   -Dgtk-x11=true \
   -Dsentry=false \
   -Dstrip=false \
#  -Dversion-string=%{version} \
}

# populates the zig cache with dependency %1 through %2
# As I understand, parametric lua macros must be expanded at use-site
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
Version:        1.1.4~tip
Release:        %autorelease
Summary:        A fast, feature-rich, and cross-platform terminal emulator in Zig

# Licenses for the dependencies themselves and in-tree bindings under pkg/ (both dependency and bindings)
# Unbundled dependencies are stubbed and do not contain source code compiled into the result
# These do not require their license added to a Fedora package
#
# ghostty-gobject:            MIT
# ghostty:                    MIT
# iTerm2-Color-Schemes:       MIT
# libvaxis:                   MIT
# libxev:                     MIT
# pixels                      CC0-1.0
# pkg/cimgui:                 MIT
# pkg/glslang:                BSD-2-Clause AND BSD-3-Clause AND GPL-3.0-or-later AND Apache-2.0 AND MIT
# pkg/highway:                Apache-2.0 AND BSD-3-Clause
# pkg/spirv-cross:            Apache-2.0
# pkg/utfcpp:                 BSL-1.0
# pkg/wuffs:                  Apache-2.0 AND MIT
# plasma-wayland-protocols    LGPL-2.1-only
# vendor/glad                 (WTFPL OR CC0-1.0) AND Apache-2.0
# wayland                     MIT
# wayland-protocols           MIT
# z2d:                        MPL-2.0
# zf:                         MIT
# zg:                         MIT
# zigimg:                     MIT
# ziglyph:                    MIT
# zig-wayland                 MIT

## Bundled Fonts
# JetBrainsMono               OFL-1.1
# NerdFontSymbolsOnly         MIT

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


License:        MIT AND Apache-2.0 AND BSD-2-Clause AND BSD-3-Clause AND BSL-1.0 AND CC0-1.0 AND GPL-3.0-or-later AND LGPL-2.1-only AND MPL-2.0 AND OFL-1.1 AND (WTFPL OR CC0-1.0)
URL:            https://ghostty.org
Source0:        https://github.com/ghostty-org/ghostty/releases/download/tip/ghostty-source.tar.gz#/%{name}-%{short_commit}.tar.gz
Source1:        https://github.com/ghostty-org/ghostty/releases/download/tip/ghostty-source.tar.gz.minisig#/%{name}-%{short_commit}.tar.gz.minisig

# Take these archives from build.zig.zon.json
Source10:       https://github.com/nemtrif/utfcpp/archive/refs/tags/v%{utfcpp_version}/utfcpp-%{utfcpp_version}.tar.gz
Source11:       https://github.com/mbadolato/iTerm2-Color-Schemes/archive/%{iterm2_color_commit}/iTerm2-Color-Schemes-%{iterm2_color_commit}.tar.gz
Source12:       https://github.com/vancluever/z2d/archive/refs/tags/v%{z2d_version}.tar.gz
Source13:       https://github.com/KhronosGroup/SPIRV-Cross/archive/%{spirv_cross_commit}/SPIRV-Cross-%{spirv_cross_commit}.tar.gz
# zf requires a different version of libvaxis than ghostty
Source14:       https://github.com/rockorager/libvaxis/archive/%{libvaxis_commit1}/libvaxis-%{libvaxis_commit1}.tar.gz
Source15:       https://github.com/rockorager/libvaxis/archive/%{libvaxis_commit2}/libvaxis-%{libvaxis_commit2}.tar.gz
# sentry is only used for catching error dumps and not for uploading
Source16:       https://github.com/KhronosGroup/glslang/archive/refs/tags/%{glslang_version}/glslang-%{glslang_version}.tar.gz
Source17:       https://github.com/google/highway/archive/%{highway_commit}/highway-%{highway_commit}.tar.gz
Source18:       https://github.com/mitchellh/libxev/archive/%{libxev_commit}/libxev-%{libxev_commit}.tar.gz
Source19:       https://github.com/ocornut/imgui/archive/%{imgui_commit}/imgui-%{imgui_commit}.tar.gz
Source20:       https://github.com/google/wuffs/archive/refs/tags/v%{wuffs_version}/wuffs-%{wuffs_version}.tar.gz
Source21:       https://deps.files.ghostty.org/ziglyph-%{ziglyph_commit}.tar.gz
Source22:       https://github.com/natecraddock/zf/archive/%{zf_commit}/zf-%{zf_commit}.tar.gz
Source23:       https://github.com/TUSF/zigimg/archive/%{zigimg_commit}/zigimg-%{zigimg_commit}.tar.gz
Source24:       https://codeberg.org/atman/zg/archive/%{zg_commit}.tar.gz
Source25:       https://codeberg.org/ifreund/zig-wayland/archive/%{zig_wayland_commit}.tar.gz
Source26:       https://gitlab.freedesktop.org/wayland/wayland/-/archive/%{wayland_commit}/wayland-%{wayland_commit}.tar.gz
Source27:       https://gitlab.freedesktop.org/wayland/wayland-protocols/-/archive/%{wayland_protocols_commit}/wayland-protocols-%{wayland_protocols_commit}.tar.gz
Source28:       https://github.com/KDE/plasma-wayland-protocols/archive/%{plasma_wayland_protocols_commit}/plasma-wayland-protocols-%{plasma_wayland_protocols_commit}.tar.gz
# FIXME: Temporary fork until it is done in-tree
Source29:       https://github.com/jcollie/ghostty-gobject/releases/download/%{ghostty_gobject_version}/ghostty-gobject-%{ghostty_gobject_version}.tar.zst
Source30:       https://deps.files.ghostty.org/JetBrainsMono-%{jetbrains_mono_version}.tar.gz
Source31:       https://deps.files.ghostty.org/NerdFontsSymbolsOnly-%{nerdfont_symbols_only_version}.tar.gz
Source32:       https://github.com/make-github-pseudonymous-again/pixels/archive/d843c2714d32e15b48b8d7eeb480295af537f877/pixels-d843c27.tar.gz

ExclusiveArch: %{zig_arches}
# Compile with zig, which bundles a C/C++ compiler
# Use pandoc to build docs, minisign to check signature
BuildRequires:  (zig >= 0.14.0 with zig < 0.15.0~)
BuildRequires:  zig-rpm-macros
# Installing systemd unit files
BuildRequires:  systemd-rpm-macros
BuildRequires:  pandoc
BuildRequires:  minisign
# Compile gtk blueprints for UI
BuildRequires:  blueprint-compiler
# Compiling locale files
BuildRequires:  gettext
BuildRequires:  zig-rpm-macros
BuildRequires:  zig-srpm-macros

BuildRequires:  pkgconfig(fontconfig)
BuildRequires:  pkgconfig(freetype2)
BuildRequires:  pkgconfig(glib-2.0)
BuildRequires:  pkgconfig(gtk4)
BuildRequires:  pkgconfig(gtk4-layer-shell-0)
BuildRequires:  pkgconfig(harfbuzz)
BuildRequires:  pkgconfig(libadwaita-1)
BuildRequires:  pkgconfig(libpng)
BuildRequires:  pkgconfig(oniguruma)
BuildRequires:  pkgconfig(simdutf) >= 5.2.8
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
Provides:       bundled(font(JetBrainsMonoNoNF)) = %{jetbrains_mono_version}
Provides:       bundled(font(NerdFontSymbolsOnly)) = %{nerdfont_symbols_only_version}

# Statically linked dependencies
Provides:       bundled(glslang) = %{glslang_version}
Provides:       bundled(highway) = 0~git%{highway_commit}
Provides:       bundled(libvaxis) = 0~git6d729a2dc3b934818dffe06d2ba3ce02841ed74b
Provides:       bundled(libxev) = 0~gitdb6a52bafadf00360e675fefa7926e8e6c0e9931
Provides:       bundled(mach-glfw) = 0~git37c2995f31abcf7e8378fba68ddcf4a3faa02de0
Provides:       bundled(spirv-cross) = 13.1.1
Provides:       bundled(wayland) = 0~git%{wayland_commit}
Provides:       bundled(wayland-protocols) = 0~git%{wayland_protocols_commit}
Provides:       bundled(plasma-wayland-protocols) = 0~git%{plasma_wayland_protocols_commit}
Provides:       bundled(z2d) = %{z2d_version}
Provides:       bundled(zf) = 0~git%{zf_commit}
Provides:       bundled(zg) = 0~git%{zg_commit}
Provides:       bundled(ghostty-gobject) = 0.3.0
Provides:       bundled(ziglyph) = 0~git%{ziglyph_commit}
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
%setup -q -n ghostty-1.1.4-main+%{short_commit}
# Fill zig_cache with dependency sources
# zig will identify fetched dependencies at build time.
%zig_extract %deps_start %deps_end

# stubbing some packages that don't need bundled sources as we opt to dynamic link
# Find hash by building without fetch which compares against build.zig.zon hash
# libxml2
%stub_package  N-V-__8AAG3RoQEyRC2Vw7Qoro5SYBf62IHn3HjqtNVY6aWK
# pixels (wuffs test)
%stub_package  N-V-__8AADYiAAB_80AWnH1AxXC0tql9thT-R-DYO1gBqTLc

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
%{_metainfodir}/%{project_id}.metainfo.xml
%{_userunitdir}/app-%{project_id}.service
%{_datadir}/dbus-1/services/%{project_id}.service


%{_datadir}/icons/hicolor/*/apps/%{project_id}.png
%{_mandir}/man{1,5}/%{name}.{1,5}*

# Shell completions
%{bash_completions_dir}/%{name}.bash
%{fish_completions_dir}/%{name}.fish
%{zsh_completions_dir}/_%{name}
# Locale files
%{expand:%{lua:
   local locales = {
   "bg_BG",
   "ca_ES",
   "de_DE",
   "es_AR",
   "es_BO",
   "fr_FR",
   "ga_IE",
   "he_IL",
   "hu_HU",
   "id_ID",
   "it_IT",
   "ja_JP",
   "ko_KR",
   "mk_MK",
   "nb_NO",
   "nl_NL",
   "pl_PL",
   "pt_BR",
   "ru_RU",
   "tr_TR",
   "uk_UA",
   "zh_CN",
   }
   local joined = table.concat(locales, ",")
   print("%{_datadir}/locale/{" .. joined .. "}.UTF-8/LC_MESSAGES/%{project_id}.mo")
}}

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
