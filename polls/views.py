from django.shortcuts import render, redirect
from django.core.paginator import Paginator
from polls.models import (Poll, Choice, Vote)
from forums.models import (ForumTopic, Post)
from django.http import HttpResponse
from django.urls import reverse

def homepageview(request):
    if request.user.is_authenticated:
        return redirect('polls:index')
    return render(request, 'polls/home.html')


def get_forum_panel_context(request):
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
    return recentforums_context


def get_polls_panel_context(request):
    recentpolls = Poll.objects.filter(public=True, active=True, visible=True).order_by('-added')[:5]
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
    return recentpolls_context


def pollshomepage(request):
    username = request.user.username
    recentpolls_context = get_polls_panel_context(request)
    # forums panel context
    recentforums_context = get_forum_panel_context(request)
    #user's polls
    recentpolls_user = Poll.objects.filter(author=request.user, visible=True).order_by('-added')
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

    #user stats panel
    stat_context = dict()
    try:
        userCreatedPolls = Poll.objects.filter(author=request.user)
        user_vote_gain = 0
        for userpoll in userCreatedPolls:
            pollVotes = userpoll.pollvote.count()
            user_vote_gain += pollVotes
        stat_context['user_vote_gain'] = user_vote_gain
    except:
        pass
    try:
        stat_context['user_created_active_polls'] = Poll.objects.filter(author=request.user, active=True).count()
        stat_context['user_created_poll_nums'] = userCreatedPolls.count()
    except:
        pass
    try:
        recentPoll = Poll.objects.filter(author=request.user).order_by('-added')[0]
        stat_context['recent_poll_id'] = recentPoll.id
        stat_context['recent_poll_title'] = recentPoll.title
    except:
        pass  
    try:
        userVotes = Vote.objects.filter(voter=request.user).order_by('-vote_time')
        stat_context['users_vote_count'] = userVotes.count()
        userLastVote = userVotes[0]
        stat_context['user_last_vote_time'] = userLastVote.vote_time
        stat_context['user_last_vote_poll_id'] = userLastVote.poll.id
        stat_context['user_last_vote_poll_title'] = userLastVote.poll.title
    except:
        pass

    return render(request, 'polls/index.html', context={'recentpolls': recentpolls_context, 'forums': recentforums_context, 
                                                        'recentpolls_user': recentpolls_user_context, 'username':username,
                                                        'paginator': paginator_context, 'stat': stat_context})


def polldetail(request, pk):
    polldetail_context = dict()
    try:
        poll = Poll.objects.get(pk=pk)
    except Poll.DoesNotExist:
        context = {}
        context['recentpolls'] = get_polls_panel_context(request)
        context['forums'] = get_forum_panel_context(request)
        context['error'] = 'Poll Not Found'
        return render(request, 'polls/error.html', context=context)
    if not poll.visible:
        context = {}
        context['recentpolls'] = get_polls_panel_context(request)
        context['forums'] = get_forum_panel_context(request)
        context['error'] = 'Only Admins Can Access'
        return render(request, 'polls/error.html', context=context)

    polldetail_context['recentpolls'] = get_polls_panel_context(request)
    polldetail_context['forums'] = get_forum_panel_context(request)
    pollViews = poll.views + 1
    Poll.objects.filter(pk=pk).update(views=pollViews)
    polldetail_context['poll_id'] = poll.id
    polldetail_context['poll_url'] = request.build_absolute_uri()
    polldetail_context['poll_title'] = poll.title
    polldetail_context['poll_author'] = poll.author
    polldetail_context['poll_added'] = poll.added
    polldetail_context['poll_views'] = pollViews
    polldetail_context['is_active_poll'] = poll.active
    if poll.active:
        polldetail_context['active_status'] = 'active'
    else:
        polldetail_context['active_status'] = 'inactive'
    
    try:
        myVote = poll.pollvote.get(voter=request.user)
        polldetail_context['my_vote_time'] = myVote.vote_time
    except Exception:
        pass
    try:
        lastVote = poll.pollvote.latest('vote_time')
        polldetail_context['last_vote_time'] = lastVote.vote_time
        polldetail_context['last_vote_voter'] = lastVote.voter
    except Exception:
        pass
    polldetail_context['poll_banner_url'] = poll.banner.url
    poll_choices = poll.choice.all()
    total_votes = poll.pollvote.count()
    choices_context = []
    for choice in poll_choices:
        choice_text = choice.choicetext
        choice_votes = choice.choicevote.count()
        try:
            percentVotes = (choice_votes/total_votes)*100
        except ZeroDivisionError:
            percentVotes = 0
        choice_votes_percent = round(percentVotes, 2)
        progressbar_progress = round(percentVotes)
        unit_context = {'choice_text':choice_text, 'choice_votes':choice_votes, 'choice_votes_percent':choice_votes_percent,
                        'progressbar_progress':progressbar_progress}
        choices_context.append(unit_context)
    polldetail_context['choices'] = choices_context
    polldetail_context['total_votes'] = total_votes
    return render(request, 'polls/poll_detail.html', context=polldetail_context)


