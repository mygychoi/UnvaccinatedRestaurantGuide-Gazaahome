from django.views.generic import TemplateView, ListView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin

from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse, reverse_lazy
from django.http import HttpResponseRedirect
from django.core.exceptions import PermissionDenied

from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST

from django.utils.text import slugify

from hitcount.views import HitCountDetailView

from corona.models import Restaurant, RestaurantComment, RestaurantTag
from corona.models import Post, PostComment, PostCategory

from corona.forms import RestaurantForm, RestaurantCommentForm
from corona.forms import PostForm, PostCommentForm


def get_num_restaurants():
    context = {
        'num_restaurants': Restaurant.objects.count(),
        'num_unvaccinated_available': Restaurant.objects.filter(unvaccinated_pass__type='미접종 친절').count(),
        'num_unvaccinated_unavailable': Restaurant.objects.filter(unvaccinated_pass__type='미접종 거부').count(),
    }

    return context


class MapView(TemplateView):
    template_name = 'corona/unvaccinated_restaurant/map.html'

    def get_context_data(self, **kwargs):
        context = super(MapView, self).get_context_data(**kwargs)

        restaurant_list = Restaurant.objects.exclude(latitude__isnull=True).exclude(longitude__isnull=True)
        context['restaurant_list'] = restaurant_list
        context['test'] = Restaurant.objects.last()
        context.update(get_num_restaurants())

        return context


class RestaurantList(ListView):
    model = Restaurant
    template_name = 'corona/unvaccinated_restaurant/index.html'
    context_object_name = 'restaurant_list'
    paginate_by = 8
    ordering = '-pk'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(RestaurantList, self).get_context_data()
        context.update(get_num_restaurants())

        return context


class PopularRestaurantList(ListView):
    model = Restaurant
    template_name = 'corona/unvaccinated_restaurant/index.html'
    context_object_name = 'restaurant_list'
    paginate_by = 8
    queryset = Restaurant.objects.order_by("-hit_count_generic__hits", '-pk')[:20]

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(PopularRestaurantList, self).get_context_data()
        context.update(get_num_restaurants())

        return context


class AvailableRestaurantList(ListView):
    model = Restaurant
    template_name = 'corona/unvaccinated_restaurant/index.html'
    context_object_name = 'restaurant_list'
    paginate_by = 8
    queryset = Restaurant.objects.filter(unvaccinated_pass__type='미접종 친절')
    ordering = '-pk'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(AvailableRestaurantList, self).get_context_data()
        context.update(get_num_restaurants())

        return context


class UnavailableRestaurantList(ListView):
    model = Restaurant
    template_name = 'corona/unvaccinated_restaurant/index.html'
    context_object_name = 'restaurant_list'
    paginate_by = 8
    queryset = Restaurant.objects.filter(unvaccinated_pass__type='미접종 거부')
    ordering = '-pk'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(UnavailableRestaurantList, self).get_context_data()
        context.update(get_num_restaurants())

        return context


class RestaurantDetail(HitCountDetailView):
    model = Restaurant
    template_name = 'corona/unvaccinated_restaurant/detail.html'
    count_hit = True

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(RestaurantDetail, self).get_context_data()
        context['restaurant_comment_form'] = RestaurantCommentForm
        context.update(get_num_restaurants())

        return context


class CreateRestaurant(CreateView):
    model = Restaurant
    form_class = RestaurantForm
    template_name = 'corona/unvaccinated_restaurant/create.html'

    def form_valid(self, form):
        current_user = self.request.user

        if current_user.is_authenticated:
            form.instance.author = current_user

        response = super(CreateRestaurant, self).form_valid(form)

        tags_str = self.request.POST.get('tags_str')

        if tags_str:
            tags_str = tags_str.strip(' #')
            tags_str = tags_str.replace(',', '#')
            tags_list = tags_str.split('#')

            for tag in tags_list:
                tag = tag.strip()
                tag, is_tag_created = RestaurantTag.objects.get_or_create(name=tag)
                if is_tag_created:
                    tag.slug = slugify(tag, allow_unicode=True)
                    tag.save()
                self.object.tags.add(tag)

        return response


