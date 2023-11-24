# Gigafida segmentation

This repository contains the code used for segmenting the Gigafida corpus. Currently, the input and output folders are hard-coded into the code files. To run the code, change the input and output locations to the desired folders and run the appropriate python file.

## find_specific_topics

This folder contains the code used for segmenting two specific kinds of articles found in Dnevnik news: stock reports (*find_stocks.py*) and movie schedules (*find_sporedi.py*). Each file extracts the designated articles from all Gigafida files present in a given folder.

## segment_gigafida

This folder contains the code for segmenting gigafida files:

* *parse_gigafida.py* contains a handful of utility functions for parsing Gigafida files
* *segment_group.py* and *segment_group_maj.py* contain the code for segmenting Gigafida. *segment_group.py* is an older version used for early testing of segmentation on Delo, Dnevnik, Dolenjski List and Novi Tednik. *segment_group_maj.py* is an improved version that was used for final segmentation of Delo and Dnevnik articles.
* *split_on_konec.py* and *remove_sport_team_breaks.py* contain a few additional functions that clean up the segmentation results and should be ran after performing segmentation to obtain the final segmented articles.

## text_to_xml

This folder contains the code for converting the text output returned by segmentation into the final xml format.

* *convert_from_ground_up.py* Can be used to convert a segmented text file into the final xml format. However, it ignores the original gigafida files and should therefore not be used when text is missing from the segmented file (e.g., when the segmented file was constructed from a de-duplicated gigafida file.
* *convert_from_ground_up_for_dedup.py* Works simiarly to *convert_from_ground_up.py* but can be used on de-duplicated files when a better alternative isn't available.
* *convert_normal_gigafida.py* Converts non-segmented gigafida files into the new format.
* *fix_ids.py* Fixes errors in filename ids by removing some information that was added during segmentation (e.g. annotator names)
* *properly_format_segmented_files-delo-dedup-to-nondedup.py* Converts segmented files that were obtained from de-duplicated Delo files.
* *properly_format_segmented_files-delo.py* Converts segmented files that were obtained from non de-duplicated Delo files.
* *properly_format_segmented_files.py* Converts segmented files that were obtained from Dnevnik files.