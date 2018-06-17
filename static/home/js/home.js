$(function () {
    topSwiper();
    topMustBuy();
});

function topSwiper() {
    var swiper = Swiper("#topSwiper", {
        direction: 'horizontal',    //设置滑动方向，可设置水平(horizontal)或垂直(vertical)
        loop: true,
        // 如果需要分页器
        pagination: '.swiper-pagination',
        paginationClickable:true,   //此参数设置为true时，点击分页器的指示点分页器会控制Swiper切换。
        effect:'cube',  //slide的切换效果，默认为"slide"（位移切换），可设置为"fade"（淡入）"cube"（方块）"coverflow"（3d流）"flip"（3d翻转）。
        autoplay:3000,    //自动播放
        //用户操作swiper之后，是否禁止autoplay。默认为true：停止。
        // 如果设置为false，用户操作swiper之后自动切换不会停止，每次都会重新启动autoplay。
        // 操作包括触碰，拖动，点击pagination等。
        autoplayDisableOnInteraction:false
    })
}

function topMustBuy() {
    var swiper2 = Swiper("#swiperMenu",{
        slidesPerView:3,
        paginationClickable:true,
        spaceBetween:4,     //slide之间的距离（单位px）
        loop:false
    })
}