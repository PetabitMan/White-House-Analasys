#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jun  3 15:41:56 2020

@author: paul
"""


#from selenium import webdriver
import requests
from bs4 import BeautifulSoup
import json
from show_graphs import Graphs
#from textblob import TextBlob
import datetime
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer


class Whitehouse:
    
    def __init__(self):
        
        #needed to filtert out unwated String or signs
        self.sentence_signs = [',', '!', '?', '.', '(', ')']   
        self.delete_items = ["<p>", "</p>", 'class=\"page-header__section\">',
                        'class=\"meta__label\">issued', '<time>june', '<span', '2020</time>',
                        'class=\"issue-flag\">', '</strong><strong></strong>', "</strong>", "\u201c",
                        "\u201dgre", "class=\"meta__label\">Issued", "class=\"meta__date\">"]
        
        self.analyzer = SentimentIntensityAnalyzer()
        
        self.word_dict = json.load(open('dict_data.json'))
        #if the user doesn't want to load new data
        if len(self.word_dict) == 0 or new_data == True:
            self.y_values, self.x_values = 0, 0
            self.links= []
            self.dates = []
            self.main_data = {}
            self.big_text = None
            self.get_data()
            
            
    #gets the data and stores it in main_data
    def get_data(self):        
        
        #pages mumber is given by User everry page has 10 Articles
        #loop through pages
        for i in range(span):
            urls = []
            result = requests.get(f"https://www.whitehouse.gov/briefings-statements/page/{i}/")
            rc = result.content
            soup = BeautifulSoup(rc, 'lxml')
            h2s = soup.find_all("h2")
            dates = soup.find_all("time")
            for date in dates:
                date = str(date)
                date = date.replace('<time>', '')
                date = date.replace('</time>', '')
                self.dates.append(date)
            for h2_tag in h2s:
                a_tag = h2_tag.find('a')
                urls.append(a_tag.attrs)
            for url in urls:
                link = url['href']
                self.links.append(link)
        #get text
        
        for i in range(len(self.links)):
            texts = []
            result = requests.get(self.links[i])
            rc = result.content
            soup = BeautifulSoup(rc, 'lxml')
            ps = soup.find_all("p")
            texts.append(ps)
            self.main_data[i] = {'date' : self.dates[i], 'text' : [texts], 'link' : self.links[i]}
    
    #to use a lot of functions
    def initialize_all(self):
        if new_data == True:
            self.big_text = self._filter_words(self._making_a_big_text())
            self._list_words()
            self._get_dict_data()
        else:
            print('You didn\'t get new data! The old data is already initialized.')
        
    def _making_a_big_text(self):
        texts = []
        for i in range(len(self.main_data)):
            texts.append(self.main_data[i]['text'])
        return texts
    
    #if you want to split a text into single sentences
    def _split_in_sentences(self, filtered_text):
        filtered_text = filtered_text.replace('!', '.')
        sentences = filtered_text.replace('?', '.')
        sentences = sentences.split('.')
        return sentences
     
    #to filter sentence signs out of a text to get just the single words
    def _filter_sentence_signs(self, text_to_filter):
            
        for delete in self.sentence_signs:
            text_to_filter = text_to_filter.replace(delete, "")
        return text_to_filter
    
    #filters unwanted strings
    def _filter_words(self, text_list_to_filter):
        
        text= "".join(str(t) for t in text_list_to_filter) 
        
        for delete in self.delete_items:
            text = text.replace(delete, "")
         
        text = self._filter_sentence_signs(text)
        
        # webscrapper replaces in ' with \u2019 we undo that her
        text = text.replace("\u2019", "`")
        text = text.replace("\u2014", "`")
        
        
        return text
        
    #list words into the word and the amount how often it is used and stores them in values
    def _list_words(self):
        
        self.big_text = self.big_text.lower() 
        single_words_unfiltered = self.big_text.split()
        single_words = single_words_unfiltered.copy()
        
        self.x_values = list(dict.fromkeys(single_words_unfiltered))
        self.y_values = []
        
        for y_value in self.x_values:
            number = single_words.count(y_value)
            self.y_values.append(number)
        

        #sort data
        self.y_values, self.x_values = zip(*sorted(zip(self.y_values, self.x_values)))
        self.y_values = list(reversed(self.y_values))
        self.x_values = list(reversed(self.x_values))
        
    #stores x and y_values in a seperate dictionary
    def _get_dict_data(self):
        data_dict = {}
        for i in range(len(self.y_values)):
            data_dict[self.x_values[i]] = self.y_values[i]
        with open('dict_data.json', 'w') as dd:
            json.dump(data_dict, dd, indent=4)
            
        
    #not really necissary anymore dict data is better
    def _store_data(self):
        with open('word_data.json', 'w') as wd:
            json.dump(self.x_values, wd, indent=4)
        with open('word_data.json', 'a') as wd:
            json.dump(self.y_values, wd, indent=4)
    
    #a function to get the number of a specific word 
    def get_word_number(self, words):
        if len(self.word_dict) == 0:
            self.word_dict = json.load(open('dict_data.json'))
        for word in words:
            try:
                print(word + ':',self.word_dict[word])
            except KeyError:
                print(f'{word}: word not found')
    
    
    #accesses another file and shows a graph
    def graph_all_stored_data(self):
        x_vals = []
        y_vals = []
        if len(self.word_dict) == 0:
            self.word_dict = json.load(open('dict_data.json'))
        for key, value in self.word_dict.items():
            x_vals.append(key)
            y_vals.append(value)
        Graphs.simple_graph(self, x_vals, y_vals)
        
    def graph_all_new_data(self):
        try:
            Graphs.simple_graph(self, self.x_values, self.y_values)
        except:
            print('Try running initialize_all first')
    
    def graph_words_out_of_dict_data(self, word_list):
        if len(self.word_dict) == 0:
            self.word_dict = json.load(open('dict_data.json'))
        x_vals = []
        y_vals = []
        for word in word_list:
            try:
                y_vals.append(self.word_dict[word])
                x_vals.append(word)
            except:
                y_vals.append(0)
                x_vals.append(word)
        Graphs.simple_graph(self, x_vals, y_vals)
    
    def get_negative_and_positive_statements(self):
        negative_statements = []
        positive_statements = []
        try:
            for i in range(len(self.main_data)):
                article_text = self._filter_words(self.main_data[i]['text'])
                if self.analyzer.polarity_scores(article_text)['compound'] >= 1:
                    positive_statements.append(article_text)
                elif self.analyzer.polarity_scores(article_text)['compound'] <= -1:
                    negative_statements.append(article_text)
                print(self.analyzer.polarity_scores(article_text)['compound'])
        except AttributeError:
            print('You have to get new data first')
           
        print(len(negative_statements))
        print(len(positive_statements))
        return negative_statements, positive_statements
#ask if user wants to get new data


new_data = input('do you want to get new data? (type in y to get new data.)\n')
if new_data == 'y':
    print('Every page holds 10 press-statements')
    span = int(input('How many pages do you want to analyse?\n'))
    print(f'This could take up to {span * 16} seconds.')
    new_data = True
else:
    span = 1

print(datetime.datetime.now())
# iniitalizing instance of Whihouse
w = Whitehouse()
print(datetime.datetime.now())
#testing out a method


w.initialize_all()
w.get_word_number(["great", "good", "magnificent", "amazing",
                   "bad", "black", "white", "corona", "virus", "best"])

w.graph_words_out_of_dict_data(["great", "good", "magnificent", "amazing",
                   "bad", "black", "white", "corona", "virus", "best"])               

one, two = w.get_negative_and_positive_statements()

