from django.conf.urls import include, url

from django.contrib import admin
admin.autodiscover()

import hello.views

# Examples:
# url(r'^$', 'gettingstarted.views.home', name='home'),
# url(r'^blog/', include('blog.urls')),

urlpatterns = [
    url(r'^$', hello.views.index, name='index'),
    url(r'^datadashboard', hello.views.dataDashBoard, name='dataDashBoard'),
    url(r'^originalHomePage', hello.views.originalHomePage, name='originalHomePage'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^about', hello.views.aboutPage, name='aboutPage'),
    #Areas of Analysis
    url(r'^BusinessRelations', hello.views.BusinessRelations, name='BusinessRelations'),
    url(r'^CountryProfile', hello.views.CountryProfile, name='CountryProfile'),
    url(r'^CulturalDiffusion', hello.views.CulturalDiffusion, name='CulturalDiffusion'),
    url(r'^GovernmentalPerspective', hello.views.GovernmentalPerspective, name='GovernmentalPerspective'),
    url(r'^PresidentialExchange', hello.views.PresidentialExchange, name='PresidentialExchange'),
    url(r'^Prestige', hello.views.Prestige, name='Prestige'),
    url(r'^SecretaryofStateExchange', hello.views.SecretaryofStateExchange, name='SecretaryofStateExchange'),
    url(r'^Security', hello.views.Security, name='Security'),
    url(r'^TradeRelations', hello.views.TradeRelations, name='TradeRelations'),
    url(r'^UnitedNations', hello.views.UnitedNations, name='UnitedNations'),
    #Apis
    url(r'^api/\w{2,20}/\w{2,20}', hello.views.get_Table_and_Column, name='column_api'),
    url(r'^api/\w{2,20}', hello.views.get_Table, name='table_api'),
]
