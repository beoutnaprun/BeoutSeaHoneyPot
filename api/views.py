

from django.http import HttpResponse
import Plugs.Method as m
import Plugs.Database as db


def Login(request):
    if request.method == 'POST':
        phone = request.POST.get('phone')
        code = request.POST.get('code')
        if str(request.session.get('phoneCode')) != str(code):
            m.logAttack(request,f'{phone} 登录验证码错误')
            return HttpResponse('手机验证码错误')
        m.logAttack(request, f'{phone} 登录成功')
        return HttpResponse('暂无登录权限 请联系管理员授权')


def phoneSMS(request):
    if request.method == 'POST':
        phone = request.POST.get('phone')
        code = request.POST.get('code')
        print(phone)
        print(code)
        # 记录
        m.logAttack(request,f'{phone} - 登录 - 获取手机验证码')
        # 模拟事件
        session_code = request.session.get('ImgCode')
        if code != session_code:
            return HttpResponse('图形验证码错误')
        data = db.SelectEx('user',f"phone='{phone}'")
        if m.isEmpty(data):
            m.logAttack(request,'获取手机验证码')
            number = m.GetRamdomSix()
            request.session['phoneCode'] = number
            return HttpResponse(str(number))
        else:
            return HttpResponse('手机号不存在')


def phoneSMSReg(request):
    if request.method == 'POST':
        phone = request.POST.get('phone')
        code = request.POST.get('code')
        print(phone)
        print(code)
        # 记录
        m.logAttack(request,f'{phone} - 注册 - 获取手机验证码')
        # 模拟事件
        session_code = request.session.get('ImgCode')
        if code != session_code:
            return HttpResponse('图形验证码错误')
        data = db.SelectEx('user',f"phone='{phone}'")
        if m.isEmpty(data):
            return HttpResponse('手机号已存在')
        else:
            m.logAttack(request, '获取手机验证码')
            number = m.GetRamdomSix()
            request.session['phoneCode'] = number
            return HttpResponse(str(number))
