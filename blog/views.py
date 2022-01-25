from django.db.models import Q
from django.shortcuts import render
from django.core.paginator import Paginator
from django.http import Http404
from django.utils import timezone

from .models import Content
from .models import Category
from .models import Tag


def index(request):
    now = timezone.now()
    if 'tag' in request.GET:
        tag_id = request.GET['tag']
        items = Content.objects \
            .filter(state=1) \
            .filter(Q(publish_up=None) | Q(publish_up__lte=now)) \
            .filter(Q(publish_down=None) | Q(publish_down__gte=now)) \
            .filter(tags__id=tag_id)
    else:
        items = Content.objects \
            .filter(state=1) \
            .filter(Q(publish_up=None) | Q(publish_up__lte=now)) \
            .filter(Q(publish_down=None) | Q(publish_down__gte=now))
    categories = Category.objects.all()
    for item in items:
        if item.publish_up is None:
            item.publish_up = item.created
        for category in categories:
            if category.id == item.category_id:
                item.category_name = category.name
                break
    items = sorted(items, key=lambda item_: item_.publish_up, reverse=True)
    paginator = Paginator(items, 3)
    if 'page' in request.GET:
        page_num = request.GET['page']
    else:
        page_num = 1
    page = paginator.get_page(page_num)
    if 'tag' in request.GET:
        tag = Tag.objects.get(id=tag_id)
        context = {'categories': categories, 'page': page, 'items': page.object_list, 'tag': tag}
        return render(request, 'blog/by_tag.html', context)
    else:
        context = {'categories': categories, 'page': page, 'items': page.object_list}
        return render(request, 'blog/index.html', context)


def by_category(request, category_id):
    now = timezone.now()
    items = Content.objects\
        .filter(state=1) \
        .filter(category_id=category_id) \
        .filter(Q(publish_up=None) | Q(publish_up__lte=now))\
        .filter(Q(publish_down=None) | Q(publish_down__gte=now))
    for item in items:
        if item.publish_up is None:
            item.publish_up = item.created
    items = sorted(items, key=lambda item_: item_.publish_up, reverse=True)
    categories = Category.objects.all()
    current_category = Category.objects.get(pk=category_id)
    paginator = Paginator(items, 3)
    if 'page' in request.GET:
        page_num = request.GET['page']
    else:
        page_num = 1
    page = paginator.get_page(page_num)
    context = {'categories': categories, 'current_category': current_category, 'page': page, 'items': page.object_list}
    return render(request, 'blog/by_category.html', context)


def detail(request, category_id, pk):
    now = timezone.now()
    try:
        post = Content.objects \
            .filter(pk=pk) \
            .filter(state=1) \
            .filter(category_id=category_id) \
            .filter(Q(publish_up=None) | Q(publish_up__lte=now))\
            .filter(Q(publish_down=None) | Q(publish_down__gte=now))[0]
        if post.publish_up is None:
            post.publish_up = post.created
        post.category_name = Category.objects.get(pk=category_id).name
        categories = Category.objects.all()
    except IndexError:
        raise Http404('Публикация не найдена.')
    context = {'post': post, 'categories': categories}
    return render(request, 'blog/detail.html', context)
