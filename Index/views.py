# Index - Views



# from django.http import HttpResponse
from django.shortcuts import render
from django.http import HttpResponse
from PIL import Image, ImageDraw, ImageFont
import Plugs.Method as m
import Plugs.Database as db
import os,io,json



# 图片宽高
width = 160
height = 50
from pathlib import Path
# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

def index_view(request):
    if request.method == 'GET':
        # 记录
        m.logAttack(request,"登录页面访问")
        a = db.SelectEx('config',"key='webconfig'")
        config = json.loads(a[0][1])
        if config['status'] == '1':
            return render(request, 'index.html',{'config':config})
        else:
            return page_not_found(request,'')

def register_view(request):
    if request.method == 'GET':
        m.logAttack(request, "访问注册页面")
        return render(request, 'Reg.html')
    elif request.method == 'POST':
        phone = request.POST.get('phone')
        code = request.POST.get('code')
        passwd1 = request.POST.get('passwd1')
        passwd2 = request.POST.get('passwd2')
        if passwd1 != passwd2:
            m.logAttack(request, f"{phone}用户注册 两次密码不一致:{passwd1}-{passwd2}")
            return HttpResponse("两次密码不一致请检查")
        # 校验code
        if str(request.session.get('phoneCode')) != str(code):
            m.logAttack(request, f"{phone}用户注册 手机验证码错误:{str(request.session.get('phoneCode'))}-{str(code)}")
            return HttpResponse("手机验证码错误")
        # 手机号写入数据库
        ret = db.InsertEx('user','phone,password,ipAddr',f'"{phone}","{passwd1}","{m.GetIpAddress(request)}"')
        if ret:
            m.logAttack(request, f"{phone}用户注册成功 password:{passwd1}")
            request.session['phoneCode'] = ""
            return HttpResponse("注册成功请前往登录")
        else:
            return HttpResponse("注册失败数据库错误")



def index_captcha(request):
    if request.method == 'GET':
        bg_color = m.getRandomColor()
        # 创建一张随机背景色的图片
        img = Image.new(mode="RGB", size=(width, height), color=bg_color)
        # 获取图片画笔，用于描绘字
        draw = ImageDraw.Draw(img)
        # 修改字体
        font_path = os.path.join(BASE_DIR, 'static', 'fonts', 'Dengb.ttf')
        font = ImageFont.truetype(font=font_path,
                                  size=40)  # Lato-BlackItalic.ttf   Linux中的字体样式  Dengb.ttf Windows中的字体样式
        a = ""
        for i in range(5):
            # 随机生成5种字符+5种颜色
            random_txt = m.getRandomChar()
            txt_color = m.getRandomColor()
            # 避免文字颜色和背景色一致重合
            while txt_color == bg_color:
                txt_color = m.getRandomColor()
            a += random_txt

            # 根据坐标填充文字
            draw.text((10 + 30 * i, 3), text=random_txt, fill=txt_color, font=font)
        request.session['ImgCode'] = a
        # 画干扰线点
        m.drawLine(draw)
        m.drawPoint(draw)

        # 将图像数据保存到内存中，而不是写入文件
        image_stream = io.BytesIO()
        img.save(image_stream, format="png")
        image_stream.seek(0)
        # 创建响应对象，并将图像数据写入响应
        response = HttpResponse(image_stream.read(), content_type='image/png')

        return response





def page_not_found(request, exception):
    return render(request, '404.html')