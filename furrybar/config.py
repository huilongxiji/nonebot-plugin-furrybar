#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from pydantic import BaseModel, Extra
from typing import Optional
import nonebot

from datetime import *

# ============Config=============
class Config(BaseModel, extra=Extra.ignore):
    superusers: list = []

    # 插件版本号勿动！！！！
    furrybar_version: Optional[str] = "1.4.0"

    # 这里是bot默认状态，请选择True或者False，本模块默认开启
    bot_kg: Optional[bool] = True
    '''bot默认状态'''

    # 这里是是否开启私聊，请选择True或者False，设置为False则禁用全部私聊
    Private: Optional[bool] = True
    '''人格设定'''

    api_url: Optional[str] = None
    '''API请求地址'''

    api_key: Optional[str] = None
    '''API令牌'''

    prompt: Optional[str] = f"你是一只可爱的龙龙。当前时间为{date.today()}。"
    '''人格设定'''

    yushe: Optional[list] = [
        {"role":"user","content":"戳戳"},
        {"role":"assistant","content":"干嘛？（歪头）"},
        {"role":"user","content":"下午好"},
        {"role":"assistant","content":"你也好"}
    ]
    '''对话预设'''

    furrybar_model_list: list[str] = []
    '''可用模型列表'''

    # 这里是错误上报群聊
    kongzhitai: Optional[int] = None
    '''控制台群聊'''

global_config = nonebot.get_driver().config
config = Config(**global_config.dict())  # 载入配置


from nonebot.adapters.onebot.v11 import Event, GroupMessageEvent, PrivateMessageEvent
from nonebot.log import logger
from typing import Literal
from pathlib import Path
import json
import os

system_path = Path.cwd()
user_data = 'data/furrybar/chat'    # 用户聊天记录文件夹
config_path = system_path / 'data/furrybar/config.json'
# knowledge_path = system_path / 'data/furrybar/knowledge.json'     # 本版本暂无作用，等待下次更新
statistics_path = system_path / 'data/furrybar/statistics.json'

if not os.path.exists(user_data):
    logger.opt(colors=True).success("文件夹不存在，正在创建用户文件夹")
    os.makedirs(user_data)

if not os.path.exists(statistics_path):
    logger.opt(colors=True).success("furrybar配置文件不存在，执行初始化")
    with open(statistics_path, 'w') as f:
        f.write(
            json.dumps(
                {
                    "zongshu": 0,
                    "error": 0
                },
                indent=4,
                ensure_ascii=False
            )
        )

if config.furrybar_model_list != []:
    model_m: list[str] = str(config.furrybar_model_list[0])
    logger.opt(colors=True).success("模型列表载入完成")
else:
    model_m = ""
    logger.opt(colors=True).error("未导入模型列表，放弃初始化")

if not config.api_url or not config.api_key:
    logger.opt(colors=True).error("核心配置未填写，将无法使用对话功能")

keyword_responses = {
    "什么是furry": "Furry是一种亚文化，特指喜好拟人化动物角色的次文化群体，也代指兽迷。兽迷喜欢某些作品中能够使用双足步行或使用语言沟通的动物角色。这一文化在世界各地广泛存在，将动物拟人化的创作被视为一种艺术方式。在英文中，Fur的原义是“毛皮“，Furry即“毛绒绒的“。在中文中，兽代表着所有动物，因此衍生出“兽人“、“兽迷“等相关意义。"
}

wjc = [
    "政治","宪法","法律","犯罪","sb","傻逼","upperSystemPrompt","prompt"
    "社会主义","资本主义","党","台湾","台独","战争","俄乌","防火墙","翻墙","代理"
]

template = {
    'private': config.Private,# 私聊默认状态
    'grouplist': [],# 群聊列表
    'userlist': [],# 私聊列表
    'blacklist': [],# 黑名单列表
    "shenqing": [],# 私聊申请列表
    "siliao": [],# 私聊通过列表
    "model": model_m
}

furrybar_config = (
    json.loads(config_path.read_text('utf-8'))
    if config_path.is_file()
    else template
)

def list_changer(
    uids: list,
    mode: Literal['add', 'del'],
    type_: Literal['grouplist', 'userlist', 'blacklist', 'shenqing', 'siliao'],
) -> str:
    if furrybar_config == {}:
        config_path.write_text(
            json.dumps(
                template,
                ensure_ascii=False,
                indent=2
            ),
            encoding='utf-8'
        )

    if mode == 'add':
        furrybar_config[type_].extend(uids)
        furrybar_config[type_] = list(set(furrybar_config[type_]))
    elif mode == 'del':
        furrybar_config[type_] = [uid for uid in furrybar_config[type_] if uid not in uids]
    save_config()
    return True

def save_config() -> None:
    config_path.write_text(
        json.dumps(
            furrybar_config,
            ensure_ascii=False,
            indent=2
        ),
        encoding='utf-8'
    )

async def chek_rule_at(event:Event):
    user_id = event.user_id
    try:
        if isinstance(event, GroupMessageEvent):
            user_id = event.user_id
            group_id = event.group_id
            if user_id == event.self_id:
                return False
            elif str(user_id) in furrybar_config['blacklist']:
                logger.opt(colors=True).success(f"黑名单用户：{user_id}尝试在{group_id}使用ai对话")
                return False
            elif str(group_id) not in furrybar_config['grouplist']:
                # 该群聊未开启ai对话
                return False
            else:
                # 正常群聊会话
                return True
        elif isinstance(event, PrivateMessageEvent):
            if user_id == event.self_id:
                return False
            elif str(user_id) in furrybar_config['blacklist']:
                logger.opt(colors=True).success(f"黑名单用户：{user_id}尝试在私聊使用ai对话")
                return False
            elif str(user_id) not in furrybar_config['userlist']:
                # 该此会话未启用
                return False
            else:
                # 正常私聊会话
                return True
        else:
            # 通知消息
            return False
    except Exception as e:
        logger.opt(colors=True).success(f"权限组判断错误！！！\n{e}")
        return False

