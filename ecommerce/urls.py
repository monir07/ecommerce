from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from account.views import (SignUpCreateView, UserLoginView, UserLogoutView, UserPasswordChangeView)
from eshop.views import HomeView

urlpatterns = [
    path('admin/', admin.site.urls),

    path('signup/', SignUpCreateView.as_view(), name='user_signup'),
    path('login/', UserLoginView.as_view(), name='user_login'),
    path('logout/', UserLogoutView.as_view(), name='user_logout'),
    path('password-change/', UserPasswordChangeView.as_view(), name='user_password_change'),

    # eshop urls
    path('', HomeView.as_view()),
    path('shop/', include('eshop.urls'))
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# ADMIN PANEL HEADER AND TITLE TEXT CHANGE.
admin.site.site_header = "E-Shop Admin"
admin.site.site_title = "E-Shop Admin Portal"
admin.site.index_title = "Welcome to E-Shop Portal"

# Custom erorrs Page
handler404 = 'account.views.custom_page_not_found'
handler500 = 'account.views.custom_server_error'
handler403 = 'account.views.custom_permission_denied_view'
handler400 = 'account.views.custom_bad_request_view'