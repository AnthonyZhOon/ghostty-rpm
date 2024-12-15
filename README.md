# Automated RPM Packaging for Ghostty

## Build tools

``` bash
# rpmbuild tools
$ dnf install gcc rpm-build rpm-devel rpmlint make python bash coreutils diffutils patch rpmdevtools
# Ghostty requires this version of zig docs are built with pandoc
# Sources ar
$ dnf install zig-0.13.0 pandoc
# Fetch github releases using the CLI, releases are signed with `minisign`
$ dnf install gh minisign
# Do we need runtime link headers?
```

## Build Steps

1. Create a directory at `~/rpmbuild` #TODO: Use `mock` for independent dirs... or copr with make...
2. Run the fetch and build script `bash package_from_tip.sh`

The completed .rpm file will be created under `RPMS/<arch>/`

Note: 
  If I forgot, I might have left this in just producing the `.spec` file and `.src.rpm`
  You can either `rpmbuild -bb SPECS/<GENERATED_SPEC_FILE>.spec` to build from the archive and spec
  Or `rpmbuild --rebuild SRPMS/<GENERATED_SRC_RPM>.src.rpm` to build the `.rpm` from the `.src.rpm`

## Reproducible builds

As we need to fetch zig package manager dependencies that are statically linked as build dependencies,
a network dependency can compromise reproducible builds.

The `bash package_from_tip.sh --without-network` flag produces a `.spec` file and `.src.rpm` file that can be built
reliably in a network-isolated environment.

This works by extracting the release, fetching the required depedencies into a cache directory inside the archive.
Then producing the archive source.

