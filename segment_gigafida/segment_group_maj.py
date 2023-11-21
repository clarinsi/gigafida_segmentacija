import re
import operator
import os
import matplotlib.pyplot as plt
import xml.etree.ElementTree as ET
import seaborn as sns
import numpy as np
from ast import literal_eval
from collections import Counter


from sentence_transformers import SentenceTransformer, util
sentsim_model = SentenceTransformer('distiluse-base-multilingual-cased-v2')


def read_names(filename):
    names = []
    with open(filename, 'r', encoding="utf-8") as f:
        for line in f:
            name = line.split('>')[1].split('<')[0]
            names.append(name)
    return set(names)
    
def read_names_upper(filename):
    names = []
    with open(filename, 'r', encoding="utf-8") as f:
        for line in f:
            name = line.split('>')[1].split('<')[0]
            names.append(name.upper())
    return set(names)
    



def get_sentsim_scores( filename):
    split_articles = []
    with open(filename, 'r', encoding='utf-8') as f:
        tree = ET.parse(f)
        #print(tree)
        root = tree.getroot()
        text = root.find('{http://www.tei-c.org/ns/1.0}text')
        body = text.find('{http://www.tei-c.org/ns/1.0}body')
        #print(body)
        current_article = []
        prev_paragraph_embedding = None
        prev_sent = None
        similarity_scores = []
        for paragraph in body:
            #print(paragraph)
            words = get_words_from_paragraph(paragraph)
            if len(words) == 0:
                continue
            sent = "".join(words)
            paragraph_embedding = sentsim_model.encode(sent)
            #print(paragraph_embedding)
            #print(len(words))
            #exit()
            #print('w', words)
            #print('p', paragraph_embedding)
            if prev_paragraph_embedding is not None:
                #print(paragraph_embedding)
                #print(prev_paragraph_embedding)
                similarity_to_prev = util.cos_sim(paragraph_embedding, prev_paragraph_embedding)[0].cpu().tolist()
                similarity_scores.append(similarity_to_prev[0])
                if similarity_to_prev[0] > 0.7:
                    print(prev_sent[:10], '-', sent[:10])
                    split_articles.append(current_article)
                    current_article = [paragraph]
                    prev_paragraph_embedding = paragraph_embedding
                else:
                    current_article.append(paragraph)
                    prev_paragraph_embedding = paragraph_embedding
                    prev_sent = sent
            else:
                prev_paragraph_embedding = paragraph_embedding
                prev_sent = sent
        split_articles.append(current_article)
        print(sorted(similarity_scores))
        print_split_articles(split_articles)
        #print(split_articles)
        return similarity_scores
        
        
        
def get_sentsim_scores_gaps(filename):
    prev_was_gap = False
    split_articles = []
    current_paragraphs_words = []
    split_vector = []
    with open(filename, 'r', encoding='utf-8') as f:
        tree = ET.parse(f)
        #print(tree)
        root = tree.getroot()
        text = root.find('{http://www.tei-c.org/ns/1.0}text')
        body = text.find('{http://www.tei-c.org/ns/1.0}body')
        #print(body)
        current_article = []
        prev_paragraph_embedding = None
        prev_sent = None
        similarity_scores = []
        for paragraph in body:
            if paragraph.tag == '{http://www.tei-c.org/ns/1.0}gap':       
                print(paragraph)
                sent = "".join(current_paragraphs_words)
                paragraph_embedding = sentsim_model.encode(sent)
                if prev_paragraph_embedding is not None:
                    similarity_to_prev = util.cos_sim(paragraph_embedding, prev_paragraph_embedding)[0].cpu().tolist()
                    similarity_scores.append(similarity_to_prev[0])
                    print(current_paragraphs_words)
                    # Check if this actually separated the two - this holds if the start of the current paragraph embedding matches the manual criteria
                    if len(current_paragraphs_words[0]) > 0 and current_paragraphs_words[0].isupper() and len(current_paragraphs_words[0]) > 2:
                        split_vector.append(1)
                    else:
                        split_vector.append(0)
                    prev_paragraph_embedding = paragraph_embedding
                    current_paragraphs_words = []
                else:
                    prev_paragraph_embedding = paragraph_embedding
                    current_paragraphs_words = []
            else:
                words = get_words_from_paragraph(paragraph)
                if len(words) == 0:
                    continue
                current_paragraphs_words += words
           
        #print(similarity_scores)
        #print(split_articles)

        return similarity_scores, split_vector
        
        
def get_sentsim_scores_gaps_max(filename):
    prev_was_gap = False
    split_articles = []
    current_paragraphs_words = []
    split_vector = []
    with open(filename, 'r', encoding='utf-8') as f:
        tree = ET.parse(f)
        #print(tree)
        root = tree.getroot()
        text = root.find('{http://www.tei-c.org/ns/1.0}text')
        body = text.find('{http://www.tei-c.org/ns/1.0}body')
        #print(body)
        current_article = []
        prev_paragraph_embedding = None
        prev_sent = None
        similarity_scores = []
        for paragraph in body:
            if paragraph.tag == '{http://www.tei-c.org/ns/1.0}gap':       
                #print(paragraph)
                #sent = "".join(current_paragraphs_words)
                paragraph_embedding = [sentsim_model.encode("".join(sent)) for sent in current_paragraphs_words]
                if prev_paragraph_embedding is not None:
                    max_sim = 0
                    for e1 in paragraph_embedding:
                        for e2 in prev_paragraph_embedding:
                            similarity_to_prev = util.cos_sim(e1, e2)[0].cpu().tolist()[0]
                            if similarity_to_prev > max_sim:    
                                max_sim = similarity_to_prev
                    print(max_sim)
                    #similarity_to_prev = util.cos_sim(paragraph_embedding, prev_paragraph_embedding)[0].cpu().tolist()
                    #similarity_scores.append(similarity_to_prev[0])
                    similarity_scores.append(max_sim)
                    print(current_paragraphs_words)
                    # Check if this actually separated the two - this holds if the start of the current paragraph embedding matches the manual criteria
                    if len(current_paragraphs_words[0][0]) > 0 and current_paragraphs_words[0][0].isupper() and len(current_paragraphs_words[0][0]) > 2:
                        split_vector.append(1)
                    else:
                        split_vector.append(0)
                    prev_paragraph_embedding = paragraph_embedding
                    current_paragraphs_words = []
                else:
                    prev_paragraph_embedding = paragraph_embedding
                    current_paragraphs_words = []
            else:
                words = get_words_from_paragraph(paragraph)
                if len(words) == 0:
                    continue
                current_paragraphs_words.append(words)
           
        #print(similarity_scores)
        #print(split_articles)

        return similarity_scores, split_vector
            
        
        
        
