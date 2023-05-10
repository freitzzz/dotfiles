# .tools

Installs all tools that I use on a daily basis

## Add new tool

To add new tool, just create a new `.tool` file and implement the instalation behaviour. The `INSTALL` tool loads all these files dynamically, installing them for you.

Note: To install a tool that is only available after adding a **PPA** to `apt` registry, you need to first add it on `REPOSITORIES` file.

## Install

```bash
./INSTALL
```