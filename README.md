# Automated RPM Packaging for Ghostty

## Build tools

```bash
# rpmbuild tools
$ dnf install rpmdevtools
# Ghostty requires this version of zig docs are built with pandoc
# Sources ar
# Fetch github releases using the CLI, releases are signed with `minisign`
```

## Build Steps

### On the system

1. Install build dependencies `sudo dnf builddep ./SPECS/ghostty.spec`
2. Download sources with `spectool -R -g SPECS/ghostty.spec`
3. Run `rpmbuild -ba SPECS/ghostty.spec` to build the package

### Isolated build

Build in mock to test build-requires are sufficient

1. `rpmbuild -bs SPECS/ghostty.spec`
2. Run `mock -r SRPMS/<generated src.rpm from step 2>`
