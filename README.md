# Omarchy Vitesse

[Vitesse](https://github.com/antfu/vscode-theme-vitesse) for
[Omarchy](https://omarchy.org/), ported to Omarchy's `colors.toml` theme format.

Five variants, one per upstream mode:

| Theme | Repository | Background | Foreground | Accent |
| --- | --- | --- | --- | --- |
| `vitesse-light` | [omarchy-vitesse-light-theme](https://github.com/AkaraChen/omarchy-vitesse-light-theme) | `#ffffff` | `#393a34` | `#1e754f` |
| `vitesse-light-soft` | [omarchy-vitesse-light-soft-theme](https://github.com/AkaraChen/omarchy-vitesse-light-soft-theme) | `#f1f0e9` | `#393a34` | `#1e754f` |
| `vitesse-dark` | [omarchy-vitesse-dark-theme](https://github.com/AkaraChen/omarchy-vitesse-dark-theme) | `#121212` | `#dbd7ca` | `#4d9375` |
| `vitesse-dark-soft` | [omarchy-vitesse-dark-soft-theme](https://github.com/AkaraChen/omarchy-vitesse-dark-soft-theme) | `#222222` | `#dbd7ca` | `#4d9375` |
| `vitesse-black` | [omarchy-vitesse-black-theme](https://github.com/AkaraChen/omarchy-vitesse-black-theme) | `#000000` | `#dbd7ca` | `#4d9375` |

The accent is Vitesse's keyword green. Bright ANSI colors intentionally match
their normal counterparts, as they do upstream.

## Install

Each variant is published as its own colors-only theme repository, installable
straight from Omarchy:

```bash
omarchy theme install https://github.com/AkaraChen/omarchy-vitesse-dark-theme
```

Those repositories carry `colors.toml`, `chromium.theme` and `preview.png` only.
This repository is the source they are generated from, plus the tools and
editor files that cannot ship in an installed theme.

### From this repository

To get the bundled `neovim.lua` and terminal configs as well:

```bash
git clone https://github.com/AkaraChen/omarchy-vitesse.git ~/Developer/omarchy-vitesse
cd ~/Developer/omarchy-vitesse
./install.sh
```

`install.sh` symlinks each directory under `themes/` into
`~/.config/omarchy/themes/`. Symlinks are used deliberately: Omarchy strips Lua,
terminal configs, and `vscode.json` from themes cloned with
`omarchy theme install`, but treats a symlink to your own working copy as a
user-authored theme.

Apply one:

```bash
omarchy theme set vitesse-dark
```

List them with `omarchy theme list`; the display names are `Vitesse Light`,
`Vitesse Dark`, and so on.

Uninstall the symlinks:

```bash
./install.sh --uninstall
```

## Wallpapers

These themes intentionally ship no `backgrounds/`. Applying one keeps your
current wallpaper. To give a variant its own wallpaper later, add images to
`themes/<slug>/backgrounds/` (or `~/.config/omarchy/backgrounds/<slug>/`); the
theme picker and `omarchy theme bg next` will find them.

## Neovim

Each theme ships a `neovim.lua` that installs
[qshan-li/neovim-theme-vitesse](https://github.com/qshan-li/neovim-theme-vitesse)
and selects the matching variant:

```lua
{ "qshan-li/neovim-theme-vitesse", lazy = false, priority = 1000,
  opts = { theme = "dark" } },
{ "LazyVim/LazyVim", opts = { colorscheme = "vitesse" } },
```

Omarchy's stock Neovim configuration loads it through the usual symlink:

```
~/.config/nvim/lua/plugins/theme.lua
  -> ~/.local/state/omarchy/current/theme/neovim.lua
```

If you use a different Neovim distribution (AstroNvim, a hand-written config,
`nvim -u NONE`, ...), that symlink is not present and the file is ignored. For
AstroNvim there is a ready-made adapter:

```bash
cp extras/astronvim.lua ~/.config/nvim/lua/plugins/vitesse.lua
```

It reads `~/.local/state/omarchy/current/theme.name` at startup, picks the
matching Vitesse variant, and points `astroui` at `vitesse`. Restart Neovim
after switching the Omarchy theme.

## VS Code

No `vscode.json` is shipped, so Omarchy generates an approximate theme from
`colors.toml`. If you want the real thing, install
[antfu.theme-vitesse](https://marketplace.visualstudio.com/items?itemName=antfu.theme-vitesse)
and add this to the theme directory:

```json
{ "name": "Vitesse Dark", "extension": "antfu.theme-vitesse" }
```

## Browser color

`chromium.theme` is the browser's **design-system** color, not the terminal
ANSI blue. Omarchy writes it into Chromium's `BrowserThemeColor` policy, and
Chromium generates its own frame, toolbar and omnibox selection colors from it.
Stock themes set this explicitly (Rose Pine ships a mauve), which is why their
browser chrome and address-bar selection follow the theme.

These themes ship a pale tint of Vitesse's keyword teal instead of reusing the
page background, so the browser UI does not fall back to Chromium's default
blue.

## Design notes

`colors.toml` only carries semantic colors; Omarchy renders the terminal,
btop, Helix, shell/bar, window borders, menus, and everything else from it.
That means the port keeps Vitesse's terminal palette and UI tone while apps
like btop and Helix get the closest equivalent from Omarchy's templates, not a
pixel-perfect upstream port.

Palette decisions:

- `muted` is the upstream comment color (`#758575` dark, `#a0ada0` light), so
  comments and dim UI text stay in the same family.
- `dark_foreground` is the bracket/punctuation gray (`#777777` / `#999999`).
- `orange` carries constants and numbers, `red` operators and errors.
- Upstream foregrounds are alpha-blended (`#dbd7caee`); they are flattened to
  solid hex because `colors.toml` values must be opaque.
- `blue` is a **design-system** color, not the terminal ANSI blue. Omarchy
  renders links, functions, info icons and other UI from it, and Vitesse does
  not use blue there, so it points at the keyword green. The terminal configs
  under each theme keep the real xterm blue (`#296aa3` light, `#6394bf` dark)
  for ANSI palette slot 4/12.

## Regenerate

`tools/generate.py` is the source of truth. It writes every `colors.toml`,
`chromium.theme` and `neovim.lua`:

```bash
python3 tools/generate.py
python3 tools/generate.py --check   # CI / pre-commit check
```

`tools/preview.py` renders the palette-card `preview.png` placeholders. Replace
them with real screenshots when convenient.

## Layout

```
themes/
  vitesse-<variant>/
    colors.toml
    chromium.theme
    alacritty.toml
    foot.ini
    ghostty.conf
    kitty.conf
    neovim.lua
    preview.png
tools/
  generate.py       # palette + generated files
  preview.py        # placeholder preview cards
  templates/        # terminal templates (palette only, no font/window settings)
extras/
  astronvim.lua     # adapter for AstroNvim users
install.sh          # symlink themes into ~/.config/omarchy/themes
```

## Credits

- Palette and original design: [antfu/vscode-theme-vitesse](https://github.com/antfu/vscode-theme-vitesse) (MIT)
- Neovim port: [qshan-li/neovim-theme-vitesse](https://github.com/qshan-li/neovim-theme-vitesse) (MIT)
