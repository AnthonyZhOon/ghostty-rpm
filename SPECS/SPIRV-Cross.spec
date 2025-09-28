%bcond test 1
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

# Checking with `rg SPDX`,
# The entire source is Apache-2.0, except:
  #
  # CC-BY-4.0:
  #   README.md
  #   CODE_OF_CONDUCT.adoc
  #
  # MIT:
  #   GLSL.std.450.h
  #
  # Apache-2.0 OR MIT:
  #   CMakeLists.txt
  #   main.cpp
  #   spirv_cfg.{cpp,hpp}
  #   spirv_common.hpp
  #   spirv_cpp.{cpp,hpp}
  #   spirv_cross.{cpp,hpp}
  #   spirv_cross.natvis
  #   spirv_cross_c.{cpp,h}
  #   spirv_cross_containers.hpp
  #   spirv_cross_error_handling.hpp
  #   spirv_cross_parsed_ir.{cpp,hpp}
  #   spirv_cross_util.{cpp,hpp}
  #   spirv_glsl.{cpp,hpp}
  #   spirv_hlsl.{cpp,hpp}
  #   spirv_msl.{cpp,hpp}
  #   spirv_parser.{cpp,hpp}
  #   spirv_reflect.{cpp,hpp}
License:        Apache-2.0 AND CC-BY-4.0 AND MIT AND (Apache-2.0 OR MIT)
URL:            https://github.com/KhronosGroup/%{name}
Source0:        %url/archive/vulkan-sdk-%{sdkver}.tar.gz#/%{name}-sdk-%{sdkver}.tar.gz

BuildRequires:  cmake
BuildRequires:  gcc-c++

%if %{with test}
BuildRequires:  glslang
BuildRequires:  spirv-tools
%endif

%description %{project_description}

%package        libs
Summary:        Shared library files for %{name}
%description    libs %{project_description}

%package        devel
Summary:        Development files for %{name}
Requires:       %{name}-libs%{?_isa} = %{version}-%{release}
%description    devel %{project_description}

%prep
%autosetup -p1 -n %{name}-vulkan-sdk-%{sdkver}

%build
%cmake -DSPIRV_CROSS_SHARED=ON
%cmake_build

%install
%{cmake_install}
# Remove unpackaged static-library files
rm %{buildroot}/%{_libdir}/libspirv-cross-{c,core,cpp,glsl,hlsl,msl,reflect,util}.a
rm %{buildroot}/%{_libdir}/pkgconfig/spirv-cross-c.pc
rm -r %{buildroot}/%{_datadir}/spirv_cross_{c,core,cpp,glsl,hlsl,msl,reflect,util}/cmake/


%check
%if %{with test}
# Upstreams tests do not support system installed glslang and spirv-tools, having spurious failures
SPIRV_CROSS_PATH=%{buildroot}%{_bindir}/spirv-cross
# ./test_shaders.py shaders --spirv-cross "$SPIRV_CROSS_PATH" || exit 1
# ./test_shaders.py shaders --opt --spirv-cross "$SPIRV_CROSS_PATH" || exit 1
# ./test_shaders.py shaders-no-opt --spirv-cross "$SPIRV_CROSS_PATH" || exit 1
# ./test_shaders.py shaders-msl --msl --spirv-cross "$SPIRV_CROSS_PATH" || exit 1
# ./test_shaders.py shaders-msl --msl --opt --spirv-cross "$SPIRV_CROSS_PATH" || exit 1
# ./test_shaders.py shaders-msl-no-opt --msl --spirv-cross "$SPIRV_CROSS_PATH" || exit 1
# ./test_shaders.py shaders-hlsl --hlsl --spirv-cross "$SPIRV_CROSS_PATH" || exit 1
# ./test_shaders.py shaders-hlsl --hlsl --opt --spirv-cross "$SPIRV_CROSS_PATH" || exit 1
# ./test_shaders.py shaders-hlsl-no-opt --hlsl --spirv-cross "$SPIRV_CROSS_PATH" || exit 1
./test_shaders.py shaders-reflection --reflect --spirv-cross "$SPIRV_CROSS_PATH" || exit 1
./test_shaders.py shaders-ue4 --msl --spirv-cross "$SPIRV_CROSS_PATH" || exit 1
./test_shaders.py shaders-ue4 --msl --opt --spirv-cross "$SPIRV_CROSS_PATH" || exit 1
./test_shaders.py shaders-ue4-no-opt --msl --spirv-cross "$SPIRV_CROSS_PATH" || exit 1
%endif

%files
%license LICENSE LICENSES/
%doc README.md
%{_bindir}/spirv-cross
%files devel
%{_includedir}/spirv_cross/
%{_libdir}/pkgconfig/spirv-cross-c-shared.pc
%{_libdir}/libspirv-cross-c-shared.so
%{_datadir}/spirv_cross_c_shared
%files libs
%license LICENSE LICENSES/
%{_libdir}/libspirv-cross-c-shared.so.0{,.*}
%changelog
%autochangelog
