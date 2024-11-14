# Guidelines

+ [Fedora Packaging Guidelines](https://docs.fedoraproject.org/en-US/packaging-guidelines/#_file_permissions)


# Important Steps

Prepare a source tar.gz by creating a directory with the `<name>-<version>/` and source cloned into it
`$ tar --create --file <name>-<version>.tar.gz <name>-<version>/`
Move this tar into the `SOURCES/` directory

We can then use `sed` to reuse the existing ghostty.spec to make a new release

Be guided by `rpmlint`, note that `rpmlint %{name}.spec` has weaker linting ability than installing the rpm and then using `rpmlint -i %{name}` on the installed package

# Configuring the Build

Build Options

Ghostty uses the Zig build system. You can see all available build options by running zig build --help. The following are options that are particularly relevant to package maintainers:

+    --prefix: The installation prefix. Combine with the DESTDIR environment variable to install to a temporary directory for packaging.

+   --system: The path to the offline cache directory. This disables any package fetching from the internet. This flag also triggers all dependencies to be dynamically linked by default.

+   -Doptimize=ReleaseFast: Build with optimizations enabled and safety checks disabled. This is the recommended build mode for distribution. I'd prefer a safe build but terminal emulators are performance-sensitive and the safe build is currently too slow. I plan to improve this in the future. Other build modes are available: Debug, ReleaseSafe, and ReleaseSmall.

+   -Dcpu=baseline: Build for the "baseline" CPU of the target architecture. This avoids building for newer CPU features that may not be available on all target machines.

+   -Dtarget=$arch-$os-$abi: Build for a specific target triple. This is often necessary for system packages to specify a specific minimum Linux version, glibc, etc. Run zig targets to a get a full list of available targets.

# Verifying keys

Do this in `%prep` add the keyring, signature and data as sources

# Configuring file attributes

Make shell integrations executable

# Test suite

Execute in the `%check` section

# Manpages

Configure manpages to be gzipped when installing
