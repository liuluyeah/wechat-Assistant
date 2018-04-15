# -*- coding: UTF-8 -*- 
import itchat, collections, os, codecs, re
import logging
from flask import Flask, jsonify, send_file, request, render_template, url_for, redirect
from snownlp import SnowNLP
from secretary import analyze, ifPersonalInfo
from wenzhi import zhengzhi, laji
import time, jieba
from itchat.content import *
from concurrent.futures import ThreadPoolExecutor

executor = ThreadPoolExecutor(1)

app = Flask(__name__)
logger = logging.getLogger('app')

mychat = mychat = itchat.Core()

@app.route("/", methods=['GET'])
def index():
    return redirect('static/index.html')

@app.route('/qr', methods=['GET'])
def get_QR():
    mychat.get_QRuuid()
    logger.info("----", mychat.uuid)
    qr_io = mychat.get_QR(enableCmdQR=2)
    qr_io.seek(0)
    return send_file(qr_io, mimetype='image/png')

def reboot_system():
    executor.submit(some_long_task1)
    return True

def some_long_task1():
    mychat.run()

@app.route('/login', methods=['GET'])
def get_isLogging():
    logger.info("----", mychat.uuid)
    if not mychat.uuid:
        return jsonify({'error': 'please request /qr and scan QR'})
    status = mychat.check_login()
    if status == '200':
        isLoggedIn = True
    elif status == '201':
        return jsonify({'error': 'Please press confirm on your phone.'})
    elif status == '408':
        return jsonify({'error': 'please request /qr and scan QR', 'status': status})
    mychat.web_init()
    mychat.show_mobile_login()
    mychat.get_contact(True)
    mychat.start_receiving()
    # 新增获取数据
    friends = mychat.get_friends(update=True)[0:]
    male = female = other = 0
    for i in friends[1:]:
        sex = i["Sex"]
        if sex == 1:
            male += 1
        elif sex == 2:
            female += 1
        else:
            other += 1
    rooms = mychat.get_chatrooms()
    ftxt = ""
    rtxt = ""
    rtxt = '总共有'+str(len(rooms))+'群聊,群聊昵称分别如下：、'
    ftxt = '总共有'+str(len(friends[1:]))+'好友,好友昵称分别如下：、'
    for i in friends[1:]:
        ftxt += i['NickName'] +'、'
    for i in rooms:
        rtxt += i['NickName'] + '、'
    p1,p2,c1,c2 = friends_area(mychat, friends)
    # mychat.run()
    reboot_system()
    return jsonify({'isLoggin': mychat.alive,
                    'friends': ftxt,
                    'rooms':rtxt,
                    'male':male,
                    'female':female,
                    'other':other,
                    'p1':p1,
                    'p2':p2,
                    'c1':c1,
                    'c2':c2
                    })



@app.route('/send', methods=['POST'])
def sendMsg():
    if not mychat.alive:
        return jsonify({'error': '请先登录'})
    json = request.json
    return jsonify(mychat.send(json[u'message'], findUserByName(mychat, json[u'name'])))

@app.route('/send-group', methods=['POST'])
def sendGroupMsg():
    if not mychat.alive:
        return jsonify({'error': '请先登录'})
    json = request.json
    return jsonify(mychat.send(json[u'message'], findGroupUserByName(mychat,json[u'name'])))


def findGroupUserByName(mychat, name):
    users = mychat.search_chatrooms(name=name)
    return users[0]['UserName']

def findUserByName(mychat, name):
    users = mychat.search_friends(name=name)
    return users[0]['UserName']

def friends_area(mychat,friends):
    provinces = []
    cities = []
    provinces.append([friend['Province'] for friend in friends[1:]])
    cities.append([friend['City'] for friend in friends[1:]])
    province = dict(collections.Counter(provinces[0]))
    city = dict(collections.Counter(cities[0]))
    del province[""]
    del city[""]
    province_b = sorted(province.items(), key=lambda province: province[1], reverse=True)
    city_b = sorted(city.items(), key=lambda city: city[1], reverse=True)
    p1,p2 = [],[]
    for ele in province_b[:10]:
        p1.append(ele[0])
        p2.append(ele[1])
    c1,c2 = [],[]
    for ele in city_b[:10]:
        c1.append(ele[0])
        c2.append(ele[1])
    return p1, p2, c1, c2

