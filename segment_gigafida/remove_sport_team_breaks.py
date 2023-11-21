import re
import sys
import os
sys.stdout.reconfigure(encoding='utf-8')


def find_delnice(filename, stock_filename):
    r1 = re.compile(r'\d{1,2}\. [a-zA-z]*')
    r2 = re.compile(r'(januar|februar|marec|april|maj|junij|julij|avgust|september|oktober|november|december)')
    STATE = 0
    curr_candidates = []
    buffer_lines = []
    breaks_at = []
    dates_at = []
    with open(filename, "r", encoding="utf-8") as f, open(stock_filename, "w", encoding="utf-8") as konecf: 
        for line in f:
            buffer_lines.append(line)
            while len(buffer_lines) > 3:
                print(buffer_lines[0][:-1], file=konecf)
                buffer_lines.pop(0)
            if len(buffer_lines) == 3:
                if buffer_lines[1][:3] == "---":
                    if (re.match(r1, buffer_lines[0]) and re.match(r1, buffer_lines[2])) and not (re.search(r2, buffer_lines[0].lower()) or re.search(r2, buffer_lines[2].lower())):
                        print("Removed break", filename, buffer_lines[0], buffer_lines[2])
                        buffer_lines.pop(1)
        while len(buffer_lines) > 0:
            print(buffer_lines[0][:-1], file=konecf)
            buffer_lines.pop(0)                
        
filenames = os.listdir("C:/dokt/gigafida_300/dnevnik_maj_final_test_delnice_konec_sporedi_all/")
print(len(filenames))
#for filename in [filenames[0]]:
for filename in filenames:
    find_delnice(os.path.join("C:/dokt/gigafida_300/dnevnik_maj_final_test_delnice_konec_sporedi_all", filename), os.path.join("C:/dokt/gigafida_300/dnevnik_maj_final_test_delnice_konec_sporedi_teams", filename))
           