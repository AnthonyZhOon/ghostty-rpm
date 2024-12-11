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

## Caveats

Currently we perform a zig build --fetch inside our build step, this compromises reproducible builds
for release packages but I think is acceptable for nightly builds.

Packaging a release will have to perform this fetch when preparing the source tar, does this mean producing
downstream archives of the source separate from the build step?

The fetch is used for zig package management which finds the pkg-config and static link source files
as dependencies for the build step.
