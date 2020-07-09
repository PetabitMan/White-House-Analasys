# White-House-Analasys
Python web-scraping tool to analyse the language patterns of the trump whitehouse


The aim of this project is to get information about the language patterns of the trump whitehouse.

The main source for our information is the official whitehouse (https://www.whitehouse.gov/briefings-statements/).

We get the data via a Webscrapper and it is organized in main_data {index: {date: date, link: link, text: text}.

In the current State of the programm the most useful Tool is to check the number of single words the Whitehouse used.
The data can also be graphed.

Through the module vader.sentiment we also get an idea if the statement is positive or negative.