def get_words_from_sentence(sent_node):
    words = []
    for e in sent_node:
        if e.tag == '{http://www.tei-c.org/ns/1.0}w' or e.tag == '{http://www.tei-c.org/ns/1.0}c' or e.tag == '{http://www.tei-c.org/ns/1.0}pc':
            #if e.text[-1] == '.':
                #print(e.text)
            words.append(e.text)
    return words       
    
def get_sentsim_scores_window(filename, window):
    split_articles = []
    split_vector = []
    with open(filename, 'r', encoding='utf-8') as f:
        tree = ET.parse(f)
        #print(tree)
        root = tree.getroot()
        text = root.find('{http://www.tei-c.org/ns/1.0}text')
        body = text.find('{http://www.tei-c.org/ns/1.0}body')
        #print(body)
        current_article = []
        both_window = []
        prev_paragraph_embedding = None
        prev_sent = None
        similarity_scores = []
        for paragraph in body:
            for sentence in paragraph:
                if sentence.tag != '{http://www.tei-c.org/ns/1.0}s':
                    #print(sentence.tag)
                    continue
                if len(both_window) != window+1:
                    both_window.append(sentence)
                else:
                    sent_words = get_words_from_sentence(sentence)
                    if len(sent_words[0]) > 0 and sent_words[0].isupper() and len(sent_words[0]) > 2:
                        #print(sent_words)
                        split_vector.append(1)
                    else:
                        split_vector.append(0)
                    prev_window = both_window[:-1]
                    curr_window = both_window[1:]
                    curr_window = "".join(["".join(get_words_from_sentence(x)) for x in curr_window])
                    prev_window = "".join(["".join(get_words_from_sentence(x)) for x in prev_window])
                    #print(curr_window)
                    prev_embedding = sentsim_model.encode(prev_window)
                    curr_embedding = sentsim_model.encode(curr_window)
                    similarity_score = util.cos_sim(curr_embedding, prev_embedding)[0].cpu().tolist()[0]
                    #print(similarity_score)
                    similarity_scores.append(similarity_score)
                    if similarity_score < 0.2:
                        print(prev_window)
                        print('-----------------------')
                        print(curr_window)
                        #print(prev_window[:10], '-', curr_window[:10])
                        #split_articles.append(current_article)
                        #current_article = [sentence]
                    #else:
                    #    current_article.append(sentence)
                    both_window.append(sentence)
                    both_window = both_window[1:]
        split_articles.append(current_article)
        #print(sorted(similarity_scores))
        print_split_articles(split_articles)
        #print(split_articles)
        return similarity_scores, split_vector
        
        
def get_sentsim_scores_window_max(filename, window):
    split_articles = []
    split_vector = []
    with open(filename, 'r', encoding='utf-8') as f:
        tree = ET.parse(f)
        #print(tree)
        root = tree.getroot()
        text = root.find('{http://www.tei-c.org/ns/1.0}text')
        body = text.find('{http://www.tei-c.org/ns/1.0}body')
        #print(body)
        current_article = []
        both_window = []
        prev_paragraph_embedding = None
        prev_sent = None
        similarity_scores = []
        for paragraph in body:
            for sentence in paragraph:
                if sentence.tag != '{http://www.tei-c.org/ns/1.0}s':
                    #print(sentence.tag)
                    continue
                if len(both_window) != window+1:
                    both_window.append(sentence)
                else:
                    sent_words = get_words_from_sentence(sentence)
                    if len(sent_words[0]) > 0 and sent_words[0].isupper() and len(sent_words[0]) > 2:
                        #print(sent_words)
                        split_vector.append(1)
                    else:
                        split_vector.append(0)
                    window_embeddings = [sentsim_model.encode("".join(get_words_from_sentence(s))) for s in both_window]
                    prev_window = both_window[:-1]
                    curr_window = both_window[-1]
                    #curr_window = "".join(["".join(get_words_from_sentence(x)) for x in curr_window])
                    #prev_window = "".join(["".join(get_words_from_sentence(x)) for x in prev_window])
                    #print(curr_window)
                    prev_embeddings = window_embeddings[:-1]
                    curr_embeddings = [window_embeddings[-1]]
                    max_sim = 0
                    print('---------------')
                    print(len(prev_embeddings), len(curr_embeddings))
                    for e1 in prev_embeddings:
                        for e2 in curr_embeddings:
                            similarity_score = util.cos_sim(e1, e2)[0].cpu().tolist()[0]
                            
                            #print(similarity_score)
                            if similarity_score > max_sim:
                                max_sim = similarity_score
                    print('---------------')            
                            
                    #exit()
                    similarity_score = max_sim
                    print(similarity_score)
                    #print(similarity_score)
                    similarity_scores.append(similarity_score)
                    if similarity_score < 0.2:
                        print(prev_window)
                        print('-----------------------')
                        print(curr_window)
                        #print(prev_window[:10], '-', curr_window[:10])
                        #split_articles.append(current_article)
                        #current_article = [sentence]
                    #else:
                    #    current_article.append(sentence)
                    both_window.append(sentence)
                    both_window = both_window[1:]
                    
        split_articles.append(current_article)
        #print(sorted(similarity_scores))
        #print_split_articles(split_articles)
        #print(split_articles)
        return similarity_scores, split_vector
           
def get_words_from_paragraph(node):
    words = []
    for sentence in node:
        for e in sentence:
            if e.tag == '{http://www.tei-c.org/ns/1.0}w' or e.tag == '{http://www.tei-c.org/ns/1.0}c' or e.tag == '{http://www.tei-c.org/ns/1.0}pc':
                #if e.text[-1] == '.':
                    #print(e.text)
                words.append(e.text)
    return words       

