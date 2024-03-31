import time

import requests


# 测试用环境变量
# os.environ['COOKIE_QUARK'] = ''


class Quark:
    def __init__(self, cookie):
        self.cookie = cookie

    def get_growth_info(self):
        url = "https://drive-m.quark.cn/1/clouddrive/capacity/growth/info"
        querystring = {"pr": "ucpro", "fr": "pc", "uc_param_str": ""}
        headers = {"cookie": self.cookie}
        response = requests.request("GET", url, headers=headers, params=querystring).json()
        if response.get("data"):
            return response["data"]
        else:
            return False

    def get_growth_sign(self):
        url = "https://drive-m.quark.cn/1/clouddrive/capacity/growth/sign"
        querystring = {"pr": "ucpro", "fr": "pc", "uc_param_str": ""}
        payload = {"sign_cyclic": True}
        headers = {"cookie": self.cookie}
        response = requests.request(
            "POST", url, json=payload, headers=headers, params=querystring).json()
        if response.get("data"):
            return True, response["data"]["sign_daily_reward"]
        else:
            return False, response["message"]

    def get_account_info(self):
        url = "https://pan.quark.cn/account/info"
        querystring = {"fr": "pc", "platform": "pc"}
        headers = {"cookie": self.cookie}
        response = requests.request("GET", url, headers=headers, params=querystring).json()
        if response.get("data"):
            return response["data"]
        else:
            return False

    def do_sign(self):
        msg = ""
        # 验证账号
        account_info = self.get_account_info()
        if not account_info:
            msg = f"\n❌该账号登录失败，cookie无效"
        else:
            log = f" 昵称: {account_info['nickname']}"
            msg += log + "\n"
            # 每日领空间
            growth_info = self.get_growth_info()
            if growth_info:
                if growth_info["cap_sign"]["sign_daily"]:
                    log = f"✅ 执行签到: 今日已签到+{int(growth_info['cap_sign']['sign_daily_reward'] / 1024 / 1024)}MB，连签进度({growth_info['cap_sign']['sign_progress']}/{growth_info['cap_sign']['sign_target']})"
                    msg += log + "\n"
                else:
                    sign, sign_return = self.get_growth_sign()
                    if sign:
                        log = f"✅ 执行签到: 今日签到+{int(sign_return / 1024 / 1024)}MB，连签进度({growth_info['cap_sign']['sign_progress'] + 1}/{growth_info['cap_sign']['sign_target']})"
                        msg += log + "\n"
                    else:
                        msg += f"✅ 执行签到: {sign_return}\n"

        return msg


def main():
    msg = ""
    global cookie_quark
    cookie_quark = [
        'kkpcwpea=a=a&uc_param_str=einibicppfmivefrlantcunwsssvjbktchnnsnddds&instance=kkpcwp&pf=145&self_service=true&wxUid=AATYKrNYvzjTBIyPAL17b1p6&plain_utdid=ZeB4jQAAACkDAL6Aoc799PXF&system_ver=Windows_NT_10.0.19045&channel_no=pckk%40other_ch&ve=3.1.3&sv=release; CwsSessionId=96f25006-331a-4aee-b995-453ccc5bd4d2; _UP_A4A_11_=wb9631b5e57248b1afc423f34a788952; _UP_30C_6A_=st96362019eyn4cph9a9q5bx3bpcmmzf; _UP_TS_=sg14e16333c3fbb6a22678fcc4774fd865d; _UP_E37_B7_=sg14e16333c3fbb6a22678fcc4774fd865d; _UP_TG_=st96362019eyn4cph9a9q5bx3bpcmmzf; _UP_335_2B_=1; __pus=b663edb09ae8eb228a1016be68b04a2fAATzpMX4li27E/O5BQOexrpVPsgIfVg8o4YeB2Ff06rrWp3bZinmQmuCJscT06AF7DLC6SnkHtQHD4WuyJZR+mrk; __kp=be227e10-e3a3-11ee-9d1a-cba7ae59e94b; __kps=AATYKrNYvzjTBIyPAL17b1p6; __ktd=KgaBQgqAssNila/5VSt7wQ==; __uid=AATYKrNYvzjTBIyPAL17b1p6; tfstk=foVHzJf3IJkCOqKnlOcCsSt20uXtdHGSmud-2bnPQco6pDh8zbRz2zhKUMa8j0q8PDPKJD3zqlnswDFLp8YQsoAJ9M6QzQc-aiIAMsUCRbGPDzdFN9xIy4gPwYkE_AFIresAMsUUXHGZriQIWrooU4lr8YkybN0Ib4-z4Dkwbq0ja08-A3_Kr6FC-xnDkkUea7fc6m4EjI4_w2SIDsiHaIPi-Pm48ERya50nL7fGI15np8zjhWEfZCGLoRlZky1HsjzEoknT0sRi_PUa2xw1VIH_j7DbTvTyLPVoxxPEIUdYof3z4Y21mI3n9RD0tJ_Wbyrxx-lQyEjLSx2ihVkwrpSP_dJqqjOS7aFMFLME5VmYEPdVx4o3QQ7GSK6ILVgdDNbMFLME5VmASNvXVvusJiC..; __puus=43d889810005734d93140fa16044f5a6AARgaZ58HZz72Psz0ppJGHBy4bOt7eXFyDdMNHl9Xjp62MX0GhNLlR/tvBKWa5j3rWI7HBe7cvs1Rd7cdy/qb0Be1USjOiSPonxHB0KUdDWe7AUBVHlHB6zkA4843zuhlBWQEyiXa7e5DVngt6X9FliojUDX4YcYP74iouiacfwS8PAH/wUBT3VcETCYRWqdsznl8sSOD7H0pZqAx1mJZyKH']

    print("✅检测到共", len(cookie_quark), "个夸克账号\n")

    i = 0
    while i < len(cookie_quark):
        # 开始任务
        log = f"🙍🏻‍♂️ 第{i + 1}个账号"
        msg += log
        # 登录
        log = Quark(cookie_quark[i]).do_sign()
        msg += log + "\n"

        i += 1

    print(msg)


if __name__ == "__main__":
    while True:
        # 获取当前时间
        current_time = time.localtime()

        # 判断是否是每天的 1 点
        if current_time.tm_hour == 1 and current_time.tm_min == 0:
            # 执行你想要的操作
            # 这里可以添加你的代码，用于执行需要在每天 1 点执行的任务
            print("----------夸克网盘开始尝试签到----------")
            main()
            # 等待到达第二天的 1 点
            time.sleep(86400)  # 24小时的秒数
            print("----------夸克网盘签到执行完毕----------")
        else:
            # 计算距离下一个 1 小时还有多久，并休眠该时间
            seconds_until_next_hour = 3600 - current_time.tm_min * 60 - current_time.tm_sec
            print(f"It's not hours yet. Waiting for it...{seconds_until_next_hour}s left.")
            time.sleep(seconds_until_next_hour)
p