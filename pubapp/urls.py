from django.urls import path

from pubapp import views

urlpatterns = [
    path('accounts/login', views.login_view),
    path('accounts/register', views.register_view),
    path('accounts/logout', views.logout_command),
    path('', views.index_view),
    # path('pub/lounge', admin.site.urls),
    path('pub/', views.pub_view),
    path('pub/admin/refresh', views.refresh_relationship_content_view),
    path('pub/characters/<int:character_id>', views.character_view),
    path('pub/characters', views.characters_list_view),
    path('pub/characters/suggest/', views.suggestion_list_view),

]
