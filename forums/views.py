from django.shortcuts import redirect, render, get_object_or_404
from forums.models import (ForumTopic, Post)
from django.core.paginator import Paginator
import datetime
from polls.views import (get_polls_panel_context, get_forum_panel_context)


def forums_all(request):
    forums_raw = ForumTopic.objects.all().order_by('-added')
    paginator_forums = Paginator(forums_raw, 10)
    page_no = request.GET.get('page')
    forums = paginator_forums.get_page(page_no)
    forums_all_context = dict()
    forums_all_context['forum_panel'] = get_forum_panel_context(request)
    forums_all_context['recentpolls'] = get_polls_panel_context(request)
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
        unit_context['last_post_username'] = lastPost.post_author
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


def forumdetail(request, pk):
    forum = get_object_or_404(ForumTopic, pk=pk, active=True)
    forumViews = forum.views + 1
    ForumTopic.objects.filter(pk=pk).update(views=forumViews)
    forum_detail_context = dict()
    forum_detail_context['forum_panel'] = get_forum_panel_context(request)
    forum_detail_context['recentpolls'] = get_polls_panel_context(request)
    forum_detail_context['forum_id'] = forum.id
    forum_detail_context['topic_title'] = forum.title
    forum_detail_context['lock_status'] = forum.locked
    forumPosts = forum.forumpost.all()
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
        posts_context.append(unit_context)
    forum_detail_context['posts'] = posts_context

    return render(request, 'forums/forum_detail.html', context=forum_detail_context)


def reply_to_forum(request, pk):
    if request.method == 'GET':
        return redirect('forums:forum_detail', pk=pk)
    else:
        reply_text = request.POST.get('reply-text', False)
        if not reply_text:
            polls_panel_context = get_polls_panel_context(request)
            forums_panel_context = get_forum_panel_context(request)
            context = {'recentpolls': polls_panel_context, 'forums': forums_panel_context, 'error':'Cannot Post Empty Reply'}
            return render(request, 'polls/error.html', context=context)
        forum_topic = get_object_or_404(ForumTopic, pk=pk)
        if forum_topic.locked == True or forum_topic.active != True:
            polls_panel_context = get_polls_panel_context(request)
            forums_panel_context = get_forum_panel_context(request)
            context = {'recentpolls': polls_panel_context, 'forums': forums_panel_context, 'error':'Topic Is Locked/Inactive'}
            return render(request, 'polls/error.html', context=context)
            
        post = Post.objects.create(post_text=reply_text, forum=forum_topic, post_author=request.user)
        post.save()
        return redirect('forums:forum_detail', pk=pk)