msg_information = {}
face_bug = None  # 针对表情包的内容


@mychat.msg_register([TEXT, PICTURE, FRIENDS, CARD,
                      MAP, SHARING, RECORDING, ATTACHMENT,
                      VIDEO], isFriendChat=True,
                     isMpChat=True)
def handle_receive_msg(msg):
    global face_bug
    # 接受消息的时间
    msg_time_rec = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    # 在好友列表中查询发送信息的好友昵称
    msg_from = mychat.search_friends(userName=msg['FromUserName'])['NickName']
    msg_time = msg['CreateTime']  # 信息发送的时间
    msg_id = msg['MsgId']  # 每条信息的id
    msg_content = None  # 储存信息的内容
    msg_share_url = None  # 储存分享的链接，比如分享的文章和音乐
    print(msg['Type'])
    print(msg['MsgId'])

    # 如果发送的消息是文本或者好友推荐
    if msg['Type'] == 'Text' or msg['Type'] == 'Friends':
        msg_content = msg['Text']
        s = SnowNLP(msg_content)
        sent = s.sentiments
        print(msg_content)
        r1 = float(zhengzhi(msg_content))
        r2 = float(laji(msg_content))
        """" 判断是否政治敏感、判断是否是垃圾消息、判断是否情感积极，如果是垃圾消息给出垃圾消息的种类"""
        if r1 > 0.5:
            degree = ''
            if r1 > 0.9:
                degree = '极高,'
            elif r1 > 0.8:
                degree = '很高,'
            elif r1 > 0.7:
                degree = '较高,'
            else:
                degree = '轻度,'
            if sent > 0.5 :

                msg_body = '您在和' + msg_from + '的聊天中收到：' + '\n' + msg_content + '--政治敏感度：' \
                           + degree + '\t'+ '该消息是积极消息'+'\n'
                mychat.send_msg(msg_body, toUserName='filehelper')
                print(msg_content + '--政治敏感度：'+ degree + '\t' + '该消息是积极消息')
            else:
                msg_body='您在和' + msg_from + '的聊天中收到：' + '\n' + msg_content + '--政治敏感度：'\
                         + degree + '\t'+ '该消息是消极消息' + '\n'
                mychat.send_msg(msg_body, toUserName='filehelper')
                print(msg_content + '--政治敏感度：' + degree + '\t' + '该消息是消极消息')
        r = jieba.cut(msg_content)
        for ele in r:
            if ele in ['淘宝']:
                print('淘宝链接')
                msg_body = '您在和' + msg_from + '的聊天中收到：' + '\n' + msg_content + '--垃圾类别为：' + '淘宝链接' + '\n'
                mychat.send_msg(msg_body, toUserName='filehelper')
                exit()
            elif ele in ['支付宝']:
                msg_body = '您在和' + msg_from + '的聊天中收到：' + '\n' + msg_content + '--垃圾类别为：' + '支付宝链接' + '\n'
                mychat.send_msg(msg_body, toUserName='filehelper')
                print('支付宝链接')
                exit()
            elif ele in ['生发', '口红', '眼霜', '面膜', '雅诗兰黛', '精华' ]:
                msg_body = '您在和' + msg_from + '的聊天中收到：' + '\n' + msg_content + '--垃圾类别为：' + '广告类' + '\n'
                mychat.send_msg(msg_body, toUserName='filehelper')
                print('广告消息')
                exit()
            else:
                if r2 > 0.6:
                    msg_body = '您在和' + msg_from + '的聊天中收到：' + '\n' + msg_content + '--垃圾类别为：' + '色情类' + '\n'
                    mychat.send_msg(msg_body, toUserName='filehelper')
                    print(msg_content + '--垃圾敏感度：' + str(r2))
                    exit()

        if analyze(msg_content, 0):
            # print(msg_from)
            mychat.send(u'您可能在和“%s”的聊天中被询问私人信息，请注意防范 聊天内容为：\n\n%s' %
                        (msg_from, msg['Text']), toUserName='filehelper')
            exit()
        elif ifPersonalInfo(msg_content):
            mychat.send(u'您可能在和“%s”的聊天中泄露了私人信息，请注意防范 聊天内容为：\n\n%s\n\n请及时撤回' %
                        (msg_from, msg['Text']),toUserName='filehelper')
            exit()
    msg_information.update(
        {
            msg_id: {
                "msg_from": msg_from, "msg_time": msg_time,
                "msg_time_rec": msg_time_rec,
                "msg_type": msg["Type"],
                "msg_content": msg_content, "msg_share_url": msg_share_url
            }
        }
    )


