$(function () {
    //返回键事件，返回上一个页面，跳转至上一个跳转到本页面的页面
    $('#backBtn').click(function () {
        window.history.back()
    });
    $('.toOrder').click(function () {
        window.open('/app/order/'+this.title,target='_self')
    });
});