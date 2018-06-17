function upload(file) {
    //上传文件
    var xhr = new XMLHttpRequest();
    xhr.open('post', '/app/upload', true)
    xhr.onload = function (ev) {
        if (xhr.status == 200 && xhr.readyState == 4) {
            console.log(xhr.responseText);
            data = JSON.parse(xhr.responseText)
            if (data.state == 'ok') {
                $('#userImg').attr('src', '/static/upload/' + data.path)
                $('#imgspan').removeClass()
            }
        }
    }

    var formdata = new FormData();
    formdata.append('img', file);
    xhr.send(formdata)

}

$(function () {
    //跳转至全部订单界面
    $('#selectOrder').click(function () {
        console.log('加载');
        window.open('/app/selectOrder', target = '_self')  //target='_self',表示替换当前页面
    });
    //待付款点击事件
    $('#waitpay').click(function () {
        window.open('/app/waitpay',target='_self')
    });
    //待收货点击事件
    $('#waitgood').click(function () {
        window.open('/app/waitgood',target='_self')
    });



    //点击收货地址事件
    $('#useraddress').click(function () {
        layer.load(2);
        // layer.alert('见到你真的很高兴', {icon: 6});
        // console.log('99999')
        setTimeout(function () {
            layer.closeAll('loading');
            window.open('/app/useraddress',target='_self')
        },1000);

    });
});