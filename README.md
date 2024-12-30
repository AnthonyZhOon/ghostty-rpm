# Automated RPM Packaging for Ghostty

## Build tools

``` bash
# rpmbuild tools
$ dnf install gcc rpm-build rpm-devel rpmlint make python bash coreutils diffutils patch rpmdevtools
# Ghostty requires this version of zig docs are built with pandoc
# Sources ar
# Fetch github releases using the CLI, releases are signed with `minisign`
```

## Build Steps

1. Grab sources with `spectool -R -g SPECS/ghostty.spec`
2. Run `rpmbuild -bs SPECS/ghostty.spec` to create the .src.rpm
  - Alternatively run `rpmbuild -bb SPECS/ghostty.spec` with the build dependencies
3. Run `mock --enable-network SRPMS/<generated src.rpm from step 2>`
4. Results available as output from `mock`, the output directory can be configured


## Reproducible builds

As we need to fetch zig package manager dependencies that are statically linked as build dependencies,
a network dependency can compromise reproducible builds.


