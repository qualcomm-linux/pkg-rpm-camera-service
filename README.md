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
2. Update `Patch0` if the upstream source layout or CamX build behavior changes.
3. Regenerate the source checksum:

   ```bash
   sha512sum --tag camera-service-<version>.tar.gz > sources
   ```

4. Commit the spec and `sources`, then open a pull request against `c10s`.
5. After the pull request is merged, run `pkg-release.yml` to publish the RPMs.

## License

This project is licensed under the BSD 3-Clause License. See
[LICENSE.txt](LICENSE.txt) for the complete license text.
