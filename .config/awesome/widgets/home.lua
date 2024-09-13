-- CPU widget

local assets   = require 'assets'
local button   = require 'widgets.button'
local palettes = require 'widgets.palettes'

local self     = {}

---Creates the home widget.
---@param args {menu: function}
function self:new(args)
    return button {
        color = palettes.home,
        icon = assets.icons.home,
        onClick = args.menu,
    }
end

return setmetatable(self, {
    __call = self.new,
})