def get_sents_from_paragraph(node):
    words = []
    sents = []
    for sentence in node:
        for e in sentence:
            if e.tag == '{http://www.tei-c.org/ns/1.0}w' or e.tag == '{http://www.tei-c.org/ns/1.0}c' or e.tag == '{http://www.tei-c.org/ns/1.0}pc':
                #if e.text[-1] == '.':
                    #print(e.text)
                words.append(e.text)
        sents.append(words)
        words = []
    return sents      

    

def split_by_short_paragraphs(filename):
    split_articles = []
    with open(filename, 'r', encoding='utf-8') as f:
        tree = ET.parse(f)
        #print(tree)
        root = tree.getroot()
        text = root.find('{http://www.tei-c.org/ns/1.0}text')
        body = text.find('{http://www.tei-c.org/ns/1.0}body')
        #print(body)
        current_article = []
        for paragraph in body:
            #print(paragraph)
            words = get_words_from_paragraph(paragraph)
            if len(words) <= 5:
                split_articles.append(current_article)
                current_article = [paragraph]
            else:
                current_article.append(paragraph)
         
            
            
def print_split_articles(split_articles, filename="./outtest.txt"):          
     with open(filename, 'w', encoding='utf-8') as outf: 
        print('------------------', file=outf)
        for article in split_articles:
            for paragraph in article:
                print("".join(get_words_from_paragraph(paragraph)), file=outf)
            print('------------------', file=outf) 

def split_by_initials(filename):
    split_articles = []
    with open(filename, 'r', encoding='utf-8') as f:
        tree = ET.parse(f)
        #print(tree)
        root = tree.getroot()
        text = root.find('{http://www.tei-c.org/ns/1.0}text')
        body = text.find('{http://www.tei-c.org/ns/1.0}body')
        #print(body)
        current_article = []
        for paragraph in body:
            #print(paragraph)
            words = get_words_from_paragraph(paragraph)
            if len(words) == 2 and words[0][-1] == '.' and words[1][-1] == '.':
                split_articles.append(current_article)
                current_article = [paragraph]
            else:
                current_article.append(paragraph)
        print_split_articles(split_articles)
        

def split_by_all_caps_name(filename):
    split_articles = []
    with open(filename, 'r', encoding='utf-8') as f:
        tree = ET.parse(f)
        #print(tree)
        root = tree.getroot()
        text = root.find('{http://www.tei-c.org/ns/1.0}text')
        body = text.find('{http://www.tei-c.org/ns/1.0}body')
        #print(body)
        current_article = []
        for paragraph in body:
            #print(paragraph)
            words = get_words_from_paragraph(paragraph)
            is_all_caps = [w.isupper() for w in words]
            if all(is_all_caps):
                split_articles.append(current_article)
                current_article = [paragraph]
            else:
                current_article.append(paragraph)
        print_split_articles(split_articles)
    

def split_by_all_caps_location(filename):
    split_articles = []
    with open(filename, 'r', encoding='utf-8') as f:
        tree = ET.parse(f)
        #print(tree)
        root = tree.getroot()
        text = root.find('{http://www.tei-c.org/ns/1.0}text')
        body = text.find('{http://www.tei-c.org/ns/1.0}body')
        #print(body)
        current_article = []
        for paragraph in body:
            words = get_words_from_paragraph(paragraph)
            print(words)
            if '-' in words:
                pre_minus = " ".join(words).split("-")[0].split(" ")[:-1]
                pre_minus = [w for w in pre_minus if w not in ["-", ",", ".", ":", ";"]]
                is_all_caps = [w.isupper() for w in pre_minus]
                if all(is_all_caps):
                    split_articles.append(current_article)
                    current_article = [paragraph]
                else:
                    current_article.append(paragraph)
        print_split_articles(split_articles)
        
        
def split_by_all_caps_location_first_word(filename):
    split_vector = []
    split_articles = []
    with open(filename, 'r', encoding='utf-8') as f:
        tree = ET.parse(f)
        #print(tree)
        root = tree.getroot()
        text = root.find('{http://www.tei-c.org/ns/1.0}text')
        body = text.find('{http://www.tei-c.org/ns/1.0}body')
        #print(body)
        current_article = []
        for paragraph in body:
            words = get_words_from_paragraph(paragraph)
            if len(words) == 0:
                continue
            if words[0].isupper() and len(words[0]) > 1:
                split_articles.append(current_article)
                current_article = [paragraph]
                split_vector.append(1)
            else:
                current_article.append(paragraph)
                split_vector.append(0)
        #print_split_articles(split_articles)
    return split_articles, split_vector
    
    
def split_by_location_minus(filename):
    split_vector = []
    split_articles = []
    with open(filename, 'r', encoding='utf-8') as f:
        tree = ET.parse(f)
        #print(tree)
        root = tree.getroot()
        text = root.find('{http://www.tei-c.org/ns/1.0}text')
        body = text.find('{http://www.tei-c.org/ns/1.0}body')
        #print(body)
        current_article = []
        for paragraph in body:
            words = get_words_from_paragraph(paragraph)
            if len(words) == 0:
                continue
            #print(words[2])
            if words[2] == '-' and len(words[0]) > 1:
                split_articles.append(current_article)
                current_article = [paragraph]
                split_vector.append(1)
            else:
                current_article.append(paragraph)
                split_vector.append(0)
        #print_split_articles(split_articles)
    return split_articles, split_vector
    
    




def split_by_simple_paragraphs(filename, filename_out):
    split_articles = []
    with open(filename, 'r', encoding='utf-8') as f:
        tree = ET.parse(f)
        #print(tree)
        root = tree.getroot()
        text = root.find('{http://www.tei-c.org/ns/1.0}text')
        body = text.find('{http://www.tei-c.org/ns/1.0}body')
        #print(body)
        current_article = []
        for paragraph in body:
            split_articles.append([paragraph])
    print_split_articles(split_articles, filename_out)

def split_by_zero_length_paragraphs(filename, filename_out):
    split_articles = []
    with open(filename, 'r', encoding='utf-8') as f:
        tree = ET.parse(f)
        #print(tree)
        root = tree.getroot()
        text = root.find('{http://www.tei-c.org/ns/1.0}text')
        body = text.find('{http://www.tei-c.org/ns/1.0}body')
        #print(body)
        current_article = []
        for paragraph in body:
            #print(paragraph)
            words = get_words_from_paragraph(paragraph)
            if len(words) ==0:
                split_articles.append(current_article)
                current_article = []
            else:
                current_article.append(paragraph)
    print_split_articles(split_articles, filename_out)
    
    
