import sys
import json
import requests
import subprocess

#dict storing data
collection={}

def execute_commandRealtime(cmd):
    """Execute shell command and print stdout in realtime.
    Function taken from pyrpipe Singh et.al. 2020
    usage:
    for output in execute_commandRealtime(['curl','-o',outfile,link]):
        print (output)
    """

    popen = subprocess.Popen(cmd, stdout=subprocess.PIPE, universal_newlines=True)

    for stdout_line in iter(popen.stdout.readline, ""):
            yield stdout_line
    popen.stdout.close()
    return_code = popen.wait()
    if return_code:
        raise subprocess.CalledProcessError(return_code, cmd)


def update_collection():
    '''
    Download bioarxiv and medarxiv collections
    '''
    link='https://connect.biorxiv.org/relate/collection_json.php?grp=181'
    outfile='collection.json'
    print('Downloading ...')
    for output in execute_commandRealtime(['curl','-o',outfile,link]):
        print (output)

def read_collection():
    '''
    open file
    '''
    filename='collection.json'
    with open(filename) as f:
        data = json.load(f)
    i=0
    for key,value in data.items() :
        #print (key,":",value)
        if key=='rels':
            val=data[key]
            print('{} records found'.format(len(val)))
            return value

def get_terms():
    print('Available terms:')
    for key,value in collection[0].items():
        print(key)

def search(term):
    #search in collection is a list of dicts
    print('Searching',term)
    result=[]
    for d in collection:
        for key,value in d.items():
            if term.lower() in str(value).lower():
                #print (d['rel_title'])
                result.append(d)
    print('total matches: {}'.format(len(result)))
    return result

def print_results(res):
    for d in res:
        print(d['rel_title'])

#step 1 update collection downloads around 15 MB .json data
#update_collection()

#read collection in memory
collection=read_collection()

#see available terms
#get_terms()

#perform search
res=search(' RNA-seq')

#print titles from result
print_results(res)
