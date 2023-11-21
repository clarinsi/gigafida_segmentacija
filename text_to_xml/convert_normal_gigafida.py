import os
from lxml import etree as ET
import re
import copy

def get_already_processed():
    already_processed = []
    FOLDERS = ["./segmentacija_dnevnik_vse",
               "./delo-popravki/delo-popravki/delo-nepregledano",
               "./delo-popravki/delo-popravki/delo-nepregledano",
               "./delo-popravki/delo-popravki/segmentacija-pregled-OK-ni-popravkov",
               "./delo-popravki/delo-popravki/segmentacija-pregled-verzija1",
               "./delo-popravki/delo-popravki/segmentacija-pregled-verzija1-original",
               "./delo-popravki/delo-popravki/segmentacija-pregled-verzija2"]
               
               
    for folder in FOLDERS:
        files = os.listdir(folder)
        for f in files:
            if "_" in f:
                f = f.split("_")[1]
            if "." in f:
                f = f.split(".")[0]
            if "-" in f:
                f = f.split("-")[0]
            #print(f)
            already_processed.append(f)
    return already_processed
        
already_processed = set(get_already_processed())

base_gigafida_folder = "./gigafida_nondedup/"


def parse_sent(e):
    words = ""
    for word in e:
        #print(word, word.text)
        words += word.text
    return words
        

def update_file(filename, outfilename):
    with open("./temp_file_for_full_gigafida.txt", 'w', encoding = 'utf-8') as tempoutf:
        with open(filename, 'r', encoding='utf-8') as inf:
            for line in inf:
                if '<body>' in line:
                    break
                print(line[:-1], file=tempoutf)
        print('</text>', file=tempoutf)
        print('</TEI>', file=tempoutf)
    #exit()
        
    tree = ET.parse("./temp_file_for_full_gigafida.txt")
    root = tree.getroot()
    for edition in root.iter('{http://www.tei-c.org/ns/1.0}edition'):
        edition.text = '2.2'
    for date in root.iter('{http://www.tei-c.org/ns/1.0}date'):
        if date.getparent().tag == "{http://www.tei-c.org/ns/1.0}publicationStmt":
            date.text = "??TO-ADD??"
    for encodingDesc in root.iter('{http://www.tei-c.org/ns/1.0}encodingDesc'):
        #print("Found encoding desc")
        encodingDesc.getparent().remove(encodingDesc)
        
    for appinfo in root.iter('{http://www.tei-c.org/ns/1.0}appInfo'):
        
        print("Found appinfo")
        application = ET.SubElement(appinfo, '{http://www.tei-c.org/ns/1.0}application', attrib={'ident':"??TO-ADD??", 'version':"1.0"})
        desc = ET.SubElement(application, '{http://www.tei-c.org/ns/1.0}desc', attrib={'lang':'sl'})
        desc.text = '<ref target="??TO-ADD??">??TO-ADD??</ref> je bil uporabljem za segmentacijo besedil.'
        desc = ET.SubElement(application, '{http://www.tei-c.org/ns/1.0}desc', attrib={'lang':'en'})
        desc.text = '<ref target="??TO-ADD??">??TO-ADD??</ref> was used for text segmentation.'
        
        application = ET.SubElement(appinfo, '{http://www.tei-c.org/ns/1.0}application', attrib={'ident':"??TO-ADD??", 'version':"1.0"})
        desc = ET.SubElement(application, '{http://www.tei-c.org/ns/1.0}desc', attrib={'lang':'sl'})
        desc.text = '<ref target="??TO-ADD??">"??TO-ADD??"</ref> je bil uporabljem za avtomatsko pripisovanje tematskih kategorij.'
        desc = ET.SubElement(application, '{http://www.tei-c.org/ns/1.0}desc', attrib={'lang':'en'})
        desc.text = '<ref target="??TO-ADD??">"??TO-ADD??"</ref> was used for automatic topic categorisation.'
        
    for textClass in root.iter('{http://www.tei-c.org/ns/1.0}textClass'):
        #print("Found textClass")
        catref = ET.SubElement(textClass, '{http://www.tei-c.org/ns/1.0}catRef', attrib={'target':"topic:??TO-ADD??"})
        catref = ET.SubElement(textClass, '{http://www.tei-c.org/ns/1.0}catRef', attrib={'target':"segment:none"})
    
    for change in root.iter('{http://www.tei-c.org/ns/1.0}change'):
    #print("Found change")
        change.attrib["when"] = "??TO-ADD??"
        
   
    text = root.find('{http://www.tei-c.org/ns/1.0}text')
    for e in text:
        if e.tag == "{http://www.tei-c.org/ns/1.0}fs":
                for child in e:
                    if child.attrib['name'] == 'neardup':
                        child.getparent().remove(child)
    
    
   
    
    tree.write(outfilename, pretty_print=True, encoding='utf-8')
    
    
    
    lines = []
    with open(outfilename, 'r', encoding='utf-8') as f:
        lines = f.readlines()
        lines = lines[:-1]
    with open(outfilename, 'w', encoding='utf-8') as f:
        for line in lines:
            if line != "</text>\n":
                print(re.sub('gt;', '>', re.sub('&lt;', '<', line[:-1])), file=f)
    tree2 = ET.parse(filename)
    root2 = tree2.getroot()
    text2 = root2.find('{http://www.tei-c.org/ns/1.0}text')
    body2 = text2.find('{http://www.tei-c.org/ns/1.0}body')
    with open(outfilename, 'a', encoding='utf-8') as outf:
        print("<body>", file=outf)
        for paragraph in body2:
            par_text = ""
            #print(paragraph.attrib.keys())
            print('<p xml:id="' + paragraph.attrib['{http://www.w3.org/XML/1998/namespace}id'] +'">', file=outf)
            for e in paragraph:
                
                if e.tag == "{http://www.tei-c.org/ns/1.0}fs":
                    print('<fs>', file=outf)
                    for child in e:
                        if child.attrib['name'] != 'neardup':
                            print('<f name="' + child.attrib['name']+'">'+child.text+'</f>', file=outf) 
                    print('</fs>', file=outf)
                    
                if e.tag == "{http://www.tei-c.org/ns/1.0}s":
                    words = parse_sent(e)
                    par_text += words
                    e.getparent().remove(e)
                
            print(par_text, file=outf)
            print("</p>", file=outf)
            paragraph.text = par_text
        print('</body>', file=outf)
        print('</text>', file=outf)
        print('</TEI>', file=outf)
    
    
    
    
    

                        
        
    
    

for i in range(0, 1):
    if i < 10:
        current_folder = os.path.join(base_gigafida_folder, 'GF'+'0'+str(i))
        current_out_folder = os.path.join("./ver4_nonsegmented", 'GF'+'0'+str(i))
    else:
        current_folder = os.path.join(base_gigafida_folder, 'GF'+str(i))
        current_out_folder = os.path.join("./ver4_nonsegmented", 'GF'+str(i))
    #print(current_folder)
    files = os.listdir(current_folder)
    for f in files:
        #print(already_processed, f)
        if f.split('.')[0] in already_processed and os.path.isfile(os.path.join(current_out_folder, f)):
            os.remove(os.path.join(current_out_folder, f))
        if f.split('.')[0] not in already_processed:
            if not os.path.isfile(os.path.join(current_out_folder, f)):
               print(f) 
               update_file(os.path.join(current_folder, f), os.path.join(current_out_folder, f))
            #exit()

                