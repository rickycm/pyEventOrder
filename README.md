pyEventOrder
====
认证问题：
准备使用任何用户可以使用后，采用如下模式：
1、任何用户在第一次需要登录系统时自动建立用户。原来不要求用户登录的场合（查看活动）依然不要求用户登录
2、系统采用authenticate(userinfo={})的模式建立用户，原先在注册时自动建立用户的过程取消。  //原先没有自动建立用户过程
3、系统进入setting界面后，如果发现获得openid参数并且处于登录状态，就使用该openid代替用户数据库及用户Cookie中的openid。 //现在应该没有Setting页面了吧
4、在add_event和show_event中，都包括一个StringInput字段显示用户的IuputName，并包括初始值。该字段为空时，用户不能提交操作。  //add_event应该是需要关注用户才可以发布活动吧
5、修改了participant的register字段，并把所有输入用户名字的地方改为20字符，需要做数据库的migrate。
