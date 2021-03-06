#
# Pyton program for Project 2, 2013s1
#
# Author: Naoko Nishimura
#
# User name: nnishimura
#
# Student ID: 620011
#
# Date: 13/9/15
#
# Modified 13/9/15 to add batch evaluate
#

import csv
import cPickle
from collections import defaultdict
import matplotlib
matplotlib.use('Svg')
from pylab import *
from operator import itemgetter
import math
from collections import OrderedDict


word=''
def strip_punc(word):
    word=word.strip(',.:;!?-"()[]{}')
    word=word.strip("'")
    return word.lower()

def make_index(datafile,picklefile):
    
    f1=open(datafile)
    data1=csv.reader(f1)
    url_desc_dict=defaultdict(str)
    
    for line1 in data1:
        '''make a dict of {URL:descriptions}'''
        
        url="http://www.youtube.com/watch?v="+line1[0]+"#t="+line1[1]+"s"
        description=strip_punc(line1[7])
        url_desc_dict[url]+=description+' '

    dict0=defaultdict(int) # will be dict1's sub dictionary
    dict1={} # will be 1st dict
    dict2_total=0 #count up total num of word tokens for dict2
    
    for url,desc in url_desc_dict.items():
        '''get freq for each word in desc'''
        
        for word in desc.split():
            dict0[strip_punc(word)]+=1
            
        dict0['__TOTAL__']=len(desc.split())
        dict1[url]=dict(dict0)#avoid output contains "defaultdict(<type 'int'>,..." 
        dict0=defaultdict(int)# initialize dict0 since we've added it to dict1
    
    dict2=defaultdict(int) # will be 2nd dict

    for dict0 in dict1.itervalues():
        '''for each word in all descriptions, get the num of doc that contains it'''
        for word in dict0.iterkeys():
            dict2[word]+=1
            
    dict2['__TOTAL__']=len(dict1)
    
    out=open(picklefile,"wb")
    '''store dict1 & dict2 to picklefile'''
    
    cPickle.dump(dict1,out)
    cPickle.dump(dict2,out)
    out.close()

def word_freq_graph(index_fname,graph_fname,word):
    
    pkl_file=open(index_fname,"rb")#open index_fname
    data=cPickle.load(pkl_file)
    
    freq_list=[] #store freq of word here
    
    for sub_dict in data.values():
        '''get freq of word in each video'''
        freq_list.append(sub_dict.get(strip_punc(word),0))
    
    if max(freq_list)==0:
        '''prevent xticks=[] when word doesnt exist in index_fname'''
        xticks_num=[0]
    else:
        xticks_num=range(min(freq_list),max(freq_list),5)
        
    clf()
    hist(freq_list,bins=int(max(freq_list))+1,log=True)
    xlim(0,max(freq_list))
    xticks(xticks_num)
    yticks([10**i for i in range(0,5)],[str(10**i) for i in range(0,5)])
    xlabel('frequency of word in description for a given video')
    ylabel('number of videos')
    title('histgram of word frequencies in video description')
    savefig(graph_fname)

    
mydict={} #{URL:score}
def sorted_url(mydict):#will be used in single_word_search () & search ()
    
    '''return a list of ranked URLs'''
    
    mytuples=[(k,v) for k, v in mydict.iteritems()]
    '''convert mydict into a list of tuples'''
    
    mytuples=sorted(mytuples, key=itemgetter(0)) #mytuples=[(URL,score)]
    '''sort mydict by URL in increasing order'''
    
    mytuples=sorted(mytuples, key=itemgetter(1),reverse=True)
    '''sort mydict by score in decreasing order'''
    
    return [x[0] for x in mytuples]#extract URLs

    
def single_word_search(index_fname,word):
        
    with open(index_fname,"rb") as dict1:
        data=cPickle.load(dict1)

    score_dict={}
    for url,freq_dict in data.items():
        if get_score(freq_dict,strip_punc(word))!=0:#avoid including zero score
            score_dict[url]=get_score(freq_dict,strip_punc(word))

    out= sorted_url(score_dict)#sorted_url(score_dict)
    return out

d={}
t=''
def get_score(d,t):#will be used in single_word_search() & search()
    '''get fdt/fd for one document, single word'''
    
    fdt=0 #default value of fdt

    if t in d.keys():
        fdt=d[t]
        
    return fdt/float(d['__TOTAL__'])


