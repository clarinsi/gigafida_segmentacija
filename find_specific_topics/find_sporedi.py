import sys
import os
import re

def find_sporedi(filename, outf_name, sporedf_name):
    in_spored = False
    in_spored_next = False
    checking_10_next = -1
    lines_waiting = []
    do_not_print_line = False
    r1 = re.compile(r'\d{2}\.\d{2} Slovenija 1')
    r2 = re.compile(r'\d{1}\.\d{2} Slovenija 1')
    r3 = re.compile(r"SLOVENIJA 1")
    r4 = re.compile(r"TV SLOVENIJA 1")
    r5 = re.compile(r'\d{2}\.\d{2} SLOVENIJA 1')
    r6 = re.compile(r'\d{1}\.\d{2} SLOVENIJA 1')
    r7 = re.compile(r'\wSLOVENIJA 1$')
    r8 = re.compile(r'\w\.SLOVENIJA 1$')
    r9 = re.compile(r"azijski squawk box")
    r10 = re.compile(r"azijski squawk bo")
    r11 = re.compile(r"\d{1,2}\.\d{2}")
    with open(filename, "r", encoding="utf-8") as f, open(outf_name, "w", encoding="utf-8") as outf, open(sporedf_name, "w", encoding="utf-8") as sporedf:
        #print(filename, file=sporedf)
        #print(filename, file=outf)
        for line in f:
            line = line[:-1]
            if checking_10_next > 0:
                checking_10_next -=1
                lines_waiting.append(line)
                do_not_print_line = True
            
            if checking_10_next == 0:
                print("----------Spored", file=sporedf)
                print("----------Spored", file=outf)
                for l in lines_waiting:
                    #print(l, file=sporedf)
                    print(l, file=outf)
                lines_waiting = []
                checking_10_next = -1
                in_spored = False
            if in_spored_next:
                if not in_spored:
                    print("----------Spored", file=sporedf)
                    print("----------Spored",  file=outf)
                in_spored = True
                in_spored_next = False
            if line[0:3] == "---":
                if not in_spored:
                    print(line, file=outf)
                    #print(line, file=sporedf)
                continue
            
            # ZACETEK SPOREDA
            
            #Vrstica, kot je »18.10 Slovenija 1Recept za zdravo življenje«, torej se začne z uro, vzorec »XX.XX (lahko tudi X.XX), potem sledi Slovenija 1 in velikokrat brez presledka naslednja beseda z veliko začetnico. Pred tako vrstico je treba dati prelom za začetek sporeda.
            if re.match(r1, line) != None:   #r'\d{2}\.\d{2} Slovenija 1'
                if not in_spored:
                    print("----------Spored", file=sporedf)
                    print("----------Spored", file=outf)
                in_spored = True
            if re.match(r2, line) != None:   #r'\d{1}\.\d{2} Slovenija 1'
                if not in_spored:
                    print("----------Spored", file=sporedf)
                    print("----------Spored", file=outf)
                in_spored = True
            #Varianta je, ko imamo prvo pojavitev SLOVENIJA 1 v vrstici, brez drugega teksta.
            if re.match(r3, line) != None:   #"SLOVENIJA 1"
                if not in_spored:
                    print("----------Spored", file=sporedf)
                    print("----------Spored", file=outf)
                in_spored = True
            if re.match(r4, line) != None:   #"TV SLOVENIJA 1"
                if not in_spored:
                    print("----------Spored", file=sporedf)
                    print("----------Spored", file=outf)
                in_spored = True
            #Še ena varianta: 17.45 SLOVENIJA 1 – spet prva pojavitev SLOVENIJA 1, tokrat s časom spredaj
            if re.match(r5, line) != None: #r'\d{2}\.\d{2} SLOVENIJA 1'
                if not in_spored:
                    print("----------Spored", file=sporedf)
                    print("----------Spored", file=outf)
                in_spored = True
            if re.match(r6, line) != None:  #r'\d{1}\.\d{2} SLOVENIJA 1'
                if not in_spored:
                    print("----------Spored", file=sporedf)
                    print("----------Spored", file=outf)
                in_spored = True
            #Varianta je tudi npr. PAVLE KAVČISLOVENIJA 1, torej ko se nam SLOVENIJA 1 prvič pojavi na koncu vrstice in ni presledka med predhodnim besedilom (tu je prišlo do napake pri pretvorbi). V takih primerih je spet treba dati prelom pred SLOVENIJA 1.
            if re.search(r7, line) != None:   #r'\wSLOVENIJA 1$'
                in_spored_next = True
            if re.search(r8, line) != None:   #r'\w\.SLOVENIJA 1$'
                in_spored_next = True
                       
            # KONEC SPOREDA
            #Pogosto sem sicer opazil, da ravno ta zadnja vrstica vsebuje »CNBC's azijski squawk box« ali varianto »CNBC's azijski squawk bo«, torej x na koncu manjka.
            if in_spored:
                if re.search(r9, line.lower()) != None:   #r"azijski squawk box"
                    
                    if checking_10_next > 0:
                        for l in lines_waiting:
                            if l[0:3] != "---":
                                print(l, file=sporedf)
                                print(l, file=outf)
                        lines_waiting = []
                        checking_10_next = -1
                    if in_spored:
                        print("----------Spored", file=sporedf)
                        print("----------Spored", file=outf)
                    in_spored = False
                elif re.search(r10, line.lower()) != None: #r"azijski squawk bo"  
                    if checking_10_next > 0:
                        for l in lines_waiting:
                            if l[0:3] != "---":
                                print(l, file=sporedf)
                                print(l, file=outf)
                        lines_waiting = []
                        checking_10_next = -1
                    if in_spored:
                        print("----------Spored", file=sporedf)
                        print("----------Spored", file=outf)
                    in_spored = False
                #Še boljše pravilo je, da se enostavno poišče zadnjo vrstico, kjer je več vzorcev X.XX naslov, npr.
                #    9.00 Pritožbe iz Evrope - 10.00 Evropski denarni krog - 10.15 CNBC Evropa - 14.30 Pritožbe iz ZDA - 16.00 MSNBC položaj - 17.00 The Site - 18.00 Narodne geografske lepote - 19.00 Vstopnica - 19.30 Talkshow - 20.00 Skozi čas - 21.00 NBC šport - 22.00 Večer z Jayom Lenom - 23.00 Noč s Conanom O'Brienom - 0.00 Z Gregom Kinnearjem - 0.30 NBC večerna poročila - 1.00 Večer z Jayom Lenom - 2.00 MSNBC Mednarodna noč v živo - 3.00 Selina Scott predstavlja - 4.30 Vstopnica - 5.00 Selina Scott predstavlja
                elif len(re.findall(r11, line)) > 5:
                    #in_spored = False
                    if checking_10_next > 0:
                        for l in lines_waiting:
                            if l[0:3] != "---":
                                print(l, file=sporedf)
                                print(l, file=outf)
                        lines_waiting = []
                    checking_10_next = 10
                    
                #So pa tudi izjeme, npr. 8.00 dsdsadsdad. Tu je treba paziti, da je čas lahko tudi X.XX. Pa paziti je treba na posebnost, ki je spet problem pretvorbe:
                #   2.00Draži me (Tease Me), am. erot., 2007. Tu se torej čas in naslov držita skupaj.
                #Skratka, za te zadnje primere bi lahko recimo iskali zadnjo pojavitev tega časa, ampak potem damo pogoj, da se tak vzorec s časom ne sme ponoviti v naslednjih 10 vrsticah (ker so v sporedu vmes tudi kakšne sinopse filmov).
                elif in_spored and re.search(r11, line):
                    #print("FOUND", line)
                    if checking_10_next > 0:
                        first_line = True
                        for l in lines_waiting:
                            if first_line:
                                if l[0:3] != "---":
                                    print(l, file=sporedf)
                                    print(l, file=outf)
                                first_line = False
                            else:
                                if l[0:3] != "---":
                                    print(l, file=sporedf)
                                    print(l, file=outf)
                                
                        lines_waiting = []
                    checking_10_next = 10
                    

            #if "SLOVENIJA 1" in line:
            #   print(line[:-1], in_spored)
            
            if not do_not_print_line:
                if in_spored:
                    if line[0:3] != "---":
                        print(line, file=sporedf)
                        print(line, file=outf)

                else:
                    print(line, file=outf)
            else:
                do_not_print_line = False
        for l in lines_waiting:
            #print(l, file=sporedf)
            print(l, file=outf)
            
sys.stdout.reconfigure(encoding='utf-8')
filenames = os.listdir("C:/dokt/gigafida_300/dnevnik_maj_final_test_delnice_konec")
print(len(filenames))
#for filename in [filenames[0]]:
for filename in filenames:
#for filename in ["6_GF1255360.xml"]:
    find_sporedi(os.path.join("C:/dokt/gigafida_300/dnevnik_maj_final_test_delnice_konec", filename), os.path.join("C:/dokt/gigafida_300/dnevnik_maj_final_test_delnice_konec_sporedi_all", filename), os.path.join("C:/dokt/gigafida_300/dnevnik_maj_final_test_delnice_konec_sporedi", filename))