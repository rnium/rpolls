from django.shortcuts import render
from polls.models import (Poll, Choice, Vote)

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

    return render(request, 'polls/index.html', context={'recentpolls': recentpolls_context})
    