-- Themed button widget
-- Original Source: https://github.com/streetturtle/awesome-buttons
-- Status: Modified

local wibox = require("wibox")
local gears = require("gears")

local margin = 4

local self = {}

function self:new(args)
    local color = args.color or '#f88'
    local icon = args.icon
    local text = args.text
    local onHover = args.onHover
    local onClick = args.onClick

    local button = wibox.widget {
        {
            {
                {
                    id = 'icon',
                    image = icon,
                    widget = wibox.widget.imagebox
                },
                margins = not icon and 0 or margin,
                widget = wibox.container.margin
            },
            {
                {
                    id = 'text',
                    markup = text,
                    widget = wibox.widget.textbox
                },
                margins = not text and 0 or margin,
                widget = wibox.container.margin
            },
            layout = wibox.layout.fixed.horizontal
        },
        bg = color,
        shape = function(cr, width, height) gears.shape.rounded_rect(cr, width, height, margin) end,
        widget = wibox.container.background
    }

    if not (not onHover) then
        button:connect_signal("mouse::enter", onHover)
    end

    if not (not onClick) then
        button:connect_signal("button::press", onClick)
    end

    return button
end

function dump(o)
    if type(o) == 'table' then
        local s = '{ '
        for k, v in pairs(o) do
            if type(k) ~= 'number' then k = '"' .. k .. '"' end
            s = s .. '[' .. k .. '] = ' .. dump(v) .. ','
        end
        return s .. '} '
    else
        return tostring(o)
    end
end

function self:update(args)
    print('1111')
    print(args)
    print('2222')
    print(self)
    print('3333')
    print(self.new)

    print('4444')
    if type(args.text) == 'string' then
        self:get_children_by_id('text')[1]:set_markup(args.text)
    end

    if type(args.icon) == 'string' then
        self:get_children_by_id('icon')[1]:set_image(args.icon)
    end
end

return setmetatable(self, {
    __call = self.new,
})
