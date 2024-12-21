<div align="center">
  <a href="https://v2.nonebot.dev/store"><img src="https://github.com/A-kirami/nonebot-plugin-template/blob/resources/nbp_logo.png" width="180" height="180" alt="NoneBotPluginLogo"></a>
  <br>
  <p><img src="https://github.com/A-kirami/nonebot-plugin-template/blob/resources/NoneBotPlugin.svg" width="240" alt="NoneBotPluginText"></p>
</div>

<div align="center">

# nonebot-plugin-furrybar

_✨ furrybar API  对接插件 ✨_

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

本插件使用标准的<a href="https://openai.xiniushu.com/docs/guides/chat"> openai API格式 </a>进行编写，主要为furrybar api进行服务，同时也兼容了所有openai标准的api，方便用户在更加灵活的选择api。安装之后需要填好相应的全局配置项，以保证该模块的正常运行，具体配置填法请见配置板块。
本模块作为bot插件，仅接受学习代码结构以及了解openai标准格式的纯本地构建形式。
若本插件存在bug欢迎各位反馈！！！
目前只支持 onebotV11 暂时还未上传nonebot商店

## 💿 安装

<details open>
<summary>使用PIP安装</summary>
在 nonebot2 项目的插件目录下, 打开命令行, 输入安装命令

```
pip install nonebot-plugin-furrybar
```

打开 nonebot2 项目根目录下的 `pyproject.toml` 文件, 在 `[tool.nonebot]` 部分追加写入

```
plugins = ["nonebot-plugin-furrybar"]
```

</details>

## ⚙️ 配置

在 nonebot2 项目的`.env`文件中添加下表中的配置，不填任何配置则自动使用默认账户

```
# 这里是设置模块默认状态的，可选True或者False
Private = True
# 你的api地址
api_url = "你获得的api地址"
# 你的apikey
api_key = "你获得的token"
# 你的人格设定
prompt = "人格设定"
# 你的对话预设
yushe = [
    {"role":"user","content":"戳戳"},
    {"role":"assistant","content":"干嘛？（歪头）"}
]
# 你的模型列表
furrybar_model_list = ["xxx","xxx"]
# 你的控制台群号（不填则不发送报错至控制台）
kongzhitai = 1234567
```

## 🎉 使用

### 指令表

|      指令      |       权限       |   是否需要参数   |                说明                |
| :-------------: | :--------------: | :---------------: | :--------------------------------: |
|        @        |       群员       |     需要艾特     |        艾特bot直接与ai对话        |
|       /ai       | 超管/群主/管理员 |  后面带on或者off  |     开启或关闭当前群聊的ai对话     |
|      /拉黑      |    超级管理员    | 需要携带对方q账号 |            拉黑对应用户            |
|    /切换模型    |    超级管理员    |  根据id切换模型  | 动态加载模型列表，用来切换当前模型 |
|  /模型调用数据  |    超级管理员    |      不需要      |   查看ai对话调用次数以及故障次数   |
|    /登记信息    |      所有人      |      不需要      |       流程式对话登记用户信息       |
| (开启/关闭)私聊 |     私聊使用     |      不需要      |          开启私聊对话功能          |

## 插件完成度

目前进度:

- [x] 模型切换
- [x] 黑名单功能
- [x] 调用记录
- [x] 个人信息登记（让ai记住你是谁）
- [x] 本地知识库
- [ ] bot默认状态设置
- [ ] 分别查询用户使用热度
- [ ] 用户对话词云
- [ ] 自由切换api和key来适配多api情况

