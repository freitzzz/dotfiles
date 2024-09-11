-- RAM widget

local assets     = require 'assets'
local button     = require 'widgets.button'
local commands   = require 'commands'
local foundation = require 'foundation'

local self       = {}

function self:new()
    return button {
        color = "#f5c2e7",
        icon = assets.icons.ram,
        onInit = function(btn)
            foundation.schedule {
                timeout = 5,
                autostart = true,
                instant = true,
                callback = function()
                    commands.ram_usage(function(out)
                        button.update(btn, { text = out })
                    end)
                end
            }
        end
    }
end

return setmetatable(self, {
    __call = self.new,
})
