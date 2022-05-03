from tika import parser
import json

raw=parser.from_file(r'C:\Users\praka\Desktop\SMART EDUCATION BOT\BOOKS\12th\Physics\chap14.pdf')

with open(r'C:\Users\praka\Desktop\SMART EDUCATION BOT\BOOKS\12th\Physics\phy14.txt','w',encoding='utf-8') as f:
    for val in raw.items():
         f.write(str(val))