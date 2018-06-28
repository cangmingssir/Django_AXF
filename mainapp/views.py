import hashlib
import os
import uuid
import time
from datetime import datetime

from django.db.models import F
from django.http import JsonResponse
from django.shortcuts import render, redirect

from django.views.decorators.csrf import csrf_exempt

from AXF_Project import settings
from mainapp.models import *


def home(request):
    topshop = TopShop.objects.all().order_by('position')
    topshop1 = topshop[0]
    topshop2 = topshop[1:3]
    topshop3 = topshop[3:7]
    topshop4 = topshop[7:11]
    print("show信息", TopMainShow.objects.all())

    mainList = TopMainShow.objects.all()

    return render(request, 'home.html',
                  {'title': '主页',
                   'topWheels': TopWheel.objects.all(),
                   'topMenus': TopMenu.objects.all().order_by('position'),
                   'topMustBuys': Topmustbuy.objects.all(),
                   'topshop1': topshop1,
                   'topshop2': topshop2,
                   'topshop3': topshop3,
                   'topshop4': topshop4,
                   'topMainShows': mainList})


def market(request, categoryid=0, childcid=0, sortid=0):
    goodsList = None
    # 获取所有的子类型
    childTypes = []

    sortColumn = 'productid'  # 设定排序的列
    if sortid == 1:
        sortColumn = '-price'  # 价格最高排
    elif sortid == 2:
        sortColumn = 'price'  # 价格最低排
    elif sortid == 3:
        sortColumn = '-productnum'  # 销量最高

    if categoryid:
        # 获取所有的子类型
        # 全部分类:0#酸奶乳酸菌:103537#牛奶豆浆:103538#面包蛋糕:103540
        cTypes = FoodTypes.objects.filter(typeid=categoryid).last().childtypenames
        cTypes = cTypes.split('#')
        for cType in cTypes:
            cType = cType.split(":")
            childTypes.append({'name': cType[0], "id": cType[1]})

        if childcid:
            goodsList = Goods.objects.filter(categoryid=categoryid, childcid=childcid).order_by(sortColumn)
        else:
            goodsList = Goods.objects.filter(categoryid=categoryid).order_by(sortColumn)
    else:
        goodsList = Goods.objects.all().order_by(sortColumn)[0:20]

    print(FoodTypes.objects.all())
    return render(request, 'market.html',
                  {'title': '闪购页面',
                   "foodTypes": FoodTypes.objects.all().order_by('typesort'),
                   "goodsList": goodsList,
                   'categoryid': str(categoryid),
                   'childTypes': childTypes,
                   'childcid': str(childcid),
                   'sortid': sortid})


# 购物车
def cart(request):
    # 获取登录用户id
    user_id = request.session.get('user_id')
    print('id:', user_id)
    # 查询当前用户的默认收货信息
    deliveryAddress = DeliveryAddress.objects.filter(user_id=user_id).get(only=1)
    print('收货地址', deliveryAddress)
    # 查询当前用户购物车中的商品信息
    carts = Cart.objects.filter(user_id=user_id)
    print('商品信息', carts)
    totalprice = 0  # 计算总价格
    for cart in carts:
        if cart.isSelected:
            totalprice += cart.goods.marketprice * cart.cnt
        print()
    return render(request, 'cart.html',
                  {'title': '购物车界面',
                   'myAddress': deliveryAddress,
                   'cards': carts,
                   'totalprice': totalprice})


def mine(request):
    print("登录", request.COOKIES.get('userToken'))
    if not request.COOKIES.get('userToken'):
        return redirect('/app/login')
    username = request.session.get('username', '未登录')
    token = request.COOKIES.get('userToken')

    user = User.objects.filter(token=token).last()

    return render(request, 'mine.html',
                  {'title': '个人中心',
                   'username': username,
                   'navs': getMyOrderNav(),
                   'menus': getMyOrderMenu(),
                   'loginuser': user})


def getMyOrderNav():
    navs = []

    navs.append({'name': '待付款', 'icon': 'glyphicon glyphicon-usd ', 'id': 'waitpay'})
    navs.append({'name': '待收货', 'icon': 'glyphicon glyphicon-envelope ', 'id': 'waitgood'})
    navs.append({'name': '待评价', 'icon': 'glyphicon glyphicon-pencil ', 'id': 'waitassess'})
    navs.append({'name': '退款/售后', 'icon': 'glyphicon glyphicon-retweet ', 'id': 'aftersale'})
    return navs


