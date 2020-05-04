from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.views import generic
from .models import Post, Comment
from .forms import CommentForm, ContactForm
from django.core.mail import EmailMessage
from django.contrib import messages
from django.db.models import Q
from django.conf import settings


# Create your views here.


class Home(generic.ListView):
    model = Post
    template_name = 'blog/home.html'
    context_object_name = 'posts'
    ordering = ['-date_posted']


class PostListView(generic.ListView):
    model = Post
    template_name = 'blog/blog.html'
    context_object_name = 'posts'
    ordering = ['-date_posted']


class UserPostListView(generic.ListView):
    model = Post
    template_name = 'blog/user_post.html'
    context_object_name = 'posts'
    ordering = ['-date_posted']
    paginate_by = 1000

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return Post.objects.filter(author=user).order_by('-date_posted')


class PostDetailView(generic.DetailView):
    model = Post


class PostCreateView(LoginRequiredMixin, generic.CreateView):
    model = Post
    fields = ['title', 'photo', 'content']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, generic.UpdateView):
    model = Post
    fields = ['title', 'photo', 'content']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, generic.DeleteView):
    model = Post
    success_url = '/'

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


def about(request):
    form_class = ContactForm

    if request.method == 'POST':
        form = form_class(request.POST)

        if form.is_valid():
            full_name = request.POST.get('full_name')
            from_email = request.POST.get('from_email')
            message = request.POST.get('message')

            email_message = EmailMessage(
                full_name,
                message,
                from_email,
                [settings.EMAIL_HOST_USER]
            )
            email_message.send()

            return redirect('thanks')

    return render(request, 'blog/about.html', {'title': 'About', 'form': form_class})


def thanks(request):
    return render(request, 'blog/thanks.html')


def newsletter(request):
    return render(request, 'blog/newsletter.html')


############################################################################################################
############################################################################################################


@login_required
def add_comment_to_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = request.POST.get('comment')
            comment = Comment.objects.create(post=post, author=request.user, comment=comment)
            comment.save()
            return redirect('post-detail', pk=post.pk)
    else:
        form = CommentForm()
    return render(request, 'blog/comment_form.html', {'form': form})


@login_required
def comment_delete(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    comment_pk = comment.post.pk
    comment.delete()
    messages.success(request, "Comment Deleted.")
    return redirect('post-detail', pk=comment_pk)


@login_required
def like_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.likes.add(request.user)
    return redirect('post-detail', pk=post.pk)


@login_required
def unlike_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.likes.remove(request.user)
    return redirect('post-detail', pk=post.pk)


def search(request):
    query = request.GET.get('q', '')
    if query is not None:
        queryset = (Q(title__icontains=query) | Q(date_posted__icontains=query) | Q(author__username__icontains=query))
        results = Post.objects.filter(queryset).order_by('-date_posted')
    return render(request, 'blog/search.html', {'results': results, 'query': query})
