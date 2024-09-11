-- CPU widget

local assets = require 'assets'
local button = require 'widgets.button'

local self = {}

function self:new()
    return button {
        color = "#FFFFFF",
        icon = assets.icons.home
    }
end

return setmetatable(self, {
    __call = self.new,
})
