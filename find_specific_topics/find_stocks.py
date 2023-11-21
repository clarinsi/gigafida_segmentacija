import re
import sys
import os
sys.stdout.reconfigure(encoding='utf-8')

# Pravila za delnice:
    # Naslov (ime firme)
    # Vrstice z številkami/le par črkami(npr. EUR, NP)
    # To se mora pojaviti ogromnokrat (recimo > 25)
    
# Napjrej še bolj točno:
    # Naslov
    # Datum (XX.XX.)
    # EUR
    # Kratka številka (ali NP)
    # Kratka številka (ali NP)
    # Kratka številka (ali NP)
    # ...
    # Single digit
    # Single digit  - TODO: Tudi state 3 ima lahko konec
    
    
def fix_incorrect_endings(filename, filename_fixed):
    r1 = re.compile(r'\d{2}\.\d{2}\.')
    r2 = re.compile(r'\-?\d+\,\d+')
    r3 = re.compile(r'\-?\d+\.\d+')
    # Stocks should always end with a number
    # look at pairs of lines. If an ending is preceeded by a non-number, swap them. Repeat until done
    line_buffer = []
    with open(filename, "r", encoding="utf-8") as f, open(filename_fixed, "w", encoding="utf-8") as fixed_f:
        for line in f:
            if len(line_buffer) < 5:
                line_buffer.append(line)
            else:
                done = True
                while done:
                    for i in range(len(line_buffer)-1):
                        if line_buffer[i+1] == "-----Delnice konec\n":
                            if not(re.search(r2, line_buffer[i]) != None or
                                   re.search(r1, line_buffer[i]) != None or 
                                   (len(line_buffer[i]) == 2 and line_buffer[i][0].isdigit())):
                                #print("swapped", line_buffer[i], line_buffer[i+1])
                                tmp = line_buffer[i+1]
                                line_buffer[i+1] = line_buffer[i]
                                line_buffer[i] = tmp
                                done=True
                                break
                    done=False
                print(line_buffer[0][:-1], file=fixed_f)
                line_buffer.pop(0)
                line_buffer.append(line)
        for l in line_buffer:
            print(l[:-1], file=fixed_f)
            
def print_candidates(curr_candidates, stockf, allf):
    if(len(curr_candidates) > 100):
        if len(curr_candidates[0][0].split(" ")) > 15:
            print(curr_candidates[0][0][:-1], file=stockf)
            print(curr_candidates[0][0][:-1], file=allf)
            curr_candidates.pop(0)
        print('-----Delnice start', file=stockf)
        print('-----Delnice start', file=allf)
        for l in curr_candidates:
            if l[0][0:3] != "---":
                print(l[0][:-1], file=stockf)
                print(l[0][:-1], file=allf)
        print('-----Delnice koned', file=stockf)
        print('-----Delnice konec', file=allf)
    else:
        for l in curr_candidates:
            print(l[0][:-1], file=allf) #TODO - fix for full outputs

def find_delnice(filename, stock_filename, all_filename):
    r1 = re.compile(r'\d{2}\.\d{2}\.')
    r2 = re.compile(r'\-?\d+\,\d+')
    r3 = re.compile(r'\-?\d+\.\d+')
    STATE = 0
    curr_candidates = []
    with open(filename, "r", encoding="utf-8") as f, open(stock_filename, "w", encoding="utf-8") as stockf, open(all_filename, "w", encoding="utf-8") as allf: 
        for line in f:
            if line[:3] == "---":
                curr_candidates.append((line[:-1], STATE))
                continue
            #print(STATE, line)
            if STATE == 0:  # Naslov, naj lahko bo karkoli
                curr_candidates.append((line, STATE))
                STATE += 1;
                # Preveri, tudi, če gre za številko:
                if re.search(r1, line) != None:
                    STATE = 2
                elif re.search(r2, line) != None or re.search(r3, line) != None or len(line) <= 5:
                    STATE = 3
            elif STATE == 1:  # Datum (XX.XX.)
                if re.search(r1, line) != None:
                    curr_candidates.append((line, STATE))
                    STATE += 1
                else:
                    print_candidates(curr_candidates, stockf, allf)
                    STATE = 0
                    curr_candidates = []
                    curr_candidates.append((line, STATE))
            elif STATE == 2:  # EUR
                if "EUR" in line or "USD" in line or (len(line) == 4): 
                    curr_candidates.append((line, STATE))
                    STATE += 1
                else:
                    print_candidates(curr_candidates, stockf, allf)
                    STATE = 0
                    curr_candidates = []
                    curr_candidates.append((line, STATE))
            elif STATE == 3:    # Kratka številka/ali len <= 5 (state ostane) ali 1. single digit (state++)
                if len(line) == 2 and line[0].isdigit():
                    curr_candidates.append((line, STATE))
                    STATE += 1
                elif re.search(r2, line) != None or re.search(r3, line) != None or len(line) <= 5:
                    curr_candidates.append((line, STATE))
                elif len(line) < 40:
                    #print("went from 3 to 1")
                    STATE = 1
                    curr_candidates.append((line, STATE))
                else:
                    #print("went from 3 to 0")
                    print_candidates(curr_candidates, stockf, allf)
                    STATE = 0
                    curr_candidates = []
                    curr_candidates.append((line, STATE))
            elif STATE == 4:  # 2. single digit  
                if len(line) == 2 and line[0].isdigit():
                    curr_candidates.append((line, STATE))
                    STATE = 0;
                elif re.search(r2, line) != None or re.search(r3, line) != None or len(line) <= 5:
                    curr_candidates.append((line, STATE))
                    STATE -= 1
                else:
                    # Try to catch errors. If the line is short, do not print and reset candidates
                    if len(line) < 40:
                        curr_candidates.append((line, STATE))
                        STATE = 0
                    else:
                        print_candidates(curr_candidates, stockf, allf)
                        STATE = 0
                        curr_candidates = []
                        curr_candidates.append((line, STATE))
                    
        for c in curr_candidates:
            print(c[0][:-1], file=allf)
            
#filenames = os.listdir("C:/dokt/gigafida_300/dnevnik_maj_final_test/")
filenames = os.listdir("C:\\Users\\Tadej\\Downloads\\delnice\\dnevnik_maj_final_test_delnice_fixed_all")
print(len(filenames))
#for filename in [filenames[0]]:
for filename in filenames:
    #find_delnice(os.path.join("C:/dokt/gigafida_300/dnevnik_maj_final_test", filename), os.path.join("C:/dokt/gigafida_300/dnevnik_maj_final_test_delnice", filename),
    #os.path.join("C:/dokt/gigafida_300/dnevnik_maj_final_test_delnice_all", filename))
    
    #find_delnice(os.path.join("C:/dokt/gigafida_300/dnevnik_maj_final_test", filename), os.path.join("C:/dokt/gigafida_300/dnevnik_maj_final_test_delnice", filename), os.path.join("C:/dokt/gigafida_300/dnevnik_maj_final_test_delnice_all", filename))
    
    fix_incorrect_endings(os.path.join("C:/dokt/gigafida_300/dnevnik_maj_final_test_delnice_all", filename),os.path.join("C:/dokt/gigafida_300/dnevnik_maj_final_test_delnice_konec", filename))