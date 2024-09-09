-- Power widget

local button = require 'widgets.button'
local commands = require 'commands'

local self = {}

local function onClick(_)
    return commands.power_menu()
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
