# Zig fetches dependencies into the project-local zig-pkg directory.
# The RPM build uses those extracted packages in offline --system mode.
%bcond test 1

%global z2d_version 0.13.0
%global z2d_commit 40af3e84a4e15a9f31d126b3f281f23ce6a3dae5
%global spirv_cross_commit 476f384eb7d9e48613c45179e502a15ab95b6b49
%global translate_c_commit 02ff0c523fb92a38939b04d0145c4a9602a74d56
%global aro_commit d0c8c4d9c55daa7ef6e40cf0f630a5b5e900989b
%global libvaxis_commit 6fd944a27fb3d6f596e981076381a3131f2448b4
%global ghostty_gobject_version 0.3.2-2026-10-02-38-1
%global glslang_version 14.2.0
%global highway_commit 66486a10623fa0d72fe91260f96c892e41aceb06
%global libxev_commit 819ffa180ca20e31c7eded74e2e1aceb1eab557f
%global imgui_version 1.92.5-docking
%global uucode_commit ea62149739404a73c202b48a33bf6dd2af4bd9b0
%global wuffs_commit 7411f488fe2e2c205c3d3b3d28638b7356522930
%global zf_commit 87153bb86b75d21fbac897b738f316d449f5d0c9
%global zigimg_commit c701c9f99779d7ddf594dcc6da8f858fd277d61f
%global zig_wayland_commit 27dda01712ddf3cb46ebd93380d88b01a7c828f8
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
# Use an absolute package directory for dependencies that run build.zig.
%global _zig_system_integration --system %{_builddir}/%{buildsubdir}/zig-pkg
# Zig 0.17 only extracts packages locally when fetch uses --save.
# The temporary manifest entry is removed in %%prep before building.
%global _zig_fetch_options --save=rpmbuild --pkg-dir %{_builddir}/%{buildsubdir}/zig-pkg
# The build command also no longer accepts --global-cache-dir.
%global _zig_advanced_options -fallow-so-scripts --cache-dir %{_zig_cache_dir}
# Zig 0.17 applies DESTDIR only to relative install subdirectories.
%global _zig_install_options --prefix %{_prefix} --prefix-lib-dir %{_lib}

%global deps_start 12
%global deps_end 34

# populates the zig cache with dependency %1 through %2
# As I understand, parametric lua macros must be expanded at use-site
%define zig_extract() %{lua:
   for i = arg[1]//1, arg[2]//1 do 
      print(rpm.expand("\%zig_fetch \%{SOURCE" .. i .. "}") .. "\\n") 
   end
}
%global stub_package() %{expand:mkdir -p %{_builddir}/%{buildsubdir}/zig-pkg/%1}

%global project_id          com.mitchellh.ghostty
%global project_description %{expand:
Ghostty is a cross-platform, GPU-accelerated terminal emulator that aims to push 
the boundaries of what is possible with a terminal emulator by exposing modern, 
opt-in features that enable CLI tool developers to build more feature rich, 
interactive applications.}


Name:           ghostty
Version:        1.4.0
Release:        %autorelease
Summary:        A fast, feature-rich, and cross-platform terminal emulator in Zig

%global app_version %{version}

# Expand the application version before the lib subpackage sets its version.
%global build_flags %{shrink:
   -fsys=simdutf \
   -Dgtk-wayland=true \
   -Dgtk-x11=true \
   -Dsentry=false \
   -Dstrip=false \
   -Demit-themes=false \
   -Dinstalled-exe-path=%{_bindir}/ghostty \
   -Dversion-string=%{version} \
}

# Licenses for the dependencies themselves and in-tree bindings under pkg/ (both dependency and bindings)
# Unbundled dependencies are stubbed and do not contain source code compiled into the result
# These do not require their license added to a Fedora package
#
# zig-gobject:                MIT
# ghostty:                    MIT
# ghostty_nautilus.py:        GPL-2.0-or-later
# libvaxis:                   MIT
# libxev:                     MIT
# pixels                      CC0-1.0
# pkg/cimgui:                 MIT
# pkg/glslang:                BSD-2-Clause AND BSD-3-Clause AND GPL-3.0-or-later AND Apache-2.0 AND MIT
# pkg/highway:                Apache-2.0 AND BSD-3-Clause
# pkg/spirv-cross:            Apache-2.0
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

## unbundled (not included by configuration)
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


