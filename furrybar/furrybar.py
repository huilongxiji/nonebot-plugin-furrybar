from nonebot.adapters.onebot.v11 import Bot,MessageEvent,MessageSegment
from nonebot.params import ArgPlainText
from nonebot.permission import SUPERUSER
from nonebot.plugin import on_command
from nonebot.params import CommandArg
from nonebot.adapters import Message
from nonebot.matcher import Matcher
from nonebot.typing import T_State
from nonebot.rule import Rule
from .config import *
import aiofiles

chat_caidan = on_command("菜单", aliases={"help"}, rule=Rule(chek_rule_at), priority=10, block=True)
model_updata = on_command("/切换模型", permission=SUPERUSER, priority=3, block=True)
black_user_add = on_command("/拉黑", permission=SUPERUSER, priority=3, block=True)
chat_statistics = on_command("/模型调用数据", permission=SUPERUSER, priority=3, block=True)
gerenxinxi = on_command("/登记信息", permission=SUPERUSER, priority=3, block=True)

help = '''
“@bot+内容”（与ai对话）
“/ai (on/off)”（对话开关）
“/拉黑+QQ号”（拉黑用户）
“/切换模型”（更换模型）
“/模型调用数据”（查看调用记录）
“/登记信息”（上传设定介绍，让煌秋记住你）
*私聊可以发送“(开启|关闭)私聊”
*（小提示：私聊第一次发送开启需要等待开发者审核）
'''

@chat_caidan.handle()
async def furbar_chat_caidan(event: MessageEvent, args: Message = CommandArg()):
    if args.extract_plain_text(): await chat_caidan.finish()
    await chat_caidan.finish(
        MessageSegment.reply(event.message_id) + help.strip())

@model_updata.handle()
async def furbar_model_updata(args: Message = CommandArg()):
    id = str(args)
    if not id:
        if config.furrybar_model_list == []:
            await model_updata.finish("未找到可用列表")
        text = ""
        for i in range(len(config.furrybar_model_list)):
            name = config.furrybar_model_list[i]
            text += f"{i}、{name}\n"
        await model_updata.finish("模型列表如下:\n"+text+f"(ps:默认使用{config.furrybar_model_list[0]}即可, 非特殊需求请勿切换模型)")
    elif int(id) > (len(config.furrybar_model_list) - 1):
        await model_updata.finish("该序号不存在")
    else:
        id = int(id)
        furrybar_config['model'] = config.furrybar_model_list[id]
        save_config()
        await model_updata.finish(f"模型已切换为{config.furrybar_model_list[id]}")

@black_user_add.handle()
async def furbar_black_user_add(args: Message = CommandArg()):
    user_id = str(args)
    if user_id in furrybar_config['blacklist']:
        await black_user_add.finish("该用户已经在黑名单里面了")
    else:
        list_changer([f'{user_id}'], 'add', 'blacklist')
        await black_user_add.finish(f"用户{user_id}拉黑成功")

@chat_statistics.handle()
async def furbar_chat_statistics(args: Message = CommandArg()):
    if not args:
        with open(statistics_path, 'r', encoding="utf-8") as mun:
            mun_data = json.load(mun)
            mun.close()
    data = f'''当前模型：{furrybar_config['model']}
总调用次数：{mun_data['zongshu']}
异常次数：{mun_data['error']}
拉黑用户：{len(furrybar_config['blacklist'])}'''
    await black_user_add.finish(data)

@gerenxinxi.handle()
async def furbar_gerenxinxi(event: MessageEvent, matcher: Matcher, args: Message = CommandArg()):
    if args.extract_plain_text(): await matcher.finish()
    await matcher.send(
        MessageSegment.reply(event.message_id) + "请发送要登记的名称:\n任何阶段都可以发“退出”来结束"
    )
    matcher.set_arg("keys", args)

