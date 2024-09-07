-- Bluetooth widget

local awful = require 'awful'
local button = require 'widgets.button'

local self = {}

local function onClick(btn)
    awful.spawn.easy_async_with_shell("/home/freitas/.local/bin/rofi-bluetooth-menu", function(out)
        if out == '0' then
            button.update(btn, { icon = '/home/freitas/.config/awesome/assets/icons/bluetooth.svg', text = nil })
        elseif out == '1' then
            button.update(btn, { icon = '/home/freitas/.config/awesome/assets/icons/bluetooth-off.svg', text = nil })
        else
            button.update(btn, { icon = '/home/freitas/.config/awesome/assets/icons/bluetooth.svg', text = out })
        end
    end)
end

function self:new()
    return button {
        icon = "/home/freitas/.config/awesome/assets/icons/bluetooth.svg",
        color = '#9bcbf8',
        onClick = function(_)
            print('oi?')
            onClick(btn)
        end
    }
end

return setmetatable(self, {
    __call = self.new,
})
