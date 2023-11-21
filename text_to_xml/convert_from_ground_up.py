import os

def print_paragraphs(all_paragraphs, curr_paragraph_num, outf):
    outf_name = outf.name.split('/')[-1].split('.')[0]
    for paragraph in all_paragraphs:
        print('<p xml:id="'+outf_name+'.'+str(curr_paragraph_num)+'">', file=outf)
        curr_paragraph_num += 1
        print(paragraph, file=outf)
        print('</p>', file=outf)
    return curr_paragraph_num


mpty_segment = False
after_empty_segment = False
start_printing=False
#segmented_folder = './Delo-popravki/Delo-popravki/Delo-nepregledano/'
segmented_folder = './Delo-popravki/Delo-popravki/segmentacija-pregled-verzija2/'
files_in_segmented_folder = os.listdir(segmented_folder)
already_skipped = False
for filename in files_in_segmented_folder:
    print(filename)
    #if filename != '137_GF1270864.xml':
    #    continue
    #filename = "50_GF7278125.xml"
    segmented_filename = segmented_folder+filename
    base_filename = filename.split("_")[1]
    folder = base_filename[0:4]
    gigafida_filename= './gigafida_nondedup/'+folder+'/'+base_filename
    lines_in_curr_segment = []
    current_segment = 1
    base_out_filename = "./ver3_delo_dedup_nondedup_midway/"+base_filename
    #parsed_gigafida = parse_gigafida(gigafida_filename)
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
                
                print(curr_filename)
                #print(all_paragraphs)
                with open(curr_filename, "w", encoding="utf-8") as outf:
                    curr_paragraph_num = print_paragraphs(all_paragraphs, curr_paragraph_num, outf)
                    all_paragraphs = []
                    current_segment += 1
                    
            else:
                all_paragraphs.append(line[:-1])
    #exit()
        