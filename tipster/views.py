from django.shortcuts import render_to_response

def index(request):
    posts = [
        {
            'title': 'Sandstorm An open source operating system for personal' +
                     ' and private clouds',
            'url': '',
            'domain': 'sandstorm.io',
            'curator': 'dack',
            'score': 172,
            'creation_date': '5 hours',
            'num_comments': 67,
        },
        {
            'title': 'HyperTerm - JS/HTML/CSS Terminal',
            'url': '',
            'domain': 'hyperterm.org',
            'curator': 'pandemicsyn',
            'score': 463,
            'creation_date': '12 hours',
            'num_comments': 193,
        },
        {
            'title': 'Mr Robot S02E01 easter egg',
            'url': '',
            'domain': '0x41.no',
            'score': 490,
            'curator': 'tilt',
            'creation_date': '14 hours',
            'num_comments': 160,
        }
    ]
    return render_to_response(
        template_name='index.html',
        context = { 'posts': posts })
