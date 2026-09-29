<!--
Copyright (c) Qualcomm Technologies, Inc. and/or its subsidiaries.
SPDX-License-Identifier: BSD-3-Clause
-->
# pkg-rpm-camera-service

RPM packaging for the Qualcomm® Linux camera service and QMMF runtime and
development packages.

This repository contains RPM packaging rules for the `camera-service` source
release. The package provides the `qti-cam-server` daemon, QMMF shared runtime
libraries, the recorder client library, and development headers and
`pkg-config` files used by Qualcomm Linux camera consumers.

The upstream camera service source archive is fetched during the RPM build
from [camera-service](https://github.com/qualcomm/camera-service). This
repository contains no compiled libraries, binaries, or source archives.

The `main` branch contains repository documentation and workflow support files.

## License

This project is licensed under the BSD 3-Clause License. See
[LICENSE.txt](LICENSE.txt) for the complete license text.
