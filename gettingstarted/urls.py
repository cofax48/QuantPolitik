from django.conf.urls import include, url
from django.views.generic.base import RedirectView

from django.contrib import admin
admin.autodiscover()

favicon_view = RedirectView.as_view(url='../favicon.ico', permanent=True)

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
    url(r'^TheTech', hello.views.theTech, name='TheTech'),
    url(r'^TheAlgorithm', hello.views.theAlgorithm, name='TheAlgorithm'),
    #Testing with angular
    url(r'^7minWorkout', hello.views.SevenminWorkout, name='SevenminWorkout'),
    url(r'^AngularTesting', hello.views.AngularTesting, name='AngularTesting'),
    url(r'^DataByCountryAngularApp', hello.views.DataByCountryAngularApp, name='DataByCountryAngularApp'),
    #################
    url(r'^DrSchenkein', hello.views.drSchenkein, name='drSchenkein'),
    url(r'^JSResume', hello.views.JSResume, name='JSResume'),
    #Areas of Analysis
    url(r'^BureaucraticExchange', hello.views.BureaucraticExchange, name='BureaucraticExchange'),
    url(r'^BusinessRelations', hello.views.BusinessRelations, name='BusinessRelations'),
    url(r'^CountryProfile', hello.views.CountryProfile, name='CountryProfile'),
    url(r'^CulturalDiffusion', hello.views.CulturalDiffusion, name='CulturalDiffusion'),
    url(r'^GovernmentalPerspective', hello.views.GovernmentalPerspective, name='GovernmentalPerspective'),
    url(r'^Prestige', hello.views.Prestige, name='Prestige'),
    url(r'^Security', hello.views.Security, name='Security'),
    url(r'^TradeRelations', hello.views.TradeRelations, name='TradeRelations'),
    url(r'^meetingjsonlist', hello.views.meeting_json_list, name='meetingjsonlist'),
    url(r'^country_name_list', hello.views.country_name_list, name='country_name_list'),
    #Apis
    url(r'^apiDynamic/\w{2,40}', hello.views.get_Dynamic_Table, name='get_Dynamic_Table'),
    url(r'^api/ByCountry/\w{2,40}', hello.views.get_Country_headline_data, name='Country_headline_data'),
    url(r'^api/\w{2,40}/\w{2,40}', hello.views.get_Table_and_Column, name='column_api'),
    url(r'^api/\w{2,20}', hello.views.get_Table, name='table_api'),
    #url(r'^favicon\.ico$', favicon_view),
]
