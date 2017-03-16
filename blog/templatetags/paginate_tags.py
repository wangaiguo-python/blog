from django import template
from django.core.paginator import PageNotAnInteger, EmptyPage, Paginator
'paginator 分页    PageNotAnInteger 页码不是一个整数异常   EmptyPage 空的页码异常'

register = template.Library()  #这是定义模板标签要用到的

@register.simple_tag(takes_context = True)
#这个装饰器标明这个函数是一个模板标签
def paginate(context, object_list, page_count):
    # context是Context对象, object_list是你要分页的对象, page_count表示每页的数量
    left = 3
    right = 3 #当前页码右边显示几个页码号 -1

    paginator = Paginator(object_list, page_count) # 通过object_list对象
    page = context['request'].GET.get('page')    # 从Http请求中获取用户请求的页码号

    try:
        object_list = paginator.page(page) #根据页码号获取第几页的数据
        context['current_page'] = int(page) #把当前页封装进context中
        pages = get_left(context['current_page'], left, paginator.num_pages) + get_right(context['current_page'], right, paginator.num_pages)
         # 调用了两个辅助函数，根据当前页得到了左右的页码号，比如设置成获取左右两边2个页码号，那么假如当前页是5，则 pages = [3,4,5,6,7],当然一些细节需要处理，比如如果当前页是2，那么获取的是pages = [1,2,3,4]
    except PageNotAnInteger:
        #异常处理,如果用户传递的page值不是整数,则把第一页的值返回给他
        object_list = paginator.page(1)
        context['current_page'] = 1  #当前页是1
        pages = get_right(context['current_page'], right, paginator.num_pages)
    except EmptyPage:
        #如果传递的 page 是一个空值,那么把最后一页的值返回给他
        object_list = paginator.page(paginator.num_pages)
        context['current_page'] = paginator.num_pages   #当前页是最后一页, num_pages的值是总分页数
        pages = get_left(context['current_page'], left, paginator.num_pages)

    context['article_list'] = object_list  #把获取到的分页的数据封装到上下文中
    context['pages'] = pages   #把页码号列表封装进去
    context['last_page'] = paginator.num_pages #最后一页的页码号
    context['first_page'] = 1  # 第一页的页码号为1

    try:
        #获取 pages 列表第一个值和最后一个值,主要用于在是否该插入省略号的判断
        context['pages_first'] = pages[0]
        context['pages_last'] = pages[-1] + 1
    except IndexError:
        context['pages_first'] = 1  #发生异常说明只有1页
        context['pages_last'] = 2  # 1 + 1 后的值

    return ''  #必须加这个, 否则首页会显示个None







def get_left(current_page, left, num_pages): #辅助函数,获取当前页码的值的左边两个页码值
    if current_page == 1:
        return []
    elif current_page == num_pages:
        l = [i - 1 for i in range(current_page, current_page - left, -1) if i - 1 > 1]
        l.sort()
        return l
    l = [i for i in range(current_page, current_page - left, -1) if i > 1]
    l.sort()
    return l


def get_right(current_page, right, num_pages):
    if current_page == num_pages:
        return []
    return [i + 1 for i in range(current_page, current_page+ right - 1) if i < num_pages - 1 ]

