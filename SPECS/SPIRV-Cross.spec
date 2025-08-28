%global sdkver 1.4.321
%global project_description %{expand:
SPIRV-Cross is a practical tool and library for performing reflection on SPIR-V
and disassembling SPIR-V back to high level languages.
SPIRV-Cross tries hard to emit readable and clean output from the SPIR-V. The
goal is to emit GLSL or MSL that looks like it was written by a human and not
awkward IR/assembly-like code.}

Name:           SPIRV-Cross
Version:        %{sdkver}
Release:        %autorelease
Summary:        A tool designed for parsing and converting SPIR-V to other shader languages

License:        Apache-2.0
URL:            https://github.com/KhronosGroup/%{name}
Source0:        %url/archive/vulkan-sdk-%{sdkver}.tar.gz#/%{name}-sdk-%{sdkver}.tar.gz

BuildRequires:  cmake3
BuildRequires:  gcc-c++

%description
%{project_description}

%package        libs
Summary:        Shared library files for %{name}
%description    libs
%{project_description}

%package        devel
Summary:        Development files for %{name}
Requires:       %{name}-libs%{?_isa} = %{version}-%{release}
Recommends:     %{name}-static%{?_isa} = %{version}-%{release}
%description    devel
%{project_description}

%package        static
Summary:        Static library files for %{name}
Requires:       %{name}-devel%{?_isa} = %{version}-%{release}
%description    static
%{project_description}

%prep
%autosetup -p1 -n %{name}-vulkan-sdk-%{sdkver}

%build
%cmake3 -DSPIRV_CROSS_SHARED=ON
%cmake_build

%install
%{cmake_install}
# Remove cmake package files
rm -r %{buildroot}/%{_datadir}


%check
# Upstreams tests do not support system installed glslang and spirv-tools, having spurious failures

%files
%license LICENSE
%doc README.md
%{_bindir}/%{lower:%{name}}
%files static
%license LICENSE
%{_libdir}/libspirv-cross-{c,core,cpp,glsl,hlsl,msl,reflect,util}.a
%{_libdir}/pkgconfig/spirv-cross-c.pc
%files devel
%license LICENSE
%{_includedir}/spirv_cross/
%{_libdir}/pkgconfig/spirv-cross-c-shared.pc
%files libs
%license LICENSE
%{_libdir}/libspirv-cross-c-shared.so*
%changelog
%autochangelog
