本文档用来保存一些有用的信息
==============================
{
    "access_token": "l3QcryY7U2p5ZAN_ddE1eOUJCTLMAPvmw5AVXWRtGUAqFBBI7Fa2k0zVPZ0VKXLjwXEnJHUlVAZNjMsI9WsDAo6Q-j3gLa_fxL4vVi9gIKMKYlXnOPbaglEZUmN-qP1pv47rHv5-4Ipwx_7js0W1dA",
    "expires_in": 7200
}
{
     "button":[
     {
          "type":"view",
          "name":"发布活动",
          "url":"http://whitemay.pythonanywhere.com/add_event/"
      },
      {
          "name":"活动管理",
           "sub_button":[
           {
               "type":"view",
               "name":"我发布的活动",
               "url":"http://whitemay.pythonanywhere.com/list_events/?type=mine"
            },
            {
               "type":"view",
               "name":"我报名的活动",
               "url":"http://whitemay.pythonanywhere.com/list_events/?type=other"
            }]
      },
      {
           "type":"click",
           "name":"个人信息",
           "key":"SETTING"
      }]
 }

在公众账号中输入set，会触发一条消息，点击进入set页面。
通过这种方式，服务端会将openid保存到浏览器Cookie内，之后就可以根据这个Cookie来判定是由谁发出的微信访问。
如果不是通过微信发起的访问，或者是在微信外浏览器中访问，就无法获得相关信息，从而不能工作。

使用如下命令来搜集系统用到的static文件：python manage.py collectstatic
但是这些文件分散在不同的包中并不影响使用。

lxml: 工作环境下已经存在lxml，在virtualenv中安装lxml需要使用如下命令
  STATIC_DEPS=true pip install lxml

django-bootstrap3：支持bootstrap3
参考：
  https://github.com/dyve/django-bootstrap3

django-bootstrap3-datepicker：用来选择日期时间的widget

django-jquery-js：最新jQuery库
django-awesome-boostrap：静态资源文件

当浏览器以JSON传递参数时，Django需要这样解析：
def api_response(request):
    try:
        data=json.loads(request.raw_post_data)
        label=data['label']
        url=data['url']
        print label, url
    except:
        print 'nope'
    return HttpResponse('')


页面链接：
1、发布活动：/add_event/
无参数
2、活动管理：/list_events/?type=
参数：type = mine 我发布的活动
     type = other 我报名的活动

TODO: 定时提醒功能
不使用Celery:
Install celery by download or pip install -U Celery
改用：django_cron（原因：更轻量级）
pip install django_cron
doc: https://github.com/Tivix/django-cron