import numpy as np
import os
import re
from tqdm import tqdm
import pandas as pd

# assumes SRT format: 
# <subtitle number>
# <start> --> <end> (hr:min:sec,ms)
# <subtitle1>
# <subtitle2> (optional)
# \n
# (next subtitle)


remove_temp = True

loc_py = "/home/ron/Downloads/forrest_stimulus/forced_alignment/p2fa/p2fa_1.003/p2fa/align2.py"
loc_wav = "/home/ron/Downloads/forrest_stimulus/forrest_PAL/output4.wav"
loc_sub = "/home/ron/Downloads/forrest_stimulus/forrest_PAL/release-English_utf.srt"
loc_out = "/home/ron/Downloads/forrest_stimulus/forced_alignment/out/"

with open(loc_sub, 'r') as file:
    subs_raw=file.readlines()

subs_raw = [i.replace('\n', '') for i in subs_raw]

headers_idx = []
starts = []
ends = []
# words = []

print("pre-processing: extracting individual lines from .SRT")
count = 0
for c,i in enumerate(subs_raw):
	if len(re.findall('^[1-9]', i)) > 0:
		headers_idx.append(count)
		count+=1 

		times = subs_raw[c+1]
		tstart = re.findall('^(.*?) --> ', times)[0].replace(":",",").split(",")
		tstart = [int(val) for val in tstart]
		starts.append(tstart[0]*3600 + tstart[1]*60 + tstart[2] + tstart[3]/1000) 
		tend = re.findall(' --> (.*)', times)[0].replace(":",",").split(",")
		tend = [int(val) for val in tend]
		ends.append(tend[0]*3600 + tend[1]*60 + tend[2] + tend[3]/1000) 
		
		word = (subs_raw[c+2] + " " + subs_raw[c+3]+"\n").replace(" ","\n").replace("\n\n","\n").replace("\n\'","\n\\\'")
		if word[0] == "'":
			word = "\\"+word

		with open(loc_out+"__temp%s.txt"%(headers_idx[-1]), "w") as text_file:
			text_file.write(word)


print("performing forced-alignment")
for i in tqdm(headers_idx):
	execute = "python %s -s %.2f -e %.2f %s %s__temp%d.txt %s__temp%d.TextGrid"%(loc_py, starts[i], ends[i], loc_wav, loc_out, i, loc_out, i)
	os.system(execute)


print("aggregating timings")
all_starts = []; all_ends = []; all_words = []
for i in headers_idx:
	with open("%s__temp%d.TextGrid"%(loc_out, i), 'r') as file:
		tmp=file.read().splitlines()
	start_idx = np.flatnonzero(np.asarray(tmp) == '"word"')[0]
	tmp = tmp[start_idx+4:]
	starts 	= tmp[::3]
	ends 	= tmp[1::3]
	words 	= tmp[2::3]
	for c,w in enumerate(words):
		if not w == '"sp"':
			all_starts.append(starts[c])
			all_ends.append(ends[c])
			all_words.append(w[1:-1])

savedat = pd.DataFrame()
savedat["start"] = all_starts
savedat["end"] = all_ends
savedat["word"] = all_words
savedat.to_csv(loc_out+"forrest_forced_aligned.csv")

if remove_temp:
	execute = "rm %s__temp*"%loc_out
	os.system(execute)
