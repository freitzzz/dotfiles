local naughty = require 'naughty'
local theme = require 'theme'

---@alias NotificationPosition "top_right" | "top_left" | "bottom_left" | "bottom_right" | "top_middle" | "bottom_middle"
---@alias Notification {id: string, text: string, fontSize: integer, timeout: number, size: number, center: boolean, position: NotificationPosition}

---@type [string]table
--- Global map of notifications that are indexable by an ID.
local global_notifications = {}

---Shows a notification.
---@param args Notification
local function show(args)
    if args.id and global_notifications[args.id] then
        naughty.destroy(global_notifications[args.id], naughty.notificationClosedReason.dismissedByCommand, false)
    end

    local notification = naughty.notify {
        text = args.text,
        font = args.fontSize and string.format("%s %i", theme.notification_font, args.fontSize),
        timeout = args.timeout or 3,
        height = args.size,
        width = args.size,
        margin = (args.center and args.size and args.fontSize) and ((args.size / 2) - (args.fontSize / 2)),
        position = args.position,
    }

    if args.id then
        global_notifications[args.id] = notification
    end
end

return {
    show = show
}
