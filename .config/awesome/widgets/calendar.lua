-- Calendar widget

local assets = require 'assets'
local button = require 'widgets.button'
local gears = require 'gears'

local self = {}

local function date_time()
    return os.date("%H:%M (%d/%m/%Y)")
end

local function timeout()
    local current_min = os.time()
    local next_minute = math.ceil(current_min / 60) * 60
    return next_minute - current_min
end

local function onInit(btn)
    local timer = gears.timer {
        timeout     = timeout(),
        single_shot = false,
        call_now    = false,
        autostart   = true,
        callback    = function(timer)
            button.update(btn, { text = date_time() })
            timer.timeout = 60
            timer:again()
        end
    }

    local kill_cb = function()
        awesome.kill(timer, awesome.unix_signal.SIGTERM)
    end

    awesome.connect_signal("exit", kill_cb)
end

function self:new()
    return button {
        color = "#94e2d5",
        icon = assets.icons.calendar,
        text = date_time(),
        onInit = onInit
    }
end

return setmetatable(self, {
    __call = self.new,
})
