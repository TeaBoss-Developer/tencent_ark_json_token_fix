import os
from flask import Flask, jsonify , request,redirect
import random
import requests
import json
import redis
import hashlib
redis_conn = redis.Redis(host='127.0.0.1', port= 6379, password= '', db= 0)#链接Redis数据库
qzone_cookies = ""
qzone_g_tk = 0
r_code = 500
r_data = ""
r_msg = ""
def Get_Cookies():#获取coookie
    result = requests.get("http://103.91.211.27:520/da_wj_o_do_j_ow_f_ha_o_iwh_of_uao_wi_eu").text
    js = json.loads(result)
    return(js["cookies"],int(js["g_tk"]))
qzone_cookies,qzone_g_tk=Get_Cookies()#初始化cookie
app = Flask(__name__)#初始化app
@app.route('/ark_sign', methods=['POST'])#注册接口
def home():#逻辑本体
    try:
        c_tk = request.values.get("c_tk")
        c_id = request.headers["c_id"]
        sc_id = str(redis_conn.get(c_id),encoding="utf-8")
        if(sum_md5(str(request.json).replace("\'","\"").replace("/","\\/").replace(" ","").replace("True","true").replace("False","false").replace("\\/","/")+sc_id)!=c_tk):
            return("{\"code\":50000,\"msg\":\"服务繁忙\"}")
        else: 
            return(ark_sign(json.dumps(request.json)))
    except Exception as e:
        return("{\"code\":-1,\"msg\":\"签名失败,"+repr(e)+".\"}")
@app.route('/', methods=['GET'])
def dir():
    return redirect('http://103.91.211.27:520/',code=302,Response=None)
def ark_sign(ark_json):#签名本体
    global qzone_cookies
    global qzone_g_tk
    global r_code
    global r_data
    global r_msg
    ark_body = {
        "ark" : ark_json
    }
    ark_header = {
        "Host": "act.qzone.qq.com",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36",
        "Content-Type": "application/json",
        "Origin": "https://act.qzone.qq.com",
        "Cookie":qzone_cookies
    }
    jsr = json.loads(requests.post("https://act.qzone.qq.com/v2/vip/tx/trpc/ark-share/GenSignedArk?g_tk="+str(qzone_g_tk),headers=ark_header,data=json.dumps(ark_body, ensure_ascii=False).encode('utf-8')).text)
    r_code = int(jsr["code"])
    r_msg = "签名成功"
    if(r_code != 0):
        r_msg = jsr["message"]
    if(r_code == 0):
        r_code=200
        r_data = jsr["data"]["signed_ark"][0:len(jsr["data"]["signed_ark"])-1]
        helojson = json.loads(r_data)
        redis_conn.set("tokened$"+sum_md5(ark_json),helojson["config"]["token"])
    if(r_code ==-3000 or r_code == 403):
        qzone_cookies,qzone_g_tk=Get_Cookies()
    result_return = {
        "code" : r_code,
        "msg" : r_msg,
        "data" : r_data
    }
    r_code = 500
    r_data = ""
    r_msg = ""
    return(json.dumps(result_return, ensure_ascii=False))
def sum_md5(content):#计算md5
    md5hash = hashlib.md5(content.encode())
    md5 = md5hash.hexdigest()
    return(md5)
if __name__ == '__main__':#通过flask启动工程
    app.run(host="0.0.0.0", port=8080,threaded=True)
