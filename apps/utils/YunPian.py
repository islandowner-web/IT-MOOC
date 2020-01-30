import requests
import json

def send_single_sms(apikey, code, mobile):
    #发送单条短信
    url = "https://sms.yunpian.com/v2/sms/single_send.json"
    text = "【薛振】您的验证码是{}。如非本人操作，请忽略本短信".format(code)

    res = requests.post(url,data={
        "apikey":apikey,
        "mobile":mobile,
        "text":text
    })
    re_json = json.loads(res.text)
    return re_json

if __name__ == "__main__":
    res = send_single_sms("82c9e3f2ca2df73febd98ce483d33612", "7683", "13958791123")
    import json
    res_json = json.loads(res.text)
    code = res_json["code"]
    msg = res_json["msg"]
    if code == 0:
        print("发送成功")
    else:
        print("发送失败:{}".format(msg))
    print(res.text)