def check_length_zero_length_paragraphs(filename):
    split_articles = []
    article_lengths = []
    curr_paragraph_words = 0
    with open(filename, 'r', encoding='utf-8') as f:
        tree = ET.parse(f)
        #print(tree)
        root = tree.getroot()
        text = root.find('{http://www.tei-c.org/ns/1.0}text')
        body = text.find('{http://www.tei-c.org/ns/1.0}body')
        #print(body)
        current_article = []
        for paragraph in body:
            #print(paragraph)
            words = get_words_from_paragraph(paragraph)
            words_to_count = [w for w in words if w != ' ']
            if len(words) == 0:
                article_lengths.append(curr_paragraph_words)
                curr_paragraph_words = 0
                split_articles.append(current_article)
                current_article = []
            else:
                current_article.append(paragraph)
                curr_paragraph_words += len(words_to_count)
    #print_split_articles(split_articles, filename_out)
    return split_articles, article_lengths
    
    
def split_by_location_minus_with_lengths(filename):
    print(filename)
    split_articles = []
    article_lengths = []
    curr_paragraph_words = 0
    with open(filename, 'r', encoding='utf-8') as f:
        tree = ET.parse(f)
        #print(tree)
        root = tree.getroot()
        text = root.find('{http://www.tei-c.org/ns/1.0}text')
        body = text.find('{http://www.tei-c.org/ns/1.0}body')
        #print(body)
        current_article = []
        for paragraph in body:
            words = get_words_from_paragraph(paragraph)
            words_to_count = [w for w in words if w != ' ']
            if len(words) == 0:
                continue
            #print(words[2])
            #print("WORDS", words)
            if len(words) >= 3 and len(words[0]) > 1 and words[2] == '-':
                split_articles.append(current_article)
                current_article = [paragraph]
                article_lengths.append(curr_paragraph_words)
                curr_paragraph_words = 0
            else:
                current_article.append(paragraph)
                curr_paragraph_words += len(words_to_count)
        #print_split_articles(split_articles)
    return split_articles, article_lengths
    
    
def split_for_delo(filename):
    print(filename)
    split_articles = []
    article_lengths = []
    curr_paragraph_words = 0
    with open(filename, 'r', encoding='utf-8') as f:
        tree = ET.parse(f)
        #print(tree)
        root = tree.getroot()
        text = root.find('{http://www.tei-c.org/ns/1.0}text')
        body = text.find('{http://www.tei-c.org/ns/1.0}body')
        #print(body)
        current_article = []
        split_on_next_paragraph = False
        split_on_prev_paragraph = False
        for paragraph in body:
            if split_on_next_paragraph:
                to_split = True
                split_on_next_paragraph = False
            else:
                to_split = False
                split_on_prev_paragraph = False
            words = get_words_from_paragraph(paragraph)
            sents = get_sents_from_paragraph(paragraph)
            words_to_count = [w for w in words if w != ' ']
            if len(words) == 0:
                continue
            # Skip by location minus - zdaj naredi samo, če je pred tem nek daljši članek (>3 paragraphs), drugače gre verjetno le za naslove
            if len(words) >= 3 and len(words[0]) > 1 and words[2] == '-':
                if len(current_article) > 4:
                    to_split = True
            # Split by all-caps organization abbreviation at the end. Also works for author abbrvs.
            if words[-1].isupper() and words[-1] != '.' and len(words[-1]) < 10:
                split_on_next_paragraph = True
            # Split by author abbrvs. Could be A. B. or A. Bb. or Aa. B or Aa. Bb.
            author_regex = "[A-Z]\."
            author_regex2 = "[A-Z][a-z]\."
            author_regex3 = "[A-Z]"
            author_regex4 = "[A-Z][a-z]"
            if len(words) >= 3:
                if re.match(author_regex, words[-1]) and re.match(author_regex, words[-3]):
                    split_on_next_paragraph = True
                if re.match(author_regex2, words[-1]) and re.match(author_regex, words[-3]):
                    split_on_next_paragraph = True
                if re.match(author_regex, words[-1]) and re.match(author_regex2, words[-3]):
                    split_on_next_paragraph = True
                if re.match(author_regex2, words[-1]) and re.match(author_regex2, words[-3]):
                    split_on_next_paragraph = True
            # Special case where the end comma is in a new word
            if len(words) >= 4:
                if re.match(author_regex3, words[-2]) and re.match(author_regex, words[-4]):
                    split_on_next_paragraph = True
                if re.match(author_regex4, words[-2]) and re.match(author_regex, words[-4]):
                    split_on_next_paragraph = True
                if re.match(author_regex3, words[-2]) and re.match(author_regex2, words[-4]):
                    split_on_next_paragraph = True
                if re.match(author_regex4, words[-2]) and re.match(author_regex2, words[-4]):
                    split_on_next_paragraph = True
            # Split by Name + Surname + No comma at the end of article
            if (len(sents[-1]) == 3 and sents[-1][0] in slo_imena and sents[-1][2] in slo_imena and sents[-1][-1] not in ['.', '!', '?', ':', ';', ' ', ',', '«', '«']):
                split_on_next_paragraph = True
            # Še za tri imena
            if (len(sents[-1]) == 5 and sents[-1][0] in slo_imena and sents[-1][2] in slo_imena and sents[-1][4] in slo_imena and sents[-1][-1] not in ['.', '!', '?', ':', ';', ' ', ',', '«', '«']):
                split_on_next_paragraph = True
            # Avoid splitting short articles, probably a mistake in one of the rules
            if to_split and len(current_article) > 1:
                split_articles.append(current_article)
                current_article = [paragraph]
                article_lengths.append(curr_paragraph_words)
                curr_paragraph_words = 0
            else:
                current_article.append(paragraph)
                curr_paragraph_words += len(words_to_count)
        #print_split_articles(split_articles)
        split_articles.append(current_article)
        current_article = [paragraph]
        article_lengths.append(curr_paragraph_words)
        curr_paragraph_words = 0
    return split_articles, article_lengths
    

