# .drivers

Installs all drivers that are required for my distro to work.

## Add new driver

To add a new driver config, just create a new `.driver` file and implement the installation behaviour. The `INSTALL` tool loads all these files dynamically, installing them for you.

Note: To install a driver that is only available after adding a **PPA** to `apt` registry, you first need to add it to `REPOSITORIES` file.

## Install

```bash
./INSTALL
```