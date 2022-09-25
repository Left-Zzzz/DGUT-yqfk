#!/usr/bin/python3
# -*- coding: utf-8 -*-

from apscheduler.schedulers.blocking import BlockingScheduler
import re
import requests
import time
import sys
import json
import traceback
from seleniumwire import webdriver
from selenium.webdriver.common.action_chains import ActionChains

username = ""
password = ""
sckey = ""  # wx_message_push-UID

cookies = {}
headers = {}

def get_page(message, target):
    global browser
    global cookies
    global headers
    #selenium模拟点击模块,浏览器设置
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--headless')#无头模式，服务器没有图形界面这个必须
    chrome_options.add_argument('--disable-gpu')#不需要gpu加速
    chrome_options.add_argument('--no-sandbox') # 这个配置很重要
    browser = webdriver.Chrome(chrome_options=chrome_options, executable_path='./chromedriver')    # 如果没有把chromedriver加入到PATH中，就需要指明路径
    browser.get(r'https://yqfk-daka.dgut.edu.cn/')
    time.sleep(2)
    # 定位搜索框
    input = browser.find_element_by_id('username')
    # 输入学号
    input.send_keys(username)
    # 定位搜索框
    input = browser.find_element_by_id('password')
    # 输入密码
    input.send_keys(password)

    btn = browser.find_element_by_id('login_submit')
    btn.click()

    time.sleep(2)
    cookies = browser.get_cookies()
    #print('当前cookie{}'.format(cookies))
    #print('cookie.type{}'.format(type(cookies)))

    cookie_list = [item["name"] + "=" + item["value"] for item in cookies]  
      
    cookiestr = ';'.join(item for item in cookie_list)  

    cookies = {'Cookie':cookiestr}
    # print('requests.cookies{}'.format(cookies))

    for request in browser.requests:
        if request.url == r'https://yqfk-daka-api.dgut.edu.cn/record/':
            headers=request.headers
            break

    # 用完后记得关闭浏览器
    browser.close()

    if not headers.get('Authorization'):
        console_msg("登陆验证失败", 1)
        message.append('登录验证失败')
        return 1
    else:
        console_msg("登陆验证成功", 0)

    return 0

def post_form(message, target):
    #创建一个会话
    yqfk_session = requests.Session()
    global cookies
    global headers
    yqfk_info = yqfk_session.get('https://yqfk-daka-api.dgut.edu.cn/record', headers=headers, cookies=cookies).json()
    #print(yqfk_info)
    yqfk_json = {'data':yqfk_info['user_data']}
    
    # 2022-9-17 接口更新，需要自己填写体温和身体情况, 不然服务器会返回500状态码
    yqfk_json['data']['health_situation'] = 1
    yqfk_json['data']['body_temperature'] = '36.0'

    console_msg(yqfk_info['message'])
    message.append(yqfk_info['message'])
    #print(yqfk_json['data'])
    #todo:提交form
    result = yqfk_session.post(url="https://yqfk-daka-api.dgut.edu.cn/record", headers=headers,
                               json=yqfk_json, cookies=cookies).json()

    
    if 'message' not in result.keys():
        console_msg('提交失败')
        message.append('提交失败')
        return 1
    else:
        if '已提交' in result['message'] or '成功' in result['message'] or '已经' in result['message']:
            console_msg('二次提交，确认成功', 0)
            message.append('二次提交，确认成功')
            result = yqfk_session.get('https://yqfk-daka-api.dgut.edu.cn/record', headers=headers, cookies=cookies).json()
            #result = yqfk_session.get(url="https://yqfk-data-api.dgut.edu.cn/record", headers=headers,
            #                           json=yqfk_json).json()
            console_msg(result['message'])
            return 0
        console_msg(result['message'])
        message.append(result['message'])
        console_msg("二次提交，确认失败", 1)
        # 开发者接口调试
        # console_msg("result:{}".format(result),1)
        # console_msg("header:{}".format(headers),1)
        # console_msg("json:{}".format(yqfk_json),1)

        return 1

def post_message(text, desp=None):
    if sckey is not None:
        url = "http://wxpusher.zjiecode.com/api/send/message/?appToken=AT_VnKPyP9NNJF6oEFtV1sujXxIL4Xifg0Y&uid="+sckey+"&content="
        # console_msg("type(message):{}".format(type(desp)), 0)
        if type(desp) is list:
            for d in desp:
                text = text + str(d) + "%0D%0A%0D%0A"
        elif type(desp) is str:
                text = text + desp + "%0D%0A%0D%0A"

        url = url + text
        rep = requests.get(url=url).json()
        #print(rep)
        if rep['success'] == 1:
            console_msg('ServerChan 发送成功', 0)
        else:
            console_msg('ServerChan 发送失败' + rep['msg'], 1)


def run():
    message = []
    target = []
    result = get_page(message, target)
    if result == 0:
        res = post_form(message, target)
        if res == 0:
            message.append('任务完成: ' + time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
            post_message("疫情防控: 成功", message)
            console_msg('任务完成', 0)
        else:
            post_message("疫情防控: 二次验证失败", message)
    else:
        post_message("疫情防控: 获取页面失败", message)


def console_msg(msg, level=2):
    header = ('[SUCCESS]', '[ERROR]', '[INFO]')
    color = ("\033[32;1m", "\033[31;1m", "\033[36;1m")
    print(color[level], header[level], time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()), msg + "\033[0m")


if __name__ == '__main__':
    if len(sys.argv) < 3 or len(sys.argv) > 5:
        console_msg("参数出错", 1)
        console_msg(sys.argv[0] + " <username> <password> [<sckey>]")
        exit(1)
    else:
        console_msg("Username: " + sys.argv[1])
        console_msg("Password: " + sys.argv[2])
        username = sys.argv[1]
        password = sys.argv[2]
    if len(sys.argv) == 4:
        console_msg("ServerChan Key: " + sys.argv[3])
        sckey = sys.argv[3]
    else:
        console_msg("不启用微信消息推送。")

    schedule = BlockingScheduler()
    try:
        schedule.add_job(run, 'cron', hour='9', minute=0)
        schedule.add_job(run, 'cron', hour='0-1', minute=20)
        console_msg('任务开始')
        run()
        schedule.start()
    except:
        console_msg('执行出错', 1)
        traceback.print_exc()
        post_message('疫情防控：失败', '脚本执行出错')

    # 关闭浏览器
    browser.close()
