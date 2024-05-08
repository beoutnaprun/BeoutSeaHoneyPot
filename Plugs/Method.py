import random
import datetime
import json
import Plugs.Database as db
import time





##################################################################
LOGINJSON = 'static/Home/data/user/loginlog.json'

##################################################################
width = 160
height = 50
"""
    创建图形验证码
"""

def getRandomColor():
    r = random.randint(0, 255)
    g = random.randint(0, 255)
    b = random.randint(0, 255)
    return (r, g, b)


def getRandomChar():
    random_num = "1"
    random_lower = "2"  # 小写字母a~z
    random_upper = "3"  # 大写字母A~Z
    a = "4"
    b = "5"
    c = "6"
    d = '7'
    random_char = random.choice([random_num, random_lower, random_upper, a, b, c, d])
    return random_char


def drawLine(draw):
    for i in range(5):
        x1 = random.randint(0, width)
        x2 = random.randint(0, width)
        y1 = random.randint(0, height)
        y2 = random.randint(0, height)
        draw.line((x1, y1, x2, y2), fill=getRandomColor())


def drawPoint(draw):
    for i in range(50):
        x = random.randint(0, width)
        y = random.randint(0, height)
        draw.point((x, y), fill=getRandomColor())

"""
    生成手机验证码 （添加接口调用发送）
"""
def GetRamdomSix():
    num = random.randint(100000,999999)
    return num

"""
    获取真实ip
    client_ip = request.META.get('REMOTE_ADDR')
"""
def GetIpAddress(request):
    client_ip = request.META.get('REMOTE_ADDR')
    return client_ip

"""
    获取事件
"""
def GetTimes():
    year = datetime.datetime.now().year
    month = datetime.datetime.now().month
    day = datetime.datetime.now().day
    hour = datetime.datetime.now().hour
    minute = datetime.datetime.now().minute
    second = datetime.datetime.now().second
    return f'{year}-{month}-{day}-{hour}:{minute}:{second}'

def GetTTimes():
    return time.time()

"""
    记录操作
"""
def logAttack(request,text):
    ipAddr = GetIpAddress(request)
    session_id = request.COOKIES.get('sessionid')
    request.session['ipaddr'] = ipAddr
    request.session['times'] = GetTimes()
    request.session['sessionid'] = session_id
    request.session['options'] = text
    db.InsertEx('attack','times,ipaddr,options,session',f"'{request.session.get('times')}','{request.session.get('ipaddr')}','{request.session.get('options')}','{request.session.get('sessionid')}'")

"""
    判断是否为空
"""
def isEmpty(string):
    if isinstance(string,str):
        if str =='' or str == '':
            return False
        return True
    elif isinstance(string,int) or isinstance(string,float):
        if string > 0 :
            return True
        return False
    elif isinstance(string,bool):
        return string
    elif isinstance(string,dict):
        if string == {}:
            return False
        return True
    elif isinstance(string,list):
        if string == []:
            return False
        return True
    elif string == None:
        return False


def ReadJson(filename):
    with open(filename,'r') as f:
        data = json.load(f)
    return data

def WriteJson(filename,context):
    try:
        with open(filename, 'w') as f:
            json.dump(context,f)
        return True
    except Exception as e:
        return False

"""
    "userName": "张三",
    "IP": "121.69.4.82",
    "status": "成功",
    "creationTime": "2018-12-02 07:30:52"
"""
def UpdateLoginLog(filename,userName,IP,status):
    try:
        dicts = ReadJson(filename)
        dicts['count'] = int(dicts['count']) + 1
        jsonContext = {
            'userName': userName,
            'IP':IP,
            'status':status,
            'creationTime':GetTimes()
        }
        dicts['data'].append(jsonContext)
        WriteJson(filename, dicts)
        return True
    except:
        return False

"""
    AdminSession
    True    校验失败
    False   校验成功
"""
def AdminSession(request):
    try:
        username = request.session.get('username')
        password = request.session.get('password')
        LoginTimes = request.session.get('LoginTimes')
        if GetTTimes() - LoginTimes >= 3600:
            return True
        data = db.SelectEx('admin', f"username = '{username}'")
        if isEmpty(data):
            if data[0][2] != password:
                return True
            else:
                return False
        else:
            return True
    except:
        return True



########################################################################################