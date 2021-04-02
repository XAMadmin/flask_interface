# 测试API
import requests
import json
import time


HEADERS = {

    "Content-Type":"application/json" # application/json
}


user_data = {
    "dwbh":"DWI00000299",
    "keyid":"hjyy123",
    "timestamp":int(time.time())
}

response = requests.post(url="", headers=HEADERS, data=json.dumps(user_data))


result = json.loads(response.text)
print(result)
res = result.get("info")["access_token"]

print(res)


order_send_data = {

   "access_token":res,
   "dwbh":"DWI00000299",
   "goods_info":"all"
}
print(json.dumps(order_send_data))

res = requests.post(url="",headers=HEADERS, data=json.dumps(order_send_data))
result = json.loads(res.text)

# print(res.text)
print(result)
# print(result["info"])
# print(json.loads(result["info"]))
