-- Volume widget

local assets   = require 'assets'
local button   = require 'widgets.button'
local commands = require 'commands'
local palettes = require 'widgets.palettes'

local self     = {}

local function onClick(_)
end

function self:new()
    return button {
        color = palettes.volume,
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
