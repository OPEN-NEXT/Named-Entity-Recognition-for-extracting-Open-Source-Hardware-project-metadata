#! /usr/bin/env python
#  -*- coding: utf-8 -*-
#
# Support module generated by PAGE version 6.0.1
#  in conjunction with Tcl version 8.6
#    Apr 28, 2021 02:08:10 PM CEST  platform: Windows NT


#This file can be considered as the back end of the tkinter window

import sys
from spacy import displacy
import spacy
import requests
from bs4 import BeautifulSoup
import pandas as pd
import pickle
import os
from wordcloud import WordCloud
import matplotlib.pyplot as plt

"""
try:
    import Tkinter as tk
except ImportError:
    import tkinter as tk

try:
    import ttk
    py3 = False
except ImportError:
    import tkinter.ttk as ttk
    py3 = True 
    
    """

#The input is the url of a website, it return the text of the html tag class_="mw-content-ltr". This tag exists for appropedia pages but
#might not exists for other url
def url_to_transcript(url):
    '''Returns transcript data specifically from scrapsfromtheloft.com.'''
    page = requests.get(url).text
    soup = BeautifulSoup(page, "lxml")
    text = [p.text for p in soup.find(class_="mw-content-ltr")]
    #print(url)
    return text

def set_Tk_var():
    #global urlLabel
    urlLabel = input("Enter website or text:")
    urlButton(urlLabel)


""" def init(top, gui, *args, **kwargs):
    global w, top_level, root
    w = gui
    top_level = top
    root = top
"""
#This function starts when you click on the run model button
def urlButton(url):
    #url = urlLabel                       #get the text you enter in the entry
    split_txt = url.split(":")
    # need to fnd out if it's a corpus txt on a website
    #if it's a web site
    if split_txt[0] == "https":

        urls = []
        urls.append(url)
        transcripts = [url_to_transcript(u) for u in urls]          #apply the url_to_transcript function to the url entered in the entry
        hardwares = ["hardware"]

        for i, c in enumerate(hardwares):                          # creating the txt file to load the data
            with open(c + ".txt", "wb") as file:
                pickle.dump(transcripts[i], file)

        data = {}                                                   #load the data into a dictionnary this time
        for i, c in enumerate(hardwares):
            with open(c + ".txt", "rb") as file:
                data[c] = pickle.load(file)

        def combine_text(list_of_text):
            '''Takes a list of text and combines them into one large chunk of text.'''
            combined_text = ' '.join(list_of_text)
            return combined_text

        data_combined = {key: [combine_text(value)] for (key, value) in data.items()}

        pd.set_option('max_colwidth', 150)                                          #create a dataFrame with Pandas library with the texte
        data_df = pd.DataFrame.from_dict(data_combined).transpose()
        data_df.columns = ['transcript']
        data_df = data_df.sort_index()

        import re
        import string

#applying cleaning text technics

        def clean_text_round1(text):
            text = text.lower()                                                         #make the text lower case
            text = re.sub('\[.*?\]', '', text)                                          #remove question marks
            text = re.sub('[%s]' % re.escape(string.punctuation), '', text)             #remove poncutation
            return text

        round1 = lambda x: clean_text_round1(x)

        data_clean = pd.DataFrame(data_df.transcript.apply(round1))

        def clean_text_round2(text):
            text = re.sub('[‘’“”…]', '', text)                      #remove some other ponctuation
            text = re.sub('\n', ' ', text)                          #remove the \n
            # text = re.sub('\w*\d\w*', '', text)                   #remove the digits
            return text

        round2 = lambda x: clean_text_round2(x)

        data_clean = pd.DataFrame(data_clean.transcript.apply(round2))
        cleaned_transcripts = [data_clean.transcript.loc[i] for i in hardwares]
        # Wordcloud
        str1 = ''.join(cleaned_transcripts)
        wordcloud = WordCloud(random_state=8,
                              normalize_plurals=False,
                              width=600, height=300,
                              max_words=300,
                              stopwords=['the', 'of', 'and', 'is', 'to', 'in', 'a', 'from', 'by', 'that', 'with', 'this', 'as', 'an', 'are','its', 'at', 'for', 'on', 'into', 'will', 'be', 'there'])
        # Apply the wordcloud to the text.
        wordcloud.generate(str1)
        plt.imshow(wordcloud, interpolation='bilinear')
        plt.show()
        print("plot erstellt")
        for i, c in enumerate(hardwares):                               #save the the cleaned txt into a txt file
            with open(c + ".txt", "w", encoding='utf-8') as file:
                file.write(cleaned_transcripts[i])

        for i, c in enumerate(hardwares):
            with open(c + ".txt", "r", encoding='utf-8') as file:
                example = file.read()

        print("I got the corpus")
        nlp = spacy.load("./best_model")                                #use the NER model that we trainned in another programe
        print("NER loaded")
        doc = nlp(example)                                              #load the clean txt file and transforme it as an spacy doc and apply the model to this doc

#display the result on a webbrowser as an html page

        html = displacy.render(doc, style='ent', page=True)
        with open("data_visualisation3.html", "w", encoding='utf-8') as file:
            file.write(html)
        print("html page created")
        file.close()

        import webbrowser
        new = 2
        url = os.getcwd() + '/data_visualisation3.html'
        webbrowser.open(url, new=new)
        print("html page opened")
        sys.stdout.flush()

    #if it is a simple txt corpus
    else:

        example = url                                       #then the corpus txt become directly the spacy doc
        print("I got the corpus")
        nlp = spacy.load("./best_model")
        print("NER loaded")
        doc = nlp(example)                                      #you can directly apply the NER model to the Doc
        # Wordcloud
        wordcloud = WordCloud(random_state=8,
                              normalize_plurals=False,
                              width=600, height=300,
                              max_words=300,
                              stopwords=['the', 'of', 'and', 'is', 'to', 'in', 'a', 'from', 'by', 'that', 'with',
                                         'this', 'as', 'an', 'are', 'its', 'at', 'for', 'on', 'into','will', 'be', 'there'])
        # Apply the wordcloud to the text.
        wordcloud.generate(example)
        plt.imshow(wordcloud, interpolation='bilinear')
        plt.show()
#same technics to display the result

        html = displacy.render(doc, style='ent', page=True)
        with open("data_visualisation3.html", "w", encoding='utf-8') as file:
            file.write(html)
        print("html page created")
        file.close()

        import webbrowser
        new = 2
        url = os.getcwd() + '/data_visualisation3.html'
        print(url)
        webbrowser.open(url, new=new)
        print("html page opened")
        sys.stdout.flush()

def destroy_window():
    # Function which closes the window.
    global top_level
    top_level.destroy()
    top_level = None

if __name__ == '__main__':
    #import runModel3
    #runModel3.vp_start_gui()
    set_Tk_var()



