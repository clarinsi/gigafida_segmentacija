import os
from  lxml import etree as ET
import re
    
TEI_P = '{http://www.w3.org/XML/1998/namespace}'
TEI_BODY_P = '{http://www.tei-c.org/ns/1.0}'



def change_header_part(tree, original_filename):
    part = original_filename.split('-')[1].split('.')[0]
    base_out_filename = out_folder+filename[:4]+'/'+original_filename

    root = tree.getroot()
    new_part = root.attrib[TEI_P+'id'].split('-')[0]+'-'+part
    root.attrib[TEI_P+'id'] = new_part
    print("a", "missing" in original_filename)
    if "missing" in original_filename:
        is_auto = "automatic"
    else:
        is_auto = "manual"
        
    for textClass in root.iter('{http://www.tei-c.org/ns/1.0}textClass'):
        #print("Found textClass")
        for subclass in textClass:
            #print(subclass.attrib.keys())
            if 'target' in subclass.attrib.keys():
                #print(subclass.attrib)
                #exit()
                if 'segment' in subclass.attrib['target']:
                    subclass.attrib['target']="segment:"+is_auto
                    
                   # exit()
    for pubStmt in root.iter('{http://www.tei-c.org/ns/1.0}publicationStmt'):
        for idno in pubStmt.iter('{http://www.tei-c.org/ns/1.0}idno'):
            if idno.attrib['type'] == 'GIGAFIDA':
                idno.text = new_part
    for text in root.iter('{http://www.tei-c.org/ns/1.0}text'):
    #print(text.attrib)
        text.attrib['{http://www.w3.org/XML/1998/namespace}id']= new_part+'.'
    tree.write(base_out_filename, pretty_print=True, encoding='utf-8')
    lines = []
    with open(base_out_filename, 'r', encoding='utf-8') as f:
        lines = f.readlines()
        lines = lines[:-1]
    with open(base_out_filename, 'w', encoding='utf-8') as f:
        for line in lines:
            print(re.sub('gt;', '>', re.sub('&lt;', '<', line[:-1])), file=f)

    
    
def upgrade_header(original_filename, tree):
    print("upgrading header")
    #GF0000866-1.xml
    if len(original_filename.split('-')) == 2:
        part = original_filename.split('-')[1].split('.')[0]
        base_filename = original_filename.split('-')[0]
        folder = base_filename[0:4]
    elif "dedup" not in original_filename:
        part = original_filename.split('-')[2].split('.')[0]
        base_filename = original_filename.split('-')[0]
        folder = base_filename[0:4]
    else:
        part = original_filename.split('-')[3].split('.')[0]
        base_filename = original_filename.split('-')[0]
        folder = base_filename[0:4]
    print(original_filename)
    print("a", "missing" in original_filename)
    if "missing" in original_filename:
        is_auto = "automatic"
    else:
        is_auto = "manual"
    
    print(part, base_filename, folder)
    #exit()
    
    base_out_filename =out_folder+filename[:4]+'/'+original_filename
    print(base_out_filename)
    #exit()
    #print(part)
    part = str(part)
    
    root = tree.getroot()
    #print(root.attrib)
    root.attrib[TEI_P+'id'] = root.attrib[TEI_P+'id']+'-'+part
    #print(root.attrib)
    #for child in root:
        #print(child)
    for edition in root.iter('{http://www.tei-c.org/ns/1.0}edition'):
        edition.text = '2.2'
        #print(edition.text)
    
    #print("1")
    for measure in root.iter('{http://www.tei-c.org/ns/1.0}measure'):
        measure.attrib['quantity'] = '??TO-ADD??'
        measure.text = '??TO-ADD?? besed'
        #print(measure.attrib, measure.text)
    
    for date in root.iter('{http://www.tei-c.org/ns/1.0}date'):
        if date.getparent().tag == "{http://www.tei-c.org/ns/1.0}publicationStmt":
            date.text = '??TO-ADD??'
        #print(date.text)
        
    for encodingDesc in root.iter('{http://www.tei-c.org/ns/1.0}encodingDesc'):
        #print("Found encoding desc")
        encodingDesc.getparent().remove(encodingDesc)
        """
        projectDesc = ET.Element('{http://www.tei-c.org/ns/1.0}projectDesc')
        encodingDesc.insert(2,projectDesc)
        e = ET.SubElement(projectDesc, '{http://www.tei-c.org/ns/1.0}p', attrib={'lang':'sl'})
        e.text = 'Projekt "<ref target="https://slokit.ijs.si/">Nadgradnja CLARIN.SI: Korpusni informator in besedilni analizator</ref>".'
        e = ET.SubElement(projectDesc, '{http://www.tei-c.org/ns/1.0}p', attrib={'lang':'en'})
        e.text = 'Project "<ref target="https://slokit.ijs.si/">Upgrading CLARIN.SI: Corpus summariser and text analyser</ref>".'
        """
        
    for appinfo in root.iter('{http://www.tei-c.org/ns/1.0}appInfo'):
        #print("Found appinfo")
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
        catref = ET.SubElement(textClass, '{http://www.tei-c.org/ns/1.0}catRef', attrib={'target':"segment:"+is_auto})
        
    for change in root.iter('{http://www.tei-c.org/ns/1.0}change'):
        #print("Found change")
        change.attrib["when"] = "??TO-ADD??"
    
    for pubStmt in root.iter('{http://www.tei-c.org/ns/1.0}publicationStmt'):
        for idno in pubStmt.iter('{http://www.tei-c.org/ns/1.0}idno'):
            if idno.attrib['type'] == 'GIGAFIDA':
                idno.text = idno.text+'-'+part
            #print(idno.text)
    #print("2")
    for text in root.iter('{http://www.tei-c.org/ns/1.0}text'):
        #print(text.attrib)
        text.getparent().remove(text)
        #text.attrib['{http://www.w3.org/XML/1998/namespace}id']= text.attrib['{http://www.w3.org/XML/1998/namespace}id'][:-1]+'-'+part+'.'
    #print("21")    
    for body in root.iter('{http://www.tei-c.org/ns/1.0}body'):
        #test = ET.Element("a")
        #body.getparent().replace(body, test)
        body.getparent().clear(body)
    #print("22")
    #tree_str = ET.tostring(tree, pretty_print=True, encoding='utf-8')
    #print(tree_str)
    #with open(base_out_filename, 'w', encoding='utf-8') as outf:
    #    print(tree_str, file=outf)
    #print("23")
    tree.write(base_out_filename, pretty_print=True, encoding='utf-8')
    lines = []
    #print("222")
    with open(base_out_filename, 'r', encoding='utf-8') as f:
        lines = f.readlines()
        lines = lines[:-1]
    with open(base_out_filename, 'w', encoding='utf-8') as f:
        for line in lines:
            print(re.sub('gt;', '>', re.sub('&lt;', '<', line[:-1])), file=f)
    #print("3")
