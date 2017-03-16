from django.shortcuts import render, get_object_or_404, HttpResponseRedirect
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from blog.models import Article, Category, Tag
import markdown2
from django.views.generic.edit import FormView
from .forms import BlogCommentForm

# Create your views here.

class IndexView(ListView):
    template_name = 'blog/index.html'
    context_object_name = 'article_list'

    def get_queryset(self):
        article_list = Article.objects.filter(status='p')
        for article in  article_list:
            article.body = markdown2.markdown(article.body, extras=['fenced-code-blocks'],)
        return article_list

    def get_context_data(self, **kwargs):
        kwargs['category_list'] = Category.objects.all().order_by('name')
        kwargs['date_archive'] = Article.objects.archive()
        kwargs['tag_list'] = Tag.objects.all().order_by('name')

        return super(IndexView, self).get_context_data(**kwargs)


class ArticleDetailView(DetailView):
    model = Article
    template_name = 'blog/detail.html'
    context_object_name = 'article'
    pk_url_kwarg = 'article_id'

    def get_object(self, queryset=None):
        obj = super(ArticleDetailView, self).get_object()
        obj.body = markdown2.markdown(obj.body, extras=['fenced-code-blocks'], )
        return obj

    # 新增 form 到 context
    def get_context_data(self, **kwargs):
        kwargs['comment_list'] = self.object.blogcomment_set.all()
        kwargs['form'] = BlogCommentForm()
        return super(ArticleDetailView, self).get_context_data(**kwargs)



'''自我认为: 本身基于类的通用视图 就是减少代码量而来的 所以大部分可以直接继承自IndexView 从而减少很多代码的重复敲敲'''
class CategoryView(IndexView):
    # template_name = 'blog/index.html'
    # context_object_name = 'article_list'
    #
    def get_queryset(self):
        article_list = Article.objects.filter(category=self.kwargs['cate_id'], status='p')
        for article in article_list:
            article.body = markdown2.markdown(article.body, extras=['fenced-code-blocks'], )
        return article_list

    # def get_context_data(self, **kwargs):
    #     kwargs['category_list'] = Category.objects.all().order_by('name')
    #     kwargs['tag_list'] = Tag.objects.all().order_by('name')
    #     return super(CategoryView, self).get_context_data(**kwargs)



class TagView(ListView):
    template_name = 'blog/index.html'
    context_object_name = 'article_list'

    def get_queryset(self):
        article_list = Article.objects.filter(tags=self.kwargs['tag_id'], status='p')
        for article in article_list:
            article.body = markdown2.markdown(article.body, extras=['fenced-code-blocks'], )
        return article_list

    def get_context_data(self, **kwargs):
        kwargs['tag_list'] = Tag.objects.all().order_by('name')
        return super(TagView, self).get_context_data(**kwargs)



class ArchiveView(ListView):
    template_name = 'blog/index.html'
    context_object_name = 'article_list'

    def get_queryset(self):
        year = int(self.kwargs['year'])
        month = int(self.kwargs['month'])
        article_list = Article.objects.filter(created_time__year=year, created_time__month=month)
        for article in article_list:
            article.body = markdown2.markdown(article.body, extras=['fenced-code-blocks'], )
        return article_list

    def get_context_data(self, **kwargs):
        kwargs['tag_list'] = Tag.objects.all().order_by('name')
        return super(ArchiveView, self).get_context_data(**kwargs)



class CommentPostView(FormView):
    form_class = BlogCommentForm  #指定使用的是哪个form
    template_name = 'blog/detail.html'  # 指定评论提交成功后跳转渲染的模板文件.

    def form_valid(self, form):
        """提交的数据验证合法后的逻辑"""
        #首先根据 url 传入的参数(在self.kwargs 中) 获取到被评论的文章
        target_article = get_object_or_404(Article, pk=self.kwargs['article_id'])

        #调用ModelForm的save方法保存评论, 设置commit=FALSE 则先不保存到数据库.
        #而是返回生成的comment实例, 直到真正调用save方法时才保存到数据.
        comment = form.save(commit = False)

        #把评论和文章关联
        comment.article = target_article
        comment.save()

        #评论生成成功, 重定向到被评论的文章页面, get_absolute_url
        self.success_url = target_article.get_absolute_url()
        return HttpResponseRedirect(self.success_url)

    def form_invalid(self, form):
        '''提交的数据验证不合法后的逻辑'''
        target_article = get_object_or_404(Article, pk=self.kwargs['article_id'])

        #不保存评论, 回到原来提交的文章详情页面
        return render(self.request, 'blog/detail.html',
                      {
                          'form': form,
                          'article': target_article,
                          'comment_list': target_article.blogcomment_set.all()
                      })