def split_for_dnevnik(filename):
    #print(filename)
    lines_since_v_srediscu = 0
    with open('./ALL_CAPS_NASLOVI', 'a', encoding='utf-8') as acf:
        print(filename, file=acf)
    
    with open('./MULTI_LINE_TITLES.txt', 'a', encoding='utf-8') as mlf:
        print(filename, file=mlf)
    split_articles = []
    article_lengths = []
    curr_paragraph_words = 0
    candidate_titles = []
    do_not_append_to_article= False
    print_candidate_titles_next_line = False
    with open(filename, 'r', encoding='utf-8') as f:
        do_not_append_to_article = False
        tree = ET.parse(f)
        #print(tree)
        root = tree.getroot()
        text = root.find('{http://www.tei-c.org/ns/1.0}text')
        body = text.find('{http://www.tei-c.org/ns/1.0}body')
        #print(body)
        current_article = []
        split_on_next_paragraph = False
        split_on_prev_paragraph = False
        for paragraph in body:
            if split_on_next_paragraph:
                to_split = True
                split_on_next_paragraph = False
            else:
                to_split = False
                split_on_prev_paragraph = False
            words = get_words_from_paragraph(paragraph)
            sents = get_sents_from_paragraph(paragraph)
            words_to_count = [w for w in words if w != ' ']
            lines_since_v_srediscu += 1

            if len(words) == 0:
                continue
            # Skip by location minus - zdaj naredi samo, če je pred tem nek daljši članek (>3 paragraphs), drugače gre verjetno le za naslove
            if len(words) >= 3 and len(words[0]) > 1 and words[2] == '-':
                if not words[0].isupper():
                    if len(current_article) > 4:
                        to_split = True
                        #print("appended6", words)
            # Split by key words (split before)
            if (words[0] in ["ODER", "GLASBA", "RAZSTAVE", "OTROŠKI"]) or (len(words)>=3 and words[0] == "DRUGI" and words[2] == "DOGODKI"):
                to_split = True
                #print("ODER in ostalo in ", filename)
                
            if (len(words)>=3 and words[0] == "V" and words[2] == "SREDIŠČU"):
                if(lines_since_v_srediscu>10):
                    to_split = True
                    lines_since_v_srediscu = 0
                    #print("V SREDISCU in ", filename)
            
            # Split by all-caps organization abbreviation at the end. Also works for author abbrvs.
            """
            if words[-1].isupper() and words[-1] != '.' and len(words[-1]) < 10:
                split_on_next_paragraph = True
                print("appended5", words)
            """
            # Split by key words (split before)
            if(words[0] == "DNEVNIKOVO" and words[2] == "BIOVREME"):
                to_split = True
                #print("DNEVNIKOVO BIOVREME in ", filename)
            if(words[0] == "BIOVREME"):
                to_split = True
                #print("BIOVREME in ", filename)
            # Split by author in brackets
            if len(words) > 3 and words[-3] == "("  and len(words[-2]) <= 3:
                split_on_next_paragraph = True;
                #print(words[-3], words[-2], words[-1])
            
            # Split by author abbrvs. Could be A. B. or A. Bb. or Aa. B or Aa. Bb.
            author_regex = "[A-Z]\."
            author_regex2 = "[A-Z][a-z]\."
            author_regex3 = "[A-Z]"
            author_regex4 = "[A-Z][a-z]"
            if len(words) >= 3:
                
                if re.match(author_regex, words[-1]) and re.match(author_regex, words[-3]):
                    split_on_next_paragraph = True
                    #print("appended4", words)
                if re.match(author_regex2, words[-1]) and re.match(author_regex, words[-3]):
                    split_on_next_paragraph = True
                    #print("appended4", words)
                if re.match(author_regex, words[-1]) and re.match(author_regex2, words[-3]):
                    split_on_next_paragraph = True
                    #print("appended4", words)
                if re.match(author_regex2, words[-1]) and re.match(author_regex2, words[-3]):
                    split_on_next_paragraph = True
                    #print("appended4", words)
            # Special case where the end comma is in a new word
            if len(words) >= 4:
                
                if re.match(author_regex3, words[-2]) and re.match(author_regex, words[-4]):
                    split_on_next_paragraph = True
                    #print("appended3", words)
                if re.match(author_regex4, words[-2]) and re.match(author_regex, words[-4]):
                    split_on_next_paragraph = True
                    #print("appended3", words)
                if re.match(author_regex3, words[-2]) and re.match(author_regex2, words[-4]):
                    split_on_next_paragraph = True
                    #print("appended3", words)
                if re.match(author_regex4, words[-2]) and re.match(author_regex2, words[-4]):
                    split_on_next_paragraph = True
                    #print("appended3", words)
                    
            # Split by Name + Surname + No comma at the end of article
            # VER MAJ ločevanje po avtorjih izgleda zmede stvari, ker so včasih vrinjeni med naslove, sedaj izbrisano

            if (len(sents[-1]) == 3 and sents[-1][0] in slo_imena and sents[-1][2] in slo_imena and sents[-1][-1] not in ['.', '!', '?', ':', ';', ' ', ',', '«', '«']):
                split_on_next_paragraph = True

            #print("appended2", words)
            # Še za tri imena
            # VER MAJ - Tudi tukaj

            if (len(sents[-1]) == 5 and sents[-1][0] in slo_imena and sents[-1][2] in slo_imena and sents[-1][4] in slo_imena and sents[-1][-1] not in ['.', '!', '?', ':', ';', ' ', ',', '«', '«']):
                split_on_next_paragraph = True
                #print("appended1", words)

            # Split on "CITY, num". Isto kot za staro lokacijo, samo če pred tem že imamo nek članek
            #if (words[0][:-1].isupper() and words[0][-1] == ',' and words[1][:-1].isdigit()):
            """
            if (words[0].isupper() and len(words) > 3 and  words[1] == ',' and words[3][:-1].isdigit()):
                print('DNEVNIK CITY SPLIT', words)
                if (len(current_article) > 2 and to_split == False):
                    split_on_prev_paragraph = True
            """
            split_on_all_caps_names = False
            
            
            # SPLIT ON ALL CAPS NAMES
            if (len(sents[-1]) == 3 and sents[-1][0] in slo_imena_upper and sents[-1][2] in slo_imena_upper and sents[-1][-1] not in ['.', '!', '?', ':', ';', ' ', ',', '«', '«']):
                split_on_next_paragraph = True
                split_on_all_caps_names = True
                #print("SLO IMENA UPPER", sents[-1])
            if('-' in sents[-1] and sents[-1][0] in slo_imena_upper):
                imena_ok = True
                for w in sents[-1]:
                    #print(w, not (w in slo_imena_upper or w==' ' or w=='-'))
                    if not (w in slo_imena_upper or w==' ' or w=='-'):
                        imena_ok = False
                        break
                if imena_ok:
                    split_on_next_paragraph = True
                    split_on_all_caps_names = True
                    #print("SLO IMENA UPPER", sents[-1])
            
                #print("appended2", words)
            
            # SPLIT ON ALL CAPS PARAGRAPH
            # VER MAJ - odstranjeno all caps, če ne gre za imena. Sedaj le izpis
            """
            if len(words) < 10:
                is_all_caps = True
                for w in words:
                    low_chars = [c for c in w if (c.islower() or c.isdigit())]
                    if low_chars != []:
                        is_all_caps = False
                        break;
                if is_all_caps:
                    #split_on_next_paragraph = True;
                    if not split_on_all_caps_names:
                        
                        with open('./ALL_CAPS_NASLOVI', 'a', encoding='utf-8') as acf:
                            print("".join(words), file=acf)
                            #print("ALL_CAPS_NASLOV: ", words)
            """           
            # Split on titles without commas followed by a location
            if (not split_on_prev_paragraph) and not (split_on_next_paragraph) and not (to_split):
            #if (not split_on_prev_paragraph) and not (split_on_next_paragraph):
                if ((words[-1] not in ['.',',', ':', ';', ')', '(']) or (words[-1] == '.' and words[-2] == '.' and words[-3] == '.')) and (len(" ".join(words)) <= 175) :
                    #print("Added " + " ".join(words))
                    candidate_titles.append(paragraph)
                    do_not_append_to_article = True
                else: 
                    # Fix nTirana
                    if words[0][0] =='n' and words[0][1:].isupper():
                        temp_word0 = words[0][1:]
                        #print("nTirana in ", filename)
                    else:
                        temp_word0 = words[0]
                    if ((temp_word0.isupper() and len(words) > 3 and  words[1] == ',' and words[3][:-1].isdigit()) 
                    or (temp_word0.isupper() and len(words) > 6 and words[1] == ',' and words[3].isupper() and words[4] == ',' and words[6][:-1].isdigit())
                    or (temp_word0.isupper() and words[1] == ' ' and words[2][0].isupper())
                    or (temp_word0.isupper() and words[1] == ' ' and words[2].isupper() and words[3] == ' ' and words[4][0].isupper())
                    or (temp_word0.isupper() and words[1] == ' ' and words[0] not in slo_imena_upper )):    
                        if candidate_titles != []:
                            #print('MULTI TITLE SPLIT', words[:3])
                            if (len(current_article) != 0):
                                split_articles.append(current_article)
                            current_article = []
                            for a in candidate_titles:
                                current_article.append(a)
                            
                            #exit()
                            current_article.append(paragraph)
                            article_lengths.append(curr_paragraph_words)
                            curr_paragraph_words = 0;
                            to_split = False
                            split_on_prev_paragraph = False
                            do_not_append_to_article = True
                            candidate_titles = []
                            
                    else:
                        for a in candidate_titles:
                            current_article.append(a)
                            #print("appended" + " ".join(get_words_from_paragraph(a)))
                        #current_article.append(paragraph)
                        #do_not_append_to_article = False
                        candidate_titles = []
            else: # If we are going to split, we need to add all the candidate titles first
                for a in candidate_titles:
                    current_article.append(a)
                if candidate_titles != []:
                    with open("./MULTI_LINE_TITLES.txt", 'a', encoding = 'utf-8') as mlf:
                        for ct in candidate_titles:
                            print("".join(get_words_from_paragraph(ct)), file=mlf)
                        print("-", file=mlf)
                        print("".join(get_words_from_paragraph(paragraph)), file=mlf)
                        print("-------------", file=mlf)
                        
                        print_candidate_titles_next_line = True
                        
                        #print("appended" + " ".join(get_words_from_paragraph(a)))
                candidate_titles = []
            # Avoid splitting short articles, probably a mistake in one of the rules
            if to_split and len(current_article) > 1:
                if print_candidate_titles_next_line == True:
                    """
                    with open("./MULTI_LINE_TITLES.txt", 'a', encoding = 'utf-8') as mlf:
                        print("".join(get_words_from_paragraph(paragraph)), file=mlf)
                        print("---------------", file=mlf)
                        print_candidate_titles_next_line = False
                    """
                split_articles.append(current_article)
                current_article = [paragraph]
                article_lengths.append(curr_paragraph_words)
                curr_paragraph_words = 0
            elif split_on_prev_paragraph and len(current_article) > 1:
                split_on_prev_paragraph = False;
                if len(split_articles) > 0:
                    paragraph_to_move = split_articles[-1][-1]
                    current_article.append(paragraph_to_move)
                    split_articles[-1] = split_articles[-1][:-1]
                split_articles.append(current_article)
                if print_candidate_titles_next_line == True:
                    """
                    with open("./MULTI_LINE_TITLES.txt", 'a', encoding = 'utf-8') as mlf:
                        print("".join(get_words_from_paragraph(paragraph)), file=mlf)
                        print("---------------", file=mlf)
                        print_candidate_titles_next_line = False
                    """
                current_article = [paragraph]
                article_lengths.append(curr_paragraph_words)
                curr_paragraph_words = 0
            else:
                if not do_not_append_to_article:
                    current_article.append(paragraph)
                    curr_paragraph_words += len(words_to_count)
                else:
                    do_not_append_to_article = False
                
            
        #print_split_articles(split_articles)
        split_articles.append(current_article)
        current_article = [paragraph]
        article_lengths.append(curr_paragraph_words)
        curr_paragraph_words = 0
    split_articles = merge_one_line_articles(split_articles);
    return split_articles, article_lengths
    

