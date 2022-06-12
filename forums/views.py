from django.http import HttpResponse
from django.shortcuts import redirect, render, get_object_or_404
from forums.models import (ForumTopic, Post)
from django.core.paginator import Paginator
import datetime
from polls.views import (get_polls_panel_context, get_forum_panel_context)
from django.contrib.auth.decorators import login_required
from polls.views import renderError

@login_required
def forums_all(request):
    forums_raw = ForumTopic.objects.all().order_by('-added')
    paginator_forums = Paginator(forums_raw, 10)
    page_no = request.GET.get('page')
    forums = paginator_forums.get_page(page_no)
    forums_all_context = dict()
    forums_all_context['forum_panel'] = get_forum_panel_context(request)
    forums_all_context['recentpolls'] = get_polls_panel_context(request)
    forums_all_context['username'] = request.user.username
    forum_topics = []
    for forum in forums:
        unit_context = dict()
        unit_context['forum_id'] = forum.id
        unit_context['title'] = forum.title
        allPosts = forum.forumpost.all().order_by('added')
        firstPost = allPosts[0]
        lastPost = forum.forumpost.latest('added')
        unit_context['views'] = forum.views
        unit_context['first_post_text'] = firstPost.post_text
        unit_context['num_replies'] = allPosts.count() - 1
        unit_context['last_post_time'] = forum.added
        forum_topics.append(unit_context)
    forums_all_context['forums'] = forum_topics
    paginator_context = dict()
    paginator_context['has_more_pages'] = forums.has_previous() or forums.has_next()
    paginator_context['has_next'] = forums.has_next()
    paginator_context['has_previous'] = forums.has_previous()
    paginator_context['current_page'] = forums.number
    paginator_context['total_pages'] = forums.paginator.num_pages
    paginator_context['prev_page_num'] = forums.previous_page_number
    paginator_context['next_page_num'] = forums.next_page_number
    forums_all_context['paginator'] = paginator_context

    return render(request, 'forums/forums_all.html', context=forums_all_context)


@login_required
def forumdetail(request, pk):
    try:
        forum = ForumTopic.objects.get(pk=pk)
    except ForumTopic.DoesNotExist:
        return renderError(request, '(404) Forum Not Found')
    if not forum.active:
        return renderError(request, '(403) Forum Restricted')
    forumViews = forum.views + 1
    ForumTopic.objects.filter(pk=pk).update(views=forumViews)
    forum_detail_context = dict()
    forum_detail_context['forum_panel'] = get_forum_panel_context(request)
    forum_detail_context['recentpolls'] = get_polls_panel_context(request)
    forum_detail_context['username'] = request.user.username
    forum_detail_context['forum_id'] = forum.id
    forum_detail_context['edit_permit'] = (forum.author == request.user ) or request.user.is_staff
    forum_detail_context['topic_title'] = forum.title
    forum_detail_context['lock_status'] = forum.locked
    forumPosts_raw = forum.forumpost.all()
    forum_paginator = Paginator(forumPosts_raw, 5)
    page_no = request.GET.get('page')
    forumPosts = forum_paginator.get_page(page_no)
    posts_context = []
    for post in forumPosts:
        unit_context = dict()
        unit_context['author'] = post.post_author
        unit_context['added'] = post.added
        unit_context['text'] = post.post_text
        added = post.added.strftime("%H:%M:%S, %d %m, %Y")
        updated = post.updated.strftime("%H:%M:%S, %d %m, %Y")
        added_t = datetime.datetime.strptime(added,"%H:%M:%S, %d %m, %Y").time()
        updated_t = datetime.datetime.strptime(updated,"%H:%M:%S, %d %m, %Y").time()
        if added_t != updated_t:
            unit_context['updated'] = post.updated
        if post.post_author == request.user:
            unit_context['own_post'] = True
            unit_context['post_id'] = post.id
        posts_context.append(unit_context)
    forum_detail_context['posts'] = posts_context
    paginator_context = dict()
    paginator_context['has_more_pages'] = forumPosts.has_previous() or forumPosts.has_next()
    paginator_context['has_next'] = forumPosts.has_next()
    paginator_context['has_previous'] = forumPosts.has_previous()
    paginator_context['current_page'] = forumPosts.number
    paginator_context['total_pages'] = forumPosts.paginator.num_pages
    paginator_context['prev_page_num'] = forumPosts.previous_page_number
    paginator_context['next_page_num'] = forumPosts.next_page_number
    forum_detail_context['paginator'] = paginator_context
    return render(request, 'forums/forum_detail.html', context=forum_detail_context)


@login_required
def reply_to_forum(request, pk):
    if request.method == 'GET':
        return redirect('forums:forum_detail', pk=pk)
    else:
        reply_text = request.POST.get('reply-text', False)
        if not reply_text:
            polls_panel_context = get_polls_panel_context(request)
            forums_panel_context = get_forum_panel_context(request)
            username = request.user.username
            context = {'username':username,'recentpolls': polls_panel_context, 'forums': forums_panel_context, 'error':'Cannot Post Empty Reply'}
            return render(request, 'polls/error.html', context=context)
        forum_topic = get_object_or_404(ForumTopic, pk=pk)
        if forum_topic.locked == True or forum_topic.active != True:
            polls_panel_context = get_polls_panel_context(request)
            forums_panel_context = get_forum_panel_context(request)
            username = request.user.username
            context = {'username':username, 'recentpolls': polls_panel_context, 'forums': forums_panel_context, 'error':'Topic Is Locked/Inactive'}
            return render(request, 'polls/error.html', context=context)
            
        post = Post.objects.create(post_text=reply_text, forum=forum_topic, post_author=request.user)
        post.save()
        return redirect('forums:forum_detail', pk=pk)


