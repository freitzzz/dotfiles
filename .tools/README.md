# .tools

Installs all tools that I use on a daily basis

## Add new tool

To add a new tool, just create a new `.tool` file and implement the installation behaviour. The `INSTALL` tool loads all these files dynamically, installing them for you.

Note: To install a tool that is only available after adding a **PPA** to `apt` registry, you first need to add it to `REPOSITORIES` file.

## Install

```bash
./INSTALL
```