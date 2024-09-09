-- Bluetooth widget

local awful = require 'awful'
local button = require 'widgets.button'

local self = {}

local function updateIcon(btn)
    awful.spawn.easy_async_with_shell("/home/freitas/.local/bin/rofi-bluetooth-menu --query-power", function(out)
        out = string.gsub(out, "%s+", "")

        if out == '0' then
            button.update(btn, { icon = '/home/freitas/.config/awesome/assets/icons/bluetooth.svg', text = nil })
        elseif out == '1' then
            button.update(btn, { icon = '/home/freitas/.config/awesome/assets/icons/bluetooth-off.svg', text = nil })
        end
    end)
end

local function onClick(btn)
    awful.spawn.easy_async_with_shell("/home/freitas/.local/bin/rofi-bluetooth-menu", function()
        updateIcon(btn)
    end)
end

function self:new()
    return button {
        color = '#9bcbf8',
        onClick = onClick,
        onInit = updateIcon
    }
end

return setmetatable(self, {
    __call = self.new,
})
