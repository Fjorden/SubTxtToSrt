from cgitb import text
import argparse
import re
import time

parser = argparse.ArgumentParser()
parser.add_argument("infile", help="Path to file we are converting")
parser.add_argument("outfile", help="Output file name")
args = parser.parse_args()


with open(args.infile, 'r', encoding="utf8") as file:
    txt = file.read()

txt = txt.splitlines()
fps = float(txt[0].strip('{1}'))
txt.pop(0)

srt = []
frase_number = 1

for line in txt:
    x = re.findall('((?={).+?(?<=}))((?={).+?(?<=}))(.+)', line)
    start = time.strftime('%H:%M:%S', time.gmtime(int(x[0][0].strip('{}'))//fps))
    miliseconds = str(int(x[0][0].strip('{}'))%fps/fps)[2:5]
    start = f'{start},{miliseconds}'
    stop = time.strftime('%H:%M:%S', time.gmtime(int(x[0][1].strip('{}'))//fps))
    miliseconds = str(int(x[0][1].strip('{}'))%fps/fps)[2:5]
    stop = f'{stop},{miliseconds}'
    text = str(x[0][2]).replace('|',' ')
    frase = f'{frase_number}\n{start} --> {stop}\n{text}\n\n'
    srt.append(frase)
    frase_number += 1

ready_srt = ''.join(srt)



with open(args.outfile, 'w', encoding='utf8') as file:
    file.write(ready_srt)