# Base image with workdir and apt (update/install) caching
FROM ubuntu AS base

WORKDIR /opt/hhg-studio

RUN <<EOT
rm -f /etc/apt/apt.conf.d/docker-clean
echo 'Binary::apt::APT::Keep-Downloaded-Packages "true";' > /etc/apt/apt.conf.d/keep-cache
EOT

RUN --mount=type=cache,target=/var/cache/apt,sharing=locked \
  --mount=type=cache,target=/var/lib/apt,sharing=locked \
  apt update


# Stage for pulling the hhg-studio snap package and
# extracting the squashfs root
FROM base AS snap

RUN --mount=type=cache,target=/var/cache/apt,sharing=locked \
  --mount=type=cache,target=/var/lib/apt,sharing=locked \
  apt update && apt install --no-install-recommends -y snapd squashfs-tools

RUN snap download hhg-studio

RUN unsquashfs hhg-studio_*.snap


FROM base

RUN --mount=type=cache,target=/var/cache/apt,sharing=locked \
  --mount=type=cache,target=/var/lib/apt,sharing=locked \
  apt update && apt install -y --no-install-recommends qtbase5-dev libpng-dev libglib2.0-dev

COPY --from=snap /opt/hhg-studio/squashfs-root ./squashfs-root

# Define environment vars used by snap (launch.sh script)
#ENV WAYLAND_DISABLE=1
#ENV QT_DEBUG_PLUGINS=1
ENV SNAP_ARCH=amd64
ENV RUNTIME=/opt/hhg-studio/squashfs-root
ENV SNAP=/opt/hhg-studio/squashfs-root
ENV SNAP_USER_COMMON=/tmp/hhg-studio/common
ENV SNAP_USER_DATA=/tmp/hhg-studio/home

RUN <<EOT
cp /opt/hhg-studio/squashfs-root/usr/share/glib-2.0/schemas/* /usr/share/glib-2.0/schemas/.
glib-compile-schemas /usr/share/glib-2.0/schemas/
EOT

ENTRYPOINT ["/opt/hhg-studio/squashfs-root/bin/desktop-launch", "/opt/hhg-studio/squashfs-root/usr/local/bin/hhg-studio"]

