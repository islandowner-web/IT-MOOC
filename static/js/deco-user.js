//修改个人中心邮箱验证码
function sendCodeChangeEmail($btn){
    var verify = verifyDialogSubmit(
        [
          {id: '#jsChangeEmail', tips: Dml.Msg.epMail, errorTips: Dml.Msg.erMail, regName: 'email', require: true}
        ]
    );
    if(!verify){
       return;
    }
    $.ajax({
        cache: false,
        type: "get",
        dataType:'json',
        url:"/users/sendemail_code/",
        data:$('#jsChangeEmailForm').serialize(),
        async: true,
        beforeSend:function(XMLHttpRequest){
            $btn.val("发送中...");
            $btn.attr('disabled',true);
        },
        success: function(data){
            if(data.email){
                Dml.fun.showValidateError($('#jsChangeEmail'), data.email);
            }else if(data.status == 'success'){
                Dml.fun.showErrorTips($('#jsChangeEmailTips'), "邮箱验证码已发送");
            }else if(data.status == 'failure'){
                 Dml.fun.showValidateError($('#jsChangeEmail'), "邮箱验证码发送失败");
            }else if(data.status == 'success'){
            }
        },
        complete: function(XMLHttpRequest){
            $btn.val("获取验证码");
            $btn.removeAttr("disabled");
        }
    });

}
//个人资料邮箱修改
function changeEmailSubmit($btn){
var verify = verifyDialogSubmit(
        [
          {id: '#jsChangeEmail', tips: Dml.Msg.epMail, errorTips: Dml.Msg.erMail, regName: 'email', require: true},
        ]
    );
    if(!verify){
       return;
    }
    $.ajax({
        cache: false,
        type: 'post',
        dataType:'json',
        url:"/users/update_email/ ",
        data:$('#jsChangeEmailForm').serialize(),
        async: true,
        beforeSend:function(XMLHttpRequest){
            $btn.val("发送中...");
            $btn.attr('disabled',true);
            $("#jsChangeEmailTips").html("验证中...").show(500);
        },
        success: function(data) {
            if(data.email){
                Dml.fun.showValidateError($('#jsChangeEmail'), data.email);
            }else if(data.status == "success"){
                Dml.fun.showErrorTips($('#jsChangePhoneTips'), "邮箱信息更新成功");
                setTimeout(function(){location.reload();},1000);
            }else{
                 Dml.fun.showValidateError($('#jsChangeEmail'), "邮箱信息更新失败");
            }
        },
        complete: function(XMLHttpRequest){
            $btn.val("完成");
            $btn.removeAttr("disabled");
        }
    });
}

//个人资料手机修改
function changePhoneSubmit($btn){
    var verify = verifyDialogSubmit(
        [
            {id: '#jsChangePhone', tips: Dml.Msg.epPhone, errorTips: Dml.Msg.erPhone, regName: 'phone', require: true},
            {id: '#jsChangePhoneCode', tips: Dml.Msg.epPhCode, errorTips: Dml.Msg.erPhCode, regName: 'phoneCode',require: true}
        ]
    );
    if(!verify){
        return;
    }
    $.ajax({
        cache: false,
        type: 'post',
        dataType:'json',
        url:"/users/update/mobile/",
        data:$('#jsChangePhoneForm').serialize(),
        beforeSend:function(XMLHttpRequest){
            $btn.val("发送中...");
            $btn.attr('disabled',true);
            Dml.fun.showErrorTips($('#jsChangePhoneTips'), "验证中...");
        },
        success: function(data) {
            refresh_captcha({"data":{"form_id":"jsChangePhoneForm"}});
            if(data.mobile){
                Dml.fun.showValidateError($('#jsChangePhoneCode'), data.mobile);
            }else if(data.mobile_code){
                Dml.fun.showValidateError($('#jsChangePhoneCode'), data.mobile_code);
            }else if(data.captcha){
                Dml.fun.showValidateError($('#jsChangePhone'), data.captcha);
            }else if(data.status == "success"){
                //验证成功，回到个人资料修改界面
                Dml.fun.showErrorTips($('#jsChangePhoneTips'), "手机信息更新成功");
                setTimeout(function(){location.reload();},1000);
            }else{
                Dml.fun.showValidateError($('#jsChangePhone'), "手机信息更新失败");
            }
        },
        complete: function(XMLHttpRequest){
            $btn.val("完成");
            $btn.removeAttr("disabled");
        }
    });
}
//修改个人中心手机号码时发动短信
function sendCodeChangePhone($btn){
    var verify = verifyDialogSubmit(
        [
            {id: '#jsChangePhone', tips: Dml.Msg.epPhone, errorTips: Dml.Msg.erPhone, regName: 'phone', require: true},
            {id: '#jsChangePhoneForm #id_captcha_1', tips: Dml.Msg.epVerifyCode, errorTips: Dml.Msg.erVerifyCode, regName: 'verifyCode', require: true}
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
        // data:$('#jsChangePhoneForm').serialize(),
        data:{
                mobile:$("#jsChangePhone").val(),
                captcha_1:$("#id_captcha_1").val(),
                captcha_0:$('#id_captcha_0').val(),
        },
        beforeSend:function(XMLHttpRequest){
            $btn.val("发送中...");
            $btn.attr('disabled',true);
        },
        success: function(data){
            if(data.mobile){
                Dml.fun.showValidateError($('#jsChangePhone'), data.mobile);
            }else if(data.captcha){
                Dml.fun.showValidateError($('#jsChangePhoneForm #id_captcha_1'), data.captcha);
            }else if(data.status == 'success'){
                Dml.fun.showErrorTips($('#jsChangePhoneTips'), "短信验证码已发送");
            }else if(data.status == 'fail'){
                Dml.fun.showValidateError($('#jsChangePhone'), "短信验证码发送失败");
            }
        },
        complete: function(XMLHttpRequest){
            $btn.val("获取验证码");
            $btn.removeAttr("disabled");
        }
    });

}

