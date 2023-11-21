import xml.etree.ElementTree as ET
import os
from collections import Counter


def get_source(filename):
    print('opening' ,filename)
    with open(filename, 'r', encoding='utf-8') as f:
        tree = ET.parse(f)
        #print(tree)
        root = tree.getroot()
        header = root.find('{http://www.tei-c.org/ns/1.0}teiHeader')
        filedesc = header.find('{http://www.tei-c.org/ns/1.0}fileDesc')
        titleStmt = filedesc.find('{http://www.tei-c.org/ns/1.0}titleStmt')
        title = filedesc.find('{http://www.tei-c.org/ns/1.0}title')
        for t in titleStmt:
            if t.tag == '{http://www.tei-c.org/ns/1.0}title':
                return " ".join(t.text.split(": ")[1:]).split("(")[0]
    
def get_source_search(filename):
    print('opening' ,filename)
    with open(filename, 'r', encoding='utf-8') as f:
        for line in f:
            if line.find("<title>") != -1:
                return line.split(">")[1].split("<")[0].split(" (")[0]

def count_sources(folder):
    sources = []
    filenames_dict = {}
    for subfolder in os.listdir(folder):
        for filename in os.listdir(os.path.join(folder, subfolder)):
            #print(filename)

            source = get_source_search(os.path.join(folder, subfolder, filename))
            #print(source)
            sources.append(source)
            if source not in filenames_dict.keys():
                filenames_dict[source] = [filename]
            else:
                filenames_dict[source].append(filename)
    return sources, filenames_dict

def get_words_in_paragraph(paragraph):
    total_words = 0
    for sent in paragraph:
        total_words += len(sent)
    return total_words
    
def join_text(paragraphs):
    joined_text = []
    for paragraph in paragraphs:
        for sent in paragraph:
            for word in sent:
                joined_text.append(word)
    return " ".join(joined_text)


def split_on_short_paragraphs(text):
    split_text = []
    curr_paragraphs = []
    for paragraph in text:
        paragraph_len = get_words_in_paragraph(paragraph)
        if paragraph_len < 10:
            split_text.append(curr_paragraphs)
            split_text.append([paragraph])
            curr_paragraphs = []
        else:
            curr_paragraphs.append(paragraph)
    return split_text
    
    
sources, filenames_dict = count_sources('./gigafida2/')
with open('filename_counts.txt', 'w', encoding='utf-8') as f:
    print(Counter(sources), file=f)
with open('filename_dict.txt', 'w', encoding='utf-8') as f:
    print(filenames_dict, file=f)
exit()    

with open('./gigafida2/GF00/GF0000290-dedup.xml', 'r', encoding='utf-8') as f:

        
    exit()
    
    
    
    
    for c in root:
        print(c.tag)
        if c.tag == '{http://www.tei-c.org/ns/1.0}text':
            for body in c:
                curr_text = []
                for paragraph in body:
                    curr_paragraph = []
                    for sent in paragraph:
                        curr_sent = []
                        for word in sent:
                            if word.tag[-1] != 'S':
                                curr_sent.append(word.text)
                        curr_paragraph.append(curr_sent)
                    curr_text.append(curr_paragraph)
    split_pars = split_on_short_paragraphs(curr_text)
    with open('tempout.txt', 'w', encoding='utf-8') as outf:
        for p in split_pars:
            print(join_text(p), file=outf)
            print('-------------------------------------', file=outf)
    
    #print(curr_text)
    #for paragraph in curr_text:
    #    print(len(paragraph), get_words_in_paragraph(paragraph))
    #text = root.find("text")
    #print(join_text(curr_text))
    #print(text)
