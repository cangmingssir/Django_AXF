$(function () {
    $('#backBtn').click(function () {
       window.history.back()
    });


    $('.toOrder').click(function () {
        // console.log('nihaohaooaoaoao')
        num = this.title;
        $('#payMsg').text('您确定收到货物了吗？');
        $('#myModal').modal({backdrop: 'static', show: true}); //显示模态框
        $('.close').click(function () {
            $('#myModal').modal('hide')
        });
        $('#sure').click(function () {
            // $('#myModal').modal('hide');
            // console.log('00000000')
            $('#payMsg').text('请求正在提交... 请稍等');
            $('#myModal').modal({backdrop: 'static', show: true});
            setTimeout(function () {
                $('#myModal').modal('hide');
                $.getJSON('/app/suregood/' + num, function (data) {
                    console.log(data.msg);
                    $('#payMsg').text(data.msg);
                    $('#myModal').modal({backdrop: 'static', show: true});
                    // layer.load();
                    // console.log('pppppp')
                    setTimeout(function () {
                        // layer.closeAll('loading');
                        // console.log('ooooo')
                        $('#myModal').modal('hide');
                        // window.open('/app/cart',target='_self')
                        window.opener.document.location.reload();   //刷新页面
                    }, 2000)
                });
            }, 2000)
        });
    })
});