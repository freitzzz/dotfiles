local _battery = require 'widgets.battery'
local _bluetooth = require 'widgets.bluetooth'
local _power = require 'widgets.power'
local _volume = require 'widgets.volume'
local _wifi = require 'widgets.wifi'

return {
    battery = function()
        return _battery {}
    end,
    bluetooth = function()
        return _bluetooth {}
    end,
    power = function()
        return _power {}
    end,
    volume = function()
        return _volume {}
    end,
    wifi = function()
        return _wifi {}
    end
}
