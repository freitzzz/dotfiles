-- CPU widget

local assets     = require 'assets'
local button     = require 'widgets.button'
local commands   = require 'commands'
local foundation = require 'foundation'

local self       = {}

function self:new()
    return button {
        color = "#eba0ac",
        icon = assets.icons.cpu,
        onInit = function(btn)
            foundation.schedule {
                timeout = 5,
                autostart = true,
                instant = true,
                callback = function()
                    commands.cpu_usage(function(out)
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