"""   
def insert_missing_words(paragraphs, gigafida):
    new_paragraphs = []
    current_par_to_append = ""
    current_paragraph_i = 0
    current_word_i = 0
    for gf_sent in gigafida:
        if gf_sent == ' ':
            new_paragraphs.append(current_par_to_append)
        if gf_sent != paragraphs[current_paragraph_i][current_word_i]:
            current_par_to_append += gf_sent
        else:
            current_word_i += 1
            if current_word_i >= len(
            
"""


def new_words_to_pars(new_words):
    #print(new_words)
    pars = " ".join(new_words).split('<par> ')
    #print(pars)
    to_ret = [p.replace('<par>', "") for p in pars if p != '']
    if len(to_ret) > 0 and to_ret[0] == '':
        to_ret = to_ret[1:]
    return [p.replace('<par>', "") for p in pars if p != '']

def insert_missing_words(paragraphs, gigafida_text):
    gf_word_index = 0
    gigafida_text = gigafida_text.replace("<par>", "<par> ")
    new_words = []
    gf_words = gigafida_text.split(" ")
    with open(".temt.txt", "w", encoding="utf-8") as temt:
        for i, paragraphs_text in enumerate(paragraphs):
            pw_index = 0
            while True:
                paragraphs_words = paragraphs_text.split(" ")
                
                
                if pw_index >= len(paragraphs_words):
                    break
                if gf_word_index >= len(gf_words):
                    break
                #print(gf_words[gf_word_index].replace("<par>", ""), paragraphs_words[pw_index], i, file=temt)
                if gf_words[gf_word_index].replace("<par>", "") != paragraphs_words[pw_index]:
                    new_words.append((gf_words[gf_word_index], i))
                    #print((gf_words[gf_word_index], i))
                    gf_word_index += 1
                else:
                   # new_words.append(paragraphs_words[pw_index])
                    pw_index += 1
                    gf_word_index += 1
                
        #print(new_words)
        #print(" ".join(new_words))
        #print("---")
        #print(gigafida_text)
        for i2 in range(len(paragraphs)):
            just_words = [w[0] for w in new_words if w[1] == i2]
            #print(just_words)
            #print(" ".join(just_words) in gigafida_text)
            if len(just_words) > 0 and just_words != ['']:
                gigafida_text = gigafida_text.replace(" ".join(just_words), "")
                gigafida_text = gigafida_text.replace("  ", "")
                gigafida_text = gigafida_text.replace("  ", "")
                gigafida_text = gigafida_text.replace("  ", "")
                gigafida_text = gigafida_text.replace("  ", "")
                #with open(".temt3.txt", "a", encoding="utf-8") as temt:
                #    print("w", just_words, file=temt)
        
        new_new_words = merge_new_words(new_words)
        #print(new_new_words)
        #exit()
    extra_stuff_to_print = []
    keys_to_insert = sorted(list(new_new_words.keys()), reverse=True)
    for k in keys_to_insert:
        
        if len(new_words_to_pars(new_new_words[k])) != 0:
            extra_stuff_to_print.append(new_words_to_pars(new_new_words[k]))
                #print("k", new_words_to_pars(new_new_words[k]))
        """
        else:
            #if len(new_new_words[k]) > 100:
            #    pass
            #else:
            for p in reversed(new_words_to_pars(new_new_words[k])):
                #print(p)
                paragraphs.insert(k, p)
        """
    #exit()
    return(paragraphs, gigafida_text, extra_stuff_to_print)
    
                
