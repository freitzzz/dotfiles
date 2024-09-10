-- Volume widget

local assets = require 'assets'
local button = require 'widgets.button'
local commands = require 'commands'

local self = {}

local function onClick(_)
    return commands.power_menu()
end

function self:new()
    return button {
        color = "#f9e2af",
        icon = assets.icons.speaker,
        onClick = onClick,
        onInit = function(btn)
            commands.volume(function(vol)
                button.update(btn, { text = vol })
            end, { watch = true })
        end,
    }
end

return setmetatable(self, {
    __call = self.new,
})
