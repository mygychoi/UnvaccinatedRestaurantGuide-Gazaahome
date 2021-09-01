from django.shortcuts import render, redirect, get_object_or_404

from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.utils.text import slugify
from django.urls import reverse, reverse_lazy
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from hitcount.views import HitCountDetailView

from forum.models import Post, Category, Tag, Comment
from forum.forms import CommentForm, PostForm
from video_forum.forms import VideoCommentForm, VideoForm
from video_forum.models import Video, VideoTag, VideoComment
from django.contrib.auth.models import User


# def tag_post(request, slug):
#     tag = Tag.objects.get(slug=slug)
#     post_list = tag.post_set.all()
#
#     context = {
#         'post_list': post_list.order_by('-pk'),
#         'tag': tag,
#         'categories': Category.objects.all().order_by("priority"),
#     }
#
#     return render(
#         request,
#         'forum/post_list.html',
#         context,
#     )
#
#
# class LikesPostList(ListView):
#     model = Post
#     template_name = 'forum/post_list.html'
#     paginate_by = 10
#     queryset = sorted(Post.objects.all(), key=lambda post: (post.num_likes(), post.pk), reverse=True)[:20]
#
#     context_object_name = 'post_list'
#
#     def get_context_data(self, **kwargs):
#         context = super(LikesPostList, self).get_context_data()
#         context['categories'] = Category.objects.all().order_by("priority")
#         context['category'] = "특급"
#
#         return context
#
#
# class PopularPostList(ListView):
#     model = Post
#     template_name = 'forum/post_list.html'
#     paginate_by = 10
#     context_object_name = 'post_list'
#     queryset = Post.objects.order_by("-hit_count_generic__hits", '-pk')[:20]
#
#     def get_context_data(self, *, object_list=None, **kwargs):
#         context = super(PopularPostList, self).get_context_data()
#         context['post_list'] = context['post_list'][:15]
#         context['categories'] = Category.objects.all().order_by("priority")
#         context['category'] = "인기"
#
#         return context
#
#


class VideoList(ListView):
    model = Video
    template_name = 'video_forum/index.html'
    context_object_name = 'video_list'
    paginate_by = 5
    ordering = '-pk'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(VideoList, self).get_context_data()
        context['video_comment_form'] = VideoCommentForm
        return context


class VideoDetail(HitCountDetailView):
    model = Video
    template_name = 'video_forum/detail.html'
    count_hit = True

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(VideoDetail, self).get_context_data()
        context['video_comment_form'] = VideoCommentForm

        return context


class CreateVideo(LoginRequiredMixin, CreateView):
    model = Video
    form_class = VideoForm
    template_name = 'video_forum/create_video.html'

    def form_valid(self, form):
        current_user = self.request.user
        if current_user.is_authenticated:
            form.instance.author = current_user
            response = super(CreateVideo, self).form_valid(form)

            tags_str = self.request.POST.get('tags_str')

            if tags_str:
                tags_str = tags_str.strip(' #')
                tags_str = tags_str.replace(',', '#')
                tags_list = tags_str.split('#')

                for tag in tags_list:
                    tag = tag.strip()
                    tag, is_tag_created = VideoTag.objects.get_or_create(name=tag)
                    if is_tag_created:
                        tag.slug = slugify(tag, allow_unicode=True)
                        tag.save()
                    self.object.tags.add(tag)

            return response
        else:
            return redirect(reverse_lazy('video_forum:index'))


class DeleteVideo(LoginRequiredMixin, DeleteView):
    model = Video
    template_name = 'video_forum/delete_video.html'

    def dispatch(self, request, *args, **kwargs):
        video = Video.objects.get(pk=self.kwargs['pk'])
        if video.author == self.request.user:
            return super(DeleteVideo, self).dispatch(request, *args, **kwargs)
        else:
            raise PermissionDenied

    def get_context_data(self, **kwargs):
        context = super(DeleteVideo, self).get_context_data(**kwargs)
        video = Video.objects.get(pk=self.kwargs['pk'])
        context['video'] = video
        return context

    def get_success_url(self):
        return reverse_lazy('video_forum:index')


class UpdateVideo(LoginRequiredMixin, UpdateView):
    model = Video
    form_class = VideoForm
    template_name = 'video_forum/update_video.html'

    def dispatch(self, request, *args, **kwargs):
        current_video = Video.objects.get(pk=self.kwargs['pk'])

        if current_video.author == self.request.user:
            return super(UpdateVideo, self).dispatch(request, *args, **kwargs)
        else:
            raise PermissionDenied

    def get_context_data(self, **kwargs):
        context = super(UpdateVideo, self).get_context_data()
        if self.object.tags.exists():
            tags_str_list = []
            for tag in self.object.tags.all():
                tags_str_list.append(tag.name)
            context['tags_str_default'] = '#' + '#'.join(tags_str_list)

        return context

    def form_valid(self, form):
        response = super(UpdateVideo, self).form_valid(form)
        self.object.tags.clear()

        tags_str = self.request.POST.get('tags_str')

        if tags_str:
            tags_str = tags_str.strip(' #')
            tags_str = tags_str.replace(',', '#')
            tags_list = tags_str.split('#')

            for tag in tags_list:
                tag = tag.strip(' #')
                tag, is_tag_created = VideoTag.objects.get_or_create(name=tag)
                if is_tag_created:
                    tag.slug = slugify(tag, allow_unicode=True)
                    tag.save()
                self.object.tags.add(tag)

        return response


@require_POST
@login_required
def like_video_comment(request, video_pk, pk):
    video_comment = get_object_or_404(VideoComment, pk=pk)
    if video_comment.likes.filter(pk=request.user.pk).exists():
        video_comment.likes.remove(request.user)
    else:
        video_comment.likes.add(request.user)

    return HttpResponseRedirect(reverse('video_forum:detail', args=(video_pk,)))


@require_POST
@login_required
def like_video(request, pk):
    video = get_object_or_404(Video, pk=pk)
    if video.likes.filter(pk=request.user.pk).exists():
        video.likes.remove(request.user)
    else:
        video.likes.add(request.user)

    return HttpResponseRedirect(reverse('video_forum:detail', args=(pk,)))


class UpdateVideoComment(LoginRequiredMixin, UpdateView):
    model = VideoComment
    form_class = VideoCommentForm
    template_name = 'video_forum/update_video_comment.html'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated and request.user == self.get_object().author:
            return super(UpdateVideoComment, self).dispatch(request, *args, **kwargs)
        else:
            raise PermissionDenied


def delete_video_comment(request, pk):
    video_comment = get_object_or_404(VideoComment, pk=pk)
    video = video_comment.video
    if request.user.is_authenticated and request.user == video.author:
        video_comment.delete()
        return redirect(video.get_absolute_url())
    else:
        raise PermissionDenied


def create_video_comment(request, pk):
    if request.user.is_authenticated:
        video = get_object_or_404(Video, pk=pk)

        if request.method == 'POST':
            video_comment_form = VideoCommentForm(request.POST)

            if video_comment_form.is_valid():
                video_comment = video_comment_form.save(commit=False)
                video_comment.video = video
                video_comment.author = request.user
                video_comment.save()

                return redirect(video_comment.get_absolute_url())
        else:
            return redirect(video.get_absolute_url())
    else:
        raise PermissionDenied