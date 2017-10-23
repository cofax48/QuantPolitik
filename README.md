# QuantPolitik
Quantification of International Relations

This is a repository of files that are used to build Quantpolitik.com. The python files are used in two main ways, to build the django 
server and to build the web scrapers that download pertinent data, build the formula, and run the formula on a daily basis. The files that
build the formula can be found in the https://github.com/cofax48/QuantPolitik/tree/master/Formula_maker folder. These files run the formula
daily and are initialized by QP_SCORE_MAKER.py. The data assets they draw off of are found in the Data_Assets folder. While the scrapers
that obtain the needed data are found in the Web_Scraper folder. These files are triggered through a redis queue initialized 
by https://github.com/cofax48/QuantPolitik/blob/master/clock.py. While the Django files can be found within the hello/getting started folder 
(the initial server framework was ported from Heroku's getting started tutorial, and has subsequently been widely expanded).

The Javascript included within Quantpolitik.com can be found https://github.com/cofax48/QuantPolitik/tree/master/hello/static/assets/js as 
this is where static JS assets are kept and employed. Within this sub-repository are the data visualizations for Quantpolitik as well the 
AngularJS logic for the country data controller.

The html for this project is found here at: https://github.com/cofax48/QuantPolitik/tree/master/hello/templates, this repository includes 
all the html pages used on Quantpolitik. 
While the css employed is found here: https://github.com/cofax48/QuantPolitik/tree/master/hello/static/assets/css 

The database is in postgres and is hosted on heroku. If interested in accessing the data hosted for the project, please message me 
and I'd be happy to share the API-key. 

Thanks for visiting the Quantpolitik repository and if there are any questions, comments, concerns, please get in touch, otherwise, enjoy!
