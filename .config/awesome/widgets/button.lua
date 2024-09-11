-- Themed button widget
-- Original Source: https://github.com/streetturtle/awesome-buttons
-- Status: Modified

local wibox = require("wibox")
local gears = require("gears")

local margin = 4

local self = {}

function self:new(args)
    local color = args.color or '#f38ba8'
    local icon = args.icon
    local text = args.text
    local onClick = args.onClick
    local onHover = args.onHover
    local onInit = args.onInit

    local button = wibox.widget {
        {
            {
                {
                    id = 'icon',
                    image = icon,
                    widget = wibox.widget.imagebox
                },
                margins = margin,
                widget = wibox.container.margin
            },
            {
                {
                    markup = text,
                    widget = wibox.widget.textbox
                },
                id = 'text',
                update = function(_self, value)
                    _self:get_all_children()[1]:set_markup(value)

                    if not value or #value == 0 then
                        _self:set_margins(0)
                    else
                        _self:set_margins(margin)
                    end
                end,
                margins = (not text or #text == 0) and 0 or margin,
                widget = wibox.container.margin
            },
            layout = wibox.layout.fixed.horizontal
        },
        bg = color,
        shape = function(cr, width, height) gears.shape.rounded_rect(cr, width, height, 8) end,
        widget = wibox.container.background
    }

    if not (not onHover) then
        button:connect_signal("mouse::enter", function()
            onHover(button)
        end)
    end

    if not (not onClick) then
        button:connect_signal("button::press", function()
            onClick(button)
        end)
    end

    if not (not onInit) then
        onInit(button)
    end

    return button
end

function self:update(args)
    if type(args.text) == 'string' then
        self:get_children_by_id('text')[1]:update(args.text)
    end

    if type(args.icon) == 'string' then
        self:get_children_by_id('icon')[1]:set_image(args.icon)
    end
end

return setmetatable(self, {
    __call = self.new,
})
