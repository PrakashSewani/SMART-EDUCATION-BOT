from flask import Flask, render_template, request
import yake
import wikipedia
from flask import send_file
import requests
from bs4 import BeautifulSoup
import json
import re
import csv
import torch
from transformers import BertForQuestionAnswering
from transformers import BertTokenizer

app = Flask(__name__)
app.static_folder = 'static'

def keyword_extractor(userquery):
    text=userquery
    language='en'
    max_ngram_size=6
    deduplication_threshold=0.9
    numOfKeywords=20
    custom_kw_extractor=yake.KeywordExtractor(lan=language,n=max_ngram_size,dedupLim=deduplication_threshold,top=numOfKeywords,features=None)
    keywords=custom_kw_extractor.extract_keywords(text)
    print("Extracted Keywords are: ")
    print(keywords)
    
    return keywords

def webscrapper(userquery):
    base_url='https://www.google.com/search'
    
    params={
        'q': '',
        'sxsrf':' APq-WBvZinugdumNu41F-j5I2hxaP1oSVA:1648960613300',
        'ei':' ZSRJYqvpEfXUmAW3ypeABQ',
        'oq':' who is lord', 
        'gs_lcp':' Cgdnd3Mtd2l6EAMYAzIFCAAQgAQyCggAEIAEEIcCEBQyBQgAEIAEMgUIABCABDIFCAAQgAQyBQgAEIAEMgUIABCABDIFCAAQgAQyBQgAEIAEMgUIABCABDoHCCMQ6gIQJzoECCMQJzoECAAQQzoHCAAQsQMQQzoICAAQgAQQsQM6CAguEIAEELEDOgUIABCRAjoLCAAQgAQQsQMQgwE6BQguEIAESgQIQRgASgQIRhgAUM4HWK4uYI5FaAJwAXgAgAGEAYgBuQuSAQQxLjEymAEAoAEBsAEKwAEB',
        'sclient':' gws-wiz'
    }

    headers={
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'accept-language':'en-GB,en-US;q=0.9,en;q=0.8',
        'cache-control':'max-age=0',
        'cookie':'HSID=AB8EBvl1soHbfbWXU; SSID=Aj5iDAe5vawQPpDKY; APISID=J67hhZqbbMpkZTEn/AtS55kBNTFjs-zsxH; SAPISID=NAX_b6mqpwDTCeD9/AaFClApNzsEC43QeX; __Secure-3PAPISID=NAX_b6mqpwDTCeD9/AaFClApNzsEC43QeX; __Secure-1PAPISID=NAX_b6mqpwDTCeD9/AaFClApNzsEC43QeX; SID=HwhcfE0uAfs_EF0Kmni6jC3uwecjSRWMrF-FsJwmmmayPt3siWG_GcO7a6dI475u_TYNFQ.; __Secure-1PSID=HwhcfE0uAfs_EF0Kmni6jC3uwecjSRWMrF-FsJwmmmayPt3sKRaTQ55ftooiOhSFiChB1A.; __Secure-3PSID=HwhcfE0uAfs_EF0Kmni6jC3uwecjSRWMrF-FsJwmmmayPt3sg1tTOcN889a5V-R6To3ibQ.; OTZ=6410536_34_34__34_; OGPC=19027092-2:; SEARCH_SAMESITE=CgQIjJUB; NID=511=pIvcybSdv_skx-sCpbKY0CwNVbc_GbOJLj8Cj757NtaPYjsZplgZjTepIxJjGWZBHKe95Amess5OL2cycVcBsF1u8bXpXjKyDSPv_b3qxITeYnFAPHnAy1IliGmwua2TyC-Kkrf2ZXOkSVL1Y73z2F9nyNO9jiQ0SqjyWFvpVc2nXOyRW8LtxQS8lWtbtdC-6ubebFIVdmIFnVpowUkd3jwpKHeF2S7Mb50RY_hmXVH88t1vMLcb41aXybQnc6pb7zKsMFMpzi0oG5mIQEPwAu94VGN7kwZrT6RuM9jOMnzjDy4J2--rgesRDMlM2nJP2xccEsflNv-K1gLNHICS9BZzZZm5_5Oi7FmaCK3Hw4UDEMdKTDu_JG_o671-5QF1hyt4namgFM-K7R9x_gOwvnU; AEC=AVQQ_LDQEKnBn8PdDJrA-FwkNuHcwCP5LnzB1ENrSVb8MgomRCIta4AQXQ; 1P_JAR=2022-04-03-05; DV=41hyXXpef7RbECBuCtWvdH2XoZve_hewjap4JjqDrAIAAICGSTB--aTywAAAAFj9N_RUZyHkOQAAALeat0bEMS8mDwAAAA; SIDCC=AJi4QfGMcys6aTfOBMRv8TrleyUkq0zN1ailLczZGr7b5Kv0JB4F2OWX3rCsq8PcbnUmqfyT0HbK; __Secure-3PSIDCC=AJi4QfEdKt6uA7rXjNUE_QfptjUx_vsGMXIrc6SF3r9AU5YYsGiqjIUuITQm7IGCnTaT9pS8Z3A',
        'referer':'https://www.google.com/',
        'upgrade-insecure-requests':'1',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.84 Safari/537.36'
    }

    params['q']=userquery
    
    response=requests.get(base_url,params=params,headers=headers)

    if response.status_code==200:
        # print("saving respond/n")
        with open('res.html','w',encoding='utf-8') as html_file:
            html_file.write(response.text)
        # print('done')
    # else:
    #     # print('bad response')
    html=''
    with open('res.html','r',encoding='utf-8') as f:
        for line in f.read():
            html+=line

    content=BeautifulSoup(html,'lxml')
        # print(html)
    # if content.findAll('span',{'class':'hgKElc'})!=[]:
    #     return(content.findAll('span',{'class':'hgKElc'})[0])
    # elif content.findAll('a',{'class':'FLP8od'})!=[]:
    #     title=content.findAll('a',{'class':'FLP8od'})
    #     return (str(title[0]).split(">")[1].split("<")[0])
    # elif content.findAll('div',{'class':'Z0LcW'})!=[]:
    #     return str(content.findAll('div',{'class':'Z0LcW'}))
    # elif content.findAll('div',{'class':'IZ6rdc'})!=[]:
    #     return str(content.findAll('div',{'class':'IZ6rdc'}))
    # else:
    #     return "I am stil learning, please keep posted I will be answer that in the future"
    if content.findAll('span',{'class':'hgKElc'})!=[]:
        return str(content.findAll('span',{'class':'hgKElc'})[0])
    elif content.findAll('div',{'class':'kno-rdesc'})!=[]:
        title=content.findAll('div',{'class':'kno-rdesc'})
        return str(title[0]).split(">")[4]
    else:
        return "I am stil learning, please keep posted I will be answer that in the future"

