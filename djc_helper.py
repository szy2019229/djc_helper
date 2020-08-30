import platform

import pyperclip

import json_parser
from dao import *
from network import *


# 道聚城自动化助手
class DjcHelper:
    def __init__(self, config_path="config.toml", local_config_path="config.toml.local"):
        # 读取配置信息
        load_config(config_path, local_config_path)
        self.cfg = config()

        # 初始化网络相关设置
        self.network = Network(self.cfg.sDeviceID, self.cfg.account_info.uin, self.cfg.account_info.skey)

        # 余额
        self.balance = "https://djcapp.game.qq.com/cgi-bin/daoju/djcapp/v5/solo/jfcloud_flow.cgi?&appVersion={appVersion}&p_tk={p_tk}&sDeviceID={sDeviceID}&weexVersion=0.9.4&platform=android&deviceModel=MIX%202&&method=balance&page=0&osVersion=Android-28&ch=10003&sVersionName=v4.1.6.0&appSource=android"
        self.money_flow = "https://djcapp.game.qq.com/daoju/igw/main/?_service=app.bean.water&appVersion={appVersion}&p_tk={p_tk}&sDeviceID={sDeviceID}&sDjcSign={sDjcSign}&&weexVersion=0.9.4&platform=android&deviceModel=MIX%202&page=1&starttime={starttime}&endtime={endtime}&osVersion=Android-28&ch=10003&sVersionName=v4.1.6.0&appSource=android"

        # 每日登录事件：imsdk登录
        self.imsdk_login = "https://djcapp.game.qq.com/daoju/igw/main/?_service=app.message.imsdk.login&appVersion={appVersion}&p_tk={p_tk}&sDeviceID={sDeviceID}&sDjcSign={sDjcSign}&osVersion=Android-28&ch=10003&sVersionName=v4.1.6.0&appSource=android"
        # 每日登录事件：app登录
        self.user_login_event = "https://djcapp.game.qq.com/daoju/igw/main/?_service=app.login.user.first&appVersion={appVersion}&p_tk={p_tk}&sDeviceID={sDeviceID}&sDjcSign={sDjcSign}&osVersion=Android-28&ch=10003&sVersionName=v4.1.6.0&appSource=android"

        # 每日签到的奖励规则
        self.sign_reward_rule = "https://djcapp.game.qq.com/daoju/igw/main/?_service=app.reward.sign.rule&appVersion={appVersion}&p_tk={p_tk}&sDeviceID={sDeviceID}&sDjcSign={sDjcSign}&output_format=json&&weexVersion=0.9.4&platform=android&deviceModel=MIX%202&&osVersion=Android-28&ch=10003&sVersionName=v4.1.6.0&appSource=android"
        # 签到相关接口的入口
        self.sign = "https://comm.ams.game.qq.com/ams/ame/amesvr?ameVersion=0.3&appVersion={appVersion}&p_tk={p_tk}&sDeviceID={sDeviceID}&sServiceType=dj&iActivityId=11117&sServiceDepartment=djc&set_info=newterminals&&weexVersion=0.9.4&platform=android&deviceModel=MIX%202&&appSource=android&ch=10003&osVersion=Android-28&sVersionName=v4.1.6.0"
        self.sign_raw_data = "appVersion={appVersion}&g_tk={g_tk}&iFlowId={iFlowId}&month={month}&p_tk={p_tk}&sDeviceID={sDeviceID}&sDjcSign={sDjcSign}&sign_version=1.0&ch=10003&iActivityId=11117&osVersion=Android-28&sVersionName=v4.1.6.0&sServiceDepartment=djc&sServiceType=dj&appSource=android"

        # 任务列表
        self.usertask = "https://djcapp.game.qq.com/daoju/v3/api/we/usertaskv2/Usertask.php?iAppId=1001&appVersion={appVersion}&p_tk={p_tk}&sDeviceID={sDeviceID}&_app_id=1001&output_format=json&_output_fmt=json&appid=1001&optype=get_usertask_list&osVersion=Android-28&ch=10003&sVersionName=v4.1.6.0&appSource=android"
        # 领取任务奖励
        self.take_task_reward = "https://djcapp.game.qq.com/daoju/v3/api/we/usertaskv2/Usertask.php?iAppId=1001&appVersion={appVersion}&iruleId={iruleId}&p_tk={p_tk}&sDeviceID={sDeviceID}&_app_id=1001&output_format=json&_output_fmt=json&appid=1001&optype=receive_usertask&osVersion=Android-28&ch=10003&sVersionName=v4.1.6.0&appSource=android"
        # 上报任务完成
        self.task_report = "https://djcapp.game.qq.com/daoju/igw/main/?_service=app.task.report&appVersion={appVersion}&task_type={task_type}&p_tk={p_tk}&sDeviceID={sDeviceID}&sDjcSign={sDjcSign}&&weexVersion=0.9.4&platform=android&deviceModel=MIX%202&osVersion=Android-28&ch=10003&sVersionName=v4.1.6.0&appSource=android"

        # 获取dnf角色列表
        self.get_dnf_role_list = "https://comm.aci.game.qq.com/main?sCloudApiName=ams.gameattr.role&appVersion={appVersion}&area={area}&callback={callback}&p_tk={p_tk}&sDeviceID={sDeviceID}&&game=dnf&sAMSAcctype=pt&&osVersion=Android-28&ch=10003&sVersionName=v4.1.6.0&appSource=android"
        # 获取剑网三指尖江湖角色列表（用于获取领取手游奖励的角色信息）
        self.get_jx3_role_list = "https://comm.aci.game.qq.com/main?sCloudApiName=ams.gameattr.role&appVersion={appVersion}&area={area}&platid={platid}&partition={partition}&callback={callback}&p_tk={p_tk}&sDeviceID={sDeviceID}&&game=jx3&sAMSAcctype=pt&sAMSTargetAppId=wxdd8ef1519da76755&&osVersion=Android-28&ch=10003&sVersionName=v4.1.6.0&appSource=android"
        # 一键领取指尖江湖的日常礼包，从而完成礼包任务
        self.recieve_jx3_gift = "https://djcapp.game.qq.com/daoju/igw/main/?_service=app.package.receive&appVersion={appVersion}&iruleId={iruleId}&sPartition={sPartition}&roleCode={roleCode}&sRoleName={sRoleName}&p_tk={p_tk}&sDeviceID={sDeviceID}&sDjcSign={sDjcSign}&&weexVersion=0.9.4&platform=android&deviceModel=MIX%202&appid=1001&output_format=json&optype=receive_usertask_game&bizcode=jx3&systemID=1&channelID=2&channelKey=qq&osVersion=Android-28&ch=10003&sVersionName=v4.1.6.0&appSource=android"
        # 查询指尖江湖的礼包列表，用于获取礼包的id信息
        self.query_jx3_gift_bags = "https://djcapp.game.qq.com/daoju/igw/main/?_service=app.package.list&appVersion={appVersion}&p_tk={p_tk}&sDeviceID={sDeviceID}&sDjcSign={sDjcSign}&output_format=json&optype=get_user_package_list&appid=1001&&weexVersion=0.9.4&platform=android&deviceModel=MIX%202&bizcode=jx3&showType=qq&osVersion=Android-28&ch=10003&sVersionName=v4.1.6.0&appSource=android"
        # 兑换道具--requestConvertCoupon
        self.exchangeItems = "https://apps.game.qq.com/cgi-bin/daoju/v3/hs/i_buy.cgi?&weexVersion=0.9.4&appVersion={appVersion}&iGoodsSeqId={iGoodsSeqId}&iZone={iZone}&lRoleId={lRoleId}&rolename={rolename}&p_tk={p_tk}&sDeviceID={sDeviceID}&sDjcSign={sDjcSign}&platform=android&deviceModel=MIX%202&&&_output_fmt=1&_plug_id=9800&_from=app&iActionId=2594&iActionType=26&_biz_code=dnf&biz=dnf&appid=1003&_app_id=1003&_cs=2&osVersion=Android-28&ch=10003&sVersionName=v4.1.6.0&appSource=android"
        # 获取所有可兑换的道具的列表
        self.show_exchange_item_list = "https://app.daoju.qq.com/jd/js/dnf_index_list_dj_info_json.js?&weexVersion=0.9.4&appVersion={appVersion}&p_tk={p_tk}&sDeviceID={sDeviceID}&platform=android&deviceModel=MIX%202&&osVersion=Android-28&ch=10003&sVersionName=v4.1.6.0&appSource=android"

    # --------------------------------------------各种操作--------------------------------------------
    def run(self):
        # 检查是否是首次运行，若是首次，则弹框提示相关风险
        self.show_tip_on_first_run()

        run_mode_dict = {
            "pre_run": self.pre_run,
            "normal": self.normal_run,
        }
        run_mode_dict[self.cfg.run_mode]()

        # 暂停一下，方便看结果
        os.system("PAUSE")

    def show_tip_on_first_run(self):
        first_run_flag_file = ".firstrun"
        import os
        if os.path.isfile(first_run_flag_file):
            return

        # 仅在window系统下检查
        if platform.system() != "Windows":
            return

        # 若不存在该文件，则说明是首次运行，提示相关信息
        tips = """# 『重要』与个人隐私有关的skey相关说明
1. skey是腾讯系应用的通用鉴权票据，个中风险，请Google搜索《腾讯skey》后自行评估
2. skey有过期时间，目前根据测试来看应该是一天。目前暂未实现自动登录或者skey的自动保活（不知道有没有这个东西），过期时需要自己更新
3. 本脚本仅使用skey进行必要操作，用以实现自动化查询、签到、领奖和兑换等逻辑，不会上传到与此无关的网站，请自行阅读源码进行审阅
4. 如果感觉有风险，请及时停止使用本软件，避免后续问题
        """
        logger.info("首次运行，弹出使用须知")

        import win32api
        import win32con

        win32api.MessageBox(0, tips, "使用须知", win32con.MB_ICONWARNING)

        # 创建该文件，从而避免再次弹出错误
        with open(first_run_flag_file, "w", encoding="utf-8") as f:
            f.write("ok")

    # 预处理阶段
    def pre_run(self):
        logger.info("预处理阶段，请按照提示进行相关操作")

        # 指引获取uin/skey/角色信息等
        self.check_skey_expired()

        logger.info("uin/skey已经填写完成，请确保已正确填写dnf的区服和手游的区服信息后再进行后续流程")

        # 如果已经填写uin/skey后，则查询角色相关信息
        self.query_all_extra_info()

        logger.info("将上述两行中dnf的想要兑换道具的角色的id和名字复制到config.toml对应位置，并将指尖江湖的角色的id和名字复制到config.toml对应配置")
        logger.info("上述操作均完成后，请使用文本编辑器（如vscode或notepad++，可从网盘下载）打开config.toml，将run_mode配置的值修改为normal，之后再运行就会进行正常流程了")
        logger.info("如果想要自动运行，请使用文本编辑器（如vscode或notepad++，可从网盘下载）打开README.MD来查看相关指引")

    # 正式运行阶段
    def normal_run(self):
        # 检查skey是否过期
        self.check_skey_expired()

        # ------------------------------初始工作------------------------------
        self.query_balance("1. 操作前：查询余额")
        # self.query_money_flow("1.1 操作前：查一遍流水")

        # ------------------------------核心逻辑------------------------------
        # 自动签到
        self.sign_in_and_take_awards()

        # 完成任务
        self.complete_tasks()

        # 领取奖励并兑换道具
        self.take_task_awards_and_exchange_items()

        # ------------------------------清理工作------------------------------
        self.query_balance("5. 操作全部完成后：查询余额")
        # self.query_money_flow("5.1 操作全部完成后：查一遍流水")

    def check_skey_expired(self):
        query_data = self.query_balance("判断skey是否过期", print_res=False)
        if str(query_data['ret']) != "0":
            js_code = """cookies=Object.fromEntries(document.cookie.split(/; */).map(cookie => cookie.split('=', 2)));console.log("uin="+cookies.uin+"\\nskey="+cookies.skey+"\\n");"""
            logger.error((
                             "skey过期，请按下列步骤获取最新skey并更新到配置中\n"
                             "1. 在本脚本自动打开的活动网页中使用通用登录组件完成登录操作\n"
                             "   1.1 指点击（亲爱的玩家，请【登录】）中的登录按钮，并完成后续登录操作\n"
                             "2. 点击F12，将默认打开DevTools（开发者工具界面）的Console界面\n"
                             "       如果默认不是该界面，则点击上方第二个tab（Console）（中文版这个tab的名称可能是命令行？）\n"
                             "3. 在下方输入区输入下列内容来从cookie中获取uin和skey（或者直接粘贴，默认已复制到系统剪贴板里了）\n"
                             "       {js_code}\n"
                             "3. 将uin/skey的值分别填写到config.toml中对应配置的值中即可\n"
                             "4. 填写dnf的区服和手游的区服信息到config.toml中\n"
                             "5. 正常使用还需要填写完成后再次运行脚本，获得角色相关信息，并将信息填入到config.toml中\n"
                             "\n"
                             "具体信息为：ret={ret} msg={msg}"
                         ).format(js_code=js_code, ret=query_data['ret'], msg=query_data['msg']))
            pyperclip.copy(js_code)
            os.popen("start https://dnf.qq.com/lbact/a20200716wgmhz/index.html?wg_ad_from=loginfloatad")
            input("\n完成上述操作后点击回车键即可退出程序，重新运行即可...")
            sys.exit(-1)

    def query_balance(self, ctx, print_res=True):
        return self.get(ctx, self.balance, print_res=print_res)

    def query_money_flow(self, ctx):
        return self.get(ctx, self.money_flow)

    def sign_in_and_take_awards(self):
        # 发送登录事件，否则无法领取签到赠送的聚豆，报：对不起，请在掌上道聚城app内进行签到
        self.get("2.1.1 发送imsdk登录事件", self.imsdk_login)
        self.get("2.1.2 发送app登录事件", self.user_login_event)
        # 签到
        self.post("2.2 签到", self.sign, self.sign_flow_data("96939"))
        # 领取本日签到赠送的聚豆
        self.post("2.3 领取签到赠送的聚豆", self.sign, self.sign_flow_data("324410"))

        # 尝试领取自动签到的奖励
        # 查询本月签到的日期列表
        signinDates = self.post("2.3.1 查询签到日期列表", self.sign, self.sign_flow_data("96938"), print_res=False)
        month_total_signed_days = len(signinDates["modRet"]["data"])
        # 根据本月已签到数，领取符合条件的每月签到若干日的奖励（也就是聚豆页面最上面的那个横条）
        for sign_reward_rule in self.get("2.3.2 查询连续签到奖励规则", self.sign_reward_rule, print_res=False)["data"]:
            if sign_reward_rule["iCanUse"] == 1 and month_total_signed_days >= int(sign_reward_rule["iDays"]):
                ctx = "2.3.3 领取连续签到{}天奖励".format(sign_reward_rule["iDays"])
                self.post(ctx, self.sign, self.sign_flow_data(str(sign_reward_rule["iFlowId"])))

    def sign_flow_data(self, iFlowId):
        return self.format(self.sign_raw_data, iFlowId=iFlowId)

    def complete_tasks(self):
        # 完成《绝不错亿》
        self.get("3.1 模拟点开活动中心", self.task_report, task_type="activity_center")

        # 完成《礼包达人》
        cfg = self.cfg.mobile_game_role_info
        if cfg.enabled():
            giftInfos = [
                Jx3GiftInfo("签到1天礼包", "401579"),
                Jx3GiftInfo("签到2天礼包", "401580"),
                Jx3GiftInfo("签到3天礼包", "401581"),
                Jx3GiftInfo("签到4天礼包", "401582"),
                Jx3GiftInfo("签到5天礼包", "401583"),
                Jx3GiftInfo("签到6天礼包", "401584"),
                Jx3GiftInfo("签到7天礼包", "401586"),
            ]
            dayIndex = datetime.datetime.now().weekday()  # 0-周一...6-周日，恰好跟下标对应
            giftInfo = giftInfos[dayIndex]
            self.get("3.2 一键领取指尖江湖日常礼包-{}".format(giftInfo.sTask), self.recieve_jx3_gift, iruleId=giftInfo.iRuleId,
                     sPartition=cfg.partition, roleCode=cfg.roleid, sRoleName=cfg.rolename)
        else:
            logger.info("未启用自动完成《礼包达人》任务功能")

    def take_task_awards_and_exchange_items(self):
        # 领取奖励
        # 领取《礼包达人》
        self.take_task_award("4.1.1", "100066", "礼包达人")
        # 领取《绝不错亿》
        self.take_task_award("4.1.2", "100040", "绝不错亿")
        # 领取《活跃度银宝箱》
        self.take_task_award("4.1.3", "100001", "活跃度银宝箱")
        # 领取《活跃度金宝箱》
        self.take_task_award("4.1.4", "100002", "活跃度金宝箱")

        # 兑换所需道具
        self.exchange_items()

        # 领取《兑换有礼》
        self.take_task_award("4.3.1", "327091", "兑换有礼")

    def take_task_award(self, prefix, iRuleId, taskName=""):
        ctx = "{} 查询当前任务状态".format(prefix)
        taskinfo = self.get(ctx, self.usertask, print_res=False)

        if self.can_take_task_award(taskinfo, iRuleId):
            ctx = "{} 领取任务-{}-奖励".format(prefix, taskName)
            self.get(ctx, self.take_task_reward, iruleId=iRuleId)

    # 尝试领取每日任务奖励
    def can_take_task_award(self, taskinfo, iRuleId):
        opt_tasks = taskinfo["data"]["list"]["day"].copy()
        for id, task in taskinfo["data"]["chest_list"].items():
            opt_tasks.append(task)
        for tinfo in opt_tasks:
            if int(iRuleId) == int(tinfo["iruleId"]):
                return int(tinfo["iCurrentNum"]) >= int(tinfo["iCompleteNum"])

        return False

    def exchange_items(self):
        # 兑换《装备品级调整箱（5个）》两次
        for i in range(2):
            self.exchange_item("4.2.1 兑换调整箱", "753")
        # 兑换《魔界抗疲劳秘药（10点）》一次
        self.exchange_item("4.2.2 兑换疲劳药", "755")

    def exchange_item(self, ctx, iGoodsSeqId):
        cfg = self.cfg.exchange_role_info
        return self.get(ctx, self.exchangeItems, iGoodsSeqId=iGoodsSeqId, rolename=cfg.rolename, lRoleId=cfg.lRoleId, iZone=cfg.iZone)

    def query_all_extra_info(self):
        # 获取玩家的dnf角色列表，note:当不知道角色的roleid和rolename的时候，可以取消注释进行查询
        self.query_dnf_rolelist()
        # 获取玩家的指尖江湖角色列表，note:当不知道角色的roleid和rolename的时候，可以取消注释进行查询
        self.query_jx3_rolelist()

        # # 显示所有可以兑换的道具列表，note：当不知道id时调用
        # self.query_dnf_gifts()
        #
        # # 获取指尖江湖礼包列表，note：当不知道id时调用
        # self.query_jx3_gifts()

    def query_dnf_rolelist(self):
        ctx = "获取dnf角色列表"
        roleListJsonRes = self.get(ctx, self.get_dnf_role_list, area=self.cfg.exchange_role_info.iZone, is_jsonp=True, print_res=False)
        roleLists = json_parser.parse_role_list(roleListJsonRes)
        logger.info("{}\t{}".format(ctx, roleLists))

    def query_jx3_rolelist(self):
        ctx = "获取指尖江湖角色列表"
        cfg = self.cfg.mobile_game_role_info
        if not cfg.enabled():
            logger.info("未启用自动完成《礼包达人》任务功能")
            return
        jx3RoleListJsonRes = self.get(ctx, self.get_jx3_role_list, area=cfg.area, platid=cfg.platid, partition=cfg.partition, is_jsonp=True, print_res=False)
        jx3RoleList = json_parser.parse_jx3_role_list(jx3RoleListJsonRes)
        logger.info("{}\t{}".format(ctx, jx3RoleList))

    def query_dnf_gifts(self):
        self.get("查询可兑换道具列表", self.show_exchange_item_list)

    def query_jx3_gifts(self):
        self.get("查询指尖江湖礼包信息", self.query_jx3_gift_bags)

    # --------------------------------------------辅助函数--------------------------------------------
    def get(self, ctx, url, pretty=False, print_res=True, is_jsonp=False, **params):
        return self.network.get(ctx, self.format(url, **params), pretty, print_res, is_jsonp)

    def post(self, ctx, url, data, pretty=False, print_res=True, is_jsonp=False, **params):
        return self.network.post(ctx, self.format(url, **params), data, pretty, print_res, is_jsonp)

    def format(self, url, **params):
        endTime = datetime.datetime.now()
        startTime = endTime - datetime.timedelta(days=int(365 / 12 * 5))
        default_params = {
            "appVersion": appVersion,
            "p_tk": self.cfg.g_tk,
            "g_tk": self.cfg.g_tk,
            "sDeviceID": self.cfg.sDeviceID,
            "sDjcSign": self.cfg.sDjcSign,
            "callback": jsonp_callback_flag,
            "month": self.get_month(),
            "starttime": self.getMoneyFlowTime(startTime.year, startTime.month, startTime.day, startTime.hour, startTime.minute, startTime.second),
            "endtime": self.getMoneyFlowTime(endTime.year, endTime.month, endTime.day, endTime.hour, endTime.minute, endTime.second),
        }
        return url.format(**{**default_params, **params})

    def get_month(self):
        now = datetime.datetime.now()
        return "%4d%02d" % (now.year, now.month)

    def getMoneyFlowTime(self, year, month, day, hour, minute, second):
        return "{:04d}{:02d}{:02d}{:02d}{:02d}{:02d}".format(year, month, day, hour, minute, second)


if __name__ == '__main__':
    djcHelper = DjcHelper()
    # djcHelper.run()
    djcHelper.query_all_extra_info()