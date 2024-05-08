from django.shortcuts import render, redirect
from django.http import HttpResponse
import Plugs.Method as m
import Plugs.Database as db
import json


def login(request):
    if request.method == 'GET':
        if m.AdminSession(request):
            return render(request, 'webAdmin/index.html')
        else:
            return redirect('webAdmin/Index')
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        data = db.SelectEx('admin', f"username='{username}'")
        if m.isEmpty(data) == False:
            print(1111)
            m.UpdateLoginLog(m.LOGINJSON, username, m.GetIpAddress(request), f"登陆失败 {password}")
            return HttpResponse('用户名/密码错误')
        if password != data[0][2]:
            m.UpdateLoginLog(m.LOGINJSON, username, m.GetIpAddress(request), f"登陆失败 {password}")
            return HttpResponse('用户名/密码错误')
        request.session['username'] = username
        request.session['password'] = password
        request.session['LoginTimes'] = m.GetTTimes()
        # 写入登录日志
        m.UpdateLoginLog(m.LOGINJSON, username, m.GetIpAddress(request), f"登陆成功")
        return HttpResponse('Success')


def index(request):
    if m.AdminSession(request):
        return redirect('/webAdmin')
    if request.method == 'GET':
        return render(request, 'webAdmin/Home.html')

def LoginOut(request):
    if m.AdminSession(request):
        return redirect('/webAdmin')
    request.session.clear()
    return redirect('/webAdmin')


def view(request):
    if m.AdminSession(request):
        return redirect('/webAdmin')
    if request.method == 'GET':
        name = request.GET.get('act')
        if name == 'webAdmin/home/index.html':
            # 查询访问量
            data = db.SelectEx('attack')
            udata = db.SelectEx('user')
            return render(request, name, {"fwNumber": len(data), "UserNumber": len(udata)})
        else:
            print(f'Backed Access -->> {name}')
            attackTab = AttackTable(request)
            webconfig = WebConfig(request)
            return render(request, name, {'acctackTable': attackTab,'webconfig': webconfig})

def Edit_Passwd(request):
    if m.AdminSession(request):
        return redirect('/webAdmin')
    if request.method == 'POST':
        oldpwd = request.POST.get('oldpwd')
        pwd1 = request.POST.get('pass1')
        pwd2 = request.POST.get('pass2')
        if pwd1 != pwd2:
            return HttpResponse('两次密码不一致请 检查后输入')
        data = db.SelectEx('admin',f"username='admin'")
        if oldpwd != data[0][2]:
            return HttpResponse('旧密码错误 请检查后输入')
        ret = db.UpdateEx('admin',f"password='{pwd1}'")
        if ret:
            return HttpResponse('Success 修改成功 请重新登录')
        else:
            return HttpResponse('Error SQL error ')




'''
    删除攻击画像
'''
def Delete_Attack(request):
    if m.AdminSession(request):
        return redirect('/webAdmin')
    if request.method == 'GET':
        id = request.GET.get('id')
        ret = db.DeleteEx('attack',f'id={id}')
        if ret == True:
            return HttpResponse('Success')
        else:
            return HttpResponse('SQL error')

'''
    删除攻击人员账号
'''
def Delete_User(request):
    if m.AdminSession(request):
        return redirect('/webAdmin')
    if request.method == 'GET':
        id = request.GET.get('id')
        ret = db.DeleteEx('User',f'id={id}')
        if ret == True:
            return HttpResponse('Success')
        else:
            return HttpResponse('SQL error')

'''
    网站设置页面
    webtitle:webtitle,
    url:url,
    status:status,
    homeTitle:homeTitle,
    copy:copy,
'''

def WebConfig(request):
    if m.AdminSession(request):
        return redirect('/webAdmin')
    if request.method == 'GET':
        data = db.SelectEx('config' ,f"key='webconfig'")
        return json.loads(data[0][1])
    if request.method == 'POST':
        webtitle = request.POST.get('webtitle')
        url = request.POST.get('url')
        status = request.POST.get('status')
        homeTitle = request.POST.get('homeTitle')
        copy = request.POST.get('copy')
        jsons = {
            'title':webtitle,
            'url':url,
            'status':status,
            'homeTitle':homeTitle,
            'copy':copy,
        }
        serJson = json.dumps(jsons)
        ret = db.UpdateEx('config',f"value='{serJson}'",'key=\'webconfig\'')
        if ret:
            return HttpResponse('Seccess')
        else:
            return HttpResponse('Error SQL error')





'''
    攻击画像页面
'''
def AttackTable(request):
    ipaddr = request.GET.get('ipaddr')
    if m.isEmpty(ipaddr):
        return SelectIpAddress(request)
    page = request.GET.get('page')
    try:
        page = int(page)
    except:
        page = 0
    if m.isEmpty(page) == False:
        page = 0
    # 获取攻击画像
    accAllData = db.SelectEx(f'attack ORDER BY id LIMIT 10 OFFSET {page * 10}')
    accResult = {}
    accResultData = []
    accAllDatas = db.SelectEx(f'attack')
    for accData in accAllData:
        appData = {
            'id':accData[0],
            'times': accData[1],
            'ipAddr': accData[2],
            'options': accData[3],
        }
        accResultData.append(appData)
    UserAllData = db.SelectEx(f'user')
    accUserData = []
    for accData in UserAllData:
        userData = {
            'id': accData[0],
            'phone': accData[1],
            'password': accData[2],
            'ipaddr': accData[3],
        }
        accUserData.append(userData)
    accResult['data'] = accResultData
    accResult['Udata'] = accUserData
    accResult['page'] = page + 1
    accResult['pageNumber'] = f'<input style="display:none" value="{page}"><a href="/api/view?act=webAdmin/home/attack.html&page={page - 1}">上一页</a>'
    pageFlag = (len(accAllDatas) % 10)
    pageNumber = int(len(accAllDatas) / 10)
    if pageFlag != 0:
        pageNumber += 1
    for i in range(0, pageNumber):
        accResult[
            'pageNumber'] += f"<span style='width:10px;'><a href = '/api/view?act=webAdmin/home/attack.html&page={str(i + 1)}'>&nbsp;&nbsp;&nbsp;{str(i + 1)}&nbsp;&nbsp;&nbsp;</a></span>"
    accResult['pageNumber'] += f'<a href="/api/view?act=webAdmin/home/attack.html&page={page + 1}">下一页</a>'
    return accResult

def SelectIpAddress(request):
    ipaddr = request.GET.get("ipaddr")
    accSelectData = db.SelectEx('attack',f'ipaddr="{ipaddr}"')
    accResultData = []
    for accData in accSelectData:
        appData = {
            'id': accData[0],
            'ipAddr': accData[2],
            'times': accData[1],
            'options': accData[3],
        }
        accResultData.append(appData)
    accResult = {}
    accResult['data'] = accResultData
    return accResult