@login_required
def forum_create(request):
    if request.method == "GET":
        polls_panel = get_polls_panel_context(request)
        forums_panel = get_forum_panel_context(request)
        username = request.user.username
        return render(request, 'forums/forum_create.html', context={'username':username,'recentpolls':polls_panel, 'forums':forums_panel})
    else:
        forum_kwargs = dict()
        forum_kwargs['title'] = request.POST.get('topic')
        forum_kwargs['author'] = request.user
        new_forum = ForumTopic.objects.create(**forum_kwargs)
        new_forum.save()
        post_kwargs = dict()
        post_kwargs['post_text'] = request.POST.get('post-text')
        post_kwargs['forum'] = new_forum
        post_kwargs['post_author'] = request.user
        new_post = Post.objects.create(**post_kwargs)
        new_post.save()
        return redirect('forums:forum_detail', pk=new_forum.id)


@login_required
def edit_forum(request, pk):
    if request.method == 'GET':
        try:
            forum = ForumTopic.objects.get(pk=pk)
        except ForumTopic.DoesNotExist:
            return renderError(request, "(404) Forum Not Found")
        edit_permit = (request.user == forum.author) or request.user.is_staff
        if not edit_permit:
            return renderError(request, "(403) Access Denied")
        if not forum.active:
            return renderError(request, "Restricted Forum")
        edit_forum_context = dict()
        edit_forum_context['recentpolls'] = get_polls_panel_context(request)
        edit_forum_context['forum_panel'] = get_forum_panel_context(request)
        edit_forum_context['forum_id'] = forum.id
        edit_forum_context['forum_title'] = forum.title
        firstPost = forum.forumpost.all().order_by('added')[0]
        edit_forum_context['post_text'] = firstPost.post_text
        return render(request, 'forums/forum_edit.html', context=edit_forum_context)
    else:
        try:
            forum = ForumTopic.objects.get(pk=pk)
        except ForumTopic.DoesNotExist:
            return renderError(request, "(404) Forum Not Found")
        title = request.POST.get('topic')
        post_text = request.POST.get('post-text')
        if not bool(title) or not bool(post_text):
            return renderError(request, "Empty Input Field")
        forum.title = title
        firstPost = forum.forumpost.all().order_by('added')[0]
        firstPost.post_text = post_text
        forum.save()
        firstPost.save()
        return redirect('forums:forum_detail', pk=pk)
        
    

@login_required
def edit_post(request):
    if request.method == 'GET':
        return redirect('forums:forum_all')
    else:
        post_pk = request.POST.get('post_id')
        if not bool(post_pk):
            return redirect('forums:forum_all')
        try:
            post = Post.objects.get(pk=post_pk)
        except Post.DoesNotExist:
            return renderError(request, 'Post Not Found')  
        if post.post_author != request.user:
            return renderError(request, 'Unauthorized')
        edit_post_context = {}
        edit_post_context['username'] = request.user.username
        edit_post_context['recentpolls'] = get_polls_panel_context(request)
        edit_post_context['forum_panel'] = get_forum_panel_context(request)
        edit_post_context['forum_id'] = post.forum.id
        edit_post_context['forum_title'] = post.forum.title
        edit_post_context['post_id'] = post.id
        edit_post_context['prev_post_text'] = post.post_text
        return render(request, 'forums/forum_post_edit.html', context=edit_post_context)


@login_required
def update_post(request):
    if request.method == 'GET':
        return redirect('forums:forum_all')
    else:
        post_pk = request.POST.get('pk')
        try:
            post = Post.objects.get(pk=post_pk)
        except Post.DoesNotExist:
            return renderError(request, "Invalid Request")
        if post.post_author != request.user:
            return renderError(request, "Unauthorized")
        new_post_text = request.POST.get('post-text')
        if not bool(new_post_text):
            return renderError(request, "No Input Text")
        post.post_text = new_post_text
        post.save()
        forum_pk = request.POST.get('forum_pk')
        return redirect('forums:forum_detail', pk=forum_pk)


@login_required
def delete_post(request, pk):
    try:
        post = Post.objects.get(pk=pk)
    except Post.DoesNotExist:
        return renderError(request, 'Post Not Found')
    if post.post_author != request.user:
        return renderError(request, 'Unauthorized')
    forum = post.forum
    posts = forum.forumpost.all().order_by('added')
    if len(posts) == 1 and post.post_author == forum.author:
        forum.delete()
    first_post = posts[0]
    is_the_first_post = first_post == post
    is_first_post_author_forum_author = first_post.post_author == forum.author
    if len(posts) > 1 and is_first_post_author_forum_author and is_the_first_post:
        return renderError(request, 'Not Permitted')
    post.delete()
    return redirect('forums:forum_all')
