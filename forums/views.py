from django.shortcuts import render, get_object_or_404
from forums.models import (ForumTopic, Post)
from django.http import HttpResponse

def forumdetail(request, pk):
    forum = get_object_or_404(ForumTopic, pk=pk, active=True)
    forum_detail_context = dict()
    forum_detail_context['topic_title'] = forum.title
    forum_detail_context['lock_status'] = forum.locked
    forumPosts = forum.forumpost.all()
    posts_context = []
    for post in forumPosts:
        unit_context = dict()
        unit_context['author'] = post.post_author
        unit_context['added'] = post.added
        unit_context['text'] = post.post_text
        if post.added != post.updated:
            unit_context['updated'] = post.updated
        if post.post_author == request.user:
            unit_context['own_post'] = True
        posts_context.append(unit_context)
    forum_detail_context['posts'] = posts_context

    return render(request, 'forums/forum_detail.html', context=forum_detail_context)