def getMyOrderMenu():
    menus = []
    menus.append({'name': '积分商城', 'icon': 'glyphicon glyphicon-bullhorn', 'id': 'story'})
    menus.append({'name': '优惠卷', 'icon': 'glyphicon glyphicon-credit-card', 'id': 'coupon'})
    menus.append({'name': '客服/反馈', 'icon': 'glyphicon glyphicon-phone-alt', 'id': 'customerService'})
    menus.append({'name': '收货地址', 'icon': 'glyphicon glyphicon-import', 'id': 'useraddress'})
    menus.append({'name': '关于我们', 'icon': 'glyphicon glyphicon-asterisk', 'id': 'aboutOut'})

    return menus


def newToken(userName):
    # uuid+用户名
    md5 = hashlib.md5()
    md5.update((str(uuid.uuid4()) + userName).encode())
    return md5.hexdigest()


def crypyt(pwd, cryptName='md5'):
    md5 = hashlib.md5()
    md5.update(pwd.encode())
    return md5.hexdigest()


def register(request):
    if request.method == 'GET':
        return render(request, 'register.html')
    user = User()
    user.usernumber = request.POST.get('number')
    user.userpasswd = crypyt(request.POST.get('passwd'))
    user.userphone = request.POST.get('phone')
    user.useraaddress = request.POST.get('useraddress')
    user.username = request.POST.get('username')
    # 设置用户的token
    user.token = newToken(user.username)
    user.save()

    # 将token设置到cookie中
    resp = redirect('/app/mine')
    resp.set_cookie('userToken', user.token)
    return resp


@csrf_exempt  # 不做csrf_token验证
def upload(req):
    msg = {}
    cookie_token = req.COOKIES.get('userToken')
    if not cookie_token:
        msg['state'] = 'fail'
        msg['msg'] = '请登录'
        msg['code'] = '201'
    else:
        qs = User.objects.filter(token=cookie_token)
        if not qs.exists():
            msg['state'] = 'fail'
            msg['msg'] = '登录失效，请重新登录'
            msg['code'] = '202'
        else:
            # 开始上传
            uploadFile = req.FILES.get('img')
            saveFileName = newFileName(uploadFile.content_type)
            saveFilePath = os.path.join(settings.MEDIA_ROOT, saveFileName)

            # 将上传文件的数据分段写入到目标文件（存放在当前服务端）
            with open(saveFilePath, 'wb') as f:
                for part in uploadFile.chunks():
                    f.write(part)
                    f.flush()
            # 将上传文件的路径更新到用户
            qs.update(userphoto=saveFileName)
            # print(type(qs.last().toDict['userphoto']))
            msg['state'] = 'ok'
            msg['msg'] = '上传成功'
            msg['code'] = '200'
            msg['path'] = qs.last().userphoto.name

    return JsonResponse(msg)


def newFileName(contentType):
    fileName = crypyt(str(uuid.uuid4()))
    extName = '.jpg'
    if contentType == 'image/png':
        extName = '.png'
    return fileName + extName


def login(request):
    if request.method == 'GET':
        return render(request, 'login.html')

    usernumber = request.POST.get('number')
    userpasswd = request.POST.get('passwd')
    user = User.objects.filter(usernumber=usernumber, userpasswd=crypyt(userpasswd))
    if user.exists():
        print("用户", user.last().username)
        user.last().token = newToken(user.last().username)
        user.last().save()
        print("token", user.last().token)
        resp = redirect('/app/mine')
        request.session['user_id'] = user.last().id
        resp.set_cookie('userToken', user.last().token)
        return resp
    else:
        return render(request, 'login.html',
                      {'error': '您输入的用户名或密码有误'})


def delectToken(req):
    resp = redirect('/app/login')
    resp.delete_cookie('userToken')
    req.session.clear()
    return resp


@csrf_exempt
def userNumber(request):
    usernumber = request.POST.get('usermuber')
    qs = User.objects.filter(usernumber=usernumber)
    print("存在", qs.exists())
    if qs.exists():
        return JsonResponse({'msg': 200})
    else:
        return JsonResponse({'msg': 101})


