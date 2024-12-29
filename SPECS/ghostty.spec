%bcond test 1
# Fedora 40 doesn't have the required simdutf version
%if 0%{?fedora} == 40
%bcond simdutf 0
%else
%bcond simdutf 1
%endif

%global debug_package %{nil}
%global project_id          com.mitchellh.ghostty
%global project_description Ghostty is a cross-platform, GPU-accelerated terminal emulator that aims to push \
the boundaries of what is possible with a terminal emulator by exposing modern, \
opt-in features that enable CLI tool developers to build more feature rich, \
interactive applications.

Name:           ghostty
Version:        1.0.0
Release:        4%{?dist}
Summary:        A modern, feature-rich terminal emulator in Zig

License:        MIT AND OFL-1.1
URL:            https://ghostty.org
Source0:        https://release.files.ghostty.org/%{version}/%{name}-source.tar.gz
Source1:        https://release.files.ghostty.org/%{version}/%{name}-source.tar.gz.minisig

# Compile with zig, which bundles a C/C++ compiler
# Use pandoc to build docs, minisign to check signature
BuildRequires:  zig >= 0.13.0, zig < 0.14.0, pandoc, minisign

# Choose zlib-ng over zlib-ng-compat as we don't require compatibility with 32-bit systems
BuildRequires:  pkgconfig(fontconfig), pkgconfig(freetype2), pkgconfig(harfbuzz)
BuildRequires:  pkgconfig(gtk4), pkgconfig(oniguruma), pkgconfig(glib-2.0),
BuildRequires:  pkgconfig(libadwaita-1), pkgconfig(libpng), pkgconfig(zlib-ng)


%if %{with simdutf}
BuildRequires: pkgconfig(simdutf) >= 4.0.9
%endif

# Deduplicate installed files using fdupes, validate .desktop spec compliance
BuildRequires:  fdupes, desktop-file-utils

# Testing requires hostname util
%if %{with test}
BuildRequires: hostname
%endif

Requires: %{name}-terminfo = %{version}-%{release}

# Static linked or compiled, referencing the build.zig.zon
Provides:      bundled(font(CodeNewRoman)), bundled(font(CozetteVector))
Provides:      bundled(font(Inconsolata)), bundled(font(JuliaMono))
Provides:      bundled(font(JetBrainsMonoNerdFont)), bundled(font(JetBrainsMonoNoNF))
Provides:      bundled(font(KawkabMono)), bundled(font(Lilex))
Provides:      bundled(font(MonaspaceNeon)), bundled(font(NotoColorEmoji))
Provides:      bundled(font(NotoEmoji))
Provides:      bundled(glslang) = 14.2.0
Provides:      bundled(spirv-cross) = 13.1.1

# There are more build dependencies statically linked
# listed in the build.zig.zon

%if %{without simdutf}
Provides:      bundled(simdutf) = 4.0.9
%endif
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
%global pubkey RWQlAjJC23149WL2sEpT/l0QKy7hMIFhYdQOFy0Z7z7PbneUgvlsnYcV
minisign -Vm %{SOURCE0} -x %{SOURCE1} -P %{pubkey}
%setup -q -n %{name}-source

ZIG_GLOBAL_CACHE_DIR="/tmp/offline-cache" ./nix/build-support/fetch-zig-cache.sh # _REQUIRES_NETWORK


%build
%global _build_flags %{?with_simdutf:-fsys=simdutf} --system "/tmp/offline-cache/p" -Dcpu=baseline -Doptimize=ReleaseFast
# I want to move this into the prep step as the fetch is part of the sources ideally
zig build %{_build_flags}


%install
# use install step of the build script
zig build install --prefix %{buildroot}/%{_prefix} %{_build_flags}
%fdupes %{buildroot}/${_datadir}

%check
desktop-file-validate %{buildroot}/%{_datadir}/applications/%{project_id}.desktop

%if %{with test}
# These are currently unit tests for individual features in ghostty
zig build test %{_build_flags}
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
