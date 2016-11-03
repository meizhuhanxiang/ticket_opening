# -*- coding: utf-8 -*-
import json
import urllib
import urllib2
from functools import wraps
import sys, os, time
import logging
import hashlib

_dir = os.path.dirname(os.path.realpath(__file__))
os.chdir(_dir)

from flask import Flask
from flask import render_template, session, redirect
from flask import request
from wechat_sdk import WechatConf
from wechat_sdk import WechatBasic
from tools.odbc import get_odbc_inst
from werkzeug.contrib.fixers import ProxyFix
from tools.global_conf import *

from tools.WRONG_CODE import *
from tools.tool import get_remain_cheer_num

app = Flask(__name__)
app.secret_key = 'opends-client-secrets'

reload(sys)
sys.setdefaultencoding("utf-8")

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                    datefmt='%a, %d %b %Y %H:%M:%S')
conf = WechatConf(
    token=TOKEN,
    appid=APPID,
    appsecret=APPSECRET,
    encrypt_mode='mormal',  # 可选项：normal/compatible/safe，分别对应于 明文/兼容/安全 模式
    # encoding_aes_key='your_encoding_aes_key'  # 如果传入此值则必须保证同时传入 token, appid
)
wechat = WechatBasic(conf=conf)


@app.route('/test', methods=['POST', 'GET'])
def test():
    return 'hello gsteps'


@app.route('/check_signature')
def check_signature():
    signature = request.args.get('signature', '')
    timestamp = request.args.get('timestamp', '')
    nonce = request.args.get('nonce', '')
    echostr = request.args.get('echostr', '')
    if wechat.check_signature(signature, timestamp, nonce):
        # return json.dumps({'echostr':echostr})
        return echostr
    else:
        return json.dumps({'echostr': ''})


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'union_id' not in session or 'access_token' not in session:
            session['target_union_id'] = request.args.get('union_id', '')
            logging.info('login_required   target_union_id:%s' % session['target_union_id'])
            callback_url = urllib.quote_plus('%s/callback' % DOMAIN)
            urls = 'https://open.weixin.qq.com/connect/oauth2/authorize?' \
                   'appid=%s&redirect_uri=%s&response_type=code&scope=snsapi_userinfo&state=STATE#wechat_redirect' % (
                       APPID, callback_url)
            urls = 'http://www.gsteps.cn/Home/Oauth/get_wx_code?appid=%s&scope=snsapi_userinfo&state=callback&redirect_uri=%s' % (
            APPID, callback_url)
            logging.info('urls :%s' % urls)
            # return urls
            return redirect(urls)
        else:
            pass
        return f(*args, **kwargs)

    return decorated_function


def url_get(urls):
    # import requests
    # res = requests.post(urls).text
    # return json.loads(res)
    req = urllib2.Request(urls)
    response = urllib2.urlopen(req)
    return json.loads(response.read())


def get_user_info():
    urls = 'https://api.weixin.qq.com/sns/userinfo?access_token=%s&openid=%s&lang=zh_CN' % (
        session['access_token'], session['open_id'])
    res = url_get(urls)
    user_info = {
        'open_id': res['openid'],
        'nickname': res['nickname'],
        'sex': res['sex'],
        'province': res['province'],
        'city': res['city'],
        'country': res['country'],
        'head_img_url': res['headimgurl'],
        'privilege': res['privilege'],
        'union_id': res['unionid'],
    }
    return user_info


def get_base_access_token():
    cache_info = get_odbc_inst().get_cache(BASE_TOKEN)
    code = cache_info['code']
    access_token = cache_info['cache']
    if code != RIGHT:
        urls = "https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid=%s&secret=%s" % (
        APPID, APPSECRET)
        res = url_get(urls)
        access_token = res.get('access_token', '')
        if access_token:
            get_odbc_inst().save_cache(access_token, BASE_TOKEN)
    return access_token


def get_wx_ticket():
    cache_info = get_odbc_inst().get_cache(WX_TICKET)
    code = cache_info['code']
    wx_ticket = cache_info['cache']
    if code != RIGHT:
        urls = "https://api.weixin.qq.com/cgi-bin/ticket/getticket?access_token=%s&type=jsapi" % get_base_access_token()
        res = url_get(urls)
        wx_ticket = res.get('ticket', '')
        if wx_ticket:
            get_odbc_inst().save_cache(wx_ticket, WX_TICKET)
    return wx_ticket


def get_menu_share_conf(url):
    noncestr = NONCESTR
    jsapi_ticket = get_wx_ticket()
    timestamps = int(time.time())
    s = 'jsapi_ticket=%s&noncestr=%s&timestamp=%s&url=%s' % (jsapi_ticket, NONCESTR, timestamps, url)
    signature = hashlib.sha1(s).hexdigest()
    logging.info('s--------:%s,    signature:%s' % (s, signature))
    return json.dumps({'appid': APPID,
                       'timestamp': timestamps,
                       'noncestr': noncestr,
                       'signature': signature,
                       'link': url,
                       'js_api_list': ['onMenuShareTimeline', 'onMenuShareAppMessage'],
                       'signature_decode': s
                       })


