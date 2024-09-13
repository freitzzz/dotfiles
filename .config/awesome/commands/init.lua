local awful = require 'awful'
local watch = awful.spawn and awful.spawn.with_line_callback

local home_path = require 'globals'.home_path

--- Executes a command as an OS call. If [cb] is passed, command is launched a in a coroutine.
---@param cmd string|table
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

--- Executes a command as an OS call and streams the output in a line manner.
--- Returns a callback that once called kills the stream. Stream is automatically
--- killed if awesome exits.
---@param cmd string
---@param cb function
---@return function
local function stream(cmd, cb)
    local cmd_args = { "stdbuf", "-oL" }
    for arg in string.gmatch(cmd, "[^%s]+") do table.insert(cmd_args, arg) end

    local pid = watch(cmd_args, {
        stdout = cb
    })

    local kill_cb = function()
        awesome.kill(-pid, awesome.unix_signal.SIGTERM)
    end

    awesome.connect_signal("exit", kill_cb)

    return kill_cb
end

--- Callls [command] returning full output if [opt.watch] parameter is false.
--- Otherwise calls [stream].
---@param cmd string
---@param cb? function
---@param opt? table
---@return string | function
local function command_or_stream(cmd, cb, opt)
    if not opt or not opt.watch or not cb then
        return command(cmd, cb)
    else
        return stream(cmd, cb)
    end
end

--- Launches bluetooth menu.
---@param cb? function
local function bluetooth_menu(cb, opt)
    return command_or_stream(home_path .. "/.local/bin/rofi-bluetooth-menu", cb, opt)
end

--- Queries bluetooth connected status. Returns 0 if connected, 1 otherwise.
---@param cb? function
local function bluetooth_connected(cb, opt)
    return command_or_stream(home_path .. "/.local/bin/rofi-bluetooth-menu --query-power", cb, opt)
end

--- Queries CPU temperature.
---@param cb? function
local function cpu_temp(cb, opt)
    return command_or_stream(home_path .. "/.local/bin/system-stats temp", cb, opt)
end

--- Queries CPU usage.
---@param cb? function
local function cpu_usage(cb, opt)
    return command_or_stream(home_path .. "/.local/bin/system-stats cpu", cb, opt)
end

--- Launches power menu.
---@param cb? function
local function power_menu(cb, opt)
    return command_or_stream(home_path .. "/.local/bin/rofi-poweroff-menu", cb, opt)
end

--- Queries RAM usage.
---@param cb? function
local function ram_usage(cb, opt)
    return command_or_stream(home_path .. "/.local/bin/system-stats ram", cb, opt)
end

--- Takes a screenshot.
---@param cb? function
local function screenshot(cb, opt)
    return command_or_stream(home_path .. "/.local/bin/screenshot select", cb, opt)
end

--- Queries master channel volume.
---@param cb? function
local function volume(cb, opt)
    return command_or_stream(home_path .. "/.local/bin/volume-level --monitor", cb, opt)
end

--- Increases master channel volume.
---@param cb? function
local function volume_increase(cb, opt)
    return command_or_stream(home_path .. "/.local/bin/volume-manager --increase", cb, opt)
end

--- Decreases master channel volume.
---@param cb? function
local function volume_decrease(cb, opt)
    return command_or_stream(home_path .. "/.local/bin/volume-manager --decrease", cb, opt)
end

--- Mutes/Unmutes master channel volume.
---@param cb? function
local function volume_mute(cb, opt)
    return command_or_stream(home_path .. "/.local/bin/volume-manager --mute", cb, opt)
end

--- Launches wifi menu.
---@param cb? function
local function wifi_menu(cb, opt)
    return command_or_stream(home_path .. "/.local/bin/rofi-wifi-menu", cb, opt)
end

--- Queries WiFi enabled status.
---@param cb? function
local function wifi_enabled(cb, opt)
    return command_or_stream(home_path .. "/.local/bin/wifi-enabled", cb, opt)
end

--- Queries connected WiFi network SSID.
---@param cb? function
local function wifi_ssid(cb, opt)
    return command_or_stream(home_path .. "/.local/bin/wifi-ssid", cb, opt)
end

return {
    command = command,
    stream = stream,
    bluetooth_menu = bluetooth_menu,
    bluetooth_connected = bluetooth_connected,
    cpu_temp = cpu_temp,
    cpu_usage = cpu_usage,
    power_menu = power_menu,
    ram_usage = ram_usage,
    screenshot = screenshot,
    volume = volume,
    volume_decrease = volume_decrease,
    volume_increase = volume_increase,
    volume_mute = volume_mute,
    wifi_enabled = wifi_enabled,
    wifi_menu = wifi_menu,
    wifi_ssid = wifi_ssid,
}
