//刷新验证码
function refresh_captcha(event){
    $.get("/captcha/refresh/?"+Math.random(), function(result){
        $('#jsRefreshCode img.captcha').attr("src",result.image_url);
        $('#id_captcha_0').attr("value",result.key);
    });
    return false;
}

$(function() {
    //兼容IE9下placeholder不显示问题
    function isPlaceholder(){
        var input = document.createElement('input');
        return 'placeholder' in input;
    }
    if(!isPlaceholder()){
        $("input").not("input[type='password']").each(
            function(){
                if($(this).val()=="" && $(this).attr("placeholder")!=""){
                    $(this).val($(this).attr("placeholder"));
                    $(this).focus(function(){
                        if($(this).val()==$(this).attr("placeholder")) $(this).val("");
                    });
                    $(this).blur(function(){
                        if($(this).val()=="") $(this).val($(this).attr("placeholder"));
                    });
                }
        });
        $("textarea").each(
            function(){
                if($(this).val()=="" && $(this).attr("placeholder")!=""){
                    $(this).val($(this).attr("placeholder"));
                    $(this).focus(function(){
                        if($(this).val()==$(this).attr("placeholder")) $(this).val("");
                    });
                    $(this).blur(function(){
                        if($(this).val()=="") $(this).val($(this).attr("placeholder"));
                    });
                }
        });
        var pwdField    = $("input[type=password]");
        var pwdVal      = pwdField.attr('placeholder');
        pwdField.after('<input id="pwdPlaceholder" type="text" value='+pwdVal+' autocomplete="off" />');
        var pwdPlaceholder = $('#pwdPlaceholder');
        pwdPlaceholder.show();
        pwdField.hide();

        pwdPlaceholder.focus(function(){
            pwdPlaceholder.hide();
            pwdField.show();
            pwdField.focus();
        });

        pwdField.blur(function(){
            if(pwdField.val() == '') {
                pwdPlaceholder.show();
                pwdField.hide();
            }
        });
    }

    $('.imgslide').unslider({
        speed: 500,
        delay: 3000,
        complete: function() {},
        keys: true,
        dots: true,
        fluid: false
    });
    var unslider = $('.imgslide').unslider();
    $('.unslider-arrow').click(function() {
        var fn = this.className.split(' ')[1];
        unslider.data('unslider')[fn]();
    });

    $('.tab > h2').click(function(){
        var _self = $(this),
            index = _self.index();
        _self.addClass('active').siblings().removeClass('active');
        $('.tab-form').eq(index).removeClass('hide').siblings('.tab-form').addClass('hide');
    });

    //input的focus和blur效果
	$('input[type=text]').focus(function(){
		$(this).parent().removeClass('blur').addClass('focus');
	});
	$('input[type=text]').blur(function(){
		$(this).parent().removeClass('focus').addClass('blur');
	});
    //input的focus和blur效果
	$('input[type=password]').focus(function(){
		$(this).parent().removeClass('blur').addClass('focus');
	});
	$('input[type=password]').blur(function(){
		$(this).parent().removeClass('focus').addClass('blur');
	});

    // 发送手机验证码
    $('#jsSendCode').on('click',function(){
        send_sms_code(this,$('#jsMobileTips'));
    });
    //发送手机验证码
    function send_sms_code(sendBtn,tipsId){
        var $sendBtn = $(sendBtn),
            $tipsId = $(tipsId),
            $inpRegMobile = $("#jsRegMobile"),
            $inpRegCaptcha = $('#id_captcha_1'),
            verify = verifyDialogSubmit(
                [
                    {id: '#jsRegMobile', tips: Dml.Msg.epPhone, errorTips: Dml.Msg.erPhone, regName: 'phone', require: true},
                    {id: '#id_captcha_1', tips: Dml.Msg.epVerifyCode, errorTips: Dml.Msg.erVerifyCode, regName: 'verifyCode', require: true}
                ]
            );
        if(!verify){
            return;
        }
        $.ajax({
            cache: false,
            type: 'post',
            dataType:'json',
            url:"/send_sms/",
            data:{
                mobile:$inpRegMobile.val(),
                "captcha_1":$inpRegCaptcha.val(),
                "captcha_0":$('#id_captcha_0').val(),
            },
            async: true,
            beforeSend:function(XMLHttpRequest){
                $sendBtn.val("发送中...");
                $sendBtn.attr("disabled","disabled");
            },
            success: function(data){
                $sendBtn.removeAttr("disabled");
                $sendBtn.val("发送验证码");
                if(data.mobile){
                    Dml.fun.showValidateError($inpRegMobile, data.mobile);
                    refresh_captcha({"data":{"form_id":"jsRefreshCode"}});
                }else if(data.captcha){
                    Dml.fun.showValidateError($inpRegCaptcha, data.captcha);
                    refresh_captcha({"data":{"form_id":"jsRefreshCode"}});
                }else if(data.msg){
                    Dml.fun.showValidateError($inpRegMobile, data.msg);
                    $sendBtn.val("重新发送");
                    refresh_captcha({"data":{"form_id":"jsRefreshCode"}});
                }else if(data.status == 'success'){
                    Dml.fun.showErrorTips($tipsId, "短信验证码已发送");
                    $sendBtn.attr("disabled","disabled");
                    show_send_sms(60);
                }
            }
        });
    }

    $('#jsMobileRegBtn').on('click',function(){
        $( "#mobile_register_form" ).submit();
    });

    //注册刷新验证码点击事件
    $('#email_register_form .captcha-refresh').click({'form_id':'email_register_form'},refresh_captcha);
    $('#email_register_form .captcha').click({'form_id':'email_register_form'},refresh_captcha);
    $('#changeCode').click({'form_id':'jsRefreshCode'},refresh_captcha);
    $('#jsFindPwdForm .captcha-refresh').click({'form_id':'jsFindPwdForm'},refresh_captcha);
    $('#jsFindPwdForm .captcha').click({'form_id':'jsFindPwdForm'},refresh_captcha);
    $('#jsChangePhoneForm .captcha').click({'form_id':'jsChangePhoneForm'},refresh_captcha);

    //刷新验证码
    $('#jsRefreshCode img.captcha').on('click', function(){
        refresh_captcha();
    });

    //重发送短信验证码计时
    function show_send_sms(time){
    $('#jsSendCode').val(time+"秒后重发");
    if(time<=0){
        clearTimeout(send_sms_time);
        $('#jsMobileTips').hide(500);
         $('#jsSendCode').val("发送验证码").removeAttr("disabled");
        return;
    }
    time--;
    send_sms_time = setTimeout("show_send_sms("+time+")", 1000);
}
});