def pdfscrapper(userquery,department):
    if department=='p1':
        with open(r'BOOKS\11th\phy.txt','rb') as f:
            lines=f.readlines()
        txt=str(lines).split(",",1)[1]
        txtsplit=txt.split("\\n")
        tokenizedpdf=[]
        for i in txtsplit:
            temp=str(i).replace("\\","")
            tokenizedpdf.append(temp)
        while("" in tokenizedpdf) :
            tokenizedpdf.remove("")
        tokenizedpdf=tokenizedpdf[:-1]

    elif department=='p2':
        with open(r'BOOKS\12th\phy.txt','rb') as f:
            lines=f.readlines()
        txt=str(lines).split(",",1)[1]
        txtsplit=txt.split("\\n")
        tokenizedpdf=[]
        for i in txtsplit:
            temp=str(i).replace("\\","")
            tokenizedpdf.append(temp)
        while("" in tokenizedpdf) :
            tokenizedpdf.remove("")
        tokenizedpdf=tokenizedpdf[:-1]

    elif department=='b1':
        with open(r'BOOKS\11th\bio.txt','rb') as f:
            lines=f.readlines()
        txt=str(lines).split(",",1)[1]
        txtsplit=txt.split("\\n")
        tokenizedpdf=[]
        for i in txtsplit:
            temp=str(i).replace("\\","")
            tokenizedpdf.append(temp)
        while("" in tokenizedpdf) :
            tokenizedpdf.remove("")
        tokenizedpdf=tokenizedpdf[:-1]

    elif department=='b2':
        with open(r'BOOKS\12th\bio.txt','rb') as f:
            lines=f.readlines()
        txt=str(lines).split(",",1)[1]
        txtsplit=txt.split("\\n")
        tokenizedpdf=[]
        for i in txtsplit:
            temp=str(i).replace("\\","")
            tokenizedpdf.append(temp)
        while("" in tokenizedpdf) :
            tokenizedpdf.remove("")
        tokenizedpdf=tokenizedpdf[:-1]

    else:
        return "Please Select an appropriate Department for your queries"

    keywords=keyword_extractor(userquery)

    context=''
    for i in range(0,len(tokenizedpdf)):
        if set(keywords[0][0].split()).issubset(set(tokenizedpdf[i].split())):
            print(i)
            for j in range(i,i+20):
                context+=tokenizedpdf[j+1]
            break

    model=BertForQuestionAnswering.from_pretrained('bert-large-uncased-whole-word-masking-finetuned-squad')
    tokenizer=BertTokenizer.from_pretrained('bert-large-uncased-whole-word-masking-finetuned-squad')
    question = userquery
    context = context
    input_ids = tokenizer.encode(question, context)
    print('The input has a total of {:} tokens.'.format(len(input_ids)))
    tokens = tokenizer.convert_ids_to_tokens(input_ids)
    for token, id in zip(tokens, input_ids):
        if id == tokenizer.sep_token_id:
            print('')
        print('{:<12} {:>6,}'.format(token, id))
        if id == tokenizer.sep_token_id:
            print('')
    sep_index = input_ids.index(tokenizer.sep_token_id)
    num_seg_a = sep_index + 1
    num_seg_b = len(input_ids) - num_seg_a
    segment_ids = [0]*num_seg_a + [1]*num_seg_b
    assert len(segment_ids) == len(input_ids)
    outputs = model(torch.tensor([input_ids]), 
                                token_type_ids=torch.tensor([segment_ids]),
                                return_dict=True)
    start_scores = outputs.start_logits
    end_scores = outputs.end_logits
    answer_start = torch.argmax(start_scores)
    answer_end = torch.argmax(end_scores)
    answer = ' '.join(tokens[answer_start:answer_end+1])
    answer = tokens[answer_start]
    for i in range(answer_start + 1, answer_end + 1):
        if tokens[i][0:2] == '##':
            answer += tokens[i][2:]
        else:
            answer += ' ' + tokens[i]

    return(answer)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/get")
def get_bot_response():
    userText = request.args.get('msg')
    # return pdfscrapper(userText)
    classifier=userText.split(",")
    print(classifier[0],classifier[1])
    if classifier[0]=="NO":
        with open('session.txt','r') as f:
            lines=f.readlines()
        return webscrapper(lines[0])
    elif classifier[0]=="YES":
        return "Happy to Help!"
    else:
        with open('session.txt','w') as f:
            f.truncate(0)
            f.write(classifier[0])
        temp=userText
        return(pdfscrapper(classifier[0],classifier[1]))

if __name__ == "__main__":
    app.run()