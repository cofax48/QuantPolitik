from django.conf.urls import include, url

from django.contrib import admin
admin.autodiscover()

import hello.views

# Examples:
# url(r'^$', 'gettingstarted.views.home', name='home'),
# url(r'^blog/', include('blog.urls')),

urlpatterns = [
    url(r'^$', hello.views.index, name='index'),
<<<<<<< HEAD
    url(r'^datadashboard', hello.views.dataDashBoard, name='dataDashBoard'),
    url(r'^originalHomePage', hello.views.originalHomePage, name='originalHomePage'),
    url(r'^admin/', include(admin.site.urls)),
    #Apis
    url(r'^api/\w{2,20}/\w{2,20}', hello.views.get_Table_and_Column, name='column_api'),
    url(r'^api/\w{2,20}', hello.views.get_Table, name='table_api'),
=======
    url(r'^db', hello.views.db, name='db'),
    url(r'^admin/', include(admin.site.urls)),
>>>>>>> 4ae7a8606aebddf0a2eee749df91e59c7b75f0d4
]