def merge_new_words(new_words):
    new_new_words = {}
    for w, i in new_words:
        if i not in new_new_words.keys():
            new_new_words[i] = [w]
        else:
            new_new_words[i].append(w)
    return new_new_words

def is_next_part_a_sent(e):
    if e.tag == "{http://www.tei-c.org/ns/1.0}s":
        return True
    else:
        return False
        
def is_next_part_a_paragraph(e):
    if e.tag == "{http://www.tei-c.org/ns/1.0}p":
        return True
    else:
        return False
        
def get_sent_text(e):
    words = []
    
    for w in e:
        #print(w)
        if w.tag == '{http://www.tei-c.org/ns/1.0}w' or w.tag == '{http://www.tei-c.org/ns/1.0}c' or w.tag == '{http://www.tei-c.org/ns/1.0}pc':
            words.append(w.text)
    return words

def parse_gigafida(gigafida_file):
    all_sents = []
    parsed_gigafida = []
    first_par = True
    with open(gigafida_file, 'r', encoding='utf-8') as f:
        tree = ET.parse(f)
        root = tree.getroot()
        text = root.find('{http://www.tei-c.org/ns/1.0}text')
        body = text.find('{http://www.tei-c.org/ns/1.0}body')
        for paragraph in body:
            parsed_gigafida.append(paragraph)
            for e in paragraph:
                parsed_gigafida.append(e)
    for e in parsed_gigafida:
        if is_next_part_a_sent(e):
            all_sents.append("".join(get_sent_text(e)))
        if first_par:
            first_par = False
        else:
            if is_next_part_a_paragraph(e):
                all_sents.append("<par>")
    return all_sents


def print_paragraphs(all_paragraphs, curr_paragraph_num, outf):
    outf_name = outf.name.split('/')[-1].split('.')[0]
    for paragraph in all_paragraphs:
        print('<p xml:id="'+outf_name+'.'+str(curr_paragraph_num)+'">', file=outf)
        curr_paragraph_num += 1
        if len(paragraph) == 0:
            continue
        if paragraph[0] == ' ':
            paragraph = paragraph[1:]
        print(paragraph, file=outf)
        print('</p>', file=outf)
    return curr_paragraph_num





folder = './ver3_delo_dedup_nondedup_midway/'
out_folder = './ver3_delo_dedup_nondedup_with_headers/'
trees = {}
#swapped remove at GF1105198-1.xml
parser = ET.XMLParser(remove_blank_text=True)
already_skipped_1 = False
for filename in os.listdir(folder):
    print(filename)
    #if filename != 'GF1105198-1.xml' and not already_skipped_1:
    #    continue
    #already_skipped_1 = True
    
    base = filename.split('-')[0]
    #if base in skipped_files:
    #    continue
    in_full_filename = folder+filename
    full_out_filename = out_folder+filename[:4]+'/'+filename
    
    if base in trees.keys():
        #print('in true')
        tree = trees[base]
        change_header_part(tree, filename)
    else:
        #print('in else')
        gf = filename[0:4]
        gigafida_filename= './gigafida_nondedup/'+gf+'/'+base+'.xml'
        #print("parsing")
        with open(gigafida_filename, 'r', encoding='utf-8') as f:
            nonbody_lines = []
            for line in f:
                if '<body>' not in line:
                    #print(line)
                    nonbody_lines.append(line)
                else:
                    break
            nonbody_lines.append('<body>\n')
            nonbody_lines.append('</body>\n')
            nonbody_lines.append('</text>\n')
            nonbody_lines.append('</TEI>\n')
            nonbody_xml = "".join(nonbody_lines)
            with open('./temp_header_file.xml', 'w', encoding='utf-8') as tempf: 
                print(nonbody_xml, file=tempf)
            t = ET.parse('./temp_header_file.xml', parser)
        #print("done parsing")
        trees[base] = t
        tree = trees[base]
        print("upgrading header", filename)
        upgrade_header(filename, tree)
        #print("done header")
    lines = []
    with open(in_full_filename, 'r', encoding='utf-8') as inf:
        lines = inf.readlines()
    with open(full_out_filename, 'a', encoding='utf-8') as outf:
        print('<text>', file=outf)
        print('<body>', file=outf)
        for line in lines:
            print(line[:-1], file=outf)
        print('</body>', file=outf)
        print('</text>', file=outf)
        print('</TEI>', file=outf)
    #print('ok')
    #exit()

