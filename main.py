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


class Whitehouse:
    
    def __init__(self):
        
        self.word_dict = json.load(open('dict_data.json'))
        if len(self.word_dict) > 0:
            self.y_values, self.x_values = 0, 0
            self.links= []
            self.urls = []
            self.texts = []
    
    def get_data(self):        
        
        #get pages number
        
        #loop through pages
        for i in range(3):
            result = requests.get(f"https://www.whitehouse.gov/briefings-statements/page/{i}/")
            rc = result.content
            soup = BeautifulSoup(rc, 'lxml')
            h2s = soup.find_all("h2")
            for h2_tag in h2s:
                a_tag = h2_tag.find('a')
                self.urls.append(a_tag.attrs)
            for url in self.urls:
                link = url['href']
                self.links.append(link)
        #get text
        
        for link in self.links:
            result = requests.get(link)
            rc = result.content
            soup = BeautifulSoup(rc, 'lxml')
            ps = soup.find_all("p")
            self.texts.append(ps)
        
        self.filter_words()
        
                                      
    def filter_words(self):
        big_text= "".join(str(t) for t in self.texts) 
        
        delete_items = ["<p>", "</p>", ".", ",", "!", "?", 'class=\"page-header__section\">',
                        'class=\"meta__label\">issued', '<time>june', '<span', '2020</time>',
                        'class=\"issue-flag\">', '</strong><strong></strong>', "</strong>"]
        
        for delete in delete_items:
            big_text.replace(delete, "")
        
        big_text.replace("\u2019", "`")
        big_text.replace("\u2014", "`")
        
        big_text = big_text.lower() 
        
        single_words_unfiltered = big_text.split()
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
        
    
    def get_dict_data(self):
        data_dict = {}
        for i in range(len(self.y_values)):
            data_dict[self.x_values[i]] = self.y_values[i]
        with open('dict_data.json', 'w') as dd:
            json.dump(data_dict, dd, indent=4)
            
        
    def store_data(self):
        with open('word_data.json', 'w') as wd:
            json.dump(self.x_values, wd, indent=4)
        with open('word_data.json', 'a') as wd:
            json.dump(self.y_values, wd, indent=4)
    
    def get_word_number(self, words):
        word_dict = json.load(open('dict_data.json'))
        for word in words:
            try:
                print(word_dict[word])
            except KeyError:
                print('word not found')
            
        
            
    def graph(self):
        Graphs.simple_graph(self.x_values, self.y_values)
              
            
w = Whitehouse()
#w.store_data()
#w.get_dict_data()
w.get_word_number(["great", "good", "magnificent", "amazing",
                   "bad", "black", "white", "corona", "virus", "best"])

            
                                       