from django.core.paginator import Paginator

POSTS_COUNT = 10


def get_paginator(queryset, request):
    paginator = Paginator(queryset, POSTS_COUNT)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return page_obj, paginator.count