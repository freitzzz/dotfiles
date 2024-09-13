-- CPU widget

local assets   = require 'assets'
local button   = require 'widgets.button'
local palettes = require 'widgets.palettes'
local menus    = require 'widgets.menus'

local self     = {}

function self:new(args)
    return button {
        color = palettes.home,
        icon = assets.icons.home,
        onClick = menus.awesome,
    }
end

return setmetatable(self, {
    __call = self.new,
})
