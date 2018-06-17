function submitForm() {
    var inputs = $('input');
    console.log(inputs)
    for (var i = 0; i < inputs.length; i++) {
        var input = inputs.get(i);
        if ($(input).val().trim() == '') {
            $(input).parent().addClass('has-error')
            $(input).parent().next().show()
            return
        } else {
            $(input).parent().removeClass('has-error')
            $(input).parent().next().hide()
        }

    }
    $('form').submit()
}

$(function () {
    $('input').blur(function () {
        if ($(this).val().trim() == ''){
            $(this).parent().addClass('has-error')
            $(this).parent().next().show()
            return
        }else{
            $(this).parent().removeClass('has-error')
            $(this).parent().next().hide()
        }

    })
})