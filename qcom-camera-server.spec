%global upstream_name camera-service
%global _hardened_build 1

Name:           qcom-camera-server
Version:        1.0.4
Release:        1%{?dist}
Summary:        Qualcomm Linux embedded camera server

License:        BSD-3-Clause-Clear
URL:            https://github.com/qualcomm/camera-service
Source0:        %{url}/archive/refs/tags/%{version}/%{name}-%{version}.tar.gz

Patch0:         0001-move-check-camx-overlay.sh-to-libexec.patch
Patch1:         0002-Fix-typos-in-log-messages.patch
Patch2:         0003-cam-server-base.service.in-add-missing-Documentation.patch
Patch3:         0004-camx-guard-target-builds-and-switch-qcs-target-to-qcs-common.patch

ExclusiveArch:  aarch64

BuildRequires:  gcc-c++
BuildRequires:  cmake >= 3.16
BuildRequires:  make
BuildRequires:  pkgconfig
BuildRequires:  systemd-rpm-macros
BuildRequires:  pkgconfig(glib-2.0)
BuildRequires:  protobuf-devel
BuildRequires:  protobuf-compiler
BuildRequires:  abseil-cpp-devel
# Optional: enables the GBM memory backend
BuildRequires:  pkgconfig(gbm)
# TODO: the Qualcomm CamX API headers are not available in CentOS Stream 10.
# The camera adaptor, memory interface and recorder service libraries require
# them. Provide them through a local package and uncomment:
BuildRequires:  libcamx-dev

Requires:       %{name}-libs%{?_isa} = %{version}-%{release}
# TODO: the CamX server runtime is dlopen'ed at runtime but is not packaged
# for CentOS Stream 10 yet.
#Recommends:     camx-server-runtime

%description
The Qualcomm MultiMedia Framework (QMMF) provides the camera recorder
service and client stack used by Qualcomm Linux camera pipelines.
This package contains the cam-server daemon, its systemd service unit,
configuration files and helper scripts that expose the camera hardware
to QMMF clients.

%package        -n libqmmf-common
Summary:        Qualcomm MultiMedia Framework - common runtime libraries

%description    -n libqmmf-common
The Qualcomm MultiMedia Framework (QMMF) provides the camera recorder
service and client stack used by Qualcomm Linux camera pipelines.
This package contains the shared runtime libraries common to both the
client and the server: the protocol buffer bindings, generic utilities,
the configuration parser and the camera-metadata helpers
(libqmmf_proto, libqmmf_utils, libqmmf_config and
libqmmf_camera_metadata).

%package        -n libqmmf-recorder-client
Summary:        Qualcomm MultiMedia Framework - client runtime library
Requires:       libqmmf-common%{?_isa} = %{version}-%{release}

%description    -n libqmmf-recorder-client
The Qualcomm MultiMedia Framework (QMMF) provides the camera recorder
service and client stack used by Qualcomm Linux camera pipelines.
This package contains the recorder client shared library
(libqmmf_recorder_client), which applications link against to talk to
the camera server.

%package        libs
Summary:        Qualcomm MultiMedia Framework - server runtime libraries
Requires:       libqmmf-common%{?_isa} = %{version}-%{release}
Provides:       libqmmf-server-lib = %{version}-%{release}
Provides:       libqmmf-server-lib%{?_isa} = %{version}-%{release}

%description    libs
The Qualcomm MultiMedia Framework (QMMF) provides the camera recorder
service and client stack used by Qualcomm Linux camera pipelines.
This package contains the server-side shared libraries used by the
camera server: the camera adaptor, the memory interface and the
recorder service, including their platform variants (for example the
kodiak build of each library).

%package        -n libqmmf-devel
Summary:        Qualcomm MultiMedia Framework - development files
Requires:       libqmmf-common%{?_isa} = %{version}-%{release}
Requires:       libqmmf-recorder-client%{?_isa} = %{version}-%{release}
Requires:       %{name}-libs%{?_isa} = %{version}-%{release}

%description    -n libqmmf-devel
The Qualcomm MultiMedia Framework (QMMF) provides the camera recorder
service and client stack used by Qualcomm Linux camera pipelines.
This package contains the public headers, the pkg-config files and the
unversioned shared-library development symlinks needed to build software
against QMMF, such as the Qualcomm GStreamer camera plugins.

%prep
%autosetup -n %{upstream_name}-%{version} -p1

%build
# BUILD_CATEGORY=ALL enables the common libraries, the recorder client,
# the server libraries and the cam-server daemon.
%cmake \
    -DCMAKE_INSTALL_SYSCONFDIR:PATH=%{_sysconfdir} \
    -DCMAKE_INSTALL_LIBEXECDIR:PATH=%{_libexecdir} \
    -DBUILD_CATEGORY:STRING=ALL

%cmake_build

%install
%cmake_install

%check
# The upstream gtest suites are disabled by the default configuration
# (RECORDER_GTEST_ENABLED=0, CAMERAADAPTOR_GTEST_ENABLED=0) and require
# camera hardware.

%post
%systemd_post cam-server.service

%preun
%systemd_preun cam-server.service

%postun
%systemd_postun_with_restart cam-server.service

%files
%license LICENSE.txt
%doc README.md NOTICE
%config(noreplace) %{_sysconfdir}/cam-server.ini
%config(noreplace) %{_sysconfdir}/cam-server-env
%{_bindir}/cam-server
%dir %{_libexecdir}/qmmf-server
%{_libexecdir}/qmmf-server/check-camx-overlay.sh
%{_unitdir}/cam-server.service

%files -n libqmmf-common
%license LICENSE.txt
%{_libdir}/libqmmf_camera_metadata.so.*
%{_libdir}/libqmmf_config.so.*
%{_libdir}/libqmmf_proto.so.*
%{_libdir}/libqmmf_utils.so.*

%files -n libqmmf-recorder-client
%license LICENSE.txt
%{_libdir}/libqmmf_recorder_client.so.*

%files libs
%license LICENSE.txt
%{_libdir}/libqmmf_camera_adaptor_kodiak.so.*
%{_libdir}/libqmmf_memory_interface_kodiak.so.*
%{_libdir}/libqmmf_recorder_service_kodiak.so.*

%files -n libqmmf-devel
%license LICENSE.txt
%{_includedir}/qmmf-sdk/
%{_includedir}/camera-metadata/
%{_includedir}/proto/
%{_libdir}/libqmmf_camera_adaptor_kodiak.so
%{_libdir}/libqmmf_camera_metadata.so
%{_libdir}/libqmmf_config.so
%{_libdir}/libqmmf_memory_interface_kodiak.so
%{_libdir}/libqmmf_proto.so
%{_libdir}/libqmmf_recorder_client.so
%{_libdir}/libqmmf_recorder_service_kodiak.so
%{_libdir}/libqmmf_utils.so
%{_libdir}/pkgconfig/qmmf_camera_metadata.pc
%{_libdir}/pkgconfig/qmmf_config.pc
%{_libdir}/pkgconfig/qmmf_proto.pc
%{_libdir}/pkgconfig/qmmf_utils.pc

%changelog
* Fri Aug 14 2026 Viswanath Srikanth Bathina <bathina@qti.qualcomm.com> - 1.0.4-1
- Initial RPM packaging for CentOS Stream 10 (aarch64)