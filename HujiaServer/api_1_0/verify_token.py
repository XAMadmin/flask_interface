from . import api
import hashlib
from flask import request, jsonify, json,current_app
from HujiaServer.models import Customer, session
# import datetime
import time


# 获取token 传值dwbh,keyid ,timestamp
@api.route("/get_token", methods = ['POST'])
def set_token():

    req_data = request.get_json()
     
    if not req_data:
        return jsonify(errno='4001', errmsg='请求参数为空！')
    
    username = req_data.get("dwbh")
    keyid = req_data.get('keyid')
    timestamp = req_data.get("timestamp")

    if not all([username, keyid, timestamp]):
        return jsonify(errno='4002', errmsg='缺少参数值！')
    
    t = time.time()
    td = int(t) - int(timestamp)
 
    if len(str(timestamp)) != 10 or  abs(td) > 10:
        return jsonify(errno='4003', errmsg='请求参数错误！')
    # else:
    #     dateArray = datetime.datetime.utcfromtimestamp(int(timestamp))
    #     otherStyleTime = dateArray.strftime("%Y-%m-%d %H:%M:%S")
    #     print(otherStyleTime)

    try:
        customer = session.query(Customer).filter_by(dwbh=username, keyID=keyid).first()
    except Exception as e:
        current_app.logger.error("请求服务器错误！")
        return jsonify(errno='4005', errmsg='请求服务器错误！')

    if not customer:
        return jsonify(errno='4004', errmsg='用户名或密钥不正确！')
    
    md5 = hashlib.md5()
    md5.update("".join([username, keyid, str(timestamp)]).encode("utf8"))
    md5_data = md5.hexdigest()

    try:
        session.query(Customer).filter_by(dwbh=username, keyID=keyid).update({"token": md5_data, "dt":timestamp})
        session.commit()
    except Exception as e:
        current_app.logger.error("请求服务器错误！")
        return jsonify(errno='4005', errmsg='请求服务器错误！')

    data = {
        "errno":"200",
        "errmsg":"请求成功！",
        "access_token":md5_data,
        "expires_in":3600
    }
    # js_data = json.dumps(data)
    return jsonify(info=data) 



