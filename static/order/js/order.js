$(function () {
    $('#backBtn').click(function () {
        //窗口返回上一个页面
        window.history.back()
    });

    $('#payBtnDiv > button').click(function () {
        console.log(this);
        // $('#myModal').on('hide.bs.modal',function (e) {
        // });
        $('#payMsg').text('使用' + $(this).text() + '正在支付...');
        $('#myModal').modal('show');   //显示模态框

        orderNum = $(this).parent().attr('title');
        payType = $(this).attr('title');
        $.getJSON('/app/pay/' + orderNum + "/" + payType, function (data) {
            console.log('data值:', data);
            if (data.status == 'ok') {
                $('#payMsg').text(data.msg + '!3秒后跳转购物车界面');
                setTimeout(function () {
                    $('#myModal').modal('hide');
                    console.log('jinlail');
                    window.open('/app/cart', target = '_self')
                }, 3000);

            }
            // //若用户未登录，则弹出提示信息，并跳转登录界面
            // else if (data.status == 404){
            //     $('#payMsg').text(data.msg+'!3秒后跳转登录界面');
            //     setTimeout(function () {
            //         $('#myModal').modal('hide');
            //         window.open('/app/login')
            //     },3000);
            //
            // }


            else {
                $('#payMsg').text(data.msg + '!3秒后跳转订单界面');
                setTimeout(function () {
                    $('#myModal').modal('hide');
                    // window.open('/app/order/'+data.num)
                }, 3000)

            }
            //$('#myModal').modal({backdrop: 'static', show: true});    //设置静态框，点击内容以外不可关闭
        })

    })

});

