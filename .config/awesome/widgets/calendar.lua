-- Calendar widget

local assets     = require 'assets'
local button     = require 'widgets.button'
local foundation = require 'foundation'
local palettes   = require 'widgets.palettes'

local self       = {}

local function date_time()
    return os.date("%H:%M (%d/%m/%Y)")
end

local function first_timeout()
    local current_min = os.time()
    local next_minute = math.ceil(current_min / 60) * 60
    return next_minute - current_min
end

local function onInit(btn)
    foundation.schedule {
        timeout   = first_timeout(),
        autostart = true,
        instant   = false,
        callback  = function(timer)
            button.update(btn, { text = date_time() })
            timer.timeout = 60
            timer:again()
        end
    }
end

function self:new()
    return button {
        color = palettes.calendar,
        icon = assets.icons.calendar,
        text = date_time(),
        onInit = onInit
    }
end

return setmetatable(self, {
    __call = self.new,
})
