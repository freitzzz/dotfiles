-- Power widget

local assets   = require 'assets'
local button   = require 'widgets.button'
local commands = require 'commands'
local palettes = require 'widgets.palettes'

local self     = {}

local function onClick(_)
    return commands.power_menu()
end

function self:new()
    return button {
        color = palettes.power,
        icon = assets.icons.power,
        onClick = onClick
    }
end

return setmetatable(self, {
    __call = self.new,
})