# 购物车选择商品
def selectCart(request, cart_id):
    if cart_id == 0 or cart_id == 9999:  # 0为全选，-1为取消全选
        # 全部更新
        carts = Cart.objects.filter(user_id=request.session.get('user_id'))
        carts.update(isSelected=True if cart_id == 0 else False)
        totalPrice = 0  # 统计全选时的总价格
        if cart_id == 0:
            for cart in carts:
                totalPrice += cart.cnt * cart.goods.marketprice
        return JsonResponse({'price': totalPrice, 'status': 200})

    data = {'status': 200, 'price': 1000}
    try:
        cart = Cart.objects.get(id=cart_id)
        cart.isSelected = not cart.isSelected
        cart.save()
        data['price'] = cart.cnt * cart.goods.marketprice
        data['isSelected'] = cart.isSelected
    except:
        data['status'] = 300
        data['price'] = 0

    return JsonResponse(data)


# 购物车减去商品时执行
def selectCnt(request, id):
    data = {}
    cart = Cart.objects.get(id=id)
    print('购物', cart)
    cart.cnt -= 1
    cart.save()
    print(cart.cnt)
    data['isSelected'] = cart.isSelected
    data['price'] = cart.goods.marketprice
    return JsonResponse(data)


# 购物车增加商品时执行
def addselectCnt(request, id):
    data = {}
    cart = Cart.objects.get(id=id)
    # print('购物',cart)
    cart.cnt += 1
    cart.save()
    data['isSelected'] = cart.isSelected
    data['price'] = cart.goods.marketprice
    return JsonResponse(data)


# 购物页面点击+号将商品添加至购物车中执行
def addgoodtoCart(request, goodID):
    data = {}
    user_id = request.session.get('user_id')
    good = Goods.objects.get(productid=goodID)
    if good.storenums < 1:
        print(40404040440)
        data['status'] = 404
        data['msg'] = '该商品库存为0，无法购买'
        return JsonResponse(data)
    carts = Cart.objects.filter(goods_id=goodID)
    if carts.exists():
        carts.update(cnt=F('cnt') + 1)
        # carts.last().save()
        data['status'] = 400
        data['cnt'] = carts.last().cnt
        return JsonResponse(data)
    else:
        cart = Cart()
        cart.cnt = 1
        cart.goods_id = goodID
        cart.user_id = user_id
        cart.save()
        data['status'] = 400
        data['cnt'] = cart.cnt
        return JsonResponse(data)


def createOrderNum():  # 生成订单号
    orderNum = '0029' + str(time.time()).replace('.', '')[-10:]
    return orderNum


# 订单模型
def order(request, num):
    order = None
    # 新建订单
    if num == '0':
        user_id = request.session.get('user_id')
        if not user_id:  # 如果用户没有登录，则进入登录界面,防止通过网址直接访问
            return render(request, '404.html',
                          {'status': 404,
                           'msg': '您未登录,请登录'})
        # 下订单
        order = Order()
        order.user_id = user_id
        # 获取用户的第一个收货地址作为默认地址
        order.orderAddress_id = User.objects.get(pk=user_id).deliveryaddress_set.first().pk  # pk指表的主键例
        # 设置订单号
        order.orderNum = createOrderNum()
        # order.save()    #保存订单
        # 设置订单金额
        # 1.查询当前用户下购物车中所有选择的商品
        carts = Cart.objects.filter(isSelected=True, user_id=user_id)

        if carts.count() == 0:
            return redirect('/app/cart')
        # 2.统计订单的总金额和将商品插入到订单明细页面中
        order.orderPrice = 0
        order.save()
        for cart in carts:
            order.orderPrice += cart.cnt * cart.goods.marketprice

            # 创建订单明细对象
            ordergoods = OrderGoogs()
            ordergoods.order_id = order.orderNum
            ordergoods.goods_id = cart.goods.pk
            ordergoods.cnt = cart.cnt
            ordergoods.price = cart.cnt * cart.goods.marketprice
            # order.ordergoogs_set.add(ordergoods)
            ordergoods.save()
        # 保存订单
        order.save()  # 更新订单的总额
        carts.delete()  # 删除购物车中的已购买的商品

    # 查询订单
    else:
        order = Order.objects.get(pk=num)
    return render(request, 'order.html',
                  {'title': '我的订单',
                   'order': order})


