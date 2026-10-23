-- AstroNvim adapter for the Omarchy Vitesse themes.
--
-- Omarchy's own Neovim config loads a theme's neovim.lua through
-- ~/.config/nvim/lua/plugins/theme.lua. AstroNvim does not have that symlink,
-- so copy this file to your AstroNvim config instead:
--
--   cp extras/astronvim.lua ~/.config/nvim/lua/plugins/vitesse.lua
--
-- It reads ~/.local/state/omarchy/current/theme.name at startup, so switching
-- the Omarchy theme and restarting Neovim is enough to switch variants.

local variants = {
  ["vitesse-light"] = "light",
  ["vitesse-light-soft"] = "light-soft",
  ["vitesse-dark"] = "dark",
  ["vitesse-dark-soft"] = "dark-soft",
  ["vitesse-black"] = "black",
}

local function current_variant()
  local path = vim.fn.expand("~/.local/state/omarchy/current/theme.name")
  if vim.fn.filereadable(path) == 0 then
    return "dark"
  end
  local name = vim.fn.readfile(path)[1]
  return variants[name] or "dark"
end

return {
  {
    "qshan-li/neovim-theme-vitesse",
    lazy = false,
    priority = 1000,
    opts = { theme = current_variant() },
  },
  {
    "AstroNvim/astroui",
    opts = { colorscheme = "vitesse" },
  },
}
