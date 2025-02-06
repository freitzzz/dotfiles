-- App tray widget

local awful = require("awful")
local gears = require("gears")
local wibox = require("wibox")
local button = require("widgets.button")
local palettes = require 'widgets.palettes'
local assets = require("assets")

local self = {}

-- Function to fetch the list of open clients and their associated icons
local function get_workspace_icons()
    local icons = {}
    for _, c in ipairs(client.get()) do
        if c.first_tag == awful.screen.focused().selected_tag then
            local icon = c.icon or assets.icons.app_placeholder
            table.insert(icons, { icon = icon, client = c })
        end
    end
    return icons
end

function self:new()
    local icon_container = wibox.widget {
        layout = wibox.layout.fixed.horizontal,
        spacing = 5,
    }

    local function update_icons()
        icon_container:reset()
        for _, data in ipairs(get_workspace_icons()) do
            local icon_path = data.icon
            local client_ref = data.client

            local icon_widget = button {
                icon = icon_path,
                color = palettes.home,
                onClick = function()
                    if client_ref and client_ref.valid then
                        client_ref:emit_signal("request::activate", "widget_click", { raise = true })
                    end
                end
            }

            icon_container:add(icon_widget)
        end
    end

    tag.connect_signal("property::selected", update_icons)
    client.connect_signal("manage", update_icons)
    client.connect_signal("unmanage", update_icons)

    update_icons()

    return icon_container
end

return setmetatable(self, {
    __call = self.new,
})
