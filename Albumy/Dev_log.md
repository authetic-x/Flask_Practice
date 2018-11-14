#   Albumy 开发流程

### 初始化

1. 创建蓝本 -- auth, user, main, admin, ajax
2. 创建扩展模块 -- extension
3. 创建配置模块 -- settings
4. 创建初始化模块 -- init
    - 工厂函数
    - 注册路由
    - 注册扩展对象
    - 注册模板上下文
    - 注册shell上下文
    - 注册错误处理函数
    - 初始化数据库函数
5. 创建数据库模块
6. 创建工具类模块 -- utils 实现redirect_back函数
7. 配置.env .flaskenv文件 
8. 创建模板文件夹 -- templates
    - auth
    - main
    - user
    - admin
    - email
    - base.html
    - macros.html
9. 在base.html中引入css, js文件， 并实现初步导航栏，消息处理函数和尾部

### 登录注册， 邮箱验证

1. 创建数据库模型User，继承UserMixin
2. 创建登录注册表单模块 -- auth
3. 在settings模块设置验证操作类Operations
4. 在utils模块利用itsdangerous生成验证令牌
    - generate_token
    - validate_token 设置confirmed为True
5. 创建邮件模块 -- email 利用flask_mail扩展发送邮件
6. 创建邮件内容模板 -- confirm.html 其中url为confirm验证函数
7. 在auth蓝图中实现注册函数，发送验证邮件
8. 实现confirm验证函数，验证成功重定向到main.index主页，否则充新发送
9. 实现login登录函数，重定向到主页
10. 修改密码需要验证，操作流程与注册类似
11. 创建decorators模板，实现过滤未验证用户装饰器 -- confirm_required
12. 在extension扩展模块中注册user_loader，完成flask_login的相关配置


### 权限处理

1. 创建Role角色和Permission权限数据库模型，并建立多对多关系
2. 在Role模型类中实现角色初始化静态函数
3. 为User模型添加Role角色对象，建立多对一关系，默认角色为User
4. 在User模型里实现can函数，并实现perimission_required装饰器
5. 实现admin_required装饰器
6. 在extensions模块中实现Guest类，继承Flask_login匿名用户类， 实现can方法和is_admin属性

### 主页

1. 实现登录后的导航栏页面，通知，上传，个人信息
2. 创建Photo数据库模型，并在User模型中添加photoes对象，建立一对多关系

#### 文件上传

1. 利用Flask_Dropzone扩展实现文件上传
2. 创建upload上传页面，配置相关css, js文件
3. 利用dropzone.create()渲染上传区域
4. 在main蓝图实现upload函数，保存图片
5. 裁剪图片
    - 在Photo模型中添加filename_s和filename_m
    - 在utils模块中实现裁剪函数resize_image

#### 用户头像

1. 利用Flask_Avatar生成随机头像
2. 在settings模块里配置保存路径和头像大小
3. 在User模型里添加三个avatar字段，利用Identicon生成头像
4. 在main蓝图中创建get_avatar视图函数

#### 图片展示

1. 在main蓝图中创建get_image视图函数
2. 创建图片详情页 -- main/photo.html
3. 创建两个模态框，分享和删除图片
4. 添加report举报表单
5. 添加评论区域
    - 添加Comment数据库模型
    - 一个用户有多个评论，与User建立一对多关系
    - 一张图片有多个评论，与Photo建立一对多关系
    - 一个评论有多个回复，与Comment自身建立一对多关系(需设置remote_side主键)
    - 创建评论页面 -- \_comment.html
    - 在main蓝图里添加new_comment, reply_comment和delete_comment视图函数
    - 删除图片需要设置数据库监听事件，同时删除本地文件
    - 注意路由规则以及重定向页面，还有用户的权限问题
    - 由于数据库先创建，就没有添加关闭评论和举报评论的功能
6. 添加侧边栏，包括前后页，作者栏，图片介绍
    - 在main蓝图中添加next_photo和previous_photo视图函数，实现图片翻页
7. 图片描述
    - 创建DescriptionForm图片描述表单
    - 在_photo_sidebar.html中添加表单，并添加js效果实现隐藏
    - 在main蓝图中添加edit_description实现添加图片描述功能
    - 创建Tag数据库模型
    - 一个图片有多个标签，一个标签属于多张图片，为标签和图片建立多对多关系
    - 添加TagForm标签表单
    - 在main蓝图中添加new_tag函数添加标签，delete_tag删除标签
    - 在main蓝图中添加show_tag视图函数展示该标签所有图片
    - 其中show_tag页面提供了两种图片排序方式，需要设置两个路由

#### 收藏图片

