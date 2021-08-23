import json
import os
import requests
import time
from ml import spacy_tokenizer

def get_page(_id):
    annotations = json.load(open('annotations.json','r',encoding='utf-8'))
    keys = list(annotations.keys())
    title = keys[int(_id)]
    page = annotations[title]
    page.update({'title':title.replace('.json','')})
    return page

def get_text(text_object):
    if type(text_object)==list:
        return '\n'.join([get_text(to) for to in text_object])
    elif text_object and 'pages' in text_object:
        return '\n'.join([get_text(i) for i in text_object['pages']])
    elif text_object and 'elements' in text_object:
        return '\n'.join([get_text(i) for i in text_object['elements']])
    elif text_object and text_object['type'] in ['paragraph', 'heading','list']:
        return '\n'.join([get_text(i) for i in text_object['content']])
    elif text_object and text_object['type'] in ['line']:
        return ' '.join([get_text(i) for i in text_object['content']])
    elif text_object and text_object['type'] in ['word']:
        if type(text_object['content']) is list:
            return ' '.join([get_text(i) for i in text_object['content']])
        else:
            return text_object['content']
    elif text_object and text_object['type'] in ['character']:
        return text_object['content']
    else:
        return ""

def process_job(filename):
    url = "http://localhost:3001/api/v1/"
    config = 'config.json'
    packet = {
                'file': (filename, open(filename, 'rb'), 'application/pdf'),
                'config': (config, open(config, 'rb'), 'application/json'),
            }
    r = requests.post(url+'document', files=packet)    
    jid = r.text
    finished = False
    tstart = time.time()
    while not finished:
        time.sleep(0.5)
        status = requests.get(url+'queue/{}'.format(jid))
        status = json.loads(status.text)
        if 'json' in status:
            finished = True
        if time.time()-tstart>5*60:
            print('Job time >5min. Skipping '+filename)
            return {}

    res = requests.get(url+'json/'+jid)
    return res.json()['pages']

def pdf_to_json():
    fdir = 'pdfs'
    jdir = 'jsons'
    files = os.listdir(fdir)
    for file in files:
        print(file)
        ffile = os.path.join(fdir, file)
        if os.path.isdir(ffile):
            subfiles = os.listdir(ffile)
            jfile = file+".json"
            if jfile not in os.listdir(jdir):
                for i,sub in enumerate(subfiles):
                    try:
                        filename = os.path.join(ffile,sub)
                        if i==0:
                            pdf_json = process_job(filename)
                        else:
                            pdf_json += process_job(filename)
                    except:
                        print('Failed ', sub)       
                with open(os.path.join(jdir, jfile), mode='w',encoding='utf-8') as f:
                    json.dump(pdf_json,f,indent=4)
        else:
            jfile = file.replace('.pdf',".json")
            if jfile not in os.listdir(jdir):
                try:
                    pdf_json = process_job(ffile)
                    with open(os.path.join(jdir, jfile), mode='w',encoding='utf-8') as f:
                        json.dump(pdf_json,f,indent=4)    
                except:
                    print('Failed ', file)    

def process_tokens():
    tdir = r"jsons"
    annotations = {}
    for i,file in enumerate(os.listdir(tdir)):
        jf = json.load(open(os.path.join(tdir, file)))
        page_text = get_text(jf)
        tokens = [{'text':t, "class":"o"} for t in spacy_tokenizer(page_text)]
        annotations.update({file:{'tokens':tokens,'annotated':False}})
    with open('annotations.json','w',encoding='utf-8') as f:
        json.dump(annotations,f,indent=4)

def update_page(id, tokens, annotated=True):
    annotations = json.load(open('annotations.json','r',encoding='utf-8'))
    keys = list(annotations.keys())    
    annotations[keys[id]]['tokens'] = tokens
    annotations[keys[id]]['annotated'] = annotated
    with open('annotations.json','w',encoding='utf-8') as f:
        json.dump(annotations,f,indent=4)
    return None

def get_annotated_pages(annotated=True):
    annotations = json.load(open('annotations.json','r',encoding='utf-8'))
    pages = {t:p for t,p in annotations.items() if p['annotated']==annotated}
    return pages