def merge_one_line_articles(split_articles):
    to_remove = []
    for i in range (len(split_articles)):
        if len(split_articles[i]) == 1 and i != len(split_articles)-1:
            split_articles[i+1].insert(0, split_articles[i][0])
            to_remove.append(i)
    return [split_articles[i] for i in range(len(split_articles)) if i not in to_remove]
            

 
   
def split_by_all_caps_location_first_word_with_lengths(filename):
    article_lengths = []
    split_articles = []
    curr_paragraph_words = 0
    with open(filename, 'r', encoding='utf-8') as f:
        tree = ET.parse(f)
        #print(tree)
        root = tree.getroot()
        text = root.find('{http://www.tei-c.org/ns/1.0}text')
        body = text.find('{http://www.tei-c.org/ns/1.0}body')
        #print(body)
        current_article = []
        for paragraph in body:
            words = get_words_from_paragraph(paragraph)
            words_to_count = [w for w in words if w != ' ']
            if len(words) == 0:
                continue
            if words[0].isupper() and len(words[0]) > 1:
                split_articles.append(current_article)
                current_article = [paragraph]
                article_lengths.append(curr_paragraph_words)
                curr_paragraph_words = 0
            else:
                current_article.append(paragraph)
                curr_paragraph_words += len(words_to_count)
        #print_split_articles(split_articles)
    return split_articles, article_lengths
    
    
