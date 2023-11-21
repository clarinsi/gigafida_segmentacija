from  lxml import etree as ET
import os
import re
import copy

TEI_P = '{http://www.w3.org/XML/1998/namespace}'
TEI_BODY_P = '{http://www.tei-c.org/ns/1.0}'

def get_source_filename(segmented_filename):
    base_filename = segmented_filename.split("_")[1]
    folder = base_filename[0:4]
    complete_filename = './gigafida_nondedup/'+folder+'/'+base_filename
    return complete_filename


def change_header_part(tree, original_filename):
    part = original_filename.split('-')[1].split('.')[0]
    base_out_filename = out_folder+original_filename

    root = tree.getroot()
    new_part = root.attrib[TEI_P+'id'].split('-')[0]+'-'+part
    root.attrib[TEI_P+'id'] = new_part
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
    #GF0000866-1.xml
    part = original_filename.split('-')[1].split('.')[0]
    base_filename = original_filename.split('-')[0]
    folder = base_filename[0:4]
    
    base_out_filename = out_folder+original_filename
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
        catref = ET.SubElement(textClass, '{http://www.tei-c.org/ns/1.0}catRef', attrib={'target':"segment:manual"})
        
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
    
    
def parse_gigafida(gigafida_file):
    parsed_gigafida = []
    with open(gigafida_file, 'r', encoding='utf-8') as f:
        tree = ET.parse(f)
        root = tree.getroot()
        text = root.find('{http://www.tei-c.org/ns/1.0}text')
        body = text.find('{http://www.tei-c.org/ns/1.0}body')
        for paragraph in body:
            parsed_gigafida.append(paragraph)
            for e in paragraph:
                parsed_gigafida.append(e)
    return parsed_gigafida
    
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
    
    
def print_fs(e, outf):
    if e.tag != "{http://www.tei-c.org/ns/1.0}fs":
        print("ERROR: expected fs when printing fs xml")
        raise TypeError
    print('<fs>', file=outf)
    for child in e:
        if child.attrib['name'] != 'neardup':
            print('<f name="' + child.attrib['name']+'">'+child.text+'</f>', file=outf) 
    print('</fs>', file=outf)
    
def print_sent_xml(e, outf, part):
        if e.tag != "{http://www.tei-c.org/ns/1.0}s":
            print("ERROR: expected s when printing sentence xml")
        else:
            gf_to_write = e.attrib['{http://www.w3.org/XML/1998/namespace}id']
            gfs = gf_to_write.split('.')
            gfs[0]=gfs[0] + '-' + str(part)
            gf_to_write = '.'.join(gfs)
            print('<s xml:id="' + gf_to_write+'">'  , file=outf)  
            
            
            
            

    
    
def merge_lines_with_gigafida_paragraphs_empty_segment(lines, parsed_gigafida, outf, part):
    print(lines)
    first_paragraph = True
    segments_to_insert = []
    last_popped_paragraph = None
    sents_to_print_new = []
    #print(lines)
    for line in lines:
        line = line[:-1]
        #print("l",line)
        line_already_printed = False
        while True:
            e = parsed_gigafida[0]
            #print(e)
            if is_next_part_a_sent(e):
                #print_sent_xml(e, outf, part)
                sents_to_print_new.append("".join(get_sent_text(e)))
                #print('</s>', file=outf)
                if line == "".join(get_sent_text(e)):
                    parsed_gigafida.pop(0)
                    break
                else:
                    print("mismatch in skipped paragraph")
                    print(line)
                    print("".join(get_sent_text(e)))
                    raise TypeError
            elif not is_next_part_a_paragraph(e):
                #should be fs
                #print(e, file=outf)           
                print_fs(e, outf)
                parsed_gigafida.pop(0)
            else:
                #print(merged_sents_from_xml, file=outf)
                if first_paragraph:
                    gf_to_write = e.attrib["{http://www.w3.org/XML/1998/namespace}id"]
                    gfs = gf_to_write.split('.')
                    gfs[0]=gfs[0] + '-' + str(part)
                    gf_to_write = '.'.join(gfs)
                    print('<p xml:id="' + gf_to_write +'">', file=outf)
                    last_popped_paragraph = parsed_gigafida.pop(0)
                    first_paragraph = False
                else:
                    #print(ET.tostring(e, pretty_print=True), file=outf)
                    #print(e.attrib)
                    print("".join(sents_to_print_new), file=outf)
                    sents_to_print_new = []
                    print("</p>", file=outf)
                    gf_to_write = e.attrib["{http://www.w3.org/XML/1998/namespace}id"]
                    gfs = gf_to_write.split('.')
                    gfs[0]=gfs[0] + '-' + str(part)
                    gf_to_write = '.'.join(gfs)
                    print('<p xml:id="' + gf_to_write +'">', file=outf)
                    last_popped_paragraph =  parsed_gigafida.pop(0)
                    break
    print("</p>", file=outf)
    return parsed_gigafida


