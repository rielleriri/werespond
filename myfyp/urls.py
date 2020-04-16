"""myfyp URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
# from django.conf.urls import url
# from django.contrib import admin

# urlpatterns = [
#     url(r'^admin/', admin.site.urls),
#     url(r'^api-auth/', include('rest_framework.urls'))
# ]

# # Use include() to add paths from the werespond application 
# from django.conf.urls import url, include
# from django.urls import path

# urlpatterns += [
#     path('werespond/', include('werespond.urls')),
# ]

# #Add URL maps to redirect the base URL to our application
# from django.views.generic import RedirectView
# urlpatterns += [
#     path('', RedirectView.as_view(url='werespond/', permanent=True)),
# ]
# # first parameter of path is empty to indicate '/' 

# # Use static() to add url mapping to serve static files during development (only)
# from django.conf import settings
# from django.conf.urls.static import static

# urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

from django.conf.urls import url, include
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from rest_framework.routers import DefaultRouter
from werespond import views

router = DefaultRouter()
router.register(r'user', views.UserViewSet)
router.register(r'post_list', views.PostListViewSet)
router.register(r'comment', views.CommentViewSet)
router.register(r'post', views.PostViewSet)
router.register(r'save', views.SaveViewSet)
router.register(r'vote', views.VoteViewSet)
router.register(r'group', views.GroupViewSet)
router.register(r'case', views.CaseViewSet)
router.register(r'achievement', views.AchievementViewSet)
router.register(r'user_achievement', views.UserAchievementViewSet)
router.register(r'achievement_reward', views.AchievementRewardViewSet)
router.register(r'report', views.ReportViewSet)
router.register(r'user_certificate', views.UserCertificateViewSet)
router.register(r'certificate', views.CertificateFormViewSet)
router.register(r'event', views.EventViewSet)
router.register(r'eventattendance', views.EventAttendanceViewSet)

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^api/', include(router.urls)),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)