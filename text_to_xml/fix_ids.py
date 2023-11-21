import os

def fix_ids(folder_in, folder_out):
    subfolders = [ f.path for f in os.scandir(folder_in) if f.is_dir() ]
    #print(subfolders)
    for folder in subfolders:
        
        files = os.listdir(folder)
        for file in files:
            new_filename = file
            search_string2 = None
            if "-missing" in file:
                new_filename = new_filename.replace("-missing", "")
            if len(new_filename.split("-")) > 2:
                new_filename = new_filename.split("-")[0]+"-"+new_filename.split("-")[-1]
                search_string2 = file.split("-")[0]+"-"+file.split("-")[1]
                print(file, search_string2)
            
            #print(file, new_filename)
            
            search_string = file.split(".")[0]
            replacement_string = new_filename.split(".")[0]
            
            out_folder_name = folder_out + "\\" + folder.split("\\")[2]
            
            out_file = os.path.join(out_folder_name, new_filename)
            #print(out_file)
            #exit()
            with open(os.path.join(folder, file), "r", encoding="utf-8") as f, open(out_file, "w", encoding="utf-8") as outf, open("temt.txt", "a", encoding = "utf-8") as temt:
                for line in f:
                    if search_string in line:
                        new_line = line.replace(search_string, replacement_string)[:-1]
                        print(new_line, file=outf)
                        print(line[:-1], new_line, file=temt)
                        
                    elif search_string2 is not  None and search_string2 in line:                    
                        new_line = line.replace(search_string2, replacement_string)[:-1]
                        print(new_line, file=outf)
                        print(line[:-1], new_line, file=temt)
                            
                    else:
                        print(line[:-1], file=outf)
                        
                        
            #exit()
        #exit()
fix_ids(".\\ver4_delo_popravki_verzija_1", ".\\ver4_delo_popravki_verzija_1_fixed_id")