from django.urls import path
from django.contrib.auth.decorators import login_required

from .views import (WelcomeView, SummaryView, SectionView, ItemCreateView, ItemEditView, ItemDeleteView,
                    CommentCreateView, CommentEditView, CommentDeleteView)

app_name = 'activity'

urlpatterns = [
    path('welcome/', login_required(WelcomeView.as_view()), name='welcome'),
    path('<int:activity_index>/', login_required(SummaryView.as_view()), name='summary'),
    path('<int:activity_index>/<int:section_index>/', login_required(SectionView.as_view()), name='section'),
    path('<int:activity_index>/<int:section_index>/create_item/',
         login_required(ItemCreateView.as_view()), name='item_create'),
    path('<int:activity_index>/<int:item_pk>/edit_item', login_required(ItemEditView.as_view()), name='item_edit'),
    path('<int:activity_index>/<int:item_pk>/delete_item',
         login_required(ItemDeleteView.as_view()), name='item_delete'),
    path('<int:activity_index>/<int:item_pk>/create_comment/',
         login_required(CommentCreateView.as_view()), name='comment_create'),
    path('<int:activity_index>/<int:comment_pk>/edit_comment/',
         login_required(CommentEditView.as_view()), name='comment_edit'),
    path('<int:activity_index>/<int:comment_pk>/delete_comment/',
         login_required(CommentDeleteView.as_view()), name='comment_delete')
]