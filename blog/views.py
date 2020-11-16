import datetime

from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.db.models import F
from django.shortcuts import render, redirect
from django.utils import timezone
from django.views.generic import ListView
from django.contrib.auth.forms import PasswordChangeForm
from .forms import TicketForm, CommentForm, UserRegisterForm, UserLoginForm, UpdateUser
from .models import Event, Ticket
from django.contrib.auth import update_session_auth_hash


class HomeListView(ListView):
    model = Event
    template_name = 'blog/index.html'
    context_object_name = 'posts'

    def get_queryset(self):
        return Event.objects.prefetch_related('tags') \
                   .filter(published=True, published_date__lte=datetime.datetime.today())[:6] \
            .select_related('category', 'author')


class AllPostsListView(ListView):
    model = Event
    template_name = 'blog/list_all_posts.html'
    context_object_name = 'posts'
    paginate_by = 6

    def get_queryset(self):
        return Event.objects.filter(published=True, published_date__lte=datetime.datetime.today()) \
            .select_related('category', 'author') \
            .prefetch_related('tags')


def view_news(request, slug):
    news_item = Event.objects.get(slug=slug)
    news_item.views = F('views') + 1
    news_item.save()
    if request.user.is_authenticated:
        tickets = Ticket.objects.filter(user=request.user, event=news_item)
    if news_item.the_date_of_the <= timezone.now() and request.user.is_authenticated:
        if request.method == 'POST':
            form = CommentForm(data=request.POST)
            if form.is_valid():
                response = form.save(commit=False)
                response.name = request.user.first_name
                response.last_name = request.user.last_name
                response.event = news_item
                response.email = request.user.email
                response.save()
                # redirect('home')
        comments = news_item.comment_set.all()
        form = CommentForm()
        return render(request, 'blog/post_detail.html', {'post': news_item, 'form': form, 'comments': comments})
    elif news_item.the_date_of_the >= timezone.now() and news_item.tickets_left != 0 and request.user.is_authenticated and not tickets:
        if request.method == 'POST':
            form = TicketForm(initial={'event': news_item}, data=request.POST)
            if form.is_valid():
                response = form.save(commit=False)
                news_item.tickets_left = F('tickets_left') - 1
                news_item.save()
                response.user = request.user
                response.event = news_item
                response.name = request.user.first_name
                response.surname = request.user.last_name
                response.email = request.user.email
                response.save()
                return redirect('profile')

        form = TicketForm()
        return render(request, 'blog/post_detail.html', {'post': news_item, 'form': form})

    return render(request, 'blog/post_detail.html', {'post': news_item})


class PostsByCategory(ListView):
    model = Event
    template_name = 'blog/views_posts_by_category.html'
    context_object_name = 'posts'
    paginate_by = 6

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = Event.objects.filter(category__slug=self.kwargs['slug']) \
            .select_related('category',
                            'author').prefetch_related('tags').first()
        return context

    def get_queryset(self):
        return Event.objects.filter(published=True, category__slug=self.kwargs['slug'],
                                    published_date__lte=datetime.datetime.today()) \
            .select_related('category', 'author') \
            .prefetch_related('tags')


class PostsByTag(ListView):
    model = Event
    template_name = 'blog/views_posts_by_tag.html'
    context_object_name = 'posts'
    paginate_by = 6

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = Event.objects.filter(tags__slug=self.kwargs['slug']) \
            .select_related('category', 'author') \
            .prefetch_related('tags') \
            .first()
        return context

    def get_queryset(self):
        return Event.objects.filter(tags__slug=self.kwargs['slug'], published=True,
                                    published_date__lte=datetime.datetime.today()) \
            .select_related('category', 'author') \
            .prefetch_related('tags')


class Search(ListView):
    model = Event
    template_name = 'blog/search_list.html'
    context_object_name = 'posts'
    paginate_by = 6

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['s'] = self.request.GET.get('q')
        return context

    def get_queryset(self):
        query = self.request.GET.get('q')
        object_list = Event.objects.filter(title__icontains=query, published=True,
                                           published_date__lte=datetime.datetime.today()) \
            .select_related('category', 'author') \
            .prefetch_related('tags')
        return object_list


def register(request):
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)

        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = UserRegisterForm()

    return render(request, 'blog/register.html', {'form': form})


def user_login(request):
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        form = UserLoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')
    else:
        form = UserLoginForm()

    return render(request, 'blog/login.html', {'form': form})


def user_logout(request):
    logout(request)
    return redirect('home')


@login_required
def profile(request):
    events = Ticket.objects.filter(user=request.user)
    if request.method == 'POST':
        ticket_id = request.POST.get('qw')
        ticket = events.get(id=ticket_id)
        event = Event.objects.filter(id=ticket.event.id)
        event.tickets_left = F('tickets_left') + 1
        event.delete()
        return redirect('profile')

    time_now = timezone.now()
    return render(request, 'blog/profile.html', {'events': events, 'time_now': time_now})


@login_required
def profile_update(request):
    if request.method == "POST":
        form = UpdateUser(data=request.POST, instance=request.user)

        if form.is_valid():
            form.save()
            return redirect('profile')

    form = UpdateUser(instance=request.user)
    return render(request, 'blog/update_profile.html', {'form': form})


@login_required
def change_password(request):
    if request.method == "POST":
        form = PasswordChangeForm(data=request.POST, user=request.user)

        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            return redirect('profile')

    form = PasswordChangeForm(user=request.user)
    return render(request, 'blog/change_password.html', {'form': form})
