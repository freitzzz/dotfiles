-- Wifi widget

local assets = require 'assets'
local button = require 'widgets.button'
local commands = require 'commands'
local foundation = require 'foundation'

local self = {}

local function updateButton(btn)
    commands.wifi_enabled(function(out)
        if out == 'enabled' then
            foundation.schedule {
                timeout = 3,
                autostart = true,
                continuous = true,
                instant = true,
                callback = function(timer)
                    commands.wifi_ssid(function(ssid)
                        if not (ssid == '')
                        then
                            button.update(btn, { text = ssid, icon = assets.icons.wifi })

                            if timer then
                                timer:stop()
                            end
                        end
                    end)
                end
            }
        else
            button.update(btn, { icon = assets.icons.wifi_off, text = '' })
        end
    end)
end

local function onClick(btn)
    commands.wifi_menu(function()
        updateButton(btn)
    end)
end

function self:new()
    return button {
        color = '#bc96f4',
        onClick = onClick,
        onInit = updateButton,
        icon = assets.icons.wifi
    }
end

return setmetatable(self, {
    __call = self.new,
})
