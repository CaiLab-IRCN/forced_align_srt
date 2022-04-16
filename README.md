# forced_align_srt

Fork of Penn Phonetics Lab Forced Aligner for use with subtitle files. 

Takes:
- A subtitle file (.srt)
- The movie audio (.wav)

Outputs:
- A .csv file with the onset and offset of each word in the movie.  

Dependencies:
https://babel.ling.upenn.edu/phonetics/old_website_2015/p2fa/index.html (runs on python 2.7)

Instructions:
- Set up a python 2.7 environment and p2fa (or try this python 3 fork https://github.com/jaekookang/p2fa_py3)
- Specify folder structure in force_align_subtitles.py
- Run force_align_subtitles.py
