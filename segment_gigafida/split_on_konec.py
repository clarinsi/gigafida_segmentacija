import re
import sys
import os
sys.stdout.reconfigure(encoding='utf-8')


def find_delnice(filename, stock_filename):
    r1 = re.compile(r'\d{1,2}\. \b(januar|februar|marec|april|maj|junij|julij|avgust|september|oktober|november|december)\b')
    STATE = 0
    curr_candidates = []
    buffer_lines = []
    breaks_at = []
    dates_at = []
    with open(filename, "r", encoding="utf-8") as f, open(stock_filename, "w", encoding="utf-8") as konecf: 
        for line in f:
            buffer_lines.append(line)
            while len(buffer_lines) > 10:
                print(buffer_lines[0][:-1], file=konecf)
                buffer_lines.pop(0)
            if len(buffer_lines) == 10:
                if buffer_lines[4][:-1] == "KONEC" or buffer_lines[4][:-1] == "K O N E C":
                    breaks_at = []
                    dates_at = []
                    print("KONEC in ", filename)
                    for i, buffer_line in enumerate(buffer_lines):
                        if buffer_line[:3] == "---":
                            breaks_at.append(i)
                            print("breaks")
                        if re.search(r1, buffer_line.lower()):
                            dates_at.append(i)
                            print("dates")
                    # če je pred tem ali po tem prelom, OK
                    if (3 in breaks_at) or (5 in breaks_at) or (6 in breaks_at):
                        continue
                    #Če je v drugi ali tretji vrstici, po K O N E C datum, npr. 6. marec 
                    #(samo ta kombinacija številke in meseca), potem je prelom tik pred datumom.
                    elif (6 in dates_at):
                        buffer_lines.insert(6, "---------------")
                    elif (7 in dates_at):
                        buffer_lines.insert(7, "---------------")
                    #če ni preloma dve vrstici prej ali potem, se doda takoj za besedilom.
                    else:
                        buffer_lines.insert(5, "---------------")
        while len(buffer_lines) > 0:
            print(buffer_lines[0][:-1], file=konecf)
            buffer_lines.pop(0)
        
filenames = os.listdir("C:/dokt/gigafida_300/dnevnik_maj_final_test_delnice_fixed2")
print(len(filenames))
#for filename in [filenames[0]]:
for filename in filenames:
    find_delnice(os.path.join("C:/dokt/gigafida_300/dnevnik_maj_final_test_delnice_fixed2", filename), os.path.join("C:/dokt/gigafida_300/dnevnik_maj_final_test_delnice_konec", filename))
           