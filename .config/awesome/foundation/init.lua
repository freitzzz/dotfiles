local timer = require 'gears.timer'


--- Schedules the execution of a function.
---@param args { timeout: number, autostart: boolean | false, instant: boolean | false, continuous: boolean | true, callback: function }
local function schedule(args)
    local ref = timer {
        timeout     = args.timeout,
        single_shot = type(args.continuous) == 'boolean' and not args.continuous or false,
        call_now    = type(args.instant) == 'boolean' and args.instant or false,
        autostart   = type(args.autostart) == 'boolean' and args.autostart or false,
        callback    = args.callback
    }

    awesome.connect_signal("exit", function()
        if ref.started then
            ref:stop()
        end
    end)
end

return {
    schedule = schedule,
}
