# .sdks

Installs all SDK that I use on a daily basis

## Add new SDK

To add a new tool, just create a new `.sdk` file and implement the installation behaviour. The `INSTALL` tool loads all these files dynamically, installing them for you.

Note: To install an SDK that is only available after adding a **PPA** to `apt` registry, you first need to add it to `REPOSITORIES` file.

## Install

```bash
./INSTALL
```