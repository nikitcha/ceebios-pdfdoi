import spacy
import requests
import time
import urllib
from urllib.error import HTTPError
import re
import json 
from fuzzywuzzy import fuzz
#!python -m spacy download en_core_web_lg

from spacy.lang.en import English
nlp = English()
nlp.tokenizer.url_match = None
infixes = nlp.Defaults.infixes + [r'\.', r'\/', r'\:\/\/'] 
infix_regex = spacy.util.compile_infix_regex(infixes)
nlp.tokenizer.infix_finditer = infix_regex.finditer

def spacy_tokenizer(text):
    doc = nlp(text)
    tokens = [t.text for t in doc]
    return tokens

def scholar_from_title(title):
    flds = ['title','authors','isOpenAccess', 'isPublishedLicensed', 'venue','year','url','fieldsOfStudy','doi','arxivId','topics','paperId']
    data = {}
    query = 'https://api.semanticscholar.org/graph/v1/paper/search?query={}&limit=1&fields=title'.format(title.replace(' ','+'))
    res = requests.get(query)
    res = res.json()
    if 'data' in res and len(res['data'])>0:
        pid = res['data'][0]['paperId']
        res = requests.get("https://api.semanticscholar.org/v1/paper/"+pid)
        paper = res.json()
    if 'title' in paper: 
        for k in flds:
            data.update({k:paper.get(k,"")})
    return data

def add_publisher(data):
    doi = data.get('doi','')
    if doi:
        url = 'http://dx.doi.org/' + doi
        req = urllib.request.Request(url)
        req.add_header('Accept', 'application/x-bibtex')
        bibtex = {}
        try:
            with urllib.request.urlopen(req) as f:
                bibtex = f.read().decode()
        except HTTPError as e:
            if e.code == 404:
                print('DOI not found.')
            else:
                print('Service unavailable.')
        key = 'publisher'
        v = re.findall(key+" = ({.*?})", bibtex)  
        if v:
            data.update({key:v[0].replace("{","").replace("}","")})
    return data


def crossref_from_title(title):
    query = 'https://api.crossref.org/works?query.bibliographic={}'.format(title.replace(' ','+'))
    res = requests.get(query)
    res = res.json()
    data = {}
    items = res['message']['items']
    for i in items:
        ratio = fuzz.ratio(title.lower(), ' '.join(i['title'][0].lower().split(' ')))
        if ratio>95:
            data = i
    return data

def unpaywall_from_doi(doi):
    q = "https://api.unpaywall.org/v2/{}?email=nikolay.tchakarov@ceebios.com".format(doi)
    res = requests.get(q)
    res = res.json()
    return res

def title_from_tokens(tokens):
    titles, this = [],[]
    for token in tokens:
        if 'title' in token['class']:
            this.append(token['text'])
        if 'e-' in token['class']:
            titles.append(this)
            this = []
    return titles

def get_dois(pages):
    dois = {}
    for p, page in pages.items():
        titles = title_from_tokens(page['tokens'])
        reflist = []
        for title in titles:
            time.sleep(0.05)
            ref = {'crossref':crossref_from_title(' '.join(title))}
            if 'DOI' in ref['crossref']:
                ref.update({'unpaywall':unpaywall_from_doi(ref['crossref']['DOI'])})
            reflist.append(ref)
        dois.update({p:reflist})
    with open('dois.json','w', encoding='utf-8') as f:
        json.dump(dois,f,indent=4)
