# ruff: noqa
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include
from django.urls import path
from django.views import defaults as default_views
from django.views.generic import TemplateView
from rest_framework import routers as rest_routers

from django_backend.users import views as user_views
from django_backend.quiz import views as quiz_views

rest_routers = rest_routers.DefaultRouter()
rest_routers.register(r'users', user_views.UserViewSet)
rest_routers.register(r'groups', user_views.GroupViewSet)
rest_routers.register(r'questions', quiz_views.QuestionViewSet, basename='question')
rest_routers.register(r'quiz', quiz_views.QuizViewSet, basename='quiz')
rest_routers.register(r'quizsession', quiz_views.QuizSessionViewSet, basename='quizsession')

urlpatterns = [
    path("", TemplateView.as_view(template_name="pages/home.html"), name="home"),
    path(
        "about/",
        TemplateView.as_view(template_name="pages/about.html"),
        name="about",
    ),
    path("quiz", TemplateView.as_view(template_name="pages/quiz.html"), name="quiz"),
    # Django Admin, use {% url 'admin:index' %}
    path(settings.ADMIN_URL, admin.site.urls),
    # User management
    path("users/", include("django_backend.users.urls", namespace="users")),
    path("accounts/", include("allauth.urls")),
    # Your stuff: custom urls includes go here
    # ...
    # Media files
    *static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT),
    path('api-auth/', include('rest_framework.urls')),
    path('api/', include(rest_routers.urls)),
]


if settings.DEBUG:
    # This allows the error pages to be debugged during development, just visit
    # these url in browser to see how these error pages look like.
    urlpatterns += [
        path(
            "400/",
            default_views.bad_request,
            kwargs={"exception": Exception("Bad Request!")},
        ),
        path(
            "403/",
            default_views.permission_denied,
            kwargs={"exception": Exception("Permission Denied")},
        ),
        path(
            "404/",
            default_views.page_not_found,
            kwargs={"exception": Exception("Page not Found")},
        ),
        path("500/", default_views.server_error),
    ]
    if "debug_toolbar" in settings.INSTALLED_APPS:
        import debug_toolbar

        urlpatterns = [path("__debug__/", include(debug_toolbar.urls))] + urlpatterns
