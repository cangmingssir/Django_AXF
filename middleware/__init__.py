# coding:utf-8
from django.shortcuts import redirect
from django.utils.deprecation import MiddlewareMixin


class Content(MiddlewareMixin):
    def process_request(self,request):
        path = request.path
        #判断当访问个人中心和购物车的时候，是否登录，存在token则已登录，不存在则没有登录
        #没有登录则跳转登录界面
        if path.find('/app/mine')==0 or path.find('/app/cart')==0:
            token = request.COOKIES.get('userToken')
            if not token:
                return redirect('/app/login')