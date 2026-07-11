#!/bin/bash
# Delete HiveMapperDrone and WordFinder demo repos (requires delete_repo scope).
set -euo pipefail
GH="${GH_BIN:-gh}"
if ! command -v "$GH" >/dev/null 2>&1 && [ -x /tmp/gh_2.63.2_linux_amd64/bin/gh ]; then
  GH=/tmp/gh_2.63.2_linux_amd64/bin/gh
fi

if ! "$GH" auth status >/dev/null 2>&1; then
  echo "Run: $GH auth login"
  exit 1
fi

echo "Grant delete_repo scope (browser/device flow):"
"$GH" auth refresh -h github.com -s delete_repo

for repo in HiveMapperDrone WordFinder; do
  echo "Deleting kevingnet/$repo ..."
  "$GH" repo delete "kevingnet/$repo" --yes
done

echo "Done. Live demos at kevingnet.github.io/HiveMapperDrone and .../WordFinder will 404."