def split_by_zero_length_paragraphs_2(filename, filename_out):
    split_articles = []
    article_lengths = []
    with open(filename, 'r', encoding='utf-8') as f:
        tree = ET.parse(f)
        #print(tree)
        root = tree.getroot()
        text = root.find('{http://www.tei-c.org/ns/1.0}text')
        body = text.find('{http://www.tei-c.org/ns/1.0}body')
        #print(body)
        current_article = []
        for paragraph in body:
            #print(paragraph)
            words = get_words_from_paragraph(paragraph)
            if len(words) ==0:
                split_articles.append(current_article)
                current_article = []
            else:
                current_article.append(paragraph)
    print_split_articles(split_articles, filename_out)
    
def just_check_num_paragraphs(filename):
    split_articles = []
    article_lengths = []
    with open(filename, 'r', encoding='utf-8') as f:
        tree = ET.parse(f)
        #print(tree)
        root = tree.getroot()
        text = root.find('{http://www.tei-c.org/ns/1.0}text')
        body = text.find('{http://www.tei-c.org/ns/1.0}body')
        #print(body)
        current_article = []
        for paragraph in body:
            
            words = get_words_from_paragraph(paragraph)
            words_to_count = [w for w in words if w != ' ']  
            if len(words_to_count) != 0:
                #print('zero-len-paragraph', words)
                split_articles.append([paragraph])
                article_lengths.append(len(words_to_count))

    return split_articles, article_lengths
    


"""

def segment_all_in_group_func(filename_list, segmentation_function):
    num_articles_vector = []
    article_length_vector = []
    article_titles = []
    for i, filename in enumerate(filename_list):
        if i % 500 == 0:
            print(i, len(filename_list))
        subdir = filename[:4]  
        path = os.path.join('./gigafida2', subdir, filename)
        with open(path, 'r', encoding='utf-8') as f:
            articles, article_lengths = check_length_zero_length_paragraphs(path)
            #print('opened', filename, len(articles))
            num_articles_vector.append(len(articles))
            average_article_length = np.mean(article_lengths)
            if np.isnan(average_article_length):
                average_article_length = 0
            article_length_vector.append(average_article_length)
            article_titles.append(os.path.join('./gigafida2', subdir, filename))

    return num_articles_vector, article_length_vector, article_titles
""" 
    
def segment_all_in_group_with_func(filename_list, func_to_segment_with, start=0, end=100000000000,limit=1000000000000):
    num_articles_vector = []
    article_length_vector = []
    article_titles = []
    all_articles = []
    for i, filename in enumerate(filename_list):
        if i % 100 == 0:
            print(i, len(filename_list))
        if i > limit or i > end:
            break
        if i < start:
            continue
        subdir = filename[:4]  
        # Modify filename for nondedup bersions
        filename = filename.split("-")[0] + ".xml"
        path = os.path.join('./gigafida_nondedup', subdir, filename)
        with open(path, 'r', encoding='utf-8') as f:
            articles, article_lengths = func_to_segment_with(path)
            #print('opened', filename, len(articles))
            num_articles_vector.append(len(articles))
            average_article_length = np.mean(article_lengths)
            if np.isnan(average_article_length):
                average_article_length = 0
            article_length_vector.append(average_article_length)
            article_titles.append(os.path.join('./gigafida_nondedup', subdir, filename))
            all_articles.append(articles)

    return all_articles, num_articles_vector, article_length_vector, article_titles
    
def segment_one_with_func(filename, func_to_segment_with):
    with open(filename, 'r', encoding='utf-8') as f:
        articles, article_lengths = func_to_segment_with(filename)
        #print('opened', filename, len(articles))
        
        print_split_articles(articles, "./outtest_testing_title_split.txt")

    return articles, article_lengths
    
    
def segment_all_in_group_delo(filename_list):
    num_articles_vector = []
    article_length_vector = []
    for filename in filename_list:
        subdir = filename[:4]  
        path = os.path.join('./gigafida2', subdir, filename)
        with open(path, 'r', encoding='utf-8') as f:
            articles, vector = split_by_location_minus(path)
            print('opened', filename, len(articles))
            num_articles_vector.append(len(articles))
    return num_articles_vector


def pick_most_average_articles_delo(num_articles, article_lengths, article_titles):
    avg_num_articles = np.mean(num_articles)
    avg_article_lengths = np.mean(article_lengths)
    print(len(num_articles))
    print(len(article_lengths))
    print(num_articles[0:5])
    #print(sorted(article_lengths)) 
    
    print(avg_article_lengths)
    #exit()
    num_articles_diff = [abs(avg_num_articles - x) for x in num_articles]
    article_lengths_diff = [abs(avg_article_lengths - x) for x in article_lengths]
    print(len(num_articles_diff))
    print(len(article_lengths_diff))
    #sorted_indices = np.argsort(num_articles_diff)
    sorted_indices = np.argsort(article_lengths_diff)
    print([article_lengths_diff[i] for i in sorted_indices])
    
    for i in range(10):
        print(article_lengths[sorted_indices[i]])
        article_to_segment = article_titles[sorted_indices[i]]
        ssplit_by_location_minus(article_to_segment, ".\\Delo\\"+ str(i) + "_" +article_to_segment.split("\\")[-1])