class UpdateRestaurant(UpdateView):
    model = Restaurant
    form_class = RestaurantForm
    template_name = 'corona/unvaccinated_restaurant/update.html'

    def get_context_data(self, **kwargs):
        context = super(UpdateRestaurant, self).get_context_data()
        if self.object.tags.exists():
            tags_str_list = []
            for tag in self.object.tags.all():
                tags_str_list.append(tag.name)
            context['tags_str_default'] = '#' + '#'.join(tags_str_list)

        return context

    def form_valid(self, form):
        response = super(UpdateRestaurant, self).form_valid(form)
        self.object.tags.clear()

        tags_str = self.request.POST.get('tags_str')

        if tags_str:
            tags_str = tags_str.strip(' #')
            tags_str = tags_str.replace(',', '#')
            tags_list = tags_str.split('#')

            for tag in tags_list:
                tag = tag.strip(' #')
                tag, is_tag_created = RestaurantTag.objects.get_or_create(name=tag)
                if is_tag_created:
                    tag.slug = slugify(tag, allow_unicode=True)
                    tag.save()
                self.object.tags.add(tag)

        return response


@require_POST
@login_required
def like_restaurant(request, pk):
    restaurant = get_object_or_404(Restaurant, pk=pk)
    if restaurant.likes.filter(pk=request.user.pk).exists():
        restaurant.likes.remove(request.user)
    else:
        restaurant.likes.add(request.user)

    return HttpResponseRedirect(reverse('corona:restaurant_detail', args=(pk,)))


@require_POST
@login_required
def dislike_restaurant(request, pk):
    restaurant = get_object_or_404(Restaurant, pk=pk)
    if restaurant.dislikes.filter(pk=request.user.pk).exists():
        restaurant.dislikes.remove(request.user)
    else:
        restaurant.dislikes.add(request.user)

    return HttpResponseRedirect(reverse('corona:restaurant_detail', args=(pk,)))


def create_restaurant_comment(request, pk):
    if request.user.is_authenticated:
        restaurant = get_object_or_404(Restaurant, pk=pk)

        if request.method == 'POST':
            restaurant_comment_form = RestaurantCommentForm(request.POST)

            if restaurant_comment_form.is_valid():
                restaurant_comment = restaurant_comment_form.save(commit=False)
                restaurant_comment.restaurant = restaurant
                restaurant_comment.author = request.user
                restaurant_comment.save()

                return redirect(restaurant_comment.get_absolute_url())
        else:
            return redirect(restaurant.get_absolute_url())
    else:
        raise PermissionDenied


def delete_restaurant_comment(request, restaurant_pk, pk):
    restaurant_comment = get_object_or_404(RestaurantComment, pk=pk)
    restaurant = restaurant_comment.restaurant

    if request.user.is_authenticated and request.user == restaurant_comment.author:
        restaurant_comment.delete()
        return redirect(restaurant.get_absolute_url())
    else:
        raise PermissionDenied


class UpdateRestaurantComment(LoginRequiredMixin, UpdateView):
    model = RestaurantComment
    form_class = RestaurantCommentForm
    template_name = 'corona/unvaccinated_restaurant/comment/update.html'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated and request.user == self.get_object().author:
            return super(UpdateRestaurantComment, self).dispatch(request, *args, **kwargs)
        else:
            raise PermissionDenied


@require_POST
@login_required
def like_restaurant_comment(request, restaurant_pk, pk):
    restaurant_comment = get_object_or_404(RestaurantComment, pk=pk)

    if restaurant_comment.likes.filter(pk=request.user.pk).exists():
        restaurant_comment.likes.remove(request.user)
    else:
        restaurant_comment.likes.add(request.user)

    return HttpResponseRedirect(reverse('corona:restaurant_detail', args=(restaurant_pk,)))


####################


class PostList(ListView):
    model = Post
    template_name = 'corona/post/index.html'
    context_object_name = 'post_list'
    paginate_by = 8
    ordering = '-pk'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(PostList, self).get_context_data()
        context['categories'] = PostCategory.objects.iterator()

        return context


class PopularPostList(ListView):
    model = Post
    template_name = 'corona/post/index.html'
    context_object_name = 'post_list'
    paginate_by = 8
    queryset = Post.objects.order_by("-hit_count_generic__hits", '-pk')[:20]

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(PopularPostList, self).get_context_data()
        context['categories'] = PostCategory.objects.iterator()

        return context


