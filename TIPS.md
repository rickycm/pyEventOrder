本文档用来保存一些有用的信息
==============================
使用如下命令来搜集系统用到的static文件：python manage.py collectstatic
对应的配置已经存在于setting文件中

django-bootstrap3：支持bootstrap3
参考：
  https://github.com/dyve/django-bootstrap3

django-awesome-boostrap：静态资源文件

django-html5-boilerplate：支持HTML5。
参考：
  https://github.com/mattsnider/django-html5-boilerplate
关键操作：
  INSTALLED_APPS 'dh5bp'
  {% extends 'dh5mbp/base.html' %}
  {% load url from future %}
  {% load staticfiles %}
  {% block title %}YOUR TITLE HERE{% endblock %}
  {% block content %}YOUR JQUERY MOBILE MARKUP HERE{% endblock %}

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