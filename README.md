# Server Replay Helper

[![MCDR](https://img.shields.io/badge/MCDR-%3E%3D2.0.0--alpha.1-blue)](https://github.com/Fallen-Breath/MCDReforged)
[![License](https://img.shields.io/github/license/Rethink_QAQ/ServerReplayHelper)](LICENSE)

[English](README_EN.md) | [中文](README_CN.md)

An MCDR plugin that can easily control the [ServerReplay](https://modrinth.com/mod/server-replay) mod. Must be used with the [ServerReplay](https://modrinth.com/mod/server-replay) mod.

## Command Reference

### Basic Commands
```
!!replay              - Display help message and recording list
!!replay help         - Display detailed help information
!!replay list         - Display current recording list
```

### Player Recording
```
!!replay start [player]  - Start recording specified player (default to self)
!!replay stop [player]   - Stop recording specified player (default to self)
```

### Chunk Recording
```
!!replay chunk start <name> <radius>  - Start recording chunks centered at current position
!!replay chunk stop <name>            - Stop chunk recording with specified name
```

## Requirements

- MCDReforged >= 2.0.0-alpha.1
- Minecraft Data API plugin
- ServerReplay mod

## Roadmap

- [ ] Recording file management
- [ ] Replay/Flashback recording identification
- [ ] Better recording detection logic