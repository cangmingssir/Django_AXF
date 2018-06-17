$(function () {
    $('#backBtn').click(function () {
       window.history.back()
    });
    //删除地址
    $('.adreDelete').click(function () {
        id=this.title;
        $('#payMsg').text('亲真的要删除这个收货地址吗？');
        $('#myModal').modal({backdrop: 'static', show: true});
        $('.close').click(function () {
            $('#myModal').modal('hide')
        });
        $('#sure').click(function () {
            $('#payMsg').text('正在删除，请稍等...');
            $('#myModal').modal({backdrop: 'static', show: true});
            setTimeout(function () {
                $('#myModal').modal('hide');
                $.getJSON('/app/deleteadre/'+id,function (data) {
                    console.log(data.msg);
                    $('#payMsg').text(data.msg);
                    $('#myModal').modal({backdrop:'static',show:true});
                    setTimeout(function () {
                        $('#myModal').modal('hide');
                        window.opener.document.location.reload();  //刷新页面
                    },2000)
                })
            },2000)
        });
    });

    //修改默认地址
    $('.defaultad').click(function () {
        console.log('进去');
        id=this.title;
        $.getJSON('/app/defaultade/'+id,function (data) {
            $('#payMsg').text(data.msg);
            $('#myModal').modal({backdrop:'static',show:true});
            setTimeout(function () {
                $('#myModal').modal('hide');
                window.opener.document.location.reload();
            },2000)
        })
    })
});