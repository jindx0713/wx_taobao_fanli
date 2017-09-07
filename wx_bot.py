# encoding: utf-8
"""
@author: xsren 
@contact: bestrenxs@gmail.com
@site: xsren.me

@version: 1.0
@license: Apache Licence
@file: wx_bot.py
@time: 2017/5/28 上午10:40

"""

import re
import threading
import traceback
import requests
import json

import itchat
from itchat.content import *

from alimama import Alimama


al = Alimama()
al.login()
#你运行下我看看
#【蚊帐空调迷你变频蚊帐小空调机床上空调卧室空调扇冷暖制冷包邮】，复制这条信息￥pEcJ03iEpIT￥后打开👉手机淘宝👈





# 检查是否是淘宝链接
def check_if_is_tb_link(msg):
    if re.search(ur'【.*】', msg.text) and (u'打开👉手机淘宝👈' in msg.text or u'打开👉天猫APP👈' in msg.text):
#        try:// 提交地址
        taokoulingurl='http://www.taokouling.com/index.php?m=api&a=taokoulingjm';
        urldata='&username=jindx&password=yjghdidr&text='
        try:
            q = re.search(ur'【.*】', msg.text).group().replace(u'【', '').replace(u'】', '')
            if u'打开👉天猫APP👈' in msg.text:
                taokouling = re.findall(r'￥(.*)￥', msg.text)
                taokouling = "￥" + str(taokouling[0]) + "￥"
                parms = {'username': 'jindx', 'password': 'yjghdidr', 'text': taokouling}
                urlres = requests.post(taokoulingurl, data=parms)
                url = json.loads(urlres.text)['url']
            else:
                taokouling = re.findall(ur'￥(.*)￥', msg.text)
                taokouling = "￥" + str(taokouling[0]) + "￥"
                parms={'username':'jindx','password':'yjghdidr','text':taokouling}
                urlres = requests.post(taokoulingurl,data=parms)
                url = json.loads(urlres.text)['url']

            #real_url = al.get_real_url(url)
            # get detai
            real_url=url

            res = al.get_detail(real_url)
            auctionid = res['auctionId']
            coupon_amount = res['couponAmount']
            tk_rate = res['tkRate']
            price = res['zkPrice']
            print 'fx rate:%s' % tk_rate




            # get tk link
            res1 = al.get_tk_link(auctionid)
            tao_token = res1['taoToken']
            short_link = res1['shortLinkUrl']
            coupon_link = res1['couponLink']

            if coupon_link != "":
                coupon_token = res1['couponLinkTaoToken']
                #                 res_text = u'''
                # %s
                # 【返现】%s元
                # 【优惠券】%s元
                # 请复制%s淘口令、打开淘宝APP下单
                # -----------------
                # 【下单地址】%s
                # ''' % (q, fx, coupon_amount, coupon_token, short_link)
                res_text = u'''%s
【优惠券】%s元
请复制%s淘口令、打开淘宝APP下单
-----------------
【下单地址】%s
            ''' % (q, coupon_amount, coupon_token, short_link)
            else:
                res_text = u'''%s
【优惠券】%s元
请复制%s淘口令、打开淘宝APP下单
-----------------
【下单地址】%s
                                ''' % (q, coupon_amount, tao_token, short_link)
            # res_text = u'''
            # %s
            # 【返现】%s元
            # 【优惠券】%s元
            # 请复制%s淘口令、打开淘宝APP下单
            # -----------------
            # 【下单地址】%s
            #                 ''' % (q, fx, coupon_amount, tao_token, short_link)
            msg.user.send(res_text)
        except Exception, e:
            traceback.print_exc()
            info = u'''%s
-----------------
该宝贝暂时没有找到内部返利通道！亲您可以换个宝贝试试，也可以联系我们群内管理员帮着寻找有返现的类似商品
            ''' % q
            msg.user.send(info)


class WxBot(object):
    @itchat.msg_register([TEXT])
    def text_reply(msg):
        # print  '%s: %s' % (msg.type, msg.text)
        print msg.Content
        check_if_is_tb_link(msg)
        # msg.user.send('%s: %s' % (msg.type, msg.text))

    @itchat.msg_register(TEXT, isGroupChat=True)
    def text_reply(msg):
        check_if_is_tb_link(msg)
        # if msg.isAt:
        #     msg.user.send(u'@%s\u2005I received: %s' % (
        #         msg.actualNickName, msg.text))

    def run(self):
        itchat.auto_login(True)
        itchat.run(True)


if __name__ == '__main__':

    mi = WxBot()
    t = threading.Thread(target=mi.run, args=())
    t.start()
