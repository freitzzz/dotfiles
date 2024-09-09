local awful = require 'awful'

--- Executes a command as an OS call. If [cb] is passed, command is launched a in a coroutine.
---@param cmd string
---@param cb? function
---@return string
local function command(cmd, cb)
    if not cb then
        return awful.spawn(cmd)
    else
        return awful.spawn.easy_async(cmd, function(out)
            return cb(string.gsub(out, "%s+", ""))
        end)
    end
end

--- Launches bluetooth menu.
---@param cb? function
---@return string
local function bluetooth_menu(cb)
    return command("/home/freitas/.local/bin/rofi-bluetooth-menu", cb)
end

--- Queries bluetooth connected status. Returns 0 if connected, 1 otherwise.
---@param cb? function
---@return "0" | "1"
local function bluetooth_connected(cb)
    return command("/home/freitas/.local/bin/rofi-bluetooth-menu --query-power", cb)
end


--- Launches power menu.
---@param cb? function
---@return string
local function power_menu(cb)
    return command("/home/freitas/.local/bin/rofi-poweroff-menu", cb)
end

--- Launches wifi menu.
---@param cb? function
---@return string
local function wifi_menu(cb)
    return command("/home/freitas/.local/bin/rofi-wifi-menu", cb)
end

--- Queries WiFi enabled status.
---@param cb? function
---@return string
local function wifi_enabled(cb)
    return command("/home/freitas/.local/bin/wifi-enabled", cb)
end

--- Queries connected WiFi network SSID.
---@param cb? function
---@return string
local function wifi_ssid(cb)
    return command("/home/freitas/.local/bin/wifi-ssid", cb)
end

return {
    command = command,
    bluetooth_menu = bluetooth_menu,
    bluetooth_connected = bluetooth_connected,
    power_menu = power_menu,
    wifi_enabled = wifi_enabled,
    wifi_menu = wifi_menu,
    wifi_ssid = wifi_ssid,
}
