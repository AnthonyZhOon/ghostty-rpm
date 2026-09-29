# Zig 0.16 fetches dependencies into the project-local zig-pkg directory.
# The RPM build uses those extracted packages in offline --system mode.
%bcond test 1
%undefine _missing_build_ids_terminate_build

# The github short commit of the source code
%global short_commit b40acce

%global utfcpp_version 4.0.5
%global iterm2_color_release_tag 20260921-150923-0b55a9e
%global z2d_version 0.12.1
%global z2d_commit 7dbae85c81784dba9988320bf9543ed9a81350c8
%global spirv_cross_commit 476f384eb7d9e48613c45179e502a15ab95b6b49
%global translate_c_commit 4e879eb8aba615de112eabd1231ea6e01920cead
%global aro_commit f97cdfc3779aec4b242299e2fc9a1c828c3547c6
%global libvaxis_commit 1dbbe575dff4586fe51e3217aa5c3fecdcbb6089
%global libvaxis_zf_commit c1e1f23be38951c425cdf31af455ba23ef178940
%global ghostty_gobject_version 0.3.2-2026-07-28-36-1
%global glslang_version 14.2.0
%global highway_commit 66486a10623fa0d72fe91260f96c892e41aceb06
%global libxev_commit 9ce8e8e6ff89e583258a7f8e7adeeeaeae8611bf
%global imgui_version 1.92.5-docking
%global uucode_commit1 2826a37a4562284fdacd8fa029d49509cc9bffcd
%global uucode_commit2 9d55524551411b493cca41ca06363625d90aff1e
%global wuffs_version 0.3.5
%global zf_commit c35c421f84895193246db06c40683c1a30e616ef
%global zigimg_commit d695acd97c02e57bb151e8f659d1280f5cd6ca70
%global zig_wayland_version 0.6.0
%global wayland_commit 9cb3d7aa9dc995ffafdbdef7ab86a949d0fb0e7d
%global wayland_protocols_commit 258d8f88f2c8c25a830c6316f87d23ce1a0f12d9
%global wayland_protocols_version 1.47
%global plasma_wayland_protocols_commit db525e8f9da548cffa2ac77618dd0fbe7f511b86
%global jetbrains_mono_version 2.304
%global nerdfont_symbols_only_version 3.4.0

%global pubkey RWQlAjJC23149WL2sEpT/l0QKy7hMIFhYdQOFy0Z7z7PbneUgvlsnYcV

# Performance issues and debug build banner in safe
%global _zig_release_mode fast
%global _zig_cache_dir %{_builddir}/zig-cache
# zig-rpm-macros defaults this to the relative project-local path.  Zig 0.16
# requires an absolute package directory for dependencies that run build.zig.
%global _zig_system_integration --system %{_builddir}/%{buildsubdir}/zig-pkg

%global deps_start 10
%global deps_end 36

