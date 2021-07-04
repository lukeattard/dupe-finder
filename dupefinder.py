from os import walk
from os import stat
import os
import sys

fGlobal = {}

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
                    wo = str(fDict) + "\n"
                    fileDB.writelines(wo)
                    fileDB.write("\n")
                    fKey = file + ' ' + str(stat(fullpath).st_size)
                    tmpDict = {}
                    tmpDict[fKey] = fGlobal.get(fKey, { 'filename': file, 'path': fullpath, 'size': (stat(fullpath)).st_size, 'modified': (stat(fullpath)).st_mtime, 'siblings': {}, 'printed': 0 })
                    newSibling = tmpDict[fKey].get('siblings')
                    #print("OldSib: ", newSibling)
                    newSibling[fullpath] = { 'filename': file, 'path': fullpath, 'size': (stat(fullpath)).st_size, 'modified': (stat(fullpath)).st_mtime }
                    tmpDict[fKey]['siblings'] = newSibling
                    fGlobal[fKey] = tmpDict[fKey]   
                    #print("heading: ", fKey)
                    #print("nothere: ", fGlobal[fKey].get('siblings').get(fullpath) )
                    #print("here: ", fGlobal[fKey],"\n")
                except Exception as e:
                    print("Error with: ", dirpath,"Error1: ", e)
                    continue

    except Exception as e:
        print("Error with: ", dirpath,"Error2: ", e)
        
    fileDB.close()
    return f

def main():
    args = sys.argv[1:]
    try:
        searchDirectory = args[1]
        print("here\n")
    except:
        searchDirectory = os.getcwd()
        pass

    files =  get_files(searchDirectory)

    dupeDB = open(r"./.dupeDB","w")
    existingFileName = []

    for cKey in fGlobal.keys():
        keyList = list(fGlobal[cKey]['siblings'].keys())
        if len(keyList) > 1:
            wo = "File: " + cKey.replace('\\','/') + " has " + str(len(keyList)) + " possible dupes:\n"
            print(wo)
            dupeDB.writelines(wo)
            for dupeFile in fGlobal[cKey]['siblings'].keys():
                wo = "\t" + dupeFile + "\n"
                print(wo)
                dupeDB.writelines(wo)
    dupeDB.close()
    return

def startSearch():
    print("to be implemented")
    return
if __name__ == "__main__":
    main()
