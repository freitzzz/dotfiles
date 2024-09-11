-- CPU widget

local assets   = require 'assets'
local button   = require 'widgets.button'
local palettes = require 'widgets.palettes'

local self     = {}

function self:new()
    return button {
        color = palettes.home,
        icon = assets.icons.home
    }
end

return setmetatable(self, {
    __call = self.new,
})
