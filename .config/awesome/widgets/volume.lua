-- Volume widget

local assets   = require 'assets'
local button   = require 'widgets.button'
local commands = require 'commands'
local palettes = require 'widgets.palettes'

local self     = {}

local function onClick(_)
    commands.volume_menu()
end

function self:new()
    return button {
        color = palettes.volume,
        icon = assets.icons.speaker,
        onClick = onClick,
        onInit = function(btn)
            commands.volume(function(vol)
                if vol == 'mute' then
                    button.update(btn, { text = '', icon = assets.icons.speaker_off })
                else
                    button.update(btn, { text = vol, icon = assets.icons.speaker })
                end
            end, { watch = true })
        end,
    }
end

return setmetatable(self, {
    __call = self.new,
})