query=''
def search(index_fname,query):
     
    pkl_file=open(index_fname,"rb")#open index_fname
    data=cPickle.load(pkl_file)
      
    data_Q4=cPickle.load(pkl_file)

    queries=[strip_punc(x) for x in query.split()]
    #strip punc from query

    sum_of_wdt=0
    sum_of_sq_wdt=0
    rel_score_dict={}
    '''map URL with relevant score'''
    
    global total_doc
    total_doc=data_Q4['__TOTAL__']
    
    for url,dict0 in data.iteritems():
        '''sum up wdt & (wdt)**2 of queries for each document'''
        
        for query in queries:
            sum_of_wdt+=get_wdt(dict0,query)
            sum_of_sq_wdt+=(get_wdt(dict0,query)**2)

            if sum_of_wdt!=0 and math.sqrt(sum_of_sq_wdt)!=0:#prevent including zero score
                rel_score_dict[url]=sum_of_wdt/math.sqrt(sum_of_sq_wdt)
        sum_of_wdt=0
        sum_of_sq_wdt=0

    
    return sorted_url(rel_score_dict)


mydict={}
term=''
def get_wdt(mydict,term):#will be used in search()
    
    ft=mydict.get(term,0)
    
    return get_score(mydict,term)*(math.log(float(total_doc))-math.log(ft+1))


def rr(query,doc_ranking,qrels):
    
    stripped_query=''
    '''remove punc from each queries'''
    for q in query.split():
        stripped_query+=strip_punc(q)+' '
    stripped_query=stripped_query[:-1]#strip ' ' from the end of query('bird'!='bird_')
            
    csv_file=open(qrels)
    iter_qrels=csv.reader(csv_file)
    
    relevant_urls=[]
    '''get relevant videos in qrels'''
    for row in iter_qrels:
        if row[0] == stripped_query:
            relevant_urls.append("http://www.youtube.com/watch?v="+row[1]+"#t="+row[2]+"s")
    
    rank=[]
    '''get index of relevant URL'''
    for url in relevant_urls:
        if url in doc_ranking:
            rank.append(doc_ranking.index(url))
    
    if rank==[]:#no relavant URL=rr will be automatically 0
        output=0
    else:
        output=float(1)/(min(rank)+1)#index+1=actual rank
        
    return output      

def batch_evaluate(index_fname,queries,qrel,html_out):

    #1st table
    
    rr_dict=OrderedDict()#preserve the ordering of queries
    mrr=0
    for q in queries:
        '''map each query with its RR'''
        
        score=rr(strip_punc(q),search(index_fname,strip_punc(q)),qrel)
        
        mrr+=score#sum up RR to get MRR
        rr_dict[strip_punc(q)]=score
    
    rr_list=rr_dict.values()
    stripped_queries=rr_dict.keys()

    html_file = open(html_out,"w")
    html_file.write(str(print_table(stripped_queries,rr_list,mrr)))
    html_file.close()
    
    #2nd graph
    
    clf()
    barwidth=0.5
    bar_locations=range(len(rr_dict))
    bar(bar_locations,rr_list,width=barwidth)
    xlim(0-barwidth,len(rr_list))
    xticks([i+barwidth/2 for i in bar_locations],stripped_queries)
    title('RR for each query')
    xlabel('queries')
    ylabel('RR')
    savefig('nnishimura-rr.svg')
    
    #3rd graph
    
    length_mrr_dict=defaultdict(float)
    for query in stripped_queries:
        '''map length of each query and its MRR'''
        
        length_mrr_dict[len(query)]+=rr(query,search(index_fname,query),qrel)

    x_axis=length_mrr_dict.keys()#length
    y_axis=length_mrr_dict.values()#MRR
    
    clf()
    bar_locations=range(len(y_axis))
    bar(bar_locations,y_axis,width=barwidth)
    xlim(0-barwidth,len(x_axis))
    xticks([i+barwidth/2 for i in bar_locations],x_axis)
    title('MRR for queries of different length')
    xlabel('Length')
    ylabel('MRR')
    savefig('nnishimura-mrr.svg')

contents=''
def print_document(contents):
    return "<!DOCTYPE html>\n<html>\n<head>\n</head>\n<body>"+contents+"</body>\n</html>"

queries=[]
rr_list=[]
eg_mrr=0
def print_table(queries,mylist,eg_mrr):
    
    out = '<table border="1"><tr><th>queries</th>'
    for q in queries:
        out += "<td>" + str(q) + "</td>"
    out += "<th>MRR</th></tr>"
    out += "<tr><th>RR</th>"
    for rr in mylist:
        out += "<td>" + str(rr) + "</td>"
    out += "<td>"+str(eg_mrr)+"</td></tr></table>"
    
    return print_document(out)
