# -*- coding:utf-8 -*-  
import re
import sys
import jieba
import jieba.posseg as pseg
import sys
try:
	reload(sys)
	sys.setdefaultencoding('utf8')
except:
	pass

def checkTel(sentence):#识别电话号码
	m = re.findall('(1[3578]\d{9})', sentence)
	if m is not None and len(m)>0:
		return True
	return False

def checkEmail(sentence):#识别邮箱
	m = re.findall('(([a-zA-Z0-9]+[_|\-|\.]?)*[a-zA-Z0-9]+\@([a-zA-Z0-9]+[_|\-|\.]?)*[a-zA-Z0-9]+(\.[a-zA-Z]{2,3})+)', sentence)		
	if m is not None and len(m)>0:
		return True
	return False

def checkID(sentence):#识别身份证号
	m = re.findall('([123456789]\d{5}((19)|(20))\d{2}((0[123456789])|(1[012]))((0[123456789])|([12][0-9])|(3[01]))\d{3}[Xx0-9])'\
	, sentence)
	if m is not None and len(m)>0:
		return True
	return False

def checkName(sentence):#识别个人姓名
	jiebaRes = pseg.cut(sentence)
	for tmp in jiebaRes:
		tmp = tmp.encode('utf-8')
		m = re.findall('(.*?)\/nr', str(tmp))
		if m is not None and len(m)>0:
			return True
	return False

def ifContainps(sentence):#匹配是否含有至少6个连续字母数字的组合，可能含有密码
	res = re.search(r'[a-zA-Z0-9]{6,}',sentence)
	if res:
		return True
	return False

def ifPersonalInfo(sentence):
	if(checkEmail(sentence)):
		return True
	elif(checkID(sentence)):
		return True
	elif(checkTel(sentence)):
		return True
	elif(ifContainps(sentence)):
		return True
	else:
		return False

def analyze(sentence, type):
	if type == 0:
		return analyzeCh(sentence)
	else:
		return analyzeEn(sentence)

zh_list = {u'钱', u'帐号', u'账户', u'银行卡', u'密码', u'中奖', u'工资'}
def analyzeCh(sentence):
	seg_list = jieba.cut(sentence, cut_all=True)
	for s in seg_list:
		if s in zh_list:
			return 1
	return 0

en_list = {'money', 'account', 'password','prize','bank'}
def analyzeEn(sentence):
	p = re.compile(r'\W+')
	seg_list = p.split(sentence)
	for s in seg_list:
		if s.lower() in en_list:
			return 1
	return 0

def analyzeJunk(sentence):
	seg_list = jieba.cut(sentence, cut_all = True)
	junk_list = {u'团购',u'红包',u'特价',u'劲爆'}
	for s in seg_list:
		if s in junk_list:
			return 1
	return 0

def groupNotice(sentence, keywords):
	flag = False
	for word in keywords:
		if word in sentence:
			flag = True
			break
	return flag