class CategoryPostList(ListView):
    model = Post
    template_name = 'corona/post/index.html'
    context_object_name = 'post_list'
    paginate_by = 5
    ordering = '-pk'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(CategoryPostList, self).get_context_data()
        context['category'] = PostCategory.objects.get(name=self.kwargs['name'])
        context['categories'] = PostCategory.objects.iterator()

        return context

    def get_queryset(self):
        queryset = Post.objects.filter(category__name=self.kwargs['name'])
        return queryset


class PostDetail(HitCountDetailView):
    model = Post
    template_name = 'corona/post/detail.html'
    count_hit = True

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(PostDetail, self).get_context_data()
        context['post_comment_form'] = PostCommentForm
        context['categories'] = PostCategory.objects.iterator()
        context['num_post'] = Post.objects.count()

        return context


class CreatePost(LoginRequiredMixin, CreateView):
    model = Post
    form_class = PostForm
    template_name = 'corona/post/create.html'

    def form_valid(self, form):
        current_user = self.request.user

        if current_user.is_authenticated:
            form.instance.author = current_user

        response = super(CreatePost, self).form_valid(form)

        return response


class UpdatePost(LoginRequiredMixin, UpdateView):
    model = Post
    form_class = PostForm
    template_name = 'corona/post/update.html'

    def dispatch(self, request, *args, **kwargs):
        post = Post.objects.get(pk=self.kwargs['pk'])
        if post.author == self.request.user:
            return super(UpdatePost, self).dispatch(request, *args, **kwargs)
        else:
            raise PermissionDenied

    def get_context_data(self, **kwargs):
        context = super(UpdatePost, self).get_context_data()
        return context

    def form_valid(self, form):
        response = super(UpdatePost, self).form_valid(form)
        return response


class DeletePost(LoginRequiredMixin, DeleteView):
    model = Post
    template_name = 'corona/post/delete.html'

    def dispatch(self, request, *args, **kwargs):
        post = Post.objects.get(pk=self.kwargs['pk'])
        if post.author == self.request.user:
            return super(DeletePost, self).dispatch(request, *args, **kwargs)
        else:
            raise PermissionDenied

    def get_context_data(self, **kwargs):
        context = super(DeletePost, self).get_context_data(**kwargs)
        post = Post.objects.get(pk=self.kwargs['pk'])
        context['post'] = post
        return context

    def get_success_url(self):
        return reverse_lazy('corona:post_index')


@require_POST
@login_required
def like_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if post.likes.filter(pk=request.user.pk).exists():
        post.likes.remove(request.user)
    else:
        post.likes.add(request.user)

    return HttpResponseRedirect(reverse('corona:post_detail', args=(pk,)))


@require_POST
@login_required
def dislike_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if post.dislikes.filter(pk=request.user.pk).exists():
        post.dislikes.remove(request.user)
    else:
        post.dislikes.add(request.user)

    return HttpResponseRedirect(reverse('corona:post_detail', args=(pk,)))


def create_post_comment(request, pk):
    if request.user.is_authenticated:
        post = get_object_or_404(Post, pk=pk)

        if request.method == 'POST':
            post_comment_form = PostCommentForm(request.POST)

            if post_comment_form.is_valid():
                post_comment = post_comment_form.save(commit=False)
                post_comment.post = post
                post_comment.author = request.user
                post_comment.save()

                return redirect(post_comment.get_absolute_url())
        else:
            return redirect(post.get_absolute_url())
    else:
        raise PermissionDenied


def delete_post_comment(request, post_pk, pk):
    post_comment = get_object_or_404(PostComment, pk=pk)
    post = post_comment.post

    if request.user.is_authenticated and request.user == post_comment.author:
        post_comment.delete()
        return redirect(post.get_absolute_url())
    else:
        raise PermissionDenied


class UpdatePostComment(LoginRequiredMixin, UpdateView):
    model = PostComment
    form_class = PostCommentForm
    template_name = 'corona/post/comment/update.html'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated and request.user == self.get_object().author:
            return super(UpdatePostComment, self).dispatch(request, *args, **kwargs)
        else:
            raise PermissionDenied


@require_POST
@login_required
def like_post_comment(request, post_pk, pk):
    post_comment = get_object_or_404(PostComment, pk=pk)

    if post_comment.likes.filter(pk=request.user.pk).exists():
        post_comment.likes.remove(request.user)
    else:
        post_comment.likes.add(request.user)

    return HttpResponseRedirect(reverse('corona:post_detail', args=(post_pk,)))