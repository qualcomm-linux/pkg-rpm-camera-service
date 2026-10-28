<!--
Copyright (c) Qualcomm Technologies, Inc. and/or its subsidiaries.
SPDX-License-Identifier: BSD-3-Clause
-->
# pkg-rpm-camera-service

RPM packaging for the Qualcomm Linux camera service and QMMF runtime and
development packages.

This repository contains RPM packaging rules for the `camera-service` source
release. It builds the `qti-cam-server` daemon, the common QMMF libraries, the
recorder client library, the server-side runtime libraries, and the QMMF
development files used by camera-service consumers.

The `c10s` branch contains the RPM packaging files. The `main` branch contains
repository documentation and workflow support files.

## Repository Layout

| File | Purpose |
|---|---|
| `qcom-camera-server.spec` | Builds the camera server and QMMF runtime and development packages. |
| `sources` | SHA-512 checksum for the `camera-service` source archive. |
| `0001-camx-guard-target-builds.patch` | Applies the CamX target-build guard required by this package. |
| `0002-add-lib64-library-search-path.patch` | Adds the lib64 library search path required by this package. |
| `README.md` | Package and repository documentation. |
| `LICENSE.txt` | License for the RPM packaging repository. |

The upstream source archive is not committed to this repository. `Source0` in
the spec points to the `camera-service` release, and the checksum in `sources`
is verified before the RPM is built.

## Package

### `qcom-camera-server`

Camera server package providing the `qti-cam-server` daemon, its systemd unit,
configuration files, and the helper scripts that expose camera hardware to
QMMF clients.

### `libqmmf-common`

Shared QMMF runtime libraries containing protocol-buffer bindings, generic
utilities, configuration parsing, and camera-metadata helpers.

### `libqmmf-recorder-client`

Recorder client shared library used by applications to communicate with the
camera server.

### `qcom-camera-server-libs`

Server-side QMMF runtime libraries for the camera adaptor, memory interface,
and recorder service, including the platform-specific library variants used by
the camera server.

### `libqmmf-devel`

Development package providing the public QMMF headers, `pkg-config` files, and
unversioned shared-library development symlinks needed to build applications
and camera plugins against QMMF.

The packages are built for `aarch64` and include the target-specific runtime
libraries required by the Qualcomm Linux camera stack.

## Installation

Install the camera service and development files from the configured CentOS
Stream 10 repository:

```bash
sudo dnf install -y qcom-camera-server libqmmf-devel
```

## Updating the Package Version

1. Update `Version:` in `qcom-camera-server.spec`. `Source0` uses the package
   version to select the corresponding `camera-service` release archive.
2. Update the relevant `PatchN` entries if downstream patch behavior changes.
3. Regenerate the source checksum:

```
Source0: https://github.com/<org>/<proj>/archive/refs/tags/v%{version}.tar.gz#/%{name}-%{version}.tar.gz
```

### 3. Record the tarball checksum

**The tarball is never committed to git.** Only its checksum is:

```bash
sha512sum --tag <your-component>-1.0.tar.gz > sources
```

which yields a line like:

```
SHA512 (mycomponent-1.0.tar.gz) = 3a7bd3e2360a3d29eea436fcfb7e44c735d117c...
```

### 4. Open a PR against this branch

`build-on-pr` fetches the tarball (from the lookaside cache, or from the spec's
`Source` URL on a cache miss), verifies the checksum, and builds the RPM(s).
Download them from the run's **Artifacts**.


### 5. Release

**Actions → Release → Run workflow**, selecting this branch. A reviewer approves
the `pkg-release-approval` gate, then the RPM(s) publish to Artifactory.

---

## Local usage

The `build-on-pr.yml` build can be reproduced on an **aarch64** host with
`docker`, `git`, `curl`, and `bash`. The steps below mirror the
`pkg-build-reusable-workflow.yml` job in
[`qcom-rpm-utils`](https://github.com/qualcomm-linux/qcom-rpm-utils). Step 1
checks out the `c10s` branch; run the later steps from the **repository root**.

1. Clone this repository, check out the `c10s` packaging branch, then fetch the
   build tooling and build the builder image. CI pulls the same image from GHCR;
   building it locally avoids the GHCR login:

   ```sh
   git clone https://github.com/qualcomm-linux/pkg-rpm-camera-service.git
   cd pkg-rpm-camera-service
   git checkout c10s
   git clone https://github.com/qualcomm-linux/qcom-rpm-utils.git tool
   docker build -f tool/docker/Dockerfile.rpm-builder -t rpm-builder:centos10 tool/docker/
   ```

2. Resolve the source archive against `sources`. `resolve-sources.sh` appends
   to `$GITHUB_OUTPUT`, so start from an empty file:

   ```sh
   export GITHUB_OUTPUT="$PWD/resolve_sources_output.env"
   : > "$GITHUB_OUTPUT"
   tool/scripts/resolve-sources.sh \
     --sources sources \
     --spec qcom-camera-server.spec \
     --cache-base-url https://dummy_url \
     --dest "$PWD/sources-cache"
   # tarballs= is an unquoted, space-separated list; sourcing the file would
   # run every path after the first as a command, so read the values instead.
   tarball="$(sed -n 's/^tarball=//p' "$GITHUB_OUTPUT")"
   tarballs="$(sed -n 's/^tarballs=//p' "$GITHUB_OUTPUT")"
   ```

   The lookaside cache is tried first. On a miss, the archive is downloaded from
   the spec's `Source0` (the GitHub tag archive), and in both cases it is verified against
   the checksum in `sources`.

3. Build:

   ```sh
   tool/scripts/build-rpm.sh \
     --tarball "$tarballs" \
     --spec qcom-camera-server.spec \
     --output output \
     --builder-image rpm-builder:centos10
   ```

   `libcamx-devel` comes from the public Qualcomm Software Center repos, which
   the `rpm-builder:centos10` image already enables, so no extra repo is
   needed. To build against packages that are only in the staging repo, add
   `--extra-repo` with an Artifactory token in the URL, and do not share the
   build log, since `build-rpm.sh` prints that URL.

   `build-rpm.sh` copies every file beside the spec into the build workspace,
   so the spec can be built straight from the repository root.

Binary and source RPMs are written to `output/`. Nothing is uploaded; publishing
happens only through `pkg-release.yml`. The build leaves `tool/`,
`sources-cache/`, `output/`, and `resolve_sources_output.env` in the repository
root; they are not part of the package and can be deleted.

---

## Updating the version

Two edits, every time:

1. Bump `Version:` in the spec (and the `Source0:` URL if its path changed).
2. Recompute the checksum:
   ```bash
   sha512sum --tag camera-service-<version>.tar.gz > sources
   ```

4. Commit the spec and `sources`, then open a pull request against `c10s`.
5. After the pull request is merged, run `pkg-release.yml` to publish the RPMs.

## License

This project is licensed under the BSD 3-Clause License. See
[LICENSE.txt](LICENSE.txt) for the complete license text.
