-- (OG) Awesome Menu

local assets               = require 'assets'
local globals              = require 'globals'

local debian               = require("debian.menu")
local has_fdo, freedesktop = pcall(require, "freedesktop")
local hotkeys_popup        = require("awful.hotkeys_popup")

-- Enable hotkeys help widget for VIM and other apps
-- when client with a matching name is opened:
require("awful.hotkeys_popup.keys")

local function menu()
    local awesome_menu = {
        { "hotkeys",     function() hotkeys_popup.show_help(nil, awful.screen.focused()) end },
        { "manual",      globals.terminal .. " -e man awesome" },
        { "edit config", globals.editor_cmd .. " " .. awesome.conffile },
        { "restart",     awesome.restart },
        { "quit",        function() awesome.quit() end },
    }

    local menu_awesome = { "awesome", awesome_menu, assets.icons.home }
    local menu_terminal = { "open terminal", terminal }

    local main_menu = has_fdo and
        freedesktop.menu.build({
            before = { menu_awesome },
            after = { menu_terminal }
        }) or
        awful.menu({
            items = {
                menu_awesome,
                { "Debian", debian.menu.Debian_menu.Debian },
                menu_terminal,
            }
        })

    return main_menu
end

--- Cache awesome menu since it won't change + it's used in several places.
local cache_awesome_menu

return setmetatable({
    init = function()
        cache_awesome_menu = menu()
    end
}, {
    __call = function()
        if not cache_awesome_menu then
            cache_awesome_menu = menu()
        end

        cache_awesome_menu:toggle()
    end,
})