def print_empty_segment_at_end(parsed_gigafida, outf, part):
    first_paragraph = True
    sents_to_print_new = []
    while True:
       if len(parsed_gigafida) == 0:
           print("".join(sents_to_print_new), file=outf)
           sents_to_print_new = []
           print("</p>", file=outf)
           return parsed_gigafida
       e = parsed_gigafida[0]
       if is_next_part_a_sent(e):
           #print_sent_xml(e, outf, part)
           sents_to_print_new.append("".join(get_sent_text(e)))
           #print('</s>', file=outf)
           merged_sents_from_xml += "".join(get_sent_text(e))
           #print(merged_sents_from_xml)
           parsed_gigafida.pop(0)
       elif not is_next_part_a_paragraph(e):
           #should be fs
           #print(e, file=outf)           
           print_fs(e, outf)
           parsed_gigafida.pop(0)
       else:
           #print(merged_sents_from_xml, file=outf)
           if first_paragraph:
               gf_to_write = e.attrib["{http://www.w3.org/XML/1998/namespace}id"]
               gfs = gf_to_write.split('.')
               gfs[0]=gfs[0] + '-' + str(part)
               gf_to_write = '.'.join(gfs)
               print('<p xml:id="' + gf_to_write +'">', file=outf)
               last_popped_paragraph = parsed_gigafida.pop(0)
               first_paragraph = False
           else:
               print("".join(sents_to_print_new), file=outf)
               sents_to_print_new = []
               print("</p>", file=outf)
               gf_to_write = e.attrib["{http://www.w3.org/XML/1998/namespace}id"]
               gfs = gf_to_write.split('.')
               gfs[0]=gfs[0] + '-' + str(part)
               gf_to_write = '.'.join(gfs)
               if i != len(lines)-1:
                   print('<p xml:id="' + gf_to_write +'">', file=outf)
               last_popped_paragraph =  parsed_gigafida.pop(0)
              

def merge_lines_with_gigafida_paragraphs(lines, parsed_gigafida, outf, part):
    #print(lines)
    first_paragraph = True
    # V primeru, da manjka tekst, ga je potrebno iz gigafida xml-a dodati v končno besedilo
    # Tekst naj bo za zdaj dodan v svoj segment, naj pa se označi da bo vidno ali je to ok
    segments_to_insert = []
    sents_to_print_new = []
    last_popped_paragraph = None
    total_prints = 0
    for i, line in enumerate(lines):
        
        line = line[:-1]
        #print("l",line)
        merged_sents_from_xml = ""
        line_already_printed = False
        
        while True:
            """
            if current_segment == 1855:
                print('---', file=outf)
                print(line, file=outf)
                print(merged_sents_from_xml, file=outf)
                print('---', file=outf)
                total_prints += 1
                if total_prints == 100:
                    exit()
            """
            if len(parsed_gigafida) == 0:
                print("".join(sents_to_print_new), file=outf)
                sents_to_print_new = []
                print("</p>", file=outf)
                return parsed_gigafida
            e = parsed_gigafida[0]
            #print(e)
            if is_next_part_a_sent(e):
                
                #if not line_already_printed:
                #    print(line, file=outf)
                #    line_already_printed=True
                #print_sent_xml(e, outf, part)
                #print("".join(get_sent_text(e)), file=outf)
                #print('</s>', file=outf)
                sents_to_print_new.append("".join(get_sent_text(e)))
                merged_sents_from_xml += "".join(get_sent_text(e))
                #print('------------')
                #print(merged_sents_from_xml)
                #print(merged_sents_from_xml)
                parsed_gigafida.pop(0)
            elif not is_next_part_a_paragraph(e):
                #should be fs
                #print(e, file=outf)           
                print_fs(e, outf)
                parsed_gigafida.pop(0)
            else:
                #print(merged_sents_from_xml, file=outf)
                if first_paragraph:
                    gf_to_write = e.attrib["{http://www.w3.org/XML/1998/namespace}id"]
                    gfs = gf_to_write.split('.')
                    gfs[0]=gfs[0] + '-' + str(part)
                    gf_to_write = '.'.join(gfs)
                    print('<p xml:id="' + gf_to_write +'">', file=outf)
                    last_popped_paragraph = parsed_gigafida.pop(0)
                    first_paragraph = False
                else:
                    if (line.replace(" ", "")) not in merged_sents_from_xml.replace(" ", "") :
                        with open('./temt.txt', 'a', encoding='utf-8') as temt: 
                            print('---', file=temt)
                            print(merged_sents_from_xml, file=temt)
                            print('-', file=temt)
                            print(line, file=temt)
                        #print("ERROR", line, merged_sents_from_xml, file=outf)
                        #segments_to_insert.append(merged_sents_from_xml)
                        merged_sents_from_xml += " "+ "".join(get_sent_text(e))
                        parsed_gigafida.pop(0)
                    else:
                        #print('did ok', "".join(sents_to_print_new))
                        #print(ET.tostring(e, pretty_print=True), file=outf)
                        #print(e.attrib)
                        print("".join(sents_to_print_new), file=outf)
                        sents_to_print_new = []
                        print("</p>", file=outf)
                        gf_to_write = e.attrib["{http://www.w3.org/XML/1998/namespace}id"]
                        gfs = gf_to_write.split('.')
                        gfs[0]=gfs[0] + '-' + str(part)
                        gf_to_write = '.'.join(gfs)
                        #print(i, len(lines))
                        if i != len(lines)-1:
                            print('<p xml:id="' + gf_to_write +'">', file=outf)
                        last_popped_paragraph =  parsed_gigafida.pop(0)
                        break
    
    parsed_gigafida.insert(0, last_popped_paragraph)

    #print("done")
    return parsed_gigafida
    
