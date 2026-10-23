#!/usr/bin/env bash
# Link the Vitesse themes into the user's Omarchy theme directory.
set -euo pipefail

repo_dir=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)
themes_dir="${XDG_CONFIG_HOME:-$HOME/.config}/omarchy/themes"

usage() {
  cat <<'EOF'
Usage: ./install.sh [--uninstall]

Without arguments, symlinks every directory under themes/ into
~/.config/omarchy/themes/. Omarchy treats a symlink to your own working copy as
a user-authored theme, so the bundled neovim.lua is allowed.

  --uninstall   Remove the symlinks created by this script.
  -h, --help    Show this help.
EOF
}

case "${1:-}" in
  "" | --install) action=install ;;
  --uninstall) action=uninstall ;;
  -h | --help)
    usage
    exit 0
    ;;
  *)
    echo "Unknown argument: $1" >&2
    usage >&2
    exit 1
    ;;
esac

mkdir -p "$themes_dir"

for source in "$repo_dir"/themes/*/; do
  source=${source%/}
  name=$(basename "$source")
  target="$themes_dir/$name"

  if [[ $action == uninstall ]]; then
    if [[ -L $target ]]; then
      rm "$target"
      echo "unlinked $name"
    fi
    continue
  fi

  if [[ -e $target && ! -L $target ]]; then
    echo "skip $name: $target exists and is not a symlink" >&2
    continue
  fi

  ln -sfn "$source" "$target"
  echo "linked $name -> $source"
done

if [[ $action == install ]]; then
  cat <<'EOF'

Done. Apply a variant with, for example:

  omarchy theme set vitesse-dark

The themes ship no backgrounds, so the current wallpaper is kept.
EOF
fi