$(function(){
    //个人资料修改密码
    $('#jsUserResetPwd').on('click', function(){
        Dml.fun.showDialog('#jsResetDialog', '#jsResetPwdTips');
    });
    $('#jsResetPwdBtn').click(function(){
        $.ajax({
            cache: false,
            type: "POST",
            dataType:'json',
            url:"/users/update/pwd/",
            data:$('#jsResetPwdForm').serialize(),
            async: true,
            success: function(data) {
                if(data.password1){
                    Dml.fun.showValidateError($("#pwd"), data.password1);
                }else if(data.password2){
                    Dml.fun.showValidateError($("#repwd"), data.password2);
                }else if(data.__all__){
                    Dml.fun.showValidateError($("#repwd"), data.__all__);
                }else if(data.status == "success"){
                    Dml.fun.showTipsDialog({
                        title:'提交成功',
                        h2:'修改密码成功，请重新登录!',
                    });
                    Dml.fun.winReload();
                }else if(data.msg){
                    Dml.fun.showValidateError($("#pwd"), data.msg);
                    Dml.fun.showValidateError($("#repwd"), data.msg);
                }
            }
        });
    });

    //个人资料头像
    $('.js-img-up').uploadPreview({ Img: ".js-img-show", Width: 94, Height: 94 ,Callback:function(){
        $('#jsAvatarForm').submit();
    }});

    $('#jsChangeEmailCodeBtn').on('click', function(){
        sendCodeChangeEmail($(this));
    });
    $('#jsChangeEmailBtn').on('click', function(){
        changeEmailSubmit($(this));
    });
    $('#jsChangePhoneBtn').on('click', function(){
        changePhoneSubmit($(this));
    });
    $('#jsChangePhoneCodeBtn').on('click', function(){
        sendCodeChangePhone($(this));
    });
    $('.changeemai_btn').on('click', function(){
        Dml.fun.showDialog('#jsChangePhoneDialog', '#jsChangePhoneTips' ,'jsChangeEmailTips');
    });

    //input获得焦点样式
    $('.perinform input[type=text]').focus(function(){
        $(this).parent('li').addClass('focus');
    });
    $('.perinform input[type=text]').blur(function(){
        $(this).parent('li').removeClass('focus');
    });

    laydate({
        elem: '#birth_day',
        format: 'YYYY-MM-DD',
        max: laydate.now()
    });

    verify(
        [
            {id: '#nick_name', tips: Dml.Msg.epNickName, require: true}
        ]
    );
    //保存个人资料
    $('#jsEditUserBtn').on('click', function(){
        var _self = $(this),
            $jsEditUserForm = $('#jsEditUserForm')
            verify = verifySubmit(
            [
                {id: '#nick_name', tips: Dml.Msg.epNickName, require: true},
                {id: '#birth_day', tips: Dml.Msg.epBirthday, require: true}
            ]
        );
        if(!verify){
           return;
        }
        $.ajax({
            cache: false,
            type: 'post',
            dataType:'json',
            url:"/users/info/",
            data:$jsEditUserForm.serialize(),
            async: true,
            beforeSend:function(XMLHttpRequest){
                _self.val("保存中...");
                _self.attr('disabled',true);
            },
            success: function(data) {
                if(data.nick_name){
                    _showValidateError($('#nick_name'), data.nick_name);
                }else if(data.birthday){
                   _showValidateError($('#birth_day'), data.birthday);
                }else if(data.address){
                   _showValidateError($('#address'), data.address);
                }else if(data.status == "fail"){
                     Dml.fun.showTipsDialog({
                        title: '保存失败',
                        h2: data.msg
                    });
                }else if(data.status == "success"){
                    Dml.fun.showTipsDialog({
                        title: '保存成功',
                        h2: '个人信息修改成功！'
                    });
                    setTimeout(function(){window.location.href = window.location.href;},1500);
                }
            },
            complete: function(XMLHttpRequest){
                _self.val("保存");
                _self.removeAttr("disabled");
            }
        });
    });


});