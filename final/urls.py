from django.conf.urls import url
from django.contrib import admin
from django.urls import path
from django.views.generic import TemplateView
from data_working.views import *
from filter.views import *
from log.views import *
from export.views import *
from superadmin.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', TemplateView.as_view(template_name="log/login.html")),
    url(r'^postsign/', postsign),
    path('dashboard/', TemplateView.as_view(template_name="data_working/dashboard.html"), name="dashboard"),
    url('ajax_update/', ajax_update, name='ajax_update'),
    url('filter/', filter_btw_dates, name='filter'),
    path('export/', export_xls, name='export'),

]