#filename = "0_GF0356009.xml"
#upgrade_header('GF0000866-1.xml')
exit()




mpty_segment = False
after_empty_segment = False
start_printing=False
#segmented_folder = './Delo-popravki/Delo-popravki/Delo-nepregledano/'
segmented_folder = './Delo-popravki/Delo-popravki/segmentacija-pregled-verzija1/'
files_in_segmented_folder = os.listdir(segmented_folder)
already_skipped = False
for filename in files_in_segmented_folder:
    print(filename)
    #if 'GF1023760-dedup-Anja.xml' not in filename:
    #    continue
    #filename = "50_GF7278125.xml"
    segmented_filename = segmented_folder+filename
    base_filename = filename.split("_")[1]
    folder = base_filename[0:4]
    gigafida_filename= './gigafida_nondedup/'+folder+'/'+base_filename.split('-')[0]+'.xml'
    lines_in_curr_segment = []
    current_segment = 1
    base_out_filename = "./ver3_delo_dedup_nondedup_midway/"+base_filename
    parsed_gigafida = "".join(parse_gigafida(gigafida_filename))
    
    parsed_gigafida_og = parse_gigafida(gigafida_filename)
    print('a')
    #with open(".temt2.txt", "w", encoding="utf-8") as temt:
    #    print(parsed_gigafida, file=temt)
    #exit()
    curr_paragraph = []
    all_paragraphs = []
    curr_paragraph_num = 1
    with open(segmented_filename, "r", encoding="utf-8") as segmented_file:
        
        for i, line in enumerate(segmented_file):
            # First line is always ----------------- so just skip it
            if i == 0:
                continue
            if line[:5] == "-----":
                #print("--------------")
                curr_filename = "."+"".join(base_out_filename.split(".")[:-1]) + '-' + str(current_segment) + ".xml"
                
                #print('-------------')               
                #print(parsed_gigafida)
                #print(" ".join(all_paragraphs) in parsed_gigafida)
                #print(" ".join(all_paragraphs) in parsed_gigafida)
                if " ".join(all_paragraphs) in parsed_gigafida.replace("<par>", " ").replace("  ", " "):
                    #print("Replaced", " ".join(all_paragraphs))
                    parsed_gigafida = parsed_gigafida.replace(" ".join(all_paragraphs), "")
                #if False:
                #    pass
                else:
                    #print(curr_filename)
                    with open(".temt2.txt", "w", encoding="utf-8") as temt:
                        #print(" ".join(all_paragraphs), file=temt)
                        #print("-----", file=temt)
                        #print(parsed_gigafida, file=temt)
                        all_paragraphs, parsed_gigafida, extra_stuff_to_print = insert_missing_words(all_paragraphs, parsed_gigafida)   
                        for s in extra_stuff_to_print:
                            curr_filename = "."+"".join(base_out_filename.split(".")[:-1]) + '-' + str(current_segment) + "-missing.xml"
                            with open(curr_filename, "w", encoding="utf-8") as outf:
                                 curr_paragraph_num = print_paragraphs(s, curr_paragraph_num, outf)
                                 current_segment += 1
                                 curr_filename = "."+"".join(base_out_filename.split(".")[:-1]) + '-' + str(current_segment) + ".xml"
                        #print(" ".join(all_paragraphs) in parsed_gigafida.replace("<par>", ""))
                        #print(" ".join(all_paragraphs), file=temt)
                        #print("---", file=temt)
                        #print(parsed_gigafida.replace("<par>", " ").replace("  ", " "), file=temt)
                        #exit()
                        #exit()
                        #parsed_gigafida = parsed_gigafida.replace(" ".join(all_paragraphs), "")
                        
                #exit()
                #print(all_paragraphs)
                with open(curr_filename, "w", encoding="utf-8") as outf:
                    curr_paragraph_num = print_paragraphs(all_paragraphs, curr_paragraph_num, outf)
                    all_paragraphs = []
                    current_segment += 1
                    
            else:
                all_paragraphs.append(line[:-1])
    #exit()
        
        
exit()

