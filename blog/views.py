import datetime
import calendar

from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .models import Post, SurveyHistory
from django.contrib.auth.models import User
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView
)


# Function based home view
#
# @login_required
# def home(request):
#     context = {
#         'posts': Post.objects.all()
#     }
#     return render(request, 'blog/home.html', context)


class PostListView(LoginRequiredMixin, ListView):
    model = Post
    template_name = 'blog/home.html'  # <app>/<model>_<viewtype>.html
    context_object_name = 'posts'
    ordering = ['-date_posted']
    paginate_by = 5


class UserPostListView(LoginRequiredMixin, ListView):
    model = Post
    template_name = 'blog/user_posts.html'  # <app>/<model>_<viewtype>.html
    context_object_name = 'posts'
    paginate_by = 3

    def get_queryset(self):
        user = get_object_or_404(User, username = self.kwargs.get('username'))
        return Post.objects.filter(author = user).order_by('-date_posted')


class PostDetailView(DetailView):
    model = Post


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['title', 'content']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ['title', 'content']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    success_url = '/'

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


@login_required
def about(request):
    return render(request, 'blog/about.html', {'title': 'About'})


@login_required
def analytics(request):
    now = datetime.datetime.utcnow()
    current_user = request.user
    current_month = now.month
    current_year = now.year
    current_month_range = calendar.monthrange(current_year, current_month)[1]

    user = User.objects.filter(username=current_user).first()
    posts = Post.objects.filter(author=user)
    posts_by_author = [post.title for post in posts]

    current_month_date_range = [datetime.date(current_year, current_month, current_day)
                           for current_day in range(1, current_month_range + 1)]

    current_month_days_range = [int(day) for day in range(1, current_month_range + 1)]

    result = {}
    for post in posts:
        current_post_surveys = SurveyHistory.objects.filter(post=post)
        for current_date in current_month_date_range:
            for survey in current_post_surveys:
                survey_record_date = survey.recorded_date.date()

                if post not in result:
                    result[post] = {}
                    result[post][current_date] = 0
                elif current_date == survey_record_date and survey.record:
                    result[post][current_date] = 1
                else:
                    if current_date not in result[post]:
                        result[post][current_date] = 0

    context = {
        'current_user': current_user,
        'current_month': current_month,
        'current_year': current_year,
        'current_month_date_range': current_month_date_range,
        'current_month_days_range': current_month_days_range,
        'posts': posts,
        'posts_by_author': posts_by_author,
        'result': result
    }

    return render(request, 'blog/analytics.html', context)
