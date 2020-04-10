# IT-MOOC  
### 基于Django2.2开发的IT教育学习平台（视频学习，线上作业，课程推荐，双后台权限分离）

## 项目说明  
项目名：IT-MOOC在线IT教学平台  

核心功能：视频学习，线上作业，课程推荐，教师及管理员双后台权限分离  

相关技术：Django、Python、Redis、MySQL、Jquery   

功能说明：功能较多下方分块说明。  
- 课程搜索与展示：  
课程列表、课程详情、课程介绍、课程相关的教师与授课机构、课程搜索、课程筛选（热度、付费/免费等）
- 课程学习：  
课程章节、课程视频推流播放、课程资料下载、课程作业及其自动批改、课程反馈评价
- 用户相关：  
个人资料修改、付费课程支付、收藏夹（收藏教师与课程）、付费课程订单管理
- 课程推荐：  
用户行为偏好课程推荐、相似课程推荐
- 教师后台：  
教师仅可查看和更新自己教授的课程的视频、资料、作业等信息，无其他权限
- 管理员后台：
管理员可对平台内所有资源与二级权限组进行管理，分别可管理课程、教师、机构、用户、用户行为这几大类的相关数据
- 其他功能：  
注册、登录、后台样式管理

背景与说明：本人本科毕设，开发时间2019.10.06-2019-12.22

