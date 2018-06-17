from django.db import models


# Create your models here.

class TopModel(models.Model):
    trackid = models.CharField(primary_key=True, max_length=10)
    img = models.CharField(max_length=300)
    name = models.CharField(max_length=50)

    class Meta:
        abstract = True


class TopWheel(TopModel):
    class Meta:
        db_table = "axf_wheel"  # 指定表名


class TopMenu(TopModel):
    position = models.IntegerField(default=1)

    class Meta:
        db_table = "axf_nav"  # 导航菜单表


class Topmustbuy(TopModel):
    class Meta:
        db_table = "axf_mustbuy"  # 必买菜单表


class TopShop(TopModel):
    position = models.IntegerField(default=1)

    class Meta:
        db_table = "axf_shop"  # 热销帮及商品分类


class TopMainShow(TopModel):
    categoryid = models.CharField(max_length=10)
    brandname = models.CharField(max_length=20)

    # img1 = models.CharField(max_length=300)
    # childcid1 = models.CharField(max_length=20)
    # productid1 = models.CharField(max_length=30)
    # longname1 = models.CharField(max_length=50)
    # price1 = models.CharField(max_length=10)
    # marketprice1 = models.CharField(max_length=10)
    #
    #
    # img2 = models.CharField(max_length=300)
    # childcid2 = models.CharField(max_length=20)
    # productid2 = models.CharField(max_length=30)
    # longname2 = models.CharField(max_length=50)
    # price2 = models.CharField(max_length=10)
    # marketprice2 = models.CharField(max_length=10)
    #
    # img3 = models.CharField(max_length=300)
    # childcid3 = models.CharField(max_length=20)
    # productid3 = models.CharField(max_length=30)
    # longname3 = models.CharField(max_length=50)
    # price3 = models.CharField(max_length=10)
    # marketprice3 = models.CharField(max_length=10)

    class Meta:
        db_table = "axf_mainshow"


class MainChild(models.Model):
    img = models.CharField(max_length=300)
    childcid = models.CharField(max_length=20)
    productid = models.CharField(max_length=30)
    longname = models.CharField(max_length=50)
    price = models.CharField(max_length=10)
    marketprice = models.CharField(max_length=10)

    class Meta:
        abstract = True


class TopMainChild(MainChild):
    topMainShow = models.ForeignKey(TopMainShow, on_delete=models.CASCADE)

    class Meta:
        db_table = "axf_mainchild"


# 食品分类模型
class FoodTypes(models.Model):
    typeid = models.CharField(max_length=10)
    typename = models.CharField(max_length=20)
    typesort = models.IntegerField(default=1)
    childtypenames = models.CharField(max_length=150)

    class Meta:
        db_table = "axf_foodtypes"


#商品模型类
class Goods(models.Model):
    #商品id
    productid = models.CharField(max_length=10, primary_key=True)
    #商品图片
    productimg = models.CharField(max_length=300)
    #商品名称
    productname = models.CharField(max_length=100)
    #商品长名称
    productlongname = models.CharField(max_length=100)
    #是否精选
    isxf = models.BooleanField(default=1)
    #是否买一送一
    pmdesc = models.IntegerField(default=1)
    #规格
    specifics = models.CharField(max_length=100)
    #价格
    price = models.DecimalField(default=0.0, max_digits=10, decimal_places=2)
    #超市价格
    marketprice = models.DecimalField(default=0.0, max_digits=10, decimal_places=2)
    #组id
    categoryid = models.IntegerField(default=0)
    #子类组id
    childcid = models.IntegerField(default=0)
    #子类组名称
    childcidname = models.CharField(max_length=100)
    #详情页id
    dealerid = models.CharField(max_length=20)
    #库存
    storenums = models.IntegerField(default=1)
    #销量
    productnum = models.BigIntegerField(default=0)

    class Meta:
        db_table = 'axf_goods'


class UserManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(state=True)


class User(models.Model):
    usernumber = models.CharField(max_length=20)
    username = models.CharField(max_length=20)
    userpasswd = models.CharField(max_length=100)
    userphone = models.CharField(max_length=11)
    useraaddress = models.CharField(max_length=100)
    userphoto = models.ImageField(upload_to='userphoto', null=True)
    token = models.CharField(max_length=200, null=True, default='')
    money = models.DecimalField(max_digits=10,decimal_places=2,default=0)
    state = models.BooleanField(default=True, verbose_name='用户状态')

    objects = UserManager()

    class Meta:
        db_table = 'axf_user'

    def toDict(self):
        return {'usernumber': self.usernumber,
                'username': self.username,
                'userpasswd': self.userpasswd,
                'userphone': self.userphone,
                'userphoto': self.userphoto.name,
                'useraaddress': self.useraaddress,
                'token': self.token}

    def delete(self, using=None, keep_parents=False):
        self.state = False
        self.save()
        return 'success'


# 收件地址模型
class DeliveryAddress(models.Model):
    name = models.CharField(max_length=20, verbose_name='收件人')
    phone = models.CharField(max_length=12, verbose_name='收件人手机号码')
    address_detail = models.TextField(default='', verbose_name='收货地址')

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    status=models.BooleanField(default=True)
    only=models.IntegerField(default=0)
    class Meta:
        db_table = 'axf_address'


# 购物车模型
class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    goods = models.ForeignKey(Goods, on_delete=models.CASCADE)
    cnt = models.IntegerField(default=1)

    # 是否被选中
    isSelected = models.BooleanField(default=True)

    class Meta:
        db_table = 'axf_cart'

#订单模型
class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    # 订单的收货地址
    orderAddress = models.ForeignKey(DeliveryAddress, on_delete=models.SET_NULL, null=True)
    # 订单的单号
    orderNum = models.CharField(primary_key=True, max_length=50, verbose_name='订单号')

    # 订单的总金额
    orderPrice = models.DecimalField(max_digits=10, decimal_places=2,default=0)

    #支付方式
    pay_types=((0,'余额'),(1,'支付宝'),(2,'微信'))
    payType=models.IntegerField(choices=pay_types,default=0)

    @property
    def payTypeName(self):
        return self.pay_types[self.payType][1]

    # 订单的支付状态
    pay_states = ((0, '待支付'), (1, '已支付'), (2, '正在支付中'), (3, '已退款'))
    payState = models.IntegerField(choices=pay_states,default=0)

    @property
    def payStatesName(self):
        return self.pay_states[self.payState][1]

    # 订单的派送状态
    order_states = ((0, '待派送'), (1, '已派送'), (2, '已送达'), (3, '已签售'), (4, '拒收'), (5, '未到达'))
    orderState = models.IntegerField(choices=order_states,default=0)

    @property
    def orderStateName(self):
        return self.order_states[self.orderState][1]

    # 生成订单时间
    orderTime = models.DateTimeField(auto_now_add=True)

    # 订单修改时间
    orderLastTime = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'axf_order'


#订单明细
class OrderGoogs(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    goods =models.ForeignKey(Goods,on_delete=models.SET_NULL,null=True)
    cnt = models.IntegerField(default=1)
    price = models.DecimalField(default=0,max_digits=10,decimal_places=2,verbose_name='小计')

    class Meta:
        db_table='axf_order_goods'