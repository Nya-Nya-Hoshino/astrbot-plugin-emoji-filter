## AstrBot 插件开发规范

### 项目结构
- 插件目录名使用 strbot_plugin_ 前缀，全小写，用下划线分隔
- 入口文件必须为 main.py，主类继承 Star
- 必须有 metadata.yaml（插件元信息）和 _conf_schema.json（配置项）

### 核心架构
- **AstrBot**: 开源 Agent 聊天机器人平台，插件系统基于 Star 基类
- **NapCatQQ**: NTQQ Bot 协议端，实现 OneBot v11 协议
- **aiocqhttp**: OneBot 协议的 Python async SDK，AstrBot 通过它对接 QQ
- 消息流程：QQ > NapCatQQ (OneBot v11 ws) > aiocqhttp > AstrBot > 插件处理 > 反向链路回复

### 插件 API 速查

#### 注册处理函数
- 指令注册: @filter.command("name")、@filter.regex(r"...")
- 事件钩子: @filter.on_decorating_result()、@filter.on_llm_request() 等
- LLM工具: @filter.llm_tool("name")

#### 消息组件 (MessageComponents)
- Plain 纯文本、Image 图片、At @提及、Record 语音
- Video 视频、File 文件、Reply 回复引用
- Node/Nodes 转发消息节点

#### 消息发送模式
- yield event.plain_result("text") — 纯文本
- yield event.image_result("url") — 图片
- event.make_result() — 组装 MessageChain 后统一发送

#### 常用信息获取
- 发送者: event.get_sender_name()、event.get_sender_id()
- 群组: event.get_group_id()、event.message_obj.group_id
- 纯文本: event.message_str
- 消息链: event.get_messages()
- 统一会话: event.unified_msg_origin (umo)

#### Context 核心能力
- LLM调用: self.context.llm_generate()
- 数据库: self.context.get_db()
- 配置: self.context.get_config()
- 平台实例: self.context.get_platform(PlatformAdapterType.AIOCQHTTP)
- 人格: self.context.persona_manager

### 编码规范
- Python 3.10+，UTF-8 编码
- 异步函数使用 sync/await
- 日志使用 rom astrbot.api import logger
- 配置 schema 类型: bool, int, float, string
