#!/usr/bin/env python

import requests
import json


# Converts AWS EC2 instance metadata to a dictionary
def load():
    metaurl = 'http://169.254.169.254/latest'
    # those 3 top subdirectories are not exposed with a final '/'
    metadict = {'dynamic': {}, 'meta-data': {}, 'user-data': {}}

    for subsect in metadict.keys():
        crawl('{0}/{1}/'.format(metaurl, subsect), metadict[subsect])

    return metadict


def crawl(url, d):
    r = requests.get(url)
    if r.status_code == 404:
        return

    for l in r.text.split('\n'):
        if not l: # "instance-identity/\n" case
            continue
        newurl = '{0}{1}'.format(url, l)
        # a key is detected with a final '/'
        if l.endswith('/'):
            newkey = l.split('/')[-2]
            d[newkey] = {}
            crawl(newurl, d[newkey])

        else:
            r = requests.get(newurl)
            if r.status_code != 404:
                try:
                    d[l] = json.loads(r.text)
                except ValueError:
                    d[l] = r.text
            else:
                d[l] = None

if __name__ == '__main__':
    val = raw_input("Enter your key with path (leave blank or type 'all' for all data): ")
    try:
        if val == 'all' or len(val) == 0:
            print(json.dumps(load(), indent = 1))
        else:
            value = val.split('/')
            allData = load()
            keyLength = len(value)
            valueToReturn = ''
            try:
                for i in range(keyLength):
                    if keyLength == 1 or i == (keyLength-1):
                        valueToReturn = allData.get(value[i])
                    else:
                        allData = allData.get(value[i])
                if(type(valueToReturn) is dict):
                    print(json.dumps(valueToReturn, indent = 1))
                else:
                    if valueToReturn == None:
                        print('Key Not Found')
                    else:
                        print(valueToReturn)
            except:
                print('Invalid key path', val)
    except EOFError as e:
        print(json.dumps(load(), indent = 1))

        
