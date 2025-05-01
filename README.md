<div align="center">
  <a href="https://v2.nonebot.dev/store"><img src="https://github.com/A-kirami/nonebot-plugin-template/blob/resources/nbp_logo.png" width="180" height="180" alt="NoneBotPluginLogo"></a>
  <br>
  <p><img src="https://github.com/A-kirami/nonebot-plugin-template/blob/resources/NoneBotPlugin.svg" width="240" alt="NoneBotPluginText"></p>
</div>

<div align="center">

# 针对deepseek优化的单文件版nonebot插件

_✨ deepseek 官方API  优化版对接插件 ✨_

</a>
<a href="https://github.com/huilongxiji/nonebot-plugin-furrybar/blob/main/LICENSE">
    <img src="https://img.shields.io/github/license/huilongxiji/nonebot-plugin-furrybar.svg" alt="license">
</a>
<a href="https://pypi.python.org/pypi/nonebot-plugin-furrybar">
    <img src="https://img.shields.io/pypi/v/nonebot-plugin-furrybar.svg" alt="pypi">
</a>
<img src="https://img.shields.io/badge/python-3.9+-blue.svg" alt="python">

</div>

基于NoneBot2进行适配的ai对话聊天插件，适合做赛博龙龙……？

## 📖 介绍

本插件使用标准的<a href="https://openai.xiniushu.com/docs/guides/chat"> openai API格式 </a>进行编写，针对deepseek的guanfangapi进行了特殊优化，更加稳定的调用DS官方的api，暂不支持兼容新版fb的api。安装之后需要填好相应的全局配置项，以保证该模块的正常运行，具体配置填法请见配置板块。

本模块作为bot插件，仅接受学习代码结构以及了解openai标准格式的对接形式。
若本插件存在bug欢迎各位反馈！！！
目前只支持 onebotV11 暂时还未上传nonebot商店

## 💿 安装

本分支不上传pypi，仅作为特殊需求使用，仅支持手动下载或直接拉取本仓库使用

## ⚙️ 配置

在 nonebot2 项目的`.env`文件中添加下表中的配置，不填任何配置无法正常使用

```
bot_kg = False
'''设置 bot 的默认状态， True 为开启 False 为关闭'''

private = False
'''设置私聊开启默认状态， True 为开启 False 为关闭'''

data_path = "D:/qqbot/ai_deepseek"
'''自定义数据存储路径'''

kongzhitai = 123456789
'''设置控制台群聊，负责接收错误上报'''

chat_model = "deepseek-chat"
'''设置默认模型，此处请根据使用 API 来填写'''

api_url = "https://api.deepseek.com"
'''设置 API 服务商的域名地址，默认为 deepseek '''

api_key = sk-xxxxxxxxxxxxxxxxx
'''设置你的 API 令牌'''

chat_prompt = 你是一只猫娘
'''BOT的人格设定'''

yushe = [
    {"role": "user", "content": "戳戳"},
    {"role": "assistant", "content": "干嘛uwu~"},
    {"role": "user", "content": "你好呀"},
    {"role": "assistant", "content": "乃好哦ww"}
]
'''BOT的对话风格预设'''
```

## 🎉 使用

### 指令表

| 指令 |       权限       |   是否需要参数   |            说明            |
| :---: | :--------------: | :---------------: | :------------------------: |
|   @   |       群员       |     需要艾特     |    艾特bot直接与ai对话    |
|  /ai  | 超管/群主/管理员 |  后面带on或者off  | 开启或关闭当前群聊的ai对话 |
| /拉黑 |    超级管理员    | 需要携带对方q账号 |        拉黑对应用户        |
| /账户余额查询 |    超级管理员    |     否     |        调用deepseek的余额擦查询        |

## 插件完成度

目前进度:

- [x] bot默认状态设置
- [x] 黑名单功能
- [x] 本地知识库
- [ ] 个人信息登记（让ai记住你是谁）
- [ ] 切换模型
- [ ] 分别查询用户使用热度
- [ ] 用户对话词云
- [ ] 自由切换api和key来适配多api情况

