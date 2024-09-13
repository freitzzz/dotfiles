local theme_assets             = require("beautiful.theme_assets")
local xresources               = require("beautiful.xresources")
local gears                    = require("gears")
local dpi                      = xresources.apply_dpi

local gfs                      = require("gears.filesystem")
local config_path              = gfs.get_configuration_dir()

local theme                    = {}

theme.font                     = "JetBrains Mono Nerd Font 12"
theme.hotkeys_font             = "JetBrains Mono Nerd Font 12"
theme.hotkeys_description_font = "JetBrains Mono Nerd Font 10"

theme.hotkeys_modifiers_fg     = "#FF0000"

theme.bg_normal                = "#b4befe"
theme.bg_focus                 = "#535d6c"
theme.bg_urgent                = "#ff0000"
theme.bg_minimize              = "#444444"
theme.bg_systray               = theme.bg_normal

theme.fg_normal                = "#000000"
theme.fg_focus                 = "#ffffff"
theme.fg_urgent                = "#ffffff"
theme.fg_minimize              = "#ffffff"

theme.useless_gap              = dpi(4)
theme.border_width             = dpi(2)
theme.border_normal            = "#6c7086"
theme.border_focus             = "#9399b2FF"
theme.border_marked            = "#9399b2F0"

local taglist_square_size      = dpi(4)
theme.taglist_squares_sel      = theme_assets.taglist_squares_sel(
    taglist_square_size, theme.fg_normal
)
theme.taglist_squares_unsel    = theme_assets.taglist_squares_unsel(
    taglist_square_size, theme.fg_normal
)

theme.notification_font        = "JetBrains Mono Nerd Font"
theme.notification_shape       = gears.shape.rounded_rect

theme.menu_height              = dpi(36)
theme.menu_width               = dpi(300)

theme.titlebar_size            = dpi(10)

theme.awesome_icon             = config_path .. "assets/icons/icon.svg"
theme.wallpaper                = config_path .. "assets/background.jpg"

return theme
