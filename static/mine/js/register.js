// var isshowForm=false
//定义一个公共函数，显示正则匹配后的结果
function showError(msg, isUser) {
    console.log(this);
    var errorp = this.parentElement.nextElementSibling;
    //var errorp=$(this).parent().next()

    errorp.innerText = isUser ? this.title + msg : msg;
    console.log('iiiiii', msg);
    $(errorp).fadeIn();
    //设置input-group 存在错误
    //addClass添加样式，removeClass移除样式
    $(this.parentElement).addClass('has-error');    //设置input样式，输入框变红
    this.value='';  //如果出现错误，清空输入框数据
    // this.focus()
    $(this).focus(function () {
        $(errorp).fadeOut();
        $(this.parentElement).removeClass('has-error');
        // this.focus()
    });
}

//js函数入口
$(function () {

    $('input[name=number]').blur(function () {

    });
    //input对象集合的失去焦点事件
    $('input').blur(function () {
        console.log('------', this.value);
        if (this.value.trim().length == 0) {
            //调用该showError,使用call方法
            showError.call(this, '不能为空', true);
            return
        } else {
            $(this).parent().removeClass('has-error');
            $(this).parent().next().fadeOut()
        }
        if (this.name == 'number' && this.value.trim().length < 8) {
            showError.call(this, '账户长度不能小于8位', false);
            return
        } else {
            //以下ajax用于判断用户名是否存在于数据库中，寻在则提示错误
            var input = this;
            var usernumber = this.value.trim();
            console.log('msg', usernumber);
            var xhr = new XMLHttpRequest();
            xhr.open('post', '/app/userNumber', true);
            xhr.onload = function (ev) {
                data = JSON.parse(xhr.responseText);
                console.log(data.msg);
                if (data.msg == 200) {
                    //下面调用的函数，因为是在ajax中this代表的是ajax本身，所以需要给该input对象定义一个变量
                    showError.call(input, '该用户已存在', false)
                } else {
                    // showError.call(input, '该账号可以使用',false)
                    var success = $(input).parent().next();
                    success.text('该账号可以使用');
                    success.css("color", 'green');
                    success.fadeIn()
                }

            };
            var formdata = new FormData();
            formdata.append('usermuber', usernumber);
            xhr.send(formdata)
        }

        if (this.name == 'passwd') {
            var passwd = this.value.trim();
            if (passwd.length < 8) {
                showError.call(this, '密码长度不能小于8位', false)
            }
            if (!/^[A-Z][a-z0-9@%$!#*&]{7,}/.test(passwd)) {
                showError.call(this, '必须以大写字母开头且长度不小于8位', false)
            }

        }

        if (this.name == 'passwd2') {
            //得到第一次密码的输入值
            var passwd1 = $('input[name=passwd]').val();
            console.log('口令1： ', passwd1);
            if (this.value.trim() != passwd1.trim())
                showError.call(this, '两次口令不相同！', false);
                return
        }
        if (this.name == 'phone') {
            var phone = this.value.trim();
            if (phone.length != 11) {
                showError.call(this, '请输入11位的手机号', false);
                return
            }
            if (!/1[3-9]\d{9}/.test(phone)) {
                showError.call(this, '手机号无效', false);
                return
            }
        }
        // isshowForm=true
        //console.log(isshowForm)
    })
});

//表单提交时验证信息
function submitForm() {
    var inputs = $('input');
    //验证是否为空，可再添加其他验证
    for (var i = 0; i < inputs.length; i++) {
        var input = inputs.get(i);
        if ($(input).val().trim() == '') {
            $(input).parent().addClass('has-error');
            $(input).parent().next().fadeIn();
            return
        } else {
            $(input).parent().removeClass('has-error');
            $(input).parent().next().hide()
        }

    }
    // if (isshowForm)
    $('form').submit();
    console.log('+++check++++')
}

// function userNumberFocus() {
//     // var username=$('input[name=number]')
//     $('input[name=number]').blur(function () {
//         var usernumber = $(this).val()
//         console.log(usernumber)
//         var xhr = new XMLHttpRequest()
//         xhr.open('post', '/app/userNumber', true);
//         xhr.onload = function (ev) {
//             data = JSON.parse(xhr.responseText)
//             if (data.msg == 101) {
//                 showError(this, '该用户已存在', false)
//             } else {
//                 showError(this, '该账号可以使用')
//             }
//
//
//         }
//         var formdata = new FormData()
//         formdata.append('usermuber', usernumber)
//         xhr.send(formdata)
//     })
//
// }