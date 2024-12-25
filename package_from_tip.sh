#!/usr/bin/bash
# https://jvns.ca/blog/2017/03/26/bash-quirks/
# Shellcheck used to lint this script
# For tips on bash scripting
set -e # Stop on any exception
set -u # Stop on using unset variables
set -x # Emit each command executed
GHOSTTY_PUB_KEY='RWQlAjJC23149WL2sEpT/l0QKy7hMIFhYdQOFy0Z7z7PbneUgvlsnYcV' # From https://github.com/ghostty-org/ghostty/blob/main/PACKAGING.md
UTC_DATE=$(date -u -I | sed "s|-||g") # UTC date in ISO8601 format without hyphens
SOURCES_DIR='./SOURCES'
SOURCE_VERSION='source'
BUILD_VERSION="0.1.0^${UTC_DATE}" # RECONSIDER THIS ONE, I want a git commit on this
# BUILD_VERSION="0.1.1" # RECONSIDER THIS ONE, I want a git commit on this
SOURCE_NAME="ghostty-${SOURCE_VERSION}"
BUILD_NAME="ghostty-${BUILD_VERSION}"
CURR=$(pwd)

# Fetch source data and check signature
fetch() {
  cd "$CURR"
  gh release download tip -R ghostty-org/ghostty --dir "$SOURCES_DIR" --pattern '*.tar.gz*' --clobber
  minisign -Vm "${SOURCES_DIR}/${SOURCE_NAME}.tar.gz" -P "$GHOSTTY_PUB_KEY"
}

extract() {
  cd "$CURR"
  cd "${SOURCES_DIR}"
  tar -xvf "${SOURCE_NAME}.tar.gz"
  mv "${SOURCE_NAME}" "${BUILD_NAME}"
}

# Optional step to cache network dependencies
cache_network_dependencies() { 
  cd "$CURR"
  cd "${SOURCES_DIR}/${BUILD_NAME}"
  # Populate dependency cache to avoid network requirement
  ZIG_GLOBAL_CACHE_DIR="$(pwd)/.zig-cache" ./nix/build-support/fetch-zig-cache.sh
}

# Rename and create appropriate archive format
create_tar() {
  cd "$CURR"
  cd "${SOURCES_DIR}"
  tar --create --file "${BUILD_NAME}.tar.gz" "${BUILD_NAME}" 
}

# Build using rpmbuild
build() {
  cd "$CURR"
  # Replace the version line in our template
  TEMPLATE_SPEC="./SPECS/ghostty.spec"
  THIS_SPEC="./SPECS/${BUILD_NAME}.spec"

  sed -e "s|Version:.*|Version:       ${BUILD_VERSION}|" < "$TEMPLATE_SPEC" > "$THIS_SPEC"
  rpmbuild -bs "$THIS_SPEC"
}

# Additionally uses the network to cache build-time dependencies from zig package management used in static linking
# Avoids requiring network when building the package, consider adding this as a separate archive source
prepare_without_network() {
  fetch
  extract
  cache_network_dependencies
  create_tar
  build
}

# Only restructures and renames the archive
build_requires_network() {
  fetch
  extract
  create_tar
  build
}

main() {
  case $@ in
    "") prepare_without_network ;;
    "--without-fetch") build_requires_network ;;
    "--help") printf "Fetches the latest release and produces a .spec file to build an rpm package for it\nOptions: --without-fetch do not perform zig fetch for build dependencies" ;;
    *) echo "Unexpected args either provide 1 arg of from --help"; return 1 ;;
  esac
}

main "$@"
