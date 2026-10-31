#!/usr/bin/env bash
set -euo pipefail

VERSION="${1:-}"
if [ -z "$VERSION" ]; then
  echo "Uso: $0 <versão> (ex: 0.1.0)" >&2
  exit 1
fi

TAG="v${VERSION#v}"
CLEAN_VER="${VERSION#v}"
REPO="cleberalves40/Sonda-Huawei"
URL="https://github.com/${REPO}/archive/refs/tags/${TAG}.tar.gz"

echo "[*] Baixando tarball da tag ${TAG}..."
TMPFILE=$(mktemp /tmp/sonda-huawei-${TAG}.XXXXXX.tar.gz)
trap 'rm -f "$TMPFILE"' EXIT

curl -sSL "$URL" -o "$TMPFILE"

SHA256=$(shasum -a 256 "$TMPFILE" | awk '{print $1}')
SIZE=$(stat -f%z "$TMPFILE" 2>/dev/null || stat -c%s "$TMPFILE")
TIMESTAMP=$(date +%s)

echo ""
echo "=== FREEBSD (freebsd/distinfo) ==="
echo "TIMESTAMP = ${TIMESTAMP}"
echo "SHA256 (cleberalves40-Sonda-Huawei-${TAG}_GH0.tar.gz) = ${SHA256}"
echo "SIZE (cleberalves40-Sonda-Huawei-${TAG}_GH0.tar.gz) = ${SIZE}"

echo ""
echo "=== HOMEBREW (Formula/sonda-huawei.rb) ==="
echo "  url \"${URL}\""
echo "  sha256 \"${SHA256}\""
echo ""

