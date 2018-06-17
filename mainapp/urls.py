
from django.urls import path

from mainapp import views

urlpatterns = [
    path("",views.home),
    path('market/<int:categoryid>/<int:childcid>/<int:sortid>',views.market),
    path('cart',views.cart),
    path('mine',views.mine),
    path('register',views.register),
    path('login',views.login),
    path('upload',views.upload),
    path('delectToken',views.delectToken),
    path('userNumber',views.userNumber),
    path('cart',views.cart),
    path('select/<int:cart_id>',views.selectCart),
    path('selectCnt/<int:id>',views.selectCnt),
    path('addselectCnt/<int:id>',views.addselectCnt),
    path('addgoodtoCart/<int:goodID>',views.addgoodtoCart),
    path('order/<str:num>',views.order),
    path('pay/<str:num>/<int:payType>',views.pay),
    path('selectOrder',views.selectOrder),
    path('waitpay',views.waitpay),
    path('waitgood',views.waitgood),
    path('suregood/<str:num>',views.suregood),
    path('useraddress',views.useraddress),
    path('deleteadre/<int:id>',views.deleteadre),
    path('defaultade/<int:id>',views.defaultade)
]
