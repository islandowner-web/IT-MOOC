function getCookie(name) {
     var cookieValue = null;
     if (document.cookie && document.cookie != '') {
         var cookies = document.cookie.split(';');
         for (var i = 0; i < cookies.length; i++) {
             var cookie = jQuery.trim(cookies[i]);
             // Does this cookie string begin with the name we want?
             if (cookie.substring(0, name.length + 1) == (name + '=')) {
                 cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                 break;
             }
         }
     }
     return cookieValue;
 };


// 顶部搜索栏
function search_click(){
    var type = $('#jsSelectOption').attr('data-value'),
        keywords = $('#search_keywords').val(),
        request_url = '';
    if(keywords == ""){
        return
    }
    if(type == "course"){
        request_url = "/course/list?keywords="+keywords
    }
    window.location.href = request_url
}


//刷新验证码
function refresh_captcha(event){
    $.get("/captcha/refresh/?"+Math.random(), function(result){
        $('#'+event.data.form_id+' .captcha').attr("src",result.image_url)
        $('#id_captcha_0').attr("value",result.key);
    });
    return false;
}


//手机注册发送手机验证码
function send_sms_code(sendBtn,tipsId){
    var $sendBtn = $(sendBtn),
        $tipsId = $(tipsId),
        $inpRegMobile = $("#jsRegMobile"),
        $inpRegCaptcha = $('#mobile-register-captcha_1'),
        verify = verifyDialogSubmit(
            [
                {id: '#jsRegMobile', tips: Dml.Msg.epPhone, errorTips: Dml.Msg.erPhone, regName: 'phone', require: true},
                {id: '#mobile-register-captcha_1', tips: Dml.Msg.epVerifyCode, errorTips: Dml.Msg.erVerifyCode, regName: 'verifyCode', require: true}
            ]
        );
    if(!verify){
        return;
    }
    $.ajax({
        cache: false,
        type: 'get',
        dataType:'json',
        url:"/user/send_sms_code_change/",
        data:{
            sms_type: 0,
            mobile:$inpRegMobile.val(),
            "captcha_1":$inpRegCaptcha.val(),
            "captcha_0":$('#mobile-register-captcha_0').val(),
        },
        async: true,
        beforeSend:function(XMLHttpRequest){
            $sendBtn.val("发送中...");
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


//手机注册发送手机验证码
$('#jsSetNewPwdBtn').on('click', function(){
    var _self = $(this),
         $idAccount = $("#account");
         verify = verifyDialogSubmit(
            [
                {id: '#jsResetPwd', tips: Dml.Msg.epResetPwd, errorTips: Dml.Msg.erResetPwd, regName: 'pwd', require: true},
                {id: '#jsResetPwd2', tips: Dml.Msg.epRePwd, repwd: '#jsResetPwd', require: true},
                {id: '#jsResetCode', tips: Dml.Msg.epPhCode, errorTips: Dml.Msg.erPhCode, regName: 'phoneCode', require: true}
            ]
        );
    if(!verify){
       return;
    }

    $.ajax({
        cache: false,
        type: 'post',
        dataType:'json',
        url:"/user/mobile/resetpassword/",
        data:$('#jsSetNewPwdForm').serialize(),
        async: true,
        beforeSend:function(XMLHttpRequest){
            _self.val("提交中...")
            _self.attr("disabled","disabled")
        },
        success: function(data) {
            if(data.status == 'success'){
                Dml.fun.showTipsDialog({
                    title:'重置成功',
                    h2:'重置密码成功！'
                });
                $('#jsSetNewPwdForm')[0].reset();
            }else if(data.status == 'faliuer'){
                 Dml.fun.showTipsDialog({
                    title:'重置失败',
                    h2:data.msg,
                    type:'failbox'
                })
            }else if(data.code){
                 Dml.fun.showValidateError($('#jsResetCode'), data.code);
            }
        },
        complete: function(XMLHttpRequest){
            _self.val("提交");
            _self.removeAttr("disabled");
        }
    });
})




function getCookie(name) {
     var cookieValue = null;
     if (document.cookie && document.cookie != '') {
         var cookies = document.cookie.split(';');
         for (var i = 0; i < cookies.length; i++) {
             var cookie = jQuery.trim(cookies[i]);
             // Does this cookie string begin with the name we want?
             if (cookie.substring(0, name.length + 1) == (name + '=')) {
                 cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                 break;
             }
         }
     }
     return cookieValue;
}


//弹框
$(function() {
    $(window).resize(function(){
        $('.dialogbox').each(function(){
            if($(this).css('display') == 'block'){
                centerDialog($(this));
            }
        });
    });
    $(".scrollLoading").scrollLoading();
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


    //顶部搜索栏搜索按钮事件
    $('#jsSelectOption').on('click', function(){
        var $jsSelectMenu = $('#jsSelectMenu');
        if($jsSelectMenu.css('display') == 'block') return;
        $jsSelectMenu.addClass('dis');
    });
    $('#jsSelectMenu > li').on('click', function(){
        var searchType = $(this).attr('data-value'),
            searchName = $(this).text(),
            $jsSelectOption = $('#jsSelectOption');
        $jsSelectOption.attr('data-value',searchType).text(searchName);
        $(this).parent().removeClass('dis');
    });
    $(document).on('click', function(e){
        if(e.target != $('#jsSelectOption')[0] && e.target != $('#jsSelectMenu')[0]){
            $('#jsSelectMenu').removeClass('dis');
        }
    });


    $('#jsSearchBtn').on('click',function(){
        search_click()
    });
    //搜索表单键盘事件
    $("#search_keywords").keydown(function(event){
        if(event.keyCode == 13){
             $('#jsSearchBtn').trigger('click');
        }
    });

    //input的focus和blur效果
	$('.dialogbox .box input').focus(function(){
		$(this).parent('.box').removeClass().addClass('box focus');
	});
	$('.dialogbox .box input').blur(function(){
		$(this).parent('.box').removeClass().addClass('box blur');
	});


    //其他需要登录的链接弹窗
    $('.notlogin').on('click', function(){
        Dml.fun.showDialog('.loginbox','#jsLoginTips');
	});
    //登录链接弹窗
    $('.dialogbox .login').on('click', function(){
        Dml.fun.showDialog('.loginbox','#jsLoginTips');
    });

    //注册链接弹窗
    $('.dialogbox .regist').on('click', function(){
        Dml.fun.showDialog('.registbox', '#jsEmailTips', '#jsMobileTips');
    });
    //其他需注册链接弹窗
    $('.jsOtherRegBtn').on('click', function(){
         Dml.fun.showDialog('.registbox', '#jsEmailTips', '#jsMobileTips');
	});

    //忘记密码链接弹窗
    $('.dialogbox .forget').on('click', function(){
        Dml.fun.showDialog('.forgetbox', '#jsForgetTips');
    });

    //邮箱注册和手机注册弹窗tab事件
    $('.jsRegTab').on('click', function(){
        var tabindex = $(this).index();
        $('.jsTabBox').addClass('hide').eq(tabindex).removeClass('hide');
        $(this).addClass('active').siblings().removeClass('active');
        $('#jsEmailTips').hide();
        $('#jsMobileTips').hide();
	});

    //layer加载扩展模块
    layer.config({
        extend: 'extend/layer.ext.js'
    });
    $('.jsLayerBox').one('mouseover', function(){
        var _self = $(this);
        layer.ready(function(){
            layer.photos({
                shift: false,
                shade: [0.8, '#000'],
                photos: _self,
                area: 'auto'
            });
        });
    });

    $('#jsDialog').on('click', '.laydate', function(){
        laydate({
            format: 'YYYY-MM-DD',
            min: laydate.now()
        });
    });

    $('.jsShowPerfect2').on('click',function(){
        var companyId = $(this).attr('data-id');
            $('#jsCompanyId').val(companyId);
        Dml.fun.showDialog('.groupbox02', '#jsPerfetTips2');
    });

    //弹出框关闭按钮
	$('.jsCloseDialog').on('click', function(){
        $('#jsDialog').hide();
        $('html').removeClass('dialog-open');
		$(this).parents('.dialogbox').hide();
        $('#dialogBg').hide();
        if($(this).parent().find('form')[0]){
            $(this).parent().find('form')[0].reset();
        }
	});

    // 发送手机注册验证码
	$('#jsSendCode').on('click',function(){
        send_sms_code(this,$('#jsMobileTips'));
    });

    //注册刷新验证码点击事件
    $('#email_register_form .captcha-refresh').click({'form_id':'email_register_form'},refresh_captcha);
    $('#email_register_form .captcha').click({'form_id':'email_register_form'},refresh_captcha);
    $('#mobile_register_form .captcha').click({'form_id':'jsRefreshCode'},refresh_captcha);
    $('#changeCode').click({'form_id':'jsRefreshCode'},refresh_captcha);
    $('#jsFindPwdForm .captcha-refresh').click({'form_id':'jsFindPwdForm'},refresh_captcha);
    $('#jsFindPwdForm .captcha').click({'form_id':'jsFindPwdForm'},refresh_captcha);
    $('#jsChangePhoneForm .captcha').click({'form_id':'jsChangePhoneForm'},refresh_captcha);
    //登录
    $('#jsLoginBtn').on('click',function(){
        login_form_submit();
    })
    //登录表单键盘事件
    $("#jsLoginForm").keydown(function(event){
        if(event.keyCode == 13) {
            $('#jsLoginBtn').trigger('click');
        }
    });



    $(".toolbar-item-fankui,.toolbar-item-gotop").hover(function(){
        $(this).children().stop().show("fast")
    },function(){
        $(this).children().stop().hide("fast")
    });
    $(".toolbar-item-gotop").click(function(){
        $('html,body').stop().animate({scrollTop: '0px'}, 800);
    });



    $('img').on('error', function(){
        $(this).off('error').attr('src', '/static/images/error-img.png');
    });
});