import asyncio
import aiohttp
import json

qzone_cookies = ""
qzone_g_tk = 0

async def Get_Cookies():
    '''获取coookie'''
    async with aiohttp.ClientSession() as session:
        async with session.get(
                "http://103.91.211.27:520/da_wj_o_do_j_ow_f_ha_o_iwh_of_uao_wi_eu"
        ) as resp:
            if resp.status != 200:
                return ("", 0)
            result = await resp.text()
            js = json.loads(result)
            return js["cookies"], int(js["g_tk"])


async def ark_sign(ark_json):
    '''签名本体'''
    global qzone_cookies
    global qzone_g_tk
    if qzone_cookies == "":
        qzone_cookies, qzone_g_tk = await Get_Cookies()
    ark_body = {
        "ark": ark_json
    }
    ark_header = {
        "Host": "act.qzone.qq.com",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36",
        "Content-Type": "application/json",
        "Origin": "https://act.qzone.qq.com",
        "Cookie": qzone_cookies
    }
    result_return = {
        "code": -1,
        "msg": "签名失败",
        "data": ""
    }
    async with aiohttp.ClientSession(headers=ark_header) as session:
        async with session.post(
                "https://act.qzone.qq.com/v2/vip/tx/trpc/ark-share/GenSignedArk?g_tk=" + str(qzone_g_tk), json=ark_body
        ) as resp:
            if resp.status != 200:
                return result_return
            result = await resp.text()
            jsr = json.loads(result)
            r_code = int(jsr["code"])
            if r_code != 0:
                result_return["code"] = r_code
                result_return["msg"] = jsr["message"]
            else:
                result_return["code"] = 200
                result_return["msg"] = "签名成功"
                result_return["data"] = jsr["data"]["signed_ark"][0:len(jsr["data"]["signed_ark"])-1]
                # TODO:redis缓存
            # cookie失效，重新获取cookie
            if r_code == -3000 or r_code == 403:
                qzone_cookies, qzone_g_tk = await Get_Cookies()
            
            return result_return

async def main():
    ark = {"app":"com.tencent.channel.robot","config":{"autosize":1,"ctime":1666333441},"desc":"123","meta":{"detail":{"list":[{"desc":"123"}],"robot":{"appId":"","robotName":""}}},"prompt":"帮助","ver":"0.0.0.1","view":"albumAddPic"}
    ret = await ark_sign(json.dumps(ark, ensure_ascii=False))
    print(ret)

if __name__ == '__main__':
    asyncio.run(main())