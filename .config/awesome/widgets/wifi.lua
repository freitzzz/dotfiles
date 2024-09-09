-- Wifi widget

local assets = require 'assets'
local button = require 'widgets.button'
local commands = require 'commands'
local gears = require 'gears'

local self = {}
local ssid_query_timer

local function updateButton(btn)
    commands.wifi_enabled(function(out)
        if out == 'enabled' then
            commands.wifi_ssid(function(ssid)
                if ssid == '' then
                    ssid_query_timer = gears.timer {
                        timeout   = 3,
                        call_now  = false,
                        autostart = true,
                        callback  = function()
                            commands.wifi_ssid(function(ssid)
                                if not (ssid == '')
                                then
                                    button.update(btn, { text = ssid, icon = assets.icons.wifi })
                                    -- cleanup (use watch)
                                    ssid_query_timer:stop()
                                    ssid_query_timer = nil
                                end
                            end)
                        end
                    }
                else
                    button.update(btn, { text = ssid, icon = assets.icons.wifi })
                end
            end)
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
