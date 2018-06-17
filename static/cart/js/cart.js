$(function () {
    //给是否选择购买的span添加点击事件
    $('.isChose').click(function () {
        console.log('chose-->', this);
        //获取当前Element的第一个子控件
        var spanChild = $(this).children().first();
        var id = spanChild.attr('id');  //获取span对象的id值
        if (spanChild.text().trim() == '') {
            spanChild.text('√');    //选择，通过text向span中写内容
            console.log('选择', id);
        } else {
            spanChild.text('');     //取消选择
            console.log('取消选择', id);
        }
        //更新后台
        //json请求,function是回调函数
        $.getJSON('/app/select/' + id, function (data) {
            console.log(data);
            if (data.status == 200) {
                //选择购物车总价格Element
                var tp = $('#totalPrice').text().trim();
                console.log('--totalPrice--', parseFloat(tp));
                if (data.isSelected) {
                    //选择
                    $('#totalPrice').text((parseFloat(tp) + parseFloat(data.price)))
                } else {
                    //取消选择
                    $('#totalPrice').text((parseFloat(tp) - parseFloat(data.price)))

                }
            }
        });
        checkAllChose()

    });
    checkAllChose();
    //跳转至支付订单页面
    $('#toOrder').click(function () {
        window.open('/app/order/0', target = '_self');
    });


    //全部选择或取消选择
    $('#allChose').click(function () {
        var span = $(this).children().first();
        console.log($('.isChose :first-child'));
        id = 0;
        if (span.text().trim() == '') {
            span.text('√');
            $('.isChose :first-child').text('√');
            id = 0
        }

        else {
            span.text('');
            $('.isChose :first-child').text('');
            id = 9999
        }

        //更新后台
        $.getJSON('/app/select/' + id, function (data) {
            //data={status:200,price:0}
            // if (data.allSelected){
            $('#totalPrice').text(data.price)
            // }
        })
    });

    //在购物车的商品的-号点击事件
    $('.subShopping').click(function () {
        cnt = $(this).next();
        if (parseInt(cnt.text()) > 1) {
            var id = cnt.attr('title');
            console.log('ID:', id);
            cnt.text(parseInt(cnt.text()) - 1);
            // spancnt=cnt.text();
            //console.log('数量',spancnt)
            //更新后台
            $.getJSON('/app/selectCnt/' + id, function (data) {
                console.log('价钱', data.price);
                var tp = $('#totalPrice').text().trim();
                if (data.isSelected)
                    console.log('00000:',Number(tp),'qqqqq:',Number(data.price))
                    $('#totalPrice').text(((Number(tp) - Number(data.price))).toFixed(2))

            })
        }


    });
    //在购物车的商品的+号点击事件
    $('.addShopping').click(function () {

        cnt = $(this).prev();
        if (parseInt(cnt.text()) >= 1) {
            var id = cnt.attr('title');
            cnt.text(parseInt(cnt.text()) + 1);
            //更新后台
            $.getJSON('/app/addselectCnt/' + id, function (data) {
                var tp = $('#totalPrice').text().trim();
                if (data.isSelected)
                    $('#totalPrice').text((Number(tp) + Number(data.price)).toFixed(2))

            })
        }

    });

    //判断购物车商品是否有全部勾选
    function checkAllChose() {
        var chosea = $('.isChose');
        for (var i = 0; i < chosea.length; i++) {
            if ($(chosea[i]).children().first().text().trim() == '') {
                $('#allChose :first-child').text('');
                return
            }
        }
        $('#allChose :first-child').text('√')
    }
});

