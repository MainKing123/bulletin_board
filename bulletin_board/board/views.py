from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import (
    ListView, DetailView, CreateView,
    UpdateView, DeleteView, View
)
from django.shortcuts import redirect, get_object_or_404
from .models import Post, Response
from .forms import PostForm, ResponseForm
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.urls import reverse
from .models import OneTimeCode
from .forms import CustomRegisterForm
from django.core.mail import send_mail
from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.models import User
from .models import Ad


class PostListView(ListView):
    model = Post
    template_name = 'post_list.html'
    context_object_name = 'posts'
    ordering = ['-created_at']
    paginate_by = 10


class PostDetailView(DetailView):
    model = Post
    template_name = 'post_detail.html'
    context_object_name = 'post'


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    form_class = PostForm
    template_name = 'post_form.html'
    success_url = reverse_lazy('post_list')

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class PostUpdateView(LoginRequiredMixin, UpdateView):
    model = Post
    form_class = PostForm
    template_name = 'post_form.html'
    success_url = reverse_lazy('post_list')

    def get_queryset(self):
        return Post.objects.filter(author=self.request.user)


class PostDeleteView(LoginRequiredMixin, DeleteView):
    model = Post
    template_name = 'post_confirm_delete.html'
    success_url = reverse_lazy('post_list')

    def get_queryset(self):
        return Post.objects.filter(author=self.request.user)


class MyPostListView(LoginRequiredMixin, ListView):
    model = Post
    template_name = 'my_post_list.html'
    context_object_name = 'posts'

    def get_queryset(self):
        return Post.objects.filter(author=self.request.user).order_by('-created_at')


class ResponseCreateView(LoginRequiredMixin, CreateView):
    model = Response
    form_class = ResponseForm
    template_name = 'response_form.html'

    def form_valid(self, form):
        post = get_object_or_404(Post, pk=self.kwargs['pk'])
        form.instance.author = self.request.user
        form.instance.post = post
        return super().form_valid(form)

    def get_success_url(self):
        return self.object.post.get_absolute_url()


class ResponseListView(LoginRequiredMixin, ListView):
    model = Response
    template_name = 'response_list.html'
    context_object_name = 'responses'

    def get_queryset(self):
        return Response.objects.filter(post__author=self.request.user).order_by('-created_at')


@method_decorator(login_required, name='dispatch')
class AcceptResponseView(View):
    def post(self, request, pk):
        response = get_object_or_404(Response, pk=pk, post__author=request.user)
        response.is_accepted = True
        response.save()
        return redirect('response_list')


@method_decorator(login_required, name='dispatch')
class DeleteResponseView(View):
    def post(self, request, pk):
        response = get_object_or_404(Response, pk=pk, post__author=request.user)
        response.delete()
        return redirect('response_list')

@login_required
def accept_response(request, pk):
    response = get_object_or_404(Response, pk=pk, post__author=request.user)
    response.is_accepted = True
    response.save()
    messages.success(request, 'Отклик принят.')
    return HttpResponseRedirect(reverse('response_list'))


@login_required
def reject_response(request, pk):
    response = get_object_or_404(Response, pk=pk, post__author=request.user)
    response.is_accepted = False
    response.save()
    messages.info(request, 'Отклик отклонён.')
    return HttpResponseRedirect(reverse('response_list'))


@login_required
def response_toggle_view(request, pk):
    """Если уже принят — отклоняет, иначе — принимает."""
    response = get_object_or_404(Response, pk=pk, post__author=request.user)
    response.is_accepted = not response.is_accepted
    response.save()
    messages.success(
        request,
        f'Статус отклика изменён на: {"Принят" if response.is_accepted else "Отклонён"}.'
    )
    return HttpResponseRedirect(reverse('response_list'))
def register_view(request):
    if request.method == 'POST':
        form = CustomRegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False  # пока не подтвердит код
            user.set_password(form.cleaned_data['password'])
            user.save()
            code = OneTimeCode.objects.create(user=user)
            send_mail(
                'Ваш код подтверждения',
                f'Код: {code.code}',
                'noreply@example.com',
                [user.email],
            )
            return redirect('confirm_email')
    else:
        form = CustomRegisterForm()
    return render(request, 'register.html', {'form': form})


def confirm_email_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        code = request.POST.get('code')
        try:
            user = User.objects.get(username=username)
            otp = OneTimeCode.objects.get(user=user)
            if otp.code == code and otp.is_valid():
                user.is_active = True
                user.save()
                otp.delete()
                login(request, user)
                return redirect('ad_list')
            else:
                messages.error(request, "Неверный или просроченный код.")
        except:
            messages.error(request, "Пользователь или код не найдены.")
    return render(request, 'confirm_email.html')
@login_required
def profile_view(request):
    user = request.user
    posts = Post.objects.filter(author=user).order_by('-created_at')
    responses = Response.objects.filter(author=user).order_by('-created_at')
    return render(request, 'account.html', {
        'posts': posts,
        'responses': responses
    })
@login_required
def response_create(request, pk):
    post = get_object_or_404(Post, pk=pk)

    # Запрет повторного отклика
    existing_response = Response.objects.filter(post=post, user=request.user).first()
    if existing_response:
        messages.error(request, 'Вы уже откликались на это объявление.')
        return redirect('ad_detail', pk=pk)

    if request.method == 'POST':
        form = ResponseForm(request.POST)
        if form.is_valid():
            response = form.save(commit=False)
            response.post = post
            response.user = request.user
            response.save()
            messages.success(request, 'Отклик отправлен!')
            return redirect('ad_detail', pk=pk)
    else:
        form = ResponseForm()

    return render(request, 'response_form.html', {'form': form})
def ad_list(request):
    ads = Ad.objects.all()
    return render(request, 'board/ad_list.html', {'ads': ads})