##这个是用于监听是否有friend消息撤回
@mychat.msg_register(NOTE, isFriendChat=True, isGroupChat=True, isMpChat=True)
def information(msg):
    # 这里如果这里的msg['Content']中包含消息撤回和id，就执行下面的语句
    if '撤回了一条消息' in msg['Content']:
        # 在返回的content查找撤回的消息的id
        old_msg_id = re.search("\<msgid\>(.*?)\<\/msgid\>", msg['Content']).group(1)
        # 得到消息
        old_msg = msg_information.get(old_msg_id)
        print(old_msg)
        if len(old_msg_id) < 11:  # 如果发送的是表情包
            mychat.send_file(face_bug, toUserName='filehelper')
        else:  # 发送撤回的提示给文件助手
            msg_body = "【" \
                       + old_msg.get('msg_from') + " 撤回了 】\n" \
                       + old_msg.get("msg_type") + " 消息：" + "\n" \
                       + old_msg.get('msg_time_rec') + "\n" \
                       + r"" + old_msg.get('msg_content')
            # 如果是分享的文件被撤回了，那么就将分享的url加在msg_body中发送给文件助手
            if old_msg['msg_type'] == "Sharing":
                msg_body += "\n就是这个链接➣ " + old_msg.get('msg_share_url')
            # 将撤回消息发送到文件助手
            mychat.send_msg(msg_body, toUserName='filehelper')
            # 有文件的话也要将文件发送回去
            if old_msg["msg_type"] == "Picture" \
                    or old_msg["msg_type"] == "Recording" \
                    or old_msg["msg_type"] == "Video" \
                    or old_msg["msg_type"] == "Attachment":
                file = '@fil@%s' % (old_msg['msg_content'])
                mychat.send(msg=file, toUserName='filehelper')
                os.remove(old_msg['msg_content'])
            # 删除字典旧消息
            msg_information.pop(old_msg_id)
    # 在好友列表中查询发送信息的好友昵称
    msg_from = mychat.search_friends(userName=msg['FromUserName'])['NickName']

@mychat.msg_register([TEXT, PICTURE, FRIENDS, CARD, MAP,
                      SHARING, RECORDING, ATTACHMENT,
                      VIDEO], isGroupChat=True)