@app.route('/conf_menu_share', methods=['GET', 'POST'])
def conf_menu_share():
    url = '%s/?union_id=%s' % (DOMAIN, session.get('union_id', ''))
    return get_menu_share_conf(url)


@app.route('/callback', methods=['POST', 'GET'])
def callback():
    logging.info('-' * 50)
    code = request.args.get('code', '')
    state = request.args.get('state')
    if code:
        code_url = 'https://api.weixin.qq.com/sns/oauth2/access_token?' \
                   'appid=%s&secret=%s&code=%s&grant_type=authorization_code' % (APPID, APPSECRET, code)
        res = url_get(code_url)
        session['access_token'] = res['access_token']
        session['open_id'] = res['openid']
        user_info = get_user_info()
        logging.info('callback user_info:%s' % user_info)
        session['union_id'] = user_info['union_id']
        get_odbc_inst().register_user(user_info)
        args = session.get('target_union_id', '')
        logging.info('callbak target_union_id:%s' % args)
        if not args:
            args = user_info['union_id']
    return redirect('/?union_id=%s' % args)


@app.route('/', methods=['POST', 'GET'])
@login_required
def index():
    logging.info('*' * 50)
    union_id = session.get('union_id', '')
    target_union_id = session.get('target_union_id', '')
    logging.info('index session target_union_id:%s' % (target_union_id))
    if not target_union_id:
        target_union_id = request.args.get('union_id', '')
        logging.info('index request.args  target_union_id:%s' % (target_union_id))
        logging.info('index request.form  target_union_id:%s' % (request.form.get('union_id', '')))
    if not target_union_id:
        logging.info('index no  target_union_id')
        return redirect('/?union_id=%s' % union_id)
    logging.info('index union_id:%s, target_union_id:%s' % (union_id, target_union_id))
    if union_id != target_union_id:
        cheer_num = get_odbc_inst().get_cheer_num(target_union_id)
        remain_cheer_num = get_remain_cheer_num(cheer_num)
        logging.info('target_cheer_num:%s' % cheer_num)
        session['target_union_id'] = ''
        return render_template('cheer.html', union_id=union_id, target_union_id=target_union_id,
                               remain_cheer_num=remain_cheer_num, satisfy_cheer_num=SATISFY_CHEER_NUM)
    else:
        cheer_num = get_odbc_inst().get_cheer_num(union_id)
        remain_cheer_num = get_remain_cheer_num(cheer_num)
        return render_template('index.html', union_id=union_id, remain_cheer_num=remain_cheer_num,
                               satisfy_cheer_num=SATISFY_CHEER_NUM)


@app.route('/get_cheer_info', methods=['GET'])
def get_cheer_info():
    code = RIGHT
    target_union_id = request.args.get('union_id', '')
    logging.info('get_cheer_info target_union_id:%s' % target_union_id)
    if not target_union_id:
        code = GET_CHEER_INFO_NO_UNION_ID
    cheer_info = get_odbc_inst().get_cheer_info(target_union_id)
    if not cheer_info:
        code = GET_CHEER_INFO_FAILED
    return json.dumps({'code': code, 'cheer_info': cheer_info})

@app.route('/cheer', methods=['POST', 'GET'])
@login_required
def cheer():
    return redirect('/?union_id=%s' % session['union_id'])


@app.route('/async_cheer', methods=['POST'])
def async_cheer():
    union_id = request.form.get('union_id', '')
    target_union_id = request.form.get('target_union_id', '')
    code = RIGHT
    if not union_id:
        code = CHEER_UNION_ID_IS_NULL
    elif not target_union_id:
        code = CHEER_TARGET_UNION_ID_IS_NULL
    else:
        code = get_odbc_inst().cheer(union_id, target_union_id)
    if code == RIGHT:
        target_cheer_num = get_odbc_inst().get_cheer_num(target_union_id)
        target_remain_cheer_num = get_remain_cheer_num(target_cheer_num)
        return json.dumps({'code': code, 'target_remain_cheer_num': target_remain_cheer_num})
    else:
        return json.dumps({'code': code})


@app.route('/activity', methods=['POST', 'GET'])
def activity():
    return render_template('activity.html')

@app.route('/index/<func>', methods=['POST', 'GET'])
def index_func(func):
    return render_template('index_%s.html' % func)


def application(env, start_response):
    start_response('200 OK', [('Content_Type', 'text/html')])
    return "Congraduation!!! uWSGI Testing OK!!!"


if __name__ == '__main__':
    # app.wsgi_app = ProxyFix(app.wsgi_app)
    app.debug = True
    app.secret_key = 'opends-client-secrets'
    app.run(host='0.0.0.0', port=9003)
    app.run()