# zig-rpm-macros is broken for system integration
# fixed in zig-rpm-macros-0.13.0-4
%global build_flags %{shrink:
   -fsys=simdutf \
   -Dgtk-wayland=true \
   -Dgtk-x11=true \
   -Dsentry=false \
   -Dstrip=false \
   -Dversion-string=%{version} \
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
Version:        1.3.2+%{short_commit}
Release:        %autorelease
Summary:        A fast, feature-rich, and cross-platform terminal emulator in Zig

# Licenses for the dependencies themselves and in-tree bindings under pkg/ (both dependency and bindings)
# Unbundled dependencies are stubbed and do not contain source code compiled into the result
# These do not require their license added to a Fedora package
#
# ghostty-gobject:            MIT
# ghostty:                    MIT
# ghostty_nautilus.py:        GPL-2.0-or-later
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
# uucode                      MIT AND Unicode-3.0
# vendor/glad                 (WTFPL OR CC0-1.0) AND Apache-2.0
# wayland                     MIT
# wayland-protocols           MIT
# z2d:                        MPL-2.0
# zf:                         MIT
# zigimg:                     MIT
# zig-wayland                 MIT

## Build-only bundled sources included in the source RPM
# aro:                        MIT
# translate-c:                MIT

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


License:        MIT AND Apache-2.0 AND BSD-2-Clause AND BSD-3-Clause AND BSL-1.0 AND CC0-1.0 AND GPL-2.0-or-later AND GPL-3.0-or-later AND LGPL-2.1-only AND MPL-2.0 AND OFL-1.1 AND Unicode-3.0 AND (WTFPL OR CC0-1.0)
URL:            https://ghostty.org
Source0:        https://github.com/ghostty-org/ghostty/releases/download/tip/ghostty-source.tar.gz#/%{name}-%{short_commit}.tar.gz
Source1:        https://github.com/ghostty-org/ghostty/releases/download/tip/ghostty-source.tar.gz.minisig#/%{name}-%{short_commit}.tar.gz.minisig

# Take these archives from build.zig.zon.json
Source10:       https://github.com/nemtrif/utfcpp/archive/refs/tags/v%{utfcpp_version}/utfcpp-%{utfcpp_version}.tar.gz
Source11:       https://github.com/mbadolato/iTerm2-Color-Schemes/releases/download/release-%{iterm2_color_release_tag}/ghostty-themes.tgz#/ghostty-themes-%{iterm2_color_release_tag}.tgz
Source12:       https://github.com/vancluever/z2d/archive/%{z2d_commit}/z2d-%{z2d_commit}.tar.gz
Source13:       https://github.com/KhronosGroup/SPIRV-Cross/archive/%{spirv_cross_commit}/SPIRV-Cross-%{spirv_cross_commit}.tar.gz
# zf requires a different version of libvaxis than ghostty
Source14:       https://github.com/rockorager/libvaxis/archive/%{libvaxis_zf_commit}/libvaxis-%{libvaxis_zf_commit}.tar.gz
# sentry is only used for catching error dumps and not for uploading
Source15:       https://github.com/KhronosGroup/glslang/archive/refs/tags/%{glslang_version}/glslang-%{glslang_version}.tar.gz
Source16:       https://github.com/google/highway/archive/%{highway_commit}/highway-%{highway_commit}.tar.gz
Source17:       https://github.com/mitchellh/libxev/archive/%{libxev_commit}/libxev-%{libxev_commit}.tar.gz
Source18:       https://github.com/ocornut/imgui/archive/refs/tags/v%{imgui_version}/imgui-%{imgui_version}.tar.gz
Source19:       https://deps.files.ghostty.org/DearBindings_v0.17_ImGui_v%{imgui_version}.tar.gz
Source20:       https://github.com/google/wuffs-mirror-release-c/archive/refs/tags/v%{wuffs_version}/wuffs-mirror-release-c-v%{wuffs_version}.tar.gz
Source21:       https://github.com/natecraddock/zf/archive/%{zf_commit}/zf-%{zf_commit}.tar.gz
Source22:       https://github.com/zigimg/zigimg/archive/%{zigimg_commit}/zigimg-%{zigimg_commit}.tar.gz
Source23:       https://codeberg.org/ifreund/zig-wayland/archive/v%{zig_wayland_version}.tar.gz
Source24:       https://gitlab.freedesktop.org/wayland/wayland/-/archive/%{wayland_commit}/wayland-%{wayland_commit}.tar.gz
Source25:       https://gitlab.freedesktop.org/wayland/wayland-protocols/-/archive/%{wayland_protocols_commit}/wayland-protocols-%{wayland_protocols_commit}.tar.gz
Source26:       https://github.com/KDE/plasma-wayland-protocols/archive/%{plasma_wayland_protocols_commit}/plasma-wayland-protocols-%{plasma_wayland_protocols_commit}.tar.gz
# FIXME: Temporary fork until it is done in-tree
Source27:       https://github.com/ghostty-org/zig-gobject/releases/download/0.10.0-2026-07-28-36-1/ghostty-gobject-0.10.0-2026-07-28-36-1.tar.zst
Source28:       https://deps.files.ghostty.org/JetBrainsMono-%{jetbrains_mono_version}.tar.gz
Source29:       https://deps.files.ghostty.org/NerdFontsSymbolsOnly-%{nerdfont_symbols_only_version}.tar.gz
Source30:       https://github.com/make-github-pseudonymous-again/pixels/archive/d843c2714d32e15b48b8d7eeb480295af537f877/pixels-d843c27.tar.gz
Source31:       https://github.com/jacobsandlund/uucode/archive/%{uucode_commit1}/uucode-%{uucode_commit1}.tar.gz
Source32:       https://github.com/jacobsandlund/uucode/archive/%{uucode_commit2}/uucode-%{uucode_commit2}.tar.gz
Source33:       https://codeberg.org/vancluever/translate-c/archive/%{translate_c_commit}.tar.gz
Source34:       https://github.com/rockorager/libvaxis/archive/%{libvaxis_commit}/libvaxis-%{libvaxis_commit}.tar.gz
Source35:       https://github.com/vancluever/arocc/archive/%{aro_commit}/arocc-%{aro_commit}.tar.gz
Source36:       https://gitlab.freedesktop.org/wayland/wayland-protocols/-/archive/%{wayland_protocols_version}/wayland-protocols-%{wayland_protocols_version}.tar.gz
Source37:       https://www.gnu.org/licenses/old-licenses/gpl-2.0.txt#/GPL-2.0-or-later.txt

ExclusiveArch: %{zig_arches}
# Compile with zig, which bundles a C/C++ compiler
# Use pandoc to build docs, minisign to check signature
BuildRequires:  (zig >= 0.16.0 with zig < 0.17.0~)
BuildRequires:  zig-rpm-macros
# Installing systemd unit files
BuildRequires:  systemd-rpm-macros
BuildRequires:  pandoc
BuildRequires:  minisign
# Compile gtk blueprints for UI
BuildRequires:  blueprint-compiler
# Fix the static archive produced by Zig when system libraries are enabled
BuildRequires:  binutils
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
BuildRequires:  valgrind
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
Provides:       bundled(libvaxis) = 0~git%{libvaxis_commit}
Provides:       bundled(libxev) = 0~git%{libxev_commit}
Provides:       bundled(mach-glfw) = 0~git37c2995f31abcf7e8378fba68ddcf4a3faa02de0
Provides:       bundled(spirv-cross) = 13.1.1
Provides:       bundled(uucode) = 0~git%{uucode_commit1}
Provides:       bundled(uucode) = 0~git%{uucode_commit2}
Provides:       bundled(wayland) = 0~git%{wayland_commit}
Provides:       bundled(wayland-protocols) = %{wayland_protocols_version}
Provides:       bundled(plasma-wayland-protocols) = 0~git%{plasma_wayland_protocols_commit}
Provides:       bundled(wuffs) = %{wuffs_version}
Provides:       bundled(z2d) = %{z2d_version}
Provides:       bundled(zf) = 0~git%{zf_commit}
Provides:       bundled(zigimg) = 0~git%{zigimg_commit}
Provides:       bundled(ghostty-gobject) = 0.3.2
Provides:       bundled(zig-wayland) = %{zig_wayland_version}

%description %{project_description}

%package lib
Summary:       Shared library for %{name}

%description lib
Shared library for %{name} to enable embedding terminal 
functionality into other applications

%package devel
Summary:       Development files for %{name}

Requires:     %{name}-lib%{?isa} = %{version}-%{release}

%description devel
Library headers for %{name} to enable embedding terminal 
functionality into other applications

%package terminfo
Summary:       Terminfo for ghostty terminal
BuildArch:     noarch

Requires:      ncurses-base
Supplements:   %{name}

%description terminfo %{project_description}

Terminfo files for %{name} terminal

%package nautilus
Summary:       Nautilus extension for %{name}
License:       GPL-2.0-or-later
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
Provides Vim syntax and file-type plugins to highlight Ghostty configuration
and theme files.

%prep
# Check source signature with minisign pubkey at https://github.com/ghostty-org/ghostty/blob/main/PACKAGING.md
minisign -Vm %{SOURCE0} -x %{SOURCE1} -P %{pubkey}
%setup -q -n ghostty-1.3.2-main+%{short_commit}

%zig_prep
%zig_extract %deps_start %deps_end

# stubbing some packages that don't need bundled sources as we opt to dynamic link
# Find hash by building without fetch which compares against build.zig.zon hash
# libxml2
%stub_package  N-V-__8AAG3RoQEyRC2Vw7Qoro5SYBf62IHn3HjqtNVY6aWK

%build
%{zig_build} %{build_flags}


%install
%{zig_install} %{build_flags}

# The Nautilus extension is GPL-2.0-or-later while the main project is MIT.
install -Dpm0644 %{SOURCE37} \
    %{buildroot}%{_licensedir}/%{name}-nautilus/GPL-2.0-or-later.txt

# Zig's archive combiner includes the dynamically linked system simdutf object
# in the static archive. Keep simdutf external as declared by the pkg-config
# metadata and leave only relocatable objects in the archive.
ar d %{buildroot}%{_libdir}/lib%{name}-vt.a libsimdutf.so
ranlib %{buildroot}%{_libdir}/lib%{name}-vt.a

# These describe architecture-specific libraries, so install them in libdir
# and correct upstream's lib path for multilib platforms.
install -d %{buildroot}%{_libdir}/pkgconfig
mv %{buildroot}%{_datadir}/pkgconfig/lib%{name}-vt{,-static}.pc \
    %{buildroot}%{_libdir}/pkgconfig/
sed -i 's|^libdir=${prefix}/lib$|libdir=%{_libdir}|' \
    %{buildroot}%{_libdir}/pkgconfig/lib%{name}-vt{,-static}.pc

%fdupes %{buildroot}/${_datadir}
%find_lang %{project_id}

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
%{zig_test} %{build_flags} -Dapp-runtime=none
%endif

%files -f %{project_id}.lang
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

%docdir %{_datadir}/%{name}/doc
%doc README.md

%files lib
%license LICENSE
%{_libdir}/lib%{name}-vt.so.0{,.*}

%files devel
%license LICENSE
%{_includedir}/%{name}/vt.h
%{_includedir}/%{name}/vt/{allocator,build_info,color,color_scheme,device,focus,formatter,grid_ref,grid_ref_tracked,io,key,kitty_graphics,modes,mouse,osc,paste,point,render,screen,search,selection,sgr,size_report,snapshot,style,sys,terminal,types,unicode,wasm}.h
%{_includedir}/%{name}/vt/key/{encoder,event}.h
%{_includedir}/%{name}/vt/mouse/{encoder,event}.h
%{_libdir}/lib%{name}-vt.so
%{_libdir}/lib%{name}-vt.a
%{_libdir}/pkgconfig/lib%{name}-vt{,-static}.pc

%files terminfo
%license LICENSE
# the terminfo/x/xterm-ghostty or terminfo/g/ghostty file is used as a sentinel to discover the GHOSTTY_RESOURCES_DIR automatically
%{_datadir}/terminfo/x/xterm-%{name}

%files nautilus
%license %{_licensedir}/%{name}-nautilus/GPL-2.0-or-later.txt
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
