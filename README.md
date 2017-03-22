# blog
模拟简书上一个小团队敲的blog系统


1、fork 本项目到你的仓库

2、克隆你的仓库到本地

3、命令行执行 pip install -r requirements.txt（注意在 requirements.txt 所在目录下执行，否则请输入完整路径名）安装依赖包

4、迁移数据库，在 manage.py 所在目录执行

 python manage.py makemigrations
 python manage.py migrate

5、类似步骤4，运行命令创建超级用户

 python manage.py createsuperuser
6、类似步骤4、5，在 manage.py 所在目录执行

 python manage.py runserver
浏览器输入 http://127.0.0.1:8000/