def pick_most_average_articles(articles, num_articles, article_lengths, article_titles, folder_name):
    avg_num_articles = np.mean(num_articles)
    avg_article_lengths = np.mean(article_lengths)
    print(len(num_articles))
    print(len(article_lengths))
    print(num_articles[0:5])
    #print(sorted(article_lengths)) 
    
    print(avg_article_lengths)
    #exit()
    num_articles_diff = [abs(avg_num_articles - x) for x in num_articles]
    article_lengths_diff = [abs(avg_article_lengths - x) for x in article_lengths]
    print(len(num_articles_diff))
    print(len(article_lengths_diff))
    #sorted_indices = np.argsort(num_articles_diff)
    sorted_indices = np.argsort(article_lengths_diff)
    print([article_lengths_diff[i] for i in sorted_indices])
    
    for i in range(len(sorted_indices)):
        if i % 50 == 0:
            print(i)
        article_to_segment = article_titles[sorted_indices[i]]
        print_split_articles(articles[sorted_indices[i]], ".\\"+folder_name+"\\"+ str(i) + "_" +article_to_segment.split("\\")[-1])
        print('done')
    print('done 2')
        #split_by_zero_length_paragraphs(article_to_segment, ".\\Novi tednik\\"+ str(i) + "_" +article_to_segment.split("\\")[-1])
        



slo_imena = read_names('./slo_imena.txt')
slo_priimki = read_names('./slo_priimki.txt')

slo_imena_upper = read_names_upper('./slo_imena.txt')
slo_priimki_upper = read_names_upper('./slo_priimki.txt')

slo_imena = slo_imena | slo_priimki
slo_imena_upper = slo_imena_upper | slo_priimki_upper


with open('filename_dict.txt', 'r', encoding='utf-8') as f:
    text = f.read()
    filename_dict = literal_eval(text)

with open('filename_counts.txt', 'r', encoding='utf-8') as f:
    text = f.read()
    counts_dict = literal_eval(text)
"""
similarity_scores, split_vector = get_sentsim_scores_gaps_max('./gigafida2/GF00/GF0000866-dedup.xml')
fig = plt.figure()
ax = fig.add_subplot(111)
colors=["#0000FF", "#00FF00"]
colors_vector = [colors[i] for i in split_vector]
#plt.plot(similarity_scores, color=colors_vector)
for i in range(len(similarity_scores)):
    ax.scatter(i, similarity_scores[i], color=colors_vector[i])
    #ax.scatter(i, similarity_scores[i], color="black")
plt.show()
exit()
"""

# Novi tednik
#articles, num_articles_vector, article_lengths, article_titles = segment_all_in_group_with_func(filename_dict['Novi tednik NT&amp;RC'], check_length_zero_length_paragraphs)
#pick_most_average_articles(articles, num_articles_vector, article_lengths, article_titles, "Novi tednik")

# Dnevnik
"""
for start in range(1500, 2300, 100):
    articles, num_articles_vector, article_lengths, article_titles = segment_all_in_group_with_func(filename_dict['Dnevnik'], split_by_all_caps_location_first_word_with_lengths, start = start, end=start+100)
    pick_most_average_articles(articles, num_articles_vector, article_lengths, article_titles, "Dnevnik")
    print('done 3')
print('done 4')
"""
# Delo
#for start in range(0, 10727, 500):
print("filename dict len", len(filename_dict['Dolenjski list']))
#exit()
"""
print("segmenting one")
segment_one_with_func("./gigafida_nondedup/GF09/GF0904780.xml", split_for_dnevnik)
print("done")
exit()
"""
for start in range(0, 2602, 100):
#or start in range(0, 50, 50):
    print(start)
    #articles, num_articles_vector, article_lengths, article_titles = segment_all_in_group_with_func(filename_dict['Delo'], split_for_delo, start=start, end=start+500)
    articles, num_articles_vector, article_lengths, article_titles = segment_all_in_group_with_func(filename_dict['Dnevnik'], split_for_dnevnik, start=start, end=start+100)
    pick_most_average_articles(articles, num_articles_vector, article_lengths, article_titles, "dnevnik_maj_final_test")
    

# Dolenjski list
#articles, num_articles_vector, article_lengths, article_titles = segment_all_in_group_with_func(filename_dict['Dolenjski list'], split_by_all_caps_location_first_word_with_lengths)
#pick_most_average_articles(articles, num_articles_vector, article_lengths, article_titles, "Dolenjski list")
exit()
num_articles_to_plot = [x for x in num_articles_vector if x < 50]
#sns.distplot(num_articles_to_plot)
#plt.show()
print(article_lengths)
print("Num articles", np.mean(num_articles_to_plot), "+-", np.std(num_articles_to_plot))
print("Article lengths", np.mean(article_lengths), "+-", np.std(article_lengths))

pick_most_average_articles(articles, num_articles_vector, article_lengths, article_titles)
with open('./Novi tednik NT_articles', 'w', encoding='utf-8') as f:
    print(Counter(num_articles_vector), file=f)
exit()
#sorted_groups = sorted(counts_dict.items(), key=operator.itemgetter(1), reverse=True)
#print(sorted_groups)

"""
#split_by_short_paragraphs('./gigafida/F0000002.xml')
#split_by_initials('./gigafida/F0000060.xml')
similarity_scores = get_sentsim_scores('./gigafida2/GF00/GF0000866-dedup.xml')



split_vector = split_by_all_caps_location_first_word('./gigafida2/GF00/GF0000866-dedup.xml')
#plt.plot(split_vector, 'o', color='red')
colors=["#0000FF", "#00FF00"]
colors_vector = [colors[i] for i in split_vector]
fig = plt.figure()
ax = fig.add_subplot(111)
#plt.plot(similarity_scores, color=colors_vector)
for i in range(len(similarity_scores)):
    ax.scatter(i, similarity_scores[i], color=colors_vector[i])
plt.show()
#split_by_all_caps_location('./gigafida/F0000005.xml')
#split_by_simple_paragraphs('./gigafida/F0000059.xml')
"""


## DELO: Split včasih po minusih, včasih to ne gre (2951)
## Novi tednik - večinoma že segmentirano
## Dnevnik: Split po all caps lokaciji (+ imena avtorjev iz non-dup)
## Dolenjski list: Split po all caps lokaciji (+ imena avtorjev iz non-dup)
