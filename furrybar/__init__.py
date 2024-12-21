from .config import *
from .chat import *
from .furrybar import *

from nonebot.permission import SUPERUSER
from nonebot.plugin import on_command

on_group = on_command('/ai on', permission=SUPERUSER|GROUP_ADMIN|GROUP_OWNER, priority=3, block=True)

@on_group.handle()
async def add_group_(event: GroupMessageEvent):
    if f'{event.group_id}' not in furrybar_config['grouplist']:
        list_changer([f'{event.group_id}'], 'add', 'grouplist')
        await on_group.finish("chat启用成功")
    await on_group.finish("请勿重复启用")

off_group = on_command('/ai off', permission=SUPERUSER|GROUP_ADMIN|GROUP_OWNER, priority=3, block=True)

@off_group.handle()
async def del_group_(event: GroupMessageEvent):
    if f'{event.group_id}' in furrybar_config['grouplist']:
        list_changer([f'{event.group_id}'], 'del', 'grouplist')
        await off_group.finish('已关闭本群回复')
    await off_group.finish('请勿重复关闭')


on_user = on_command('开启私聊', priority=3, block=True)

@on_user.handle()
async def add_user_(bot: Bot, event: PrivateMessageEvent):
    user_id = str(event.user_id)
    userlist = furrybar_config['userlist']
    blacklist = furrybar_config['blacklist']
    siliao = furrybar_config['siliao']
    shenqing = furrybar_config['shenqing']
    if user_id in blacklist:
        await on_user.finish()
    elif user_id not in shenqing:
        list_changer([f'{user_id}'], 'add', 'shenqing')
        await bot.send_group_msg(group_id=config.kongzhitai,message=f"接收到用户申请ai私聊对话\nQQ:{user_id}\n状态: 正常模式",auto_escape=False)
        await on_user.finish("私聊权限申请已发送至主人w")
    elif user_id not in siliao and user_id in shenqing:
        await on_user.finish("你已经提交过申请w")
    elif user_id not in userlist:
        list_changer([f'{user_id}'], 'add', 'userlist')
        await chat_shauxin(user_id)
        await on_user.finish("来咯来咯~唤我何事？（微微抬头看向对方）")
    else:
        await on_user.finish("干嘛干嘛？？我这不是在这里嘛！！！")


off_user = on_command('关闭私聊', priority=3, block=True)

@off_user.handle()
async def del_user_(event: PrivateMessageEvent):
    user_id = str(event.user_id)
    userlist = furrybar_config['userlist']
    blacklist = furrybar_config['blacklist']
    siliao = furrybar_config['siliao']
    shenqing = furrybar_config['shenqing']
    if user_id in blacklist:
        await off_user.finish()
    elif user_id in userlist:
        list_changer([f'{user_id}'], 'del', 'userlist')
        await chat_shauxin(user_id)
        await off_user.finish('好叭，那我退下了')
    elif user_id not in userlist and user_id in siliao:
        await off_user.finish('(ps: 龙已经走了)')
    elif user_id in shenqing:
        await off_group.finish("请耐心等待审核w")
    else:
        await off_user.finish()


userlist_sq = on_command('同意私聊申请', permission=SUPERUSER, priority=10, block=True)

@userlist_sq.handle()
async def userlist_sq_(bot: Bot, args: Message = CommandArg()):
    if str(args) in furrybar_config['siliao']:
        await userlist_sq.finish("该用户已经存在于通过列表")
    elif str(args) in furrybar_config['shenqing']:
        list_changer([f'{args}'], 'add', 'siliao')
        await bot.send_private_msg(user_id=int(str(args)),message="你的私聊申请已通过\n你可以使用以下指令\n（开启/关闭）私聊",auto_escape=False)
        await userlist_sq.finish(f'用户{args}申请同意成功')
    else:
        await userlist_sq.finish('操作失败')

# 检查更新
def check_update():
    new_verision, time = update_syj()
    if not new_verision and not time:
        logger.error(f"furrybar:无法获取最新的版本，当前版本为{config.furrybar_version}，可能已经过时！")
    else:
        if new_verision <= config.furrybar_version:
            logger.success(f"furrybar:当前版本为{config.furrybar_version},仓库版本为{new_verision}")
        else:
            logger.success("furrybar:检查到本插件有新版本！")
            venv = os.getcwd()
            if os.path.exists(f"{venv}/.venv"):
                logger.success("正在自动更新中--找到虚拟环境![开始安装]")
                os.system(f'"{venv}/.venv/Scripts/python.exe" -m pip install nonebot-plugin-furrybar=={new_verision} -i https://pypi.Python.org/simple/')
                logger.success(f"furrybar:更新完成！最新版本为{new_verision}|当前使用版本为{config.furrybar_version}")
                logger.warning(f"furrybar:你可能需要重新启动nonebot来完成插件的重载")
            else:
                logger.warning("正在自动更新中--未找到虚拟环境！[安装在本地环境]")
                os.system(f'pip install nonebot-plugin-furrybar=={new_verision} -i https://pypi.Python.org/simple/')
                logger.success(f"furrybar:更新完成！最新版本为{new_verision}|当前使用版本为{config.furrybar_version}")
                logger.warning(f"furrybar:你可能需要重新启动nonebot来完成插件的重载")

#update-----syj
def update_syj():
    fails = 0
    while True:
        try:
            if fails >= 20:
                verision = False
                time = False
                break
            headers = {'content-type': 'application/json'}
            get_json = httpx.get(url="https://pypi.org/pypi/nonebot-plugin-furrybar/json", headers=headers ,timeout=50)
            if get_json.status_code == 200:
                json = get_json.json()
                verision = json["info"]["version"]
                time = json["releases"][f"{verision}"][0]["upload_time"]
            else:
                continue
        except:
            fails += 1
            logger.warning("网络状况不佳，检查最新版本失败，正在重新尝试")
        else:
            break
    return verision,time


try:
    check_update()
except Exception as e:
    logger.opt(colors=True).error(f"检测更新失败！！{e}")