# 支付处理
def pay(request, num, payType=0):
    print('pay支付:', num)
    try:
        order = Order.objects.get(pk=num)
        order.payType = payType
        # 必须要登录
        users = User.objects.filter(pk=request.session.get('user_id'))

        if not users.exists():
            return render(request, '404.html',
                          {'status': 404,
                           'msg': '您未登录,请登录'})
        # 判断用户余额是否足够支付
        user = users.last()
        print('用户余额：', user.money)
        print('商品金额', order.orderPrice)
        if user.money < order.orderPrice:
            return JsonResponse({'status': 'fail',
                                 'msg': '余额不足'})
        else:
            user.money -= order.orderPrice
            user.save()
            order.payState = 1  # 已支付
            order.save()
            # 减去库存量
            # 优化业务：在添加到购物车时，判断商品的库存量，如果不足，则提醒
            for item in order.ordergoogs_set.all():
                goods = item.goods
                goods.productnum += item.cnt  # 销售量
                goods.storenums -= item.cnt  # 库存量
                goods.save()
    except:
        return JsonResponse({'status': 'fail',
                             'msg': '支付失败'})
    return JsonResponse({'status': 'ok',
                         'msg': '支付成功'})


# 全部订单界面
def selectOrder(request):
    orders = Order.objects.all().order_by('payState')
    ordert = []
    for order in orders:
        order.orderTime = order.orderTime.strftime('%Y-%m-%d %H:%M:%S')
        order.save()
        ordert.append(order)
    print(ordert)
    data = 1
    return render(request, 'selectOrder.html',
                  {'orders': ordert,
                   'data': data})


# 待支付
def waitpay(request):
    data = 2
    orders = Order.objects.filter(payState=0)
    ordert = []
    for order in orders:
        order.orderTime = order.orderTime.strftime('%Y-%m-%d %H:%M:%S')
        order.save()
        ordert.append(order)
    return render(request, 'selectOrder.html',
                  {'orders': ordert,
                   'data': data})


# 待签收
def waitgood(request):
    orders = Order.objects.filter(payState=1, orderState__in=(0, 1, 2, 4, 5)).order_by('-orderState')
    ordert = []
    for order in orders:
        order.orderTime = order.orderTime.strftime('%Y-%m-%d %H:%M:%S')
        order.save()
        ordert.append(order)
    return render(request, 'waitgood.html',
                  {'orders': ordert})


# 确认收货
def suregood(request, num):
    order = Order.objects.get(orderNum=num)
    order.orderState = 3
    order.save()

    return JsonResponse({'msg': '确认收货成功，感谢您的购买！'})


# 收货地址管理
def useraddress(request):
    user_id = request.session.get('user_id')
    deliveryAddress = DeliveryAddress.objects.filter(user_id=user_id, status=1).order_by('-only')
    print(deliveryAddress.first().only)
    return render(request, 'useraddress.html',
                  {'deliveryAddress': deliveryAddress})


# 删除收货地址
def deleteadre(request, id):
    try:
        deliveryAddress = DeliveryAddress.objects.get(id=id)
        if deliveryAddress.only == 1:  # 判断该地址是否为默认地址
            print('是默认')
            deliveryAddress.only = 0
            deliveryAddress.status = 0
            deliveryAddress.save()
            # 如果要删除的地址为默认地址，则设置其他地址为默认地址
            newdelADD = DeliveryAddress.objects.filter(status=1).first()
            newdelADD.only = 1
            newdelADD.save()

        deliveryAddress.status = 0
        deliveryAddress.save()

    except:
        return render(request, '404.html',
                      {'status': 404,
                       'msg': '未知错误'})

    return JsonResponse({'msg': '删除成功！'})


# 设置默认收货地址
def defaultade(request,id):
    try:
        deliveryAddress = DeliveryAddress.objects.get(id=id)
        if deliveryAddress.only == 1:  # 判断该地址是否为默认地址
            return JsonResponse({'msg':'亲，这个就是默认地址'})
        onlyaddress=DeliveryAddress.objects.get(only=1)
        onlyaddress.only=0
        onlyaddress.save()
        deliveryAddress.only=1
        deliveryAddress.save()
    except:
        return render(request, '404.html',
                      {'status': 404,
                       'msg': '未知错误'})
    return JsonResponse({'msg':'默认地址设置成功'})