@gerenxinxi.got("key")
async def furbar_gerenxinxi_got(state: T_State, event: MessageEvent, matcher: Matcher, key: str = ArgPlainText("key")):
    qq = event.user_id
    tg_code = state.get("tg_code", 0)
    if not key:
        tg_try = state.get("tg_try", 1)
        if tg_try >= 5:
            await matcher.finish("输入错误次数过多，进程结束")
        else:
            state["tg_try"] = tg_try + 1
            await matcher.reject("请携带参数发送哦")
    else:
        if key == "退出":
            await matcher.finish("退出登记模式")
        elif tg_code == 0:
            state["姓名"] = key
            state["tg_code"] = 1
            await matcher.reject(
                MessageSegment.reply(event.message_id) + 
                "请发送别名：\n(没有请发“无”)")
        elif tg_code == 1:
            if key == "" or key == "无":
                state["别名"] = ""
            else:
                state["别名"] = key
            state["tg_code"] = 2
            await matcher.reject(
                MessageSegment.reply(event.message_id) + 
                "请选择性别：\n[雌/雄/中性/未知]")
        elif tg_code == 2:
            if key not in ["雌","雄","中性","未知"]:
                tg_xb = state.get("tg_xb", 1)
                if tg_xb >= 5:
                    await matcher.finish("输入错误次数过多，进程结束")
                else:
                    state["tg_xb"] = tg_xb + 1
                    await matcher.reject(
                MessageSegment.reply(event.message_id) + 
                "请从列表中选择w\n特殊情况可联系开发者修改")
            else:
                state["性别"] = key
                state["tg_code"] = 3
                await matcher.reject(
                MessageSegment.reply(event.message_id) + 
                "请输入年龄：")
        elif tg_code == 3:
            state["年龄"] = key
            state["tg_code"] = 4
            await matcher.reject(
                MessageSegment.reply(event.message_id) + 
                "请输入种族：")
        elif tg_code == 4:
            state["种族"] = key
            state["tg_code"] = 5
            await matcher.reject(
                MessageSegment.reply(event.message_id) + 
                "请输入一段设定外貌描写：")
        elif tg_code == 5:
            state["外貌"] = key
            state["tg_code"] = 6
            await matcher.reject(
                MessageSegment.reply(event.message_id) + 
                "请输入一段个人介绍：")
        elif tg_code == 6:
            state["个人介绍"] = key
            state["tg_code"] = 7
            text = f"设定名称:{state['姓名']}\n别名:{state['别名']}\n性别:{state['性别']}\n年龄:{state['年龄']}\n种族:{state['种族']}\n外貌:{state['外貌']}\n个人介绍:{state['个人介绍']}\n\n"
            await matcher.reject(
                MessageSegment.reply(event.message_id) + 
                text + "请检查登记信息是否无误[确认/退出]")
        elif tg_code == 7:
            if key != "确认":
                tg_qr = state.get("tg_qr", 1)
                if tg_qr >= 5:
                    await matcher.finish("输入错误次数过多，进程结束")
                else:
                    state["tg_qr"] = tg_qr + 1
                    await matcher.reject("只能输入“确认”或者“退出”")
            else:
                async with aiofiles.open(Path.cwd() / f'data/furrybar/user/{qq}.json', 'w', encoding='utf-8') as f:
                    await f.write(
                        {
                            "姓名": state['姓名'],
                            "别名": state['别名'],
                            "性别": state['性别'],
                            "年龄": state['年龄'],
                            "种族":  state['种族'],
                            "与自己的关系": "朋友",
                            "外貌": state['外貌'],
                            "个人介绍": state['个人介绍']
                        })
                    await f.close()
                await matcher.finish("登记已完成")
        else:
            await matcher.finish("运行错误")

'''{
    "姓名": "绿茶龙·筱翯",
    "别名": [
        "绿茶龙",
        "绿龙"
    ],
    "性别": "男（公）",
    "年龄": 16,
    "种族": "羽化鳞龙",
    "与自己的关系": "绿龙是煌秋的主人",
    "外貌": "绿龙拥有着一身亮丽的绿色毛发，小腿毛色为紫色，有三圈白色花纹，手臂为淡蓝色，手爪为纯白。绿龙拥有一双巨大的纯白色翅膀，以及那标志性的冰蓝色双瞳。",
    "个人介绍": "绿龙是一只拥有掌控风与光元素的羽化鳞龙，有着修长的身体长长的尾巴，纯白的羽翼以及没有肉垫但却强壮有力的手爪，绿龙是一只实验体，最擅长的是敏捷的战斗。"
}'''