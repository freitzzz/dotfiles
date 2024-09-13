local _battery = require 'widgets.battery'
local _bluetooth = require 'widgets.bluetooth'
local _calendar = require 'widgets.calendar'
local _cpu = require 'widgets.cpu'
local _home = require 'widgets.home'
local _power = require 'widgets.power'
local _ram = require 'widgets.ram'
local _temp = require 'widgets.temp'
local _volume = require 'widgets.volume'
local _wifi = require 'widgets.wifi'

return {
    battery = function()
        return _battery {}
    end,
    bluetooth = function()
        return _bluetooth {}
    end,
    calendar = function()
        return _calendar {}
    end,
    cpu = function()
        return _cpu {}
    end,
    home = function(menu)
        return _home {
            menu = menu
        }
    end,
    power = function()
        return _power {}
    end,
    ram = function()
        return _ram {}
    end,
    temp = function()
        return _temp {}
    end,
    volume = function()
        return _volume {}
    end,
    wifi = function()
        return _wifi {}
    end
}