1. 创建中间模型Collect，分别与User和Photo建立一对多关系
2. 在User模型中添加collect, uncollect, is_collecting函数
3. 在main蓝本中添加collect, uncollect视图函数
4. 在_photo_sidebar.html添加收藏或取消收藏按钮
5. 创建user_card宏来渲染用户卡片
6. 在main蓝本中添加show_collectors视图函数显示图片的收藏者
7. 创建collectors.html来显示收藏者页面
8. 在user蓝本中添加show_collections函数显示用户收藏的图片
9. 创建user/collections.html页面


### 用户页面

1. 创建用户主页局部模板_header.html
2. 创建图片宏photo_card，显示小号图片以及收藏数和评论数
3. 在user蓝图里创建index函数，展示用户图片，包括各种用户信息(头像小了)
4. follow, collect等信息后续完善_

#### 用户资料弹窗

1. 通过设置js悬停来触发用户弹窗
2. 创建弹窗页面profile_popup.html
3. ajax返回，创建蓝本ajax_bp，在其中添加get_profile函数返回弹窗
4. 触发方式为将url存储在data-href属性里
5. jquery.hover触发事件...

#### 用户关注

1. 创建Follow中间模型，与User类建立两个一对多关系，表示关注和被关注
2. 在User模型中添加follow, unfollow, is_following方法
3. 在user蓝本中添加follow, unfollow视图函数
4. 添加follow_area宏渲染关注操作
5. 在user蓝本中添加show_followers函数显示关注者，show_following
6. 创建followers.html和follwing.html页面
7. 使用ajax在用户弹窗中实现关注和取消关注

#### 消息提醒

1. 创建Notification数据库模型，与User建立多对一关系
2. 创建notification模块实现推送评论，关注，收藏消息
3. 在follow等视图函数中添加消息推送逻辑
4. 在main蓝本中添加show_notification函数显示消息
5. 创建main/notification.html消息页面
6. 在main蓝本中添加read_notification和read_all_notifications实现阅读消息
7. 通过ajax轮询实时更新未读计数

### 用户设置

1. 创建设置页面基模板base.html
2. 创建个人资料EditProfileForm表单，创建edit_profile.html页面
3. 自定义头像(有问题！)
    - 在User模型里创建avatar_raw存储原图文件
    - 使用Flask_Avatar实现图片裁剪
    - 创建change_avatar.html页面，引入相应的css, js文件
    - 创建UploadAvatarForm头像上传表单
    - 创建CropAvatarForm头像裁剪表单
    - 在user蓝本里添加change_avatar函数转向裁剪页面
    - 在user蓝本里添加upload_avatar函数实现头像上传
    - 在user蓝本里添加crop_avatar函数实现头像裁剪
4. 更改密码
    - 创建更改密码表单ChangerPasswordForm
    - 在user蓝本中添加change_password函数更改密码
    - 设置fresh_login_required装饰器，并添加相应函数和配置
5. 提醒消息开关
    - 在User数据库模型中添加三个提醒开关字段
    - 创建NotificationSettingForm消息提醒表单
    - 在User蓝本中添加notification_setting设置消息提醒
    - 在follow, collect, comment等视图函数添加消息提醒判断
6. 收藏仅自己可见
    - 在User模型中添加show_collections字段
    - 创建表单
    - 添加视图函数
7. 注销账户
    - 创建注销表单
    - 添加视图函数
    - 在model模块中设置注销监听，删除头像
8. 更改邮箱
    - 创建表单
    - 添加视图函数
    - 发送重新确认电子邮件

### 完善主页和添加explore

1. 完成main蓝本中的index函数
2. 添加侧边栏，显示热门标签(使用联结分组查询)
3. 获取随机图片，实现探索功能
4. 使用Flask_Whooshee实现全局搜索
    - 实例化Whooshee对象
    - 创建索引，为User, Photo, Tag模型添加装饰器
    - 创建搜索表单
    - 在main蓝本中添加视图函数search实现搜索


### 添加网站后台

1. 锁定用户
    - 在User字段里添加locked字段，并添加lock和unlock方法
    - 在admin蓝本里添加lock_user和unlock_user视图函数
    - 在user/\_header_bar.html里添加锁定按钮
    - 在user蓝本index函数里发送锁定消息
2. 封禁用户
    - 在User模型里添加active字段，并添加is_active属性，继承SessionMixin
    - Flask_Login会判断用户属性is_active是否为True，否则拒绝登录
3. 添加删除图片逻辑
4. 面向管理员的用户资料编辑
    - 创建EditProfileAdminForm表单
    - 在admin蓝本里添加edit_profile_admin视图函数
5. 此外还包括评论，标签，用户等各种管理，未完善...