License:        MIT AND Apache-2.0 AND BSD-2-Clause AND BSD-3-Clause AND CC0-1.0 AND GPL-2.0-or-later AND GPL-3.0-or-later AND LGPL-2.1-only AND MPL-2.0 AND OFL-1.1 AND Unicode-3.0 AND (WTFPL OR CC0-1.0)
URL:            https://ghostty.org

Source0:        https://release.files.ghostty.org/%{version}/ghostty-%{version}.tar.gz
Source1:        https://release.files.ghostty.org/%{version}/ghostty-%{version}.tar.gz.minisig

# Take these archives from build.zig.zon.json
Source12:       https://github.com/vancluever/z2d/archive/%{z2d_commit}/z2d-%{z2d_commit}.tar.gz
Source13:       https://github.com/KhronosGroup/SPIRV-Cross/archive/%{spirv_cross_commit}/SPIRV-Cross-%{spirv_cross_commit}.tar.gz
Source14:       https://github.com/KhronosGroup/glslang/archive/refs/tags/%{glslang_version}/glslang-%{glslang_version}.tar.gz
Source15:       https://github.com/google/highway/archive/%{highway_commit}/highway-%{highway_commit}.tar.gz
Source16:       https://deps.files.ghostty.org/libxev-%{libxev_commit}.tar.gz
Source17:       https://github.com/ocornut/imgui/archive/refs/tags/v%{imgui_version}/imgui-%{imgui_version}.tar.gz
Source18:       https://deps.files.ghostty.org/DearBindings_v0.17_ImGui_v%{imgui_version}.tar.gz
Source19:       https://deps.files.ghostty.org/wuffs-%{wuffs_commit}.tar.gz
Source20:       https://deps.files.ghostty.org/zf-%{zf_commit}.tar.gz
Source21:       https://github.com/sergot/zigimg/archive/%{zigimg_commit}/zigimg-%{zigimg_commit}.tar.gz
Source22:       https://deps.files.ghostty.org/zig_wayland-%{zig_wayland_commit}.tar.gz
Source23:       https://gitlab.freedesktop.org/wayland/wayland/-/archive/%{wayland_commit}/wayland-%{wayland_commit}.tar.gz
Source24:       https://gitlab.freedesktop.org/wayland/wayland-protocols/-/archive/%{wayland_protocols_commit}/wayland-protocols-%{wayland_protocols_commit}.tar.gz
Source25:       https://github.com/KDE/plasma-wayland-protocols/archive/%{plasma_wayland_protocols_commit}/plasma-wayland-protocols-%{plasma_wayland_protocols_commit}.tar.gz
# FIXME: Temporary fork until it is done in-tree
Source26:       https://deps.files.ghostty.org/gobject-2026-10-02-38-1.tar.zst
Source27:       https://deps.files.ghostty.org/JetBrainsMono-%{jetbrains_mono_version}.tar.gz
Source28:       https://deps.files.ghostty.org/NerdFontsSymbolsOnly-%{nerdfont_symbols_only_version}.tar.gz
Source29:       https://github.com/make-github-pseudonymous-again/pixels/archive/d843c2714d32e15b48b8d7eeb480295af537f877/pixels-d843c27.tar.gz
Source30:       https://deps.files.ghostty.org/uucode-%{uucode_commit}.tar.gz
Source31:       https://deps.files.ghostty.org/translate_c-%{translate_c_commit}.tar.gz
Source32:       https://deps.files.ghostty.org/vaxis-%{libvaxis_commit}.tar.gz
Source33:       https://codeberg.org/ziglang/arocc/archive/%{aro_commit}.tar.gz
Source34:       https://gitlab.freedesktop.org/wayland/wayland-protocols/-/archive/%{wayland_protocols_version}/wayland-protocols-%{wayland_protocols_version}.tar.gz
Source35:       https://www.gnu.org/licenses/old-licenses/gpl-2.0.txt#/GPL-2.0-or-later.txt

ExclusiveArch: %{zig_arches}
# Compile with zig, which bundles a C/C++ compiler
# Use pandoc to build docs, minisign to check signature
BuildRequires:  (zig >= 0.17.0 with zig < 0.18.0~)
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

BuildRequires:  pkgconfig(egl)
BuildRequires:  pkgconfig(fontconfig)
BuildRequires:  pkgconfig(freetype2)
BuildRequires:  pkgconfig(glib-2.0)
BuildRequires:  pkgconfig(gtk4) >= 4.18
BuildRequires:  pkgconfig(gtk4-layer-shell-0) >= 1.0.4
BuildRequires:  pkgconfig(harfbuzz)
BuildRequires:  pkgconfig(libadwaita-1) >= 1.7
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