def polls_all(request):
    polls_all_raw = Poll.objects.filter(public=True, active=True, visible=True).order_by('-added')
    polls_paginator = Paginator(polls_all_raw, 5)
    page_no = request.GET.get('page')
    page_polls = polls_paginator.get_page(page_no)
    browse_poll_context = dict()
    polls_context = []
    for poll in page_polls:
        unit_context = dict()
        unit_context['poll_id'] = poll.id
        unit_context['poll_title'] = poll.title
        unit_context['added'] = poll.added
        unit_context['author'] = poll.author
        unit_context['title'] = poll.pollvote.count()
        users_vote = poll.pollvote.filter(voter=request.user)
        if len(users_vote) > 0:
            unit_context['voted'] = True
        polls_context.append(unit_context)
    
    paginator_context = dict()
    paginator_context['has_more_pages'] = page_polls.has_previous() or page_polls.has_next()
    paginator_context['has_next'] = page_polls.has_next()
    paginator_context['has_previous'] = page_polls.has_previous()
    paginator_context['current_page'] = page_polls.number
    paginator_context['total_pages'] = page_polls.paginator.num_pages
    paginator_context['prev_page_num'] = page_polls.previous_page_number
    paginator_context['next_page_num'] = page_polls.next_page_number
    browse_poll_context['paginator'] = paginator_context
    browse_poll_context['polls'] = polls_context
    return render(request, 'polls/polls_all.html', context=browse_poll_context)


def create_poll(request):
    polls_panel = get_polls_panel_context(request)
    forums_panel = get_forum_panel_context(request)
    if request.method == "GET":
        return render(request, 'polls/poll_create.html', context={'recentpolls':polls_panel, 'forums':forums_panel})
    else:
        poll_kwargs = dict()
        poll_kwargs['title'] = request.POST.get('poll-title')
        poll_kwargs['author'] = request.user
        visibility = request.POST.get('visibility')
        if bool(visibility):
            poll_kwargs['public'] = True
        else:
            poll_kwargs['public'] = False
        banner_img = request.FILES.get('poll-banner', False)
        if bool(banner_img):
            poll_kwargs['banner'] = banner_img
        new_poll = Poll.objects.create(**poll_kwargs)
        new_poll.save()
        choices_raw = list(request.POST)[3:]
        choices = []
        for choice in choices_raw:
            choice_text = request.POST.get(choice)
            choices.append(Choice(choicetext=choice_text, poll=new_poll))
        Choice.objects.bulk_create(choices)
        poll_link = request.build_absolute_uri(reverse('polls:polldetails', args=(new_poll.id,)))
        confirm_page_context = {'recentpolls':polls_panel, 'forums':forums_panel, 'poll_id':new_poll.id, 'poll_link':poll_link}
        return render(request, 'polls/poll_creation_info.html', context=confirm_page_context)
    