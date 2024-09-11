-- Temperature widget

local assets     = require 'assets'
local button     = require 'widgets.button'
local commands   = require 'commands'
local foundation = require 'foundation'
local palettes   = require 'widgets.palettes'

local self       = {}

function self:new()
    return button {
        color = palettes.temp,
        icon = assets.icons.thermometer,
        onInit = function(btn)
            foundation.schedule {
                timeout = 10,
                autostart = true,
                instant = true,
                callback = function()
                    commands.cpu_temp(function(out)
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
