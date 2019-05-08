from django.urls import path

from simplechoice.views import GameIndex, GameNew, GameContinue, GameDelete, GameList, GameDebug

app_name = 'simplechoice'

urlpatterns = [
    path('', GameIndex.as_view(), name='index'),
    path('new/', GameNew.as_view(), name='new'),
    path('continue/', GameContinue.as_view(), name='continue'),
    path('delete/', GameDelete.as_view(), name='delete'),
    path('list/', GameList.as_view(), name='list'),
    path('debug/', GameDebug.as_view(), name='debug'),
]
