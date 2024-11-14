# Automated RPM Packaging for Ghostty

## Build tools

``` bash
$ dnf install gcc rpm-build rpm-devel rpmlint make python bash coreutils diffutils patch rpmdevtools
```

## Build Steps

1. Retrieve source to compile a .tar.gz
	- Verify against key
2. Fetch zig package manager dependencies as a source
3. Run `rpmbuild -bb SPECS/ghostty.spec`

The completed .rpm file will be created under `RPM/<arch>/`
