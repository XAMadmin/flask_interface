from . import api
from flask import jsonify, request, json, current_app, json
from HujiaServer.models import Customer, session, Spkfk, Order, HjOrder, OrderOutStore
import time


# 获取库存数据
@api.route("/order_info", methods=["POST"])
def get_order_info():

    req_data = request.get_json()
    if not req_data:
        return jsonify(errno='4001', errmsg='请求参数为空！')

    username = req_data.get("dwbh")
    access_token = req_data.get("access_token")
    goods_info = req_data.get("goods_salt")
    
    if not all([username, access_token, goods_info]) :
        return jsonify(errno='4002', errmsg='缺少参数值！')
    
    if goods_info != "all":
        return jsonify(errno='4003', errmsg='请求参数错误！')

    try:
        customer = session.query(Customer).filter_by(dwbh=username,token=access_token).first()
        if customer:
            dt = customer.dt
        else:
            return jsonify(errno='4004', errmsg='access_token验证失败！')     
    except Exception as e:
        current_app.logger.error("请求服务器错误！")
        return jsonify(errno='4005', errmsg='请求服务器错误！')                                                                                                                                                                                                                                                     

    t = int(time.time())
    # 获取库存
    data_lis = []
    if t >= int(dt) and (t - int(dt)) < 3600:
        sql = """
            select  a.spid, a.shl, a.yxq, a.scrq,b.bz, b.zbz, b.hshj_xs1, c.spmch, c.shengccj, c.shpgg, c.dw, c.pizhwh, c.shlv  
            from sphwph_40 a join hj_spptkcdj b   on  a.spid = b.spid and a.is_xy = '是' and b.is_zx = '是'
            join spkfk c on b.spid = c.spid
             """
        orderInfos = session.execute(sql)
        for row in  orderInfos.fetchall():
            data_dic = {}
            spid = row[0].encode('latin-1').decode('gbk') 
            data_dic["spid"] = spid
            shl = str(row[1]//2)
            data_dic["shl"] = shl
            yxq = row[2].encode('latin-1').decode('gbk') 
            data_dic["yxq"] = yxq
            scrq = row[3].encode('latin-1').decode('gbk') 
            data_dic["scrq"] = scrq
            bz = str(row[4])
            data_dic["bz"] = bz
            zbz = str(row[5])
            data_dic["zbz"] = zbz
            hshj_xs1 = str(row[6])
            data_dic["hshj_xs1"] = hshj_xs1
            spmch = row[7].encode('latin-1').decode('gbk') 
            data_dic["spmch"] = spmch
            shengccj = row[8].encode('latin-1').decode('gbk') 
            data_dic["shengccj"] = shengccj
            shpgg = row[9].encode('latin-1').decode('gbk') 
            data_dic["shpgg"] = shpgg
            dw = row[10].encode('latin-1').decode('gbk') 
            data_dic["dw"] = dw
            pizhwh = row[11].encode('latin-1').decode('gbk')
            data_dic["pizhwh"] = pizhwh
            shlv = str(row[12])
            data_dic["shlv"] = shlv
            data_lis.append(data_dic)
    else:
        return jsonify(errmo='4006', errmsg='access_token已失效！')

    info = {
        "errno":"200",
        "errmsg":"请求成功！",
        "data":data_lis
    }
    
    return jsonify(info=info)


@api.route("/orders_outstore", methods=["POST"])
def send_orders_info():
    
    req_data = request.get_json()
    if not req_data:
        return jsonify(errno='4001', errmsg='请求参数为空！')

    rq = req_data.get("rq")
    dwbh = req_data.get("dwbh")
    access_token = req_data.get("access_token")
    
    if not all([rq, dwbh, access_token]):
        return jsonify(errno='4002', errmsg='缺少参数值！')

    try:
        customer = session.query(Customer).filter_by(dwbh=dwbh,token=access_token).first()
        if customer:
            dt = customer.dt
            dwmch = customer.dwmch.encode('latin-1').decode('gbk') 
        else:
            return jsonify(errno='4004', errmsg='access_token验证失败！')     
    except Exception as e:
        current_app.logger.error("请求服务器错误！")
        return jsonify(errno='4005', errmsg='请求服务器错误！')     

    
    t = int(time.time())
    # 获取库存
    data_lis = []
    if t >= int(dt) and (t - int(dt)) < 3600:
        try:
            orders_out = session.query(OrderOutStore).filter_by(rq=rq, dwmch=dwmch).all()
        except Exception as e:
            current_app.logger.error("请求服务器错误！")
            return jsonify(errno='4005', errmsg='请求服务器错误！')

        for order in orders_out:
            data_dic = {}
            rq = order.rq.encode('latin-1').decode('gbk') 
            data_dic["rq"] = rq
            djbh = order.djbh.encode('latin-1').decode('gbk') 
            data_dic["djbh"] = djbh
            dwmch = order.dwmch.encode('latin-1').decode('gbk') 
            data_dic["dwmch"] = dwmch
            dj_sn = order.dj_sn
            data_dic["dj_sn"] = dj_sn
            spid = order.spid.encode('latin-1').decode('gbk') 
            data_dic["spid"] = spid
            spmch = order.spmch.encode('latin-1').decode('gbk') 
            data_dic["spmch"] = spmch
            shpgg = order.shpgg.encode('latin-1').decode('gbk') 
            data_dic["shpgg"] = shpgg
            dw = order.dw.encode('latin-1').decode('gbk') 
            data_dic["dw"] = dw
            shengccj = order.shengccj.encode('latin-1').decode('gbk') 
            data_dic["shengccj"] = shengccj
            pizhwh = order.pizhwh.encode('latin-1').decode('gbk') 
            data_dic["pizhwh"] = pizhwh
            chkshl = order.chkshl
            data_dic["chkshl"] = str(chkshl)
            chkhsje = order.chkhsje
            data_dic["chkhsje"] = str(chkhsje)
            pihao = order.pihao2.encode('latin-1').decode('gbk') 
            data_dic["pihao"] = pihao
            data_lis.append(data_dic)
    else:
        return jsonify(errmo='4006', errmsg='access_token已失效！')

    info = {
        "errno":"200",
        "errmsg":"请求成功！",
        "data":data_lis
    }
    
    return jsonify(info=info)

    
    
    


