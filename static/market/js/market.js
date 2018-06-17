$(function () {
    $('#allType').click(function () {

        // 获取分类的<span>内显示图标的子标签<span><span></span></span>
        $(this.lastChild).toggleClass('glyphicon-chevron-down');

        if ($('#typeDiv')[0].style.display == 'block') {
            $('#typeSortDiv').css('display', 'none');
            $('#typeDiv').css('display', 'none');
            return;
        }

        $('#typeSortDiv').css('display', 'block');
        $('#typeDiv').css('display', 'block');

        //还原排序
        $('#goodsSort :last-child').removeClass('glyphicon-chevron-down');
        $('#sortDiv').css('display', 'none');
    });

    $('#goodsSort').click(function () {
        // this -> 被点击的DOM对象
        $(this.lastChild).toggleClass('glyphicon-chevron-down');
        console.log($('#sortDiv')[0].style.display);
        if ($('#sortDiv')[0].style.display == 'block') {
            $('#typeSortDiv').css('display', 'none');
            $('#sortDiv').css('display', 'none');
            return;
        }

        $('#typeSortDiv').css('display', 'block');
        $('#sortDiv').css('display', 'block');

        //还原分类
        $('#typeDiv').css('display', 'none');
        $('#allType :last-child').removeClass('glyphicon-chevron-down');
    })

    $('#typeSortDiv').click(function () {
        $(this).css('display', 'none');
        //隐藏排序和分类div
        $('#sortDiv').css('display', 'none');
        $('#typeDiv').css('display', 'none');


        $('#allType :last-child').removeClass('glyphicon-chevron-down');
        $('#goodsSort :last-child').removeClass('glyphicon-chevron-down');
    });


    //添加商品到购物车
    $('.addShopping').click(function () {
        var goodID = $(this).attr('title');
        // $.getJSON('/app/addgoodtoCart/' + goodID, function (data) {
        //     // $('.addShopping').prev().text(data.cnt)
        //     console.log(data)
        //
        //     if (data.status == 400) {
        //         $('#cartCnt').text(parseInt($('#cartCnt').text()) + 1);
        //         if ($('#cartCnt').css('visibility') != 'visible') {
        //             $('#cartCnt').css('visibility', 'visible')
        //         }
        //     }else {
        //         console.log('767676767767');
        //
        //         layer.alert('见到你真的很高兴', {icon: 6});
        //     }
        //
        // });
        $.ajax({
            type:'get',
            url:'/app/addgoodtoCart/' + goodID,
            dataType:'json',
            // before:function()
            success:function (data) {
                if (data.status == 400) {
                    $('#cartCnt').text(parseInt($('#cartCnt').text()) + 1);
                    if ($('#cartCnt').css('visibility') != 'visible') {
                        $('#cartCnt').css('visibility', 'visible')
                    }
                } else {
                    console.log('767676767767');
                    // alert('ooooo')
                    layer.alert(data.msg, {icon: 2});
                }
            }
        })
    });
    if ($('#cartCnt').text(parseInt($('#cartCnt').text())) == '') {
        $('#cartCnt').css('visibility', 'hidden')
    }
});


