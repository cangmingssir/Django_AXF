// $(document).ready(function(){
//     document.documentElement.style.fontSize = innerWidth / 10 + "px";
// })


$(function(){
    //获取窗口对象（根元素），可以使用em（相对于父节点），rem（相对于根节点）来获取相对值(相对于一下设置的宽度)
    //例：窗口800px 一下设置基准值为80px
    //给其设置样式，基准字体大小=内宽的十分之一
    document.documentElement.style.fontSize=innerWidth/10 +"px";

    $('.cartCnt')

});