def treat_missing_text():
    pass
    
def write_segment_to_file(folder, base_filename, segment, lines_in_curr_segment):
    full_filename = folder + base_filename + "-" + str(part) + ".xml"

"""    
with open("xmltestoutput.xml", "wb") as outf:
    filename = "0_GF0356009.xml"
    segmented_filename = "./segmentacija_dnevnik_vse/0_GF0356009.xml"
    #upgrade_header(get_source_filename('0_GF0356009.xml'), 1, outf)
    base_filename = filename.split("_")[1]
    base_out_filename = "./testing_proper_formatting/"+base_filename
    folder = base_filename[0:4]
    gigafida_filename= './gigafida_nondedup/'+folder+'/'+base_filename
    
    lines_in_curr_segment = []
    current_segment = 1
    
    parsed_gigafida = parse_gigafida(gigafida_filename)[1:]
    empty_segment = False
    with open(segmented_filename, "r", encoding="utf-8") as segmented_file:
        with open(base_out_filename, "w", encoding="utf-8") as outf:
            for i, line in enumerate(segmented_file):
                # First line is always ----------------- so just skip it
                if i == 0:
                    continue
                if line[:5] == "-----":
                    if empty_segment:
                       print("found empty segment") 
                    parsed_gigafida = merge_lines_with_gigafida_paragraphs(lines_in_curr_segment, parsed_gigafida, outf, 1)
                    current_segment += 1
                    lines_in_curr_segment = []
                    print("-----", file=outf)
                    empty_segment = True
                else:
                    empty_segment = False
                    lines_in_curr_segment.append(line)
                    
"""                 




folder = './ver3_delo_dedup_nondedup_midway/'
out_folder = './ver3_delo_dedup_nondedup/'
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
    full_out_filename = out_folder+filename
    
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
        #print("upgrading header")
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



#base_filename = filename.split("_")[1]
#base_out_filename = "./testing_proper_formatting/"+base_filename
#base_out_filename = "./testing_proper_formatting_delo_popravki/"+base_filename
#folder = base_filename[0:4]

#gigafida_filename= './gigafida_nondedup/'+folder+'/'+base_filename

#lines_in_curr_segment = []
#current_segment = 1

#parsed_gigafida = parse_gigafida(gigafida_filename)
#for p in parsed_gigafida[:10]:
#    print(p, p.attrib)

# TODO - poglej, kaj j

e
                
                
                
                
                
                

