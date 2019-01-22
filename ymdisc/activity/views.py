from django.shortcuts import render, redirect
from django.views import View

import datetime

import utilities

from .models import Activity, Section, Item, Comment

class WelcomeView(View):
    template_name = 'activity/welcome.html'

    def get(self, request):
        activities = Activity.objects.filter(publish_date__lte=datetime.date.today(), archive=False)
        context = {'activities': activities, 'image': utilities.get_quote_image()}
        return render(request, self.template_name, context)


class SummaryView(View):
    template_name = 'activity/summary.html'

    def get(self, request, activity_index):
        activity = Activity.objects.get(index=activity_index)
        sections = Section.objects.filter(activity=activity, visible=True)
        context = {'activity': activity, 'sections': sections}
        return render(request, self.template_name, context)


class SectionView(View):
    template_name = 'activity/section.html'

    def get(self, request, activity_index, section_index):
        activity = Activity.objects.get(index=activity_index)
        section = Section.objects.get(activity=activity, index=section_index)
        items = Item.objects.filter(section=section)
        context = {'activity': activity, 'section': section, 'items': items, 'user': request.user}
        return render(request, self.template_name, context)


class ItemCreateView(View):
    template_name = 'activity/item_create.html'

    def get(self, request, activity_index, section_index):
        activity = Activity.objects.get(index=activity_index)
        section = Section.objects.get(activity=activity, index=section_index)
        items = Item.objects.filter(section=section)
        context = {'activity':activity, 'section':section, 'items': items}
        return render(request, self.template_name, context)

    def post(self, request, activity_index, section_index):
        activity = Activity.objects.get(index=activity_index)
        section = Section.objects.get(activity=activity, index=section_index)
        items = Item.objects.filter(section=section)
        index = len(items) + 1
        new_item = Item(index=index, section=section, text=request.POST['item_text'], author=request.user)
        new_item.save()
        return redirect('activity:section', activity_index, section_index)


class ItemEditView(View):
    template_name = 'activity/item_edit.html'

    def get(self, request, activity_index, item_pk):
        activity = Activity.objects.get(index=activity_index)
        item = Item.objects.get(pk=item_pk)
        comments = Comment.objects.filter(item=item)
        error_msg = ''
        if len(comments) > 0:
            error_msg = 'People have made comments on this item. You may want to be careful about editing it.'
        context = {'activity': activity, 'item': item, 'comments': comments, 'error': error_msg}
        return render(request, self.template_name, context)

    def post(self, request, activity_index, item_pk):
        activity = Activity.objects.get(index=activity_index)
        item = Item.objects.get(pk=item_pk)
        item.text = request.POST['item_text']
        item.save()
        return redirect('activity:section', activity_index, item.section.index)


class ItemDeleteView(View):
    template_name = 'activity/item_delete.html'

    def get(self, request, activity_index, item_pk):
        activity = Activity.objects.get(index=activity_index)
        item = Item.objects.get(pk=item_pk)
        comments = Comment.objects.filter(item=item)
        error_msg = ''
        if len(comments) > 0:
            error_msg = 'This item already includes comments. Be absolutely sure you want to delete it!'
        context = {'activity': activity, 'item': item, 'comments': comments, 'error': error_msg}
        return render(request, self.template_name, context)

    def post(self, request, activity_index, item_pk):
        activity = Activity.objects.get(index=activity_index)
        item = Item.objects.get(pk=item_pk)
        comments = Comment.objects.filter(item=item)
        if len(comments) > 0:
            for comment in comments:
                comment.delete()
        item_section_index = item.section.index     # better get it before deleting the item
        item.delete()
        return redirect('activity:section', activity.index, item_section_index)


class CommentCreateView(View):
    template_name = 'activity/comment_create.html'

    def get(self, request, activity_index, item_pk):
        activity = Activity.objects.get(index=activity_index)
        item = Item.objects.get(pk=item_pk)
        comments = Comment.objects.filter(item=item)
        context = {'activity': activity, 'item': item, 'comments': comments}
        return render(request, self.template_name, context)

    def post(self, request, activity_index, item_pk):
        item = Item.objects.get(pk=item_pk)
        new_comment = Comment(user=request.user, item=item, text=request.POST['comment_text'])
        new_comment.save()
        return redirect('activity:section', activity_index, item.section.index)


class CommentEditView(View):
    template_name = 'activity/comment_edit.html'

    def get(self, request, activity_index, comment_pk):
        activity = Activity.objects.get(index=activity_index)
        comment = Comment.objects.get(pk=comment_pk)
        item = comment.item
        context = {'activity': activity, 'edit_comment': comment, 'item': item}
        return render(request, self.template_name, context)

    def post(self, request, activity_index, comment_pk):
        comment = Comment.objects.get(pk=comment_pk)
        comment.text = request.POST['comment_text']
        comment.save()
        return redirect('activity:section', activity_index, comment.item.section.index)


class CommentDeleteView(View):
    template_name = 'activity/comment_delete.html'

    def get(self, request, activity_index, comment_pk):
        activity = Activity.objects.get(index=activity_index)
        comment = Comment.objects.get(pk=comment_pk)
        item = comment.item
        context = {'activity': activity, 'delete_comment': comment, 'item': item}
        return render(request, self.template_name, context)

    def post(self, request, activity_index, comment_pk):
        comment = Comment.objects.get(pk=comment_pk)
        item = comment.item     # get the item this comment belongs to before deleting the comment
        comment.delete()
        return redirect('activity:section', activity_index, item.section.index)