项目中使用的第三方服务与开源项目：  
[七牛云对象存储OSS --- 用于教学视频推流与CDN加速](https://www.qiniu.com/products/kodo)   
[支付宝开放平台（沙箱环境） --- 用于付费课程购买与支付](https://opendocs.alipay.com/apis/api_1)    
[云片 --- 用于注册登录部分短信发码](https://github.com/yunpian/yunpian-python-sdk)   
[ueditor富文本编辑器 --- 用于课程详情富文本编辑](https://github.com/fex-team/ueditor)  
[xadmin --- 用于替代Django自带后台，提供更加美观的界面与更完善的中文支持](https://github.com/fex-team/ueditor) 
  
## 搭建说明
### 开发环境
核心开发环境(版本号尽量一致)：
- Python  3.7.3
- Django  2.2
- Mysql  5.7.27
- Redis  5.0.6  

### 初步搭建步骤
1. 克隆项目至本地，并确保本地Mysql，Redis服务运行正常。

2. 终端cd进入项目目录，执行`pip install -r requitements.txt`命令。  
   注意mysqlclient在Mac电脑环境下安装100%会报错，需要修改部分源码解决问题，教程如下，win环境下通过pip即可顺利安装。  
   [Mac上mysqlclient安装教程](https://www.jianshu.com/p/1eb691ce4a35) 

3. 打开项目`Education_106`文件夹中下的`settings.py`文件
    ```
    DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': '此处填写数据库名',
        'USER': '此处填写登录数据库的用户名',
        'PASSWORD': '密码',
        'HOST': '本机填127.0.0.1，云数据库根据实际情况填写',
      }
    } 
    ```

4. 终端cd进入项目目录，依次执行，并检查相应数据库中是否生成对应的数据表
    ```
    python manage.py makemigrations
    python manage.py migrate
    ```

5. 数据库无误后执行下列命令创建超级管理员，并根据提示设置用户名和密码
    ```
    python manage.py createsuperuser
    ```

6. 使用以下指令或者直接以pychrm运行项目
    ```
    python manage.py runserver
    ```

7. 打开`http://127.0.0.1:8000/xadmin`，以第5步设置的账号和密码登录管理员后台，首先添课程机构，再添加机构下的教师、最后添加课程，即可完成初步搭建。

### 截止至此项目中除了`视频播放`、`付费课程支付`和`短信验证码注册登录`这三项功能，其他功能均可正常使用，下方介绍这三项功能需要的额外搭建步骤

8. 视频播放功能，进入 `七牛云OSS控制台`或者其他任意的对象存储以及视频推流云服务对象存储，上传视频，生成视频外链，将视频外链存入后台管理系统的课程视频部分，即可实现视频播放。目前主流视频托管及加速服务均需备案，使用前需进行备案。  
[七牛云对象存储OSS --- 用于教学视频推流与CDN加速](https://www.qiniu.com/products/kodo)  

9. 付费课程支付功能，进入`支付宝开放平台`，按照下文博客中的步骤生成RSA密钥，进入keys文件夹，将`公钥`填入`alipay_public_2048.txt`中，`私钥`填入`app_private_2048.txt`中，之后进入支付宝开放平台---沙箱环境，下载`沙箱钱包App`,使用给定的账号密码登录App后即可付款。  
[支付宝开放平台](https://open.alipay.com/platform/home.htm)   
[博客园---作者Thanlon---基于python-django框架的支付宝支付案例](https://www.cnblogs.com/qikeyishu/p/11564756.html) 

10. 短信验证码注册登录功能，进入`云片`，注册账号并且实名认证，若无企业资质和备案认证，需要联系客服获取开发时短信模版及接口授权，短信模版自己定义，进入utils.py以及settings.py中，依次填写完成以下信息。填写完成后接口若已通过云片认证即可发送短信验证码。
    ```
    //utils.py
    def send_single_sms(apikey, code, mobile):
    url = "https://sms.yunpian.com/v2/sms/single_send.json"
    text = "这里填写短信模版".format(code)
    ```
    ```
    //settings.py
    yp_apikey = "这里填写授权码"
    ```
    [云片 --- 用于注册登录部分短信发码](https://github.com/yunpian/yunpian-python-sdk) 



## 效果展示（部分页面）

- 首页  
<img src="/pic/home.png">
- 课程列表  
<img src="/pic/courselist.png">
- 课程详情  
<img src="/pic/coursedetail.png">
- 课程视频列表  
<img src="/pic/videolist.png">
- 课程视频播放  
<img src="/pic/video.png">
- 课程作业  
<img src="/pic/homework.png">
- 教师详情  
<img src="/pic/teadetail.png">
- 机构详情  
<img src="/pic/orgdetail.png">
- 课程收藏  
<img src="/pic/collect.png">
- 订单列表  
<img src="/pic/orderlist.png">
- 管理员后台  
<img src="/pic/root.png">
- 教师后台  
<img src="/pic/tearoot.png">


## 附录：依赖的所有python库及其版本(涉及订单生成、支付、ueditor等部分)
  ```
      alipay-sdk-python      3.3.202  
      backports.csv          1.0.7    
      certifi                2019.9.11
      chardet                3.0.4    
      defusedxml             0.6.0    
      diff-match-patch       20181111 
      Django                 2.2      
      django-crispy-forms    1.7.2    
      django-formtools       2.1      
      django-import-export   1.2.0    
      django-pure-pagination 0.3.0    
      django-ranged-response 0.2.0    
      django-reversion       3.0.4    
      django-simple-captcha  0.5.12   
      et-xmlfile             1.0.1    
      future                 0.17.1   
      httplib2               0.14.0   
      idna                   2.8      
      jdcal                  1.4.1    
      mysqlclient            1.4.4    
      odfpy                  1.4.0    
      openpyxl               3.0.0    
      Pillow                 6.2.0    
      pip                    19.2.3   
      pyasn1                 0.4.8    
      pycrypto               2.6.1    
      pycryptodome           3.9.4    
      pytz                   2019.2   
      PyYAML                 5.1.2    
      redis                  3.3.8    
      requests               2.22.0   
      reversion              0.2      
      rsa                    4.0      
      setuptools             41.2.0   
      six                    1.12.0   
      sqlparse               0.3.0    
      tablib                 0.13.0   
      toml                   0.10.0   
      urllib3                1.25.6   
      wheel                  0.33.6   
      xlrd                   1.2.0    
      XlsxWriter             1.2.1    
      xlwt                   1.3.0
  ```


## 更多信息
- 有问题可扫码加我微信，能帮就帮能答就答  
<img src="/pic/wx.jpeg" height='300'>
