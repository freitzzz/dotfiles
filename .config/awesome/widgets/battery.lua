-- Battery widget

local assets   = require 'assets'
local gears    = require("gears")
local button   = require 'widgets.button'
local palettes = require 'widgets.palettes'

local tolower  = string.lower

local function readfile(command)
    local file = io.open(command)
    if not file then return nil end
    local text = file:read('*all')
    file:close()
    return text
end

local function trim(s)
    if not s then return nil end
    return (s:gsub("^%s*(.-)%s*$", "%1"))
end

local function read_trim(filename)
    return trim(readfile(filename)) or ""
end

local function folder_exists(filename)
    local file = io.open(filename)
    if not file then return false end

    file:close()
    return true
end

local self = {}

function self:new()
    self.percentage = ''
    self.isCharging = false
    local battery_exists = folder_exists("/sys/class/power_supply/BAT0")
    if battery_exists then self:update() else self.isCharging = true end

    local btn = button {
        icon = self.isCharging and assets.icons.plug_charging or assets.icons.plug,
        color = palettes.battery,
        text = self.percentage,
    }

    if not battery_exists then
        return btn
    end

    gears.timer {
        timeout   = 10,
        call_now  = true,
        autostart = true,
        callback  = function()
            self:update()
            button.update(btn, {
                text = self.percentage,
                -- prevent duplicate
                icon = self.isCharging and assets.icons.plug_charging or assets.icons.plug,
            })
        end
    }

    return btn
end

function self:update()
    local current = tolower(read_trim("/sys/class/power_supply/BAT0/capacity"))
    local status = tolower(read_trim("/sys/class/power_supply/BAT0/status"))

    self.percentage = current .. "%"
    self.isCharging = status == 'charging'
end

return setmetatable(self, {
    __call = self.new,
})
