# Server Replay Helper

[![MCDR](https://img.shields.io/badge/MCDR-%3E%3D2.0.0--alpha.1-blue)](https://github.com/Fallen-Breath/MCDReforged)
[![License](https://img.shields.io/github/license/Rethink_QAQ/ServerReplayHelper)](LICENSE)

[English](README.md) | [中文](README_CN.md)

一个可以便捷控制 [ServerReplay](https://modrinth.com/mod/server-replay) 模组的 MCDR 插件。 务必搭配 [ServerReplay](https://modrinth.com/mod/server-replay) 模组。

## 命令说明

### 基础命令
```
!!replay              - 显示帮助信息和录制列表
!!replay help         - 显示详细帮助信息
!!replay list         - 显示当前录制列表
```

### 玩家录制
```
!!replay start [玩家名]  - 开始录制指定玩家（默认为自己）
!!replay stop [玩家名]   - 停止录制指定玩家（默认为自己）
```

### 区块录制
```
!!replay chunk start <名称> <半径>  - 开始录制以当前位置为中心的区块
!!replay chunk stop <名称>          - 停止指定名称的区块录制
```

## 安装要求

- MCDReforged >= 2.0.0-alpha.1
- Minecraft Data API 插件
- ServerReplay 模组

## 计划功能

- [ ] 录制文件管理
- [ ] Replay/Flashback 录制识别
- [ ] 更好的录制检测逻辑