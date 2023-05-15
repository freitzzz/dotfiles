# .vpn

Configures all VPN tools and related topics.

## Add new VPN config

To add a new VPN config, just create a new `.vpn` file and implement the configuration behaviour. The `INSTALL` tool loads all these files dynamically, installing them for you.

Note: To install a config that is only available after adding a **PPA** to `apt` registry, you first need to add it to `REPOSITORIES` file.

## Install

```bash
./INSTALL
```