def handle_receive_msg(msg):
    global face_bug
    # 接受消息的时间
    msg_time_rec = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    msg_Actual_from = msg['ActualNickName']
    msg_from = msg_Actual_from
    msg_time = msg['CreateTime']  # 信息发送的时间
    msg_id = msg['MsgId']  # 每条信息的id
    msg_content = None  # 储存信息的内容
    msg_share_url = None  # 储存分享的链接，比如分享的文章和音乐
    print(msg['Type'])
    print(msg['MsgId'])
    # 如果发送的消息是文本或者好友推荐
    if msg['Type'] == 'Text' or msg['Type'] == 'Friends':
        msg_content = msg['Text']
        print(msg_content)
        s = SnowNLP(msg_content)
        sent = s.sentiments
        r1 = float(zhengzhi(msg_content))
        r2 = float(laji(msg_content))
        if r1 > 0.5 :
            degree = ''
            if r1 > 0.9:
                degree = '极高,'
            elif r1 > 0.8:
                degree = '很高,'
            elif r1 > 0.7:
                degree = '较高,'
            else:
                degree = '轻度,'

            if sent > 0.5 :
                msg_body = '您在和' + msg_from + '的聊天中收到：' + '\n' + msg_content + '--政治敏感度：' + \
                           degree + '\t'+ '该消息是积极消息'+'\n'
                mychat.send_msg(msg_body, toUserName='filehelper')
                exit()
            else:
                msg_body = '您在和' + msg_from + '的聊天中收到：' + '\n' + msg_content + '--政治敏感度：' \
                           + degree + '\t'+ '该消息是消极消息' + '\n'
                mychat.send_msg(msg_body, toUserName='filehelper')
                exit()
        r = jieba.cut(msg_content)
        for ele in r:
            if ele in ['淘宝']:
                print('淘宝链接')
                msg_body = '您在和' + msg_from + '的聊天中收到：' + '\n' + msg_content + '--垃圾类别为：' + '淘宝链接' + '\n'
                mychat.send_msg(msg_body, toUserName='filehelper')
                exit()
            elif ele in ['支付宝']:
                msg_body = '您在和' + msg_from + '的聊天中收到：' + '\n' + msg_content + '--垃圾类别为：' + '支付宝链接' + '\n'
                mychat.send_msg(msg_body, toUserName='filehelper')
                print('支付宝链接')
                exit()
            elif ele in ['生发', '口红', '眼霜', '面膜', '雅诗兰黛', '精华' ]:
                msg_body = '您在和' + msg_from + '的聊天中收到：' + '\n' + msg_content + '--垃圾类别为：' + '广告类' + '\n'
                mychat.send_msg(msg_body, toUserName='filehelper')
                print('广告消息')
                exit()
            else:
                if r2 > 0.6:
                    msg_body = '您在和' + msg_from + '的聊天中收到：' + '\n' + msg_content + '--垃圾类别为：' + '色情类' + '\n'
                    mychat.send_msg(msg_body, toUserName='filehelper')
                    print(msg_content + '--垃圾敏感度：' + str(r2))
                    exit()
        if analyze(msg_content, 0):
            # print(msg_from)
            mychat.send(u'您可能在和“%s”的聊天中被询问私人信息，请注意防范 聊天内容为：\n\n%s' %
                        (msg_from, msg['Text']), toUserName='filehelper')
            exit()
        elif ifPersonalInfo(msg_content):
            mychat.send(u'您可能在和“%s”的聊天中泄露了私人信息，请注意防范 聊天内容为：\n\n%s\n\n请及时撤回' %
                        (msg_from, msg['Text']), toUserName='filehelper')
            exit()
    face_bug = msg_content
    msg_information.update(
        {
            msg_id: {
                "msg_from": msg_from, "msg_time": msg_time, "msg_time_rec": msg_time_rec,
                "msg_type": msg["Type"],
                "msg_content": msg_content, "msg_share_url": msg_share_url
            }
        }
    )

##这个是用于监听是否有Group消息撤回
@mychat.msg_register(NOTE, isGroupChat=True, isMpChat=True)
def information(msg):
    # 这里如果这里的msg['Content']中包含消息撤回和id，就执行下面的语句
    if '撤回了一条消息' in msg['Content']:
        # 在返回的content查找撤回的消息的id
        old_msg_id = re.search("\<msgid\>(.*?)\<\/msgid\>", msg['Content']).group(1)
        old_msg = msg_information.get(old_msg_id)  # 得到消息
        print(old_msg)
        if len(old_msg_id) < 11:  # 如果发送的是表情包
            mychat.send_file(face_bug, toUserName='filehelper')
        else:  # 发送撤回的提示给文件助手
            msg_body = "【" \
                       + old_msg.get('msg_from') + " 群消息撤回提醒】\n" \
                       + " 撤回了 " + old_msg.get("msg_type") + " 消息：" + "\n" \
                       + old_msg.get('msg_time_rec') + "\n" \
                       + r"" + old_msg.get('msg_content')
            # 如果是分享的文件被撤回了，那么就将分享的url加在msg_body中发送给文件助手
            if old_msg['msg_type'] == "Sharing":
                msg_body += "\n就是这个链接➣ " + old_msg.get('msg_share_url')
            # 将撤回消息发送到文件助手
            mychat.send_msg(msg_body, toUserName='filehelper')
            # 有文件的话也要将文件发送回去
            if old_msg["msg_type"] == "Picture" \
                    or old_msg["msg_type"] == "Recording" \
                    or old_msg["msg_type"] == "Video" \
                    or old_msg["msg_type"] == "Attachment":
                file = '@fil@%s' % (old_msg['msg_content'])
                mychat.send(msg=file, toUserName='filehelper')
                os.remove(old_msg['msg_content'])
            # 删除字典旧消息
            msg_information.pop(old_msg_id)


if __name__ == '__main__':
    app.run()
