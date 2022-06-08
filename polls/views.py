from django.shortcuts import render
from django.core.paginator import Paginator
from polls.models import (Poll, Choice, Vote)
from forums.models import (ForumTopic, Post)

def homepageview(request):
    return render(request, 'polls/home.html')


def pollshomepage(request):
    recentpolls = Poll.objects.filter(public=True, active=True).order_by('-added')[:3]
    recentpolls_context = []
    for poll in recentpolls:
        poll_id = poll.id
        poll_title = poll.title
        try:
            vote_count = poll.pollvote.count()
            lastVote = poll.pollvote.latest('vote_time')
        except Vote.DoesNotExist:
            unit_context = {'poll_id': poll_id, 'poll_title': poll_title, 'vote_count': 0}
            recentpolls_context.append(unit_context)
            continue
        last_vote_time = lastVote.vote_time
        last_vote_voter = lastVote.voter
        unit_context = {'poll_id': poll_id, 'poll_title': poll_title, 'vote_count': vote_count,
                        'last_vote_time': last_vote_time, 'last_vote_voter': last_vote_voter}
        recentpolls_context.append(unit_context)
    # forums panel context
    recentforums = ForumTopic.objects.filter(active=True).order_by('-added')[:5]
    recentforums_context = []
    for forum in recentforums:
        forum_id = forum.id
        forum_title = forum.title
        lastPost = forum.forumpost.latest('added')
        last_post_time = lastPost.added
        last_post_user = lastPost.post_author
        unit_context = {'forum_id': forum_id, 'forum_title': forum_title, 'last_post_time': last_post_time, 'last_post_user': last_post_user}
        recentforums_context.append(unit_context)
    #user's polls
    recentpolls_user = Poll.objects.filter(author=request.user).order_by('-added')
    recentpolls_user_context = []
    paginator_context = dict()
    if recentpolls_user.count() > 0:
        paginator = Paginator(recentpolls_user, 5)
        page_no = request.GET.get('page')
        pollspage = paginator.get_page(page_no)
        for poll in pollspage:
            poll_id = poll.id
            poll_title = poll.title
            poll_views = poll.views
            active_status = poll.active
            try:
                vote_count = poll.pollvote.count()
                lastVote = poll.pollvote.latest('vote_time')
            except Vote.DoesNotExist:
                unit_context = {'poll_id': poll_id, 'poll_views': poll_views, 'active_status': active_status, 
                                'poll_title': poll_title, 'vote_count': 0}
                recentpolls_user_context.append(unit_context)
                continue
            last_vote_time = lastVote.vote_time
            unit_context = {'poll_id': poll_id, 'poll_title': poll_title, 'vote_count': vote_count, 'poll_views': poll_views,
                            'active_status': active_status, 'last_vote_time': last_vote_time}
            recentpolls_user_context.append(unit_context)
        current_page = pollspage.number
        total_page = pollspage.paginator.num_pages
        has_more_page = pollspage.has_previous() or pollspage.has_next()
        has_prev = pollspage.has_previous()
        has_next = pollspage.has_next()
        next_page_num = current_page + 1
        prev_page_num = current_page - 1
        paginator_context = {'current_page': current_page, 'total_page': total_page, 'has_more_page': has_more_page,
                                    'has_prev': has_prev, 'has_next': has_next, 'next_page_num': next_page_num, 'prev_page_num': prev_page_num} 

    
    return render(request, 'polls/index.html', context={'recentpolls': recentpolls_context, 'forums': recentforums_context, 
                                                        'recentpolls_user': recentpolls_user_context,
                                                        'paginator': paginator_context})
    