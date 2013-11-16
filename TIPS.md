本文档用来保存一些有用的信息
==============================
django-html5-mobile-boilerplate：支持HTML5以及jQuery Mobile。
参考：
    https://pypi.python.org/pypi/django-html5-mobile-boilerplate
    https://github.com/mattsnider/django-html5-boilerplate
关键操作：
    INSTALLED_APPS 'dh5mbp'
    {% extends 'dh5mbp/base.html' %}
    {% load url from future %}
    {% load staticfiles %}
    {% block title %}YOUR TITLE HERE{% endblock %}
    {% block content %}YOUR JQUERY MOBILE MARKUP HERE{% endblock %}

django使用jQuery Mobile时的一些技巧：http://blog.vrplumber.com/b/2011/06/08/miscellaneous-jquery-mobile-django/
.使用"content"和"title"块，会被自动映射到data-role=header/content; provide your navigation, django message-display and login/logout buttons in the overall page template, use the JQM theme system if possible to control display of these elements
.必要时添加data-role="none"，如果你不希望某些区域mobileized (e.g. image inputs, which are somewhat useless when mobile-ized)
.必须添加rel="external" (or the like) 来防止使用JQM的URL加载机制。(e.g. 下载链接 / the django admin portal / 其它非JQM页面)
.在表单提交到同一URL时，考虑使用data-json="false"。它会停用JQM的页面切换机制，但同时也会避免错误的历史记录，正确在当前页面显示错误信息，或成功redirect到一个成功页面。
.不要使用redirect;
.page-level脚本应在page里面
.use named URLs and {% url name %} (in templates) or reverse( name ) to provide all URLs, this has the effect of canonicalizing the urls (as well as giving you a flexible URL mapping, of course), which avoids the nastiness where you load the same page with e.g. '/' or '/.' at the end versus the same url without
.JQM不会自动清理pages, 得自己处理

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