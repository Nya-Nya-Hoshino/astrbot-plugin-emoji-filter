# astrbot-plugin-emoji-filter

[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![AstrBot](https://img.shields.io/badge/AstrBot-plugin-6c5ce7.svg)](https://github.com/AstrBotDevs/AstrBot)

AstrBot 插件 —— 在机器人发送消息前，通过 Unicode 正则匹配并移除所有 emoji 表情字符。

## 功能

- 拦截机器人发出的每条消息，过滤 Plain 文本中的 emoji 字符
- 覆盖 Unicode emoji 全部主要码块（表情、符号、国旗、变体选择器、零宽连接符等）
- 非文本组件（图片、@、回复引用等）不受影响
- WebUI 一键开关

## 安装

`ash
# 进入 AstrBot 插件目录
cd ~/.astrbot/data/plugins

# 克隆插件
git clone https://github.com/liu2006jw-source/astrbot-plugin-emoji-filter.git emoji_filter

# 重启 AstrBot
`

## 配置

重启后在 WebUI **插件管理** → emoji_filter 中可看到开关：

| 配置项 | 类型 | 默认值 | 说明 |
|---|---|---|---|
| emoji_filter_enabled | bool | 	rue | 是否启用 emoji 过滤 |

## 覆盖的 emoji 范围

| 码点范围 | 说明 |
|---|---|
| U+1F600-U+1F64F | 表情符号 (Emoticons) |
| U+1F300-U+1F5FF | 杂项符号与图形 |
| U+1F680-U+1F6FF | 交通与地图符号 |
| U+1F1E0-U+1F1FF | 国旗 (Regional Indicators) |
| U+2702-U+27B0 | Dingbats |
| U+1F900-U+1F9FF | 补充符号与图形 |
| U+2600-U+26FF | 杂项符号 |
| U+FE00-U+FE0F | 变体选择器 (VS1-VS16) |
| U+200D | 零宽连接符 (ZWJ) |
| +30+ 零散 emoji | ⭐⭕▶〰㊗ 等 |

## 效果示例

`
输入:  Hello 😀 World 🌍!
输出:  Hello  World !

输入:  混合😀中文🎉测试
输出:  混合中文测试

输入:  你好啊👋
输出:  你好啊
`

## 许可证

MIT License