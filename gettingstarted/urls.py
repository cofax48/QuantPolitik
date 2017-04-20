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
    url(r'^AreasofAnalysis', hello.views.areaOfAnalysis, name='areaOfAnalysis'),
    #Areas of Analysis
    url(r'^BureaucraticExchange', hello.views.BureaucraticExchange, name='BureaucraticExchange'),
    url(r'^BusinessRelations', hello.views.BusinessRelations, name='BusinessRelations'),
    url(r'^CountryProfile', hello.views.CountryProfile, name='CountryProfile'),
    url(r'^CulturalDiffusion', hello.views.CulturalDiffusion, name='CulturalDiffusion'),
    url(r'^GovernmentalPerspective', hello.views.GovernmentalPerspective, name='GovernmentalPerspective'),
    url(r'^Prestige', hello.views.Prestige, name='Prestige'),
    url(r'^Security', hello.views.Security, name='Security'),
    url(r'^TradeRelations', hello.views.TradeRelations, name='TradeRelations'),
    #Apis
    url(r'^api/ByCountry/\w{2,40}', hello.views.get_Country_headline_data, name='Country_headline_data'),
    url(r'^api/\w{2,20}/\w{2,20}', hello.views.get_Table_and_Column, name='column_api'),
    url(r'^api/\w{2,20}', hello.views.get_Table, name='table_api'),
]
