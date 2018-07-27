#coding=utf-8
from flask import Flask
from flask import request
import requests
import logging
import json
app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'jiaoyishuo houtai!'

@app.route('/code', methods=['POST'])
def setcode():
    logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(levelname)s %(message)s', datefmt='%a, %d %b %Y %H:%M:%S', filename='/root/jys/flask.log', filemode='w')


    logging.info("=================start handle111===================")
    res = json.loads(request.data)
    logging.debug(request.data)
    logging.debug(res['code'])

    wxRet =jscode2session(res['code'])
    logging.debug(wxRet)

    dic_wxRet =json.loads(wxRet)
    logging.debug(dic_wxRet['openid'])

    wxRetTmp =sendTip(dic_wxRet['openid'],res['formId'])



    return 'setcode'

def jscode2session(code):
    url = ('https://api.weixin.qq.com/sns/jscode2session?'+ 'appid={}&secret={}&js_code={}&grant_type=authorization_code').format('wx3367d21c68cea6a0' ,'6b53aedd3052e2651cff4d006d26e1ef', code)
    r = requests.get(url)
    return r.content.decode()


def sendTip(openid,form_id):
    payload = { 'grant_type': 'client_credential', 'appid': 'wx3367d21c68cea6a0', 'secret': '6b53aedd3052e2651cff4d006d26e1ef' }
    requests.packages.urllib3.disable_warnings()
    req = requests.get('https://api.weixin.qq.com/cgi-bin/token', params=payload, timeout=3, verify=False)
    access_token = req.json().get('access_token')

    data = {
        "touser": openid,
        "template_id": 'qF-C0-Z1AHWHCElmKPqekJj2OlY29spIcehbWW97I2c',
        "page": 'pages/index/index',
        "form_id": form_id,
        "data": {
            'keyword1': { 'value': '[沪深300]前高点[3506.24][7月16],[3520]买入,上涨[0.8%]，ATR[65.0]止损金额[3.9万]左宽[12]天,右宽[5]天收盘[3492.89]期指[3458.6]价差[-34.0' },
            'keyword2': { 'value': '沪深300' }
        },
        "emphasis_keyword": ''
    }
    push_url = 'https://api.weixin.qq.com/cgi-bin/message/wxopen/template/send?access_token={}'.format(access_token)
    r =requests.post(push_url, json=data, timeout=3, verify=False)
    return r.content.decode()


if __name__ == '__main__':
    app.run()
