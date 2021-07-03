from os import walk
from os import stat
import sys

def get_files(mypath):
    fileDB = open(r"./.tmpList","w")
    f = []
    try:
        for (dirpath, dirnames, filenames) in walk(mypath):
            print('Processing:', dirpath)
        
            for file in filenames:
                try:
                    fullpath = dirpath + '/' + file
                    fDict = { 'filename': file, 'path': fullpath, 'size': (stat(fullpath)).st_size, 'modified': (stat(fullpath)).st_mtime }
                    f.append(fDict)
                    fKey = file + ' ' + str(stat(fullpath).st_size)
                    tmpDict = {}
                    tmpDict[fKey] = fGlobal.get(fKey, { 'filename': file, 'path': fullpath, 'size': (stat(fullpath)).st_size, 'modified': (stat(fullpath)).st_mtime, 'siblings': {}, 'printed': 0 })
                    newSibling = tmpDict[fKey].get('siblings')
                    print("OldSib: ", newSibling)
                    newSibling[fullpath] = { 'filename': file, 'path': fullpath, 'size': (stat(fullpath)).st_size, 'modified': (stat(fullpath)).st_mtime }
                    tmpDict[fKey]['siblings'] = newSibling
                    fGlobal[fKey] = tmpDict[fKey]   
                    print("heading: ", fKey)
                    print("nothere: ", fGlobal[fKey].get('siblings').get(fullpath) )
                    print("here: ", fGlobal[fKey],"\n")
                except:
                    e = sys.exc_info()[0]
                    ehook = sys.last_traceback
                    print("Error with: ", dirpath,"Error1: ", e)
                    print("Error Hook: ", ehook)
                    continue
    except:
        e = sys.exc_info()[0]
        ehook = sys.last_traceback
        print("Error with: ", dirpath,"Error2: ", e)
        print("Error Hook: ", ehook)
    fileDB.close()
    return f

fGlobal = {}
files =  get_files('/mnt/f/VMConf')

dupeDB = open(r"./.dupeDB","w")
existingFileName = []
print("there:",fGlobal.keys())

""" for file in files:

    lKey = file['filename'] + " " + str(file['size'])
    fullpath =  fGlobal[lKey]['path']
    keyList = list(fGlobal[lKey]['siblings'].keys())
    #print("here :",fGlobal[lKey]['siblings'],"\n")
    print("here2 : ",type(keyList),"  ",len(keyList), "\n\n")
    if len(keyList) > 1 and fGlobal[lKey]['printed'] == "0":
        print("Possible dupes found for: ", lKey, f"\n")
        fGlobal[lKey]['printed'] = 1
        for dupe in keyList:
            print(fGlobal[lKey]['siblings'][dupe]['path']) """
for cKey in fGlobal.keys():
    print("File name and size: ", cKey)
    print("Siblings: ",fGlobal[cKey]['siblings'],"\n\n")
    keyList = list(fGlobal[cKey]['siblings'].keys())
    if len(keyList) > 1:
        print("File: ",cKey," has ",len(keyList)," possible dupes:")
        print(fGlobal[cKey]['siblings'].keys())

dupeDB.close()