# Wayland protocol xml files
Provides:       bundled(wayland) = 0~git%{wayland_commit}
Provides:       bundled(wayland-protocols) = 0~git%{wayland_protocols_commit}
Provides:       bundled(plasma-wayland-protocols) = 0~git%{plasma_wayland_protocols_commit}

# Bundled images to test wuffs
Provides:       bundled(pixels) = 0~git

# Statically linked dependencies
Provides:       bundled(glslang) = %{glslang_version}
Provides:       bundled(highway) = 0~git%{highway_commit}
Provides:       bundled(libvaxis) = 0~git%{libvaxis_commit}
Provides:       bundled(libxev) = 0~git%{libxev_commit}
Provides:       bundled(mach-glfw) = 0~git37c2995f31abcf7e8378fba68ddcf4a3faa02de0
Provides:       bundled(spirv-cross) = 13.1.1
Provides:       bundled(uucode) = 0~git%{uucode_commit}
Provides:       bundled(wayland) = 0~git%{wayland_commit}
Provides:       bundled(wayland-protocols) = %{wayland_protocols_version}
Provides:       bundled(plasma-wayland-protocols) = 0~git%{plasma_wayland_protocols_commit}
Provides:       bundled(wuffs) = 0~git%{wuffs_commit}
Provides:       bundled(z2d) = %{z2d_version}
Provides:       bundled(zf) = 0~git%{zf_commit}
Provides:       bundled(zigimg) = 0~git%{zigimg_commit}
Provides:       bundled(ghostty-gobject) = 0.3.2
Provides:       bundled(zig-wayland) = 0~git%{zig_wayland_commit}

%description %{project_description}

%package lib
Summary:       Shared library for %{name}
# Doesn't have a versioned release upstream yet
Version:       0.0.0
%global lib_version %{version}
# A subpackage Version also changes the global macro. Restore the application
# version for the remaining dependencies, build steps, and changelog.
%global version %{app_version}

%description lib
Shared library for %{name} to enable embedding terminal 
functionality into other applications

%package devel
Summary:       Development files for %{name}

Requires:     %{name}-lib%{?isa} = %{lib_version}-%{release}

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
%setup -q
# Fill zig_cache with dependency sources
# zig will identify fetched dependencies at build time.
cp build.zig.zon build.zig.zon.rpm-original
%zig_extract %deps_start %deps_end
mv build.zig.zon.rpm-original build.zig.zon

# stubbing some packages that don't need bundled sources as we opt to dynamic link
# Find hash by building without fetch which compares against build.zig.zon hash
# libxml2
%stub_package  N-V-__8AAG3RoQEyRC2Vw7Qoro5SYBf62IHn3HjqtNVY6aWK

%build
%{zig_build} %{build_flags}


%install
%{zig_install} %{build_flags}

# The Nautilus extension is GPL-2.0-or-later while the main project is MIT.
install -Dpm0644 %{SOURCE35} \
    %{buildroot}%{_licensedir}/%{name}-nautilus/GPL-2.0-or-later.txt

# Zig's archive combiner includes the dynamically linked system simdutf object
# in the static archive. Keep simdutf external as declared by the pkg-config
# metadata and leave only relocatable objects in the archive.
ar d %{buildroot}%{_libdir}/lib%{name}-vt.a libsimdutf.so
ranlib %{buildroot}%{_libdir}/lib%{name}-vt.a

# These describe architecture-specific libraries, so install them in libdir.
# Remove DESTDIR from the generated prefix and use the multilib library path.
install -d %{buildroot}%{_libdir}/pkgconfig
mv %{buildroot}%{_datadir}/pkgconfig/lib%{name}-vt{,-static}.pc \
    %{buildroot}%{_libdir}/pkgconfig/
sed -i -e 's|^prefix=.*$|prefix=%{_prefix}|' \
    -e 's|^libdir=${prefix}/lib$|libdir=%{_libdir}|' \
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
# Avoid conflict with ncurses-term packaging a terminfo file with this name
rm %{buildroot}/%{_datadir}/terminfo/g/ghostty

%check
desktop-file-validate %{buildroot}/%{_datadir}/applications/%{project_id}.desktop
%{buildroot}/%{_bindir}/%{name} --version

%if %{with test}
# These are currently unit tests for individual features in ghostty
# Tests require Debug mode asserts to run
%{zig_test} %{build_flags} -Doptimize=Debug -Dapp-runtime=none
%endif

%files -f %{project_id}.lang
%{_bindir}/%{name}
%license LICENSE
# Owned directory containing shell integration and docs
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
