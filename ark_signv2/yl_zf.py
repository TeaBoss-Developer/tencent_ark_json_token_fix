import json
nwordar = [
    "com.tencent.troopsharecard",
    "代码群",
    "jq.qq.com",
    "com.tencent.qqavchat",
    "com.tencent.qzone",
    "com.tencent.mobileqq.reading",
    "com.tencent.gamecenter.mall",
    "com.tencent.gwh.video",
    "大一JK",
    "学妹含棒棒糖",
    "金主",
    "调教",
    "技术支持",
    "点我观看",
    "https:\/\/docs.qq.com\/scenario\/",
    "https://docs.qq.com/scenario/",
    "shp.qpic.cn",
    "https:\/\/ssl.ptlogin2.qq.com\/jump",
    "https://ssl.ptlogin2.qq.com/jump",
    "SMRYYDS",
    "拔枪",
    "喷水",
    "少萝",
    "卡泡",
    "嫩穴",
    "保底",
    #"群发",
    #"红包",
    #"抢包",
    #"裙发",
    #"引流系统",
    "保底",
    "门槛"
    ]
from flask import Flask, jsonify , request,redirect
app = Flask(__name__)
@app.route('/check', methods=['POST'])
def home():
    ar = str(request.data.decode('utf-8'))
    for nword in nwordar:
        if(nword not in ar):
            continue
        if(nword in ar):
            if(nword == "com.tencent.qzone" and "structmsg" not in ar):
                print(nword)
                return("Yes")
    return("No")
app.run(host="0.0.0.0", port=1543,threaded=True)