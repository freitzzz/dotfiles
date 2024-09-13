local terminal = "x-terminal-emulator"

return {
    terminal = terminal,
    editor_cmd = terminal .. " -e " .. (os.getenv("EDITOR") or "editor"),
    home_path = os.getenv("HOME")
}
