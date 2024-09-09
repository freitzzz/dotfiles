-- Bluetooth widget

local button = require 'widgets.button'
local commands = require 'commands'

local self = {}

local function updateIcon(btn)
    commands.bluetooth_connected(function(out)
        if out == '0' then
            button.update(btn, { icon = '/home/freitas/.config/awesome/assets/icons/bluetooth.svg', text = nil })
        elseif out == '1' then
            button.update(btn, { icon = '/home/freitas/.config/awesome/assets/icons/bluetooth-off.svg', text = nil })
        end
    end)
end

local function onClick(btn)
    commands.bluetooth_menu(function()
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
