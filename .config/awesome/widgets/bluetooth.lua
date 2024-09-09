-- Bluetooth widget

local assets = require 'assets'
local button = require 'widgets.button'
local commands = require 'commands'

local self = {}

local function updateIcon(btn)
    commands.bluetooth_connected(function(out)
        if out == '0' then
            button.update(btn, { icon = assets.icons.bluetooth, text = nil })
        elseif out == '1' then
            button.update(btn, { icon = assets.icons.bluetooth_off, text = nil })
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