mpty_segment = False
after_empty_segment = False
start_printing=False
#segmented_folder = './Delo-popravki/Delo-popravki/Delo-nepregledano/'
segmented_folder = './Delo-popravki/Delo-popravki/segmentacija-pregled-OK-ni-popravkov/'
files_in_segmented_folder = os.listdir(segmented_folder)
already_skipped = False
for filename in files_in_segmented_folder:
    
    if filename != '137_GF1270864.xml':
        continue
    
    print(filename)
    """
    if filename == '36_GF2502190.xml':
        exit()
    continue
    """
    #filename = "50_GF7278125.xml"
    segmented_filename = segmented_folder+filename
    base_filename = filename.split("_")[1]
    folder = base_filename[0:4]
    gigafida_filename= './gigafida_nondedup/'+folder+'/'+base_filename
    lines_in_curr_segment = []
    current_segment = 1
    base_out_filename = "./ver3_delo_dedup_nondedup_midway/"+base_filename
    parsed_gigafida = parse_gigafida(gigafida_filename)
    """
    while True:
        e = parsed_gigafida[0]
        #print(e)
        if is_next_part_a_sent(e):
            text = "".join(get_sent_text(e))
            if "Public Enemies" in text:
                if start_printing == True:
                    exit()
                start_printing = True
            if start_printing == True:
                print("".join(get_sent_text(e)))
        else:
            if start_printing == True:
                print(e)

        parsed_gigafida.pop(0)
    exit()
    """
        
    print(base_out_filename)
    

    with open(segmented_filename, "r", encoding="utf-8") as segmented_file:
        
        for i, line in enumerate(segmented_file):
            # First line is always ----------------- so just skip it
            if after_empty_segment:
                line_to_get_to = line[:-1]
                #print(line_to_get_to)
                for pg in [parsed_gigafida[2]]:
                    if is_next_part_a_sent(pg):
                        #print("".join(get_sent_text(pg)))
                        if line_to_get_to[:-1] == "".join(get_sent_text(pg)):
                            print("ok to skip empty segment")
                            #lines_in_curr_segment.append(line)
                        else:
                            print("not ok")
                            print(line_to_get_to)
                            #print("".join(get_sent_text(pg)))
                            for pg2 in parsed_gigafida:
                                if is_next_part_a_sent(pg2):
                                    print("".join(get_sent_text(pg2)))
                                    #print(line_to_get_to)
                                    if line_to_get_to[:10] == "".join(get_sent_text(pg2))[:10]:
                                        curr_filename = "."+"".join(base_out_filename.split(".")[:-1]) + '-' + str(current_segment) + ".xml"
                                        with open(curr_filename, "w", encoding="utf-8") as outf:
                                            print(curr_filename)
                                            #print(base_out_filename)
                                            parsed_gigafida = merge_lines_with_gigafida_paragraphs_empty_segment(lines_in_curr_segment, parsed_gigafida, outf, current_segment)
                                            lines_in_curr_segment = []
                                            current_segment += 1
                                        break
                                    lines_in_curr_segment.append("".join(get_sent_text(pg2))+"a")
                after_empty_segment = False

            if i == 0:
                continue
            if line[:5] == "-----":
                if empty_segment:
                    print("found empty segment in", base_filename)
                    #print("lines_in_curr_segment", lines_in_curr_segment)
                    #print(parsed_gigafida[:3])
                    after_empty_segment = True
                    continue
                    exit()
                curr_filename = "."+"".join(base_out_filename.split(".")[:-1]) + '-' + str(current_segment) + ".xml"
                with open(curr_filename, "w", encoding="utf-8") as outf:
                    #print("lcs", lines_in_curr_segment[-1])
                    #print(curr_filename)
                    #print(curr_filename)
                    parsed_gigafida = merge_lines_with_gigafida_paragraphs(lines_in_curr_segment, parsed_gigafida, outf, current_segment)
                    current_segment += 1
                    lines_in_curr_segment = []
                    #print("-----", file=outf)
                    empty_segment = True
            else:
                empty_segment = False
                lines_in_curr_segment.append(line)
        if after_empty_segment:
            curr_filename = "."+"".join(base_out_filename.split(".")[:-1]) + '-' + str(current_segment) + ".xml"
            with open(curr_filename, "w", encoding="utf-8") as outf:
                print("empty segment at end")
                parsed_gigafida = print_empty_segment_at_end(parsed_gigafida, outf, current_segment)
                current_segment += 1
                empty_segment = False
                after_empty_segment = False
                print(len(parsed_gigafida))
    exit()            
                
               


 