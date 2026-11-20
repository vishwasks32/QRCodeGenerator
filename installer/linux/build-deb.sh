#!/bin/sh
set -eu

repo_root=$(CDPATH= cd -- "$(dirname -- "$0")/../.." && pwd)
version=$(sed -n 's/^version = "\(.*\)"/\1/p' "$repo_root/pyproject.toml" | head -n 1)

if [ -z "$version" ]; then
    printf '%s\n' "Could not read the project version from pyproject.toml" >&2
    exit 1
fi

mkdir -p "$repo_root/dist"
stage=$(mktemp -d)
trap 'rm -rf "$stage"' EXIT

package="$stage/qr-code-generator-app"
python_dir="$package/usr/lib/python3/dist-packages/qr_code_generator"

install -d "$python_dir/assets"
find "$repo_root/qr_code_generator" -maxdepth 1 -type f -name '*.py' \
    -exec install -m 644 {} "$python_dir/" \;
install -m 644 "$repo_root/qr_code_generator/assets/qr_gen_icon.png" "$python_dir/assets/"

install -D -m 644 "$repo_root/QR Code Generator.desktop" \
    "$package/usr/share/applications/qr-code-generator.desktop"
install -D -m 644 "$repo_root/qr_code_generator/assets/qr_gen_icon.png" \
    "$package/usr/share/pixmaps/qr_gen_icon.png"
install -D -m 644 /dev/stdin "$package/DEBIAN/control" <<EOF
Package: qr-code-generator-app
Version: $version
Section: graphics
Priority: optional
Architecture: all
Depends: python3 (>= 3.9), python3-qrcode, python3-pil, python3-tk
Maintainer: QR Code Generator Project <noreply@github.com>
Description: Generate QR codes using a graphical or command-line interface
 A simple application for generating and saving QR codes.
EOF

install -d "$package/usr/bin"
printf '%s\n' '#!/bin/sh' 'exec /usr/bin/python3 -m qr_code_generator.launcher "$@"' \
    > "$package/usr/bin/qr-generator-ui"
printf '%s\n' '#!/bin/sh' 'exec /usr/bin/python3 -m qr_code_generator.generator "$@"' \
    > "$package/usr/bin/qr-generator"
chmod 755 "$package/usr/bin/qr-generator-ui" "$package/usr/bin/qr-generator"

dpkg-deb --build --root-owner-group "$package" \
    "$repo_root/dist/qr-code-generator-app_${version}_all.deb"
