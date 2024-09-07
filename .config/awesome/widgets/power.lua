-- Power widget

local awful = require 'awful'
local button = require 'widgets.button'

local self = {}

local function onClick(_)
    return awful.spawn("/home/freitas/.local/bin/rofi-poweroff-menu")
end

function self:new(args)
    return button {
        icon = "/home/freitas/.config/awesome/assets/icons/power.svg",
        onClick = onClick
    }
end

return setmetatable(self, {
    __call = self.new,
})
