#!/bin/bash
# Create GitHub repo (if needed) and push for GitHub Pages.
set -euo pipefail
cd "$(dirname "$0")"

GH="${GH_BIN:-gh}"
if ! command -v "$GH" >/dev/null 2>&1 && [ -x /tmp/gh_2.63.2_linux_amd64/bin/gh ]; then
  GH=/tmp/gh_2.63.2_linux_amd64/bin/gh
fi

REPO="${GITHUB_REPO:-kevingnet/kg-portfolio}"
GIT_NAME="${GIT_NAME:-Kevin Alexander Guerra}"
GIT_EMAIL="${GIT_EMAIL:-kevingnet1@gmail.com}"
export GIT_AUTHOR_NAME="$GIT_NAME" GIT_AUTHOR_EMAIL="$GIT_EMAIL"
export GIT_COMMITTER_NAME="$GIT_NAME" GIT_COMMITTER_EMAIL="$GIT_EMAIL"

if ! "$GH" auth status >/dev/null 2>&1; then
  echo "Not logged into GitHub. Run once:"
  echo "  $GH auth login"
  echo "Then re-run: ./deploy.sh"
  exit 1
fi

python3 build_site.py
git add README.md build_site.py css/ js/ assets/ index.html about.html services.html samples.html projects/ .github/ .gitignore deploy.sh
if ! git diff --cached --quiet; then
  git commit -m "Rebuild site for deploy"
fi

if ! git remote get-url origin >/dev/null 2>&1; then
  "$GH" repo create "$REPO" --public --source=. --remote=origin --push
else
  git push -u origin main
fi

echo ""
echo "Enable Pages: repo → Settings → Pages → Source: GitHub Actions"
echo "Site URL: https://${REPO%%/*}.github.io/${REPO##*/}/"
