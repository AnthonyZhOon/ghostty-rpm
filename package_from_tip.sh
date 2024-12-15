#!/usr/bin/bash
# https://jvns.ca/blog/2017/03/26/bash-quirks/
# Shellcheck used to lint this script
# For tips on bash scripting
set -e # Stop on any exception
set -u # Stop on using unset variables
set -x
GHOSTTY_PUB_KEY='RWQlAjJC23149WL2sEpT/l0QKy7hMIFhYdQOFy0Z7z7PbneUgvlsnYcV' # From https://github.com/ghostty-org/ghostty/blob/main/PACKAGING.md
UTC_DATE=$(date -u -I | sed "s|-||g") # UTC date in ISO8601 format without hyphens
SOURCES_DIR='./SOURCES'
SOURCE_VERSION='source'
# BUILD_VERSION="0.1.0^${UTC_DATE}" # RECONSIDER THIS ONE, I want a git commit on this
BUILD_VERSION="0.1.1" # RECONSIDER THIS ONE, I want a git commit on this
SOURCE_TAR="ghostty-${SOURCE_VERSION}.tar.gz"
RELEASE_TAR="ghostty-${BUILD_VERSION}.tar.gz"
BUILD_NAME="ghostty-${BUILD_VERSION}"
CURR=$(pwd)

# Fetch source data and check signature
fetch() {
  gh release download tip -R ghostty-org/ghostty --dir "$SOURCES_DIR" --pattern '*.tar.gz*' --clobber
  minisign -Vm "${SOURCES_DIR}/${SOURCE_TAR}" -P "$GHOSTTY_PUB_KEY"
}

# Rename and create appropriate archive format
create_tar() {
  cd "${SOURCES_DIR}"
  mkdir -p "$BUILD_NAME" # Silent if directory already exists
  tar -xvf "${SOURCE_TAR}" -C "$BUILD_NAME"
  tar --create --file "${BUILD_NAME}.tar.gz" "${BUILD_NAME}" 
  cd "${CURR}"
}

# Build using rpmbuild
build() {
  # Replace the version line in our template
  TEMPLATE_SPEC="./SPECS/ghostty.spec"
  THIS_SPEC="./SPECS/${BUILD_NAME}.spec"

  sed -e "s|Version:.*|Version:       ${BUILD_VERSION}|" < "$TEMPLATE_SPEC" > "$THIS_SPEC"
  rpmbuild -bs "$THIS_SPEC"
}

main() {
  fetch
  create_tar
  build
}

main
