from os import walk
from os import stat
import sys

def get_files(mypath):
    fileDB = open(r".\.tmpList","w")
    f = []
    try:
        for (dirpath, dirnames, filenames) in walk(mypath):
            print('Processing:', dirpath)
        
            for file in filenames:
                try:
                    fullpath = dirpath + '\\' + file
                    fDict = { 'filename': file, 'path': fullpath, 'size': (stat(fullpath)).st_size, 'modified': (stat(fullpath)).st_mtime }
                    f.append(fDict)
                    wo = str(fDict) + "\n"
                    fileDB.writelines(wo)

                    fKey = file + ' ' + str(stat(fullpath).st_size)
                    tmpDict = {}
                    tmpDict[fKey] = fGlobal.get(fKey, { 'filename': file, 'path': fullpath, 'size': (stat(fullpath)).st_size, 'modified': (stat(fullpath)).st_mtime, 'siblings': {}, 'printed': 0 })
                    newSibling = tmpDict[fKey].get('siblings')

                    newSibling[fullpath] = { 'filename': file, 'path': fullpath, 'size': (stat(fullpath)).st_size, 'modified': (stat(fullpath)).st_mtime }
                    tmpDict[fKey]['siblings'] = newSibling
                    fGlobal[fKey] = tmpDict[fKey]   
                except Exception as e:
                    print("Error with: ", dirpath,"Error1: ", e)
                    continue

    except Exception as e:
        print("Error with: ", dirpath,"Error2: ", e)
        
    fileDB.close()
    return f

fGlobal = {}
files =  get_files('F:\\Luke')

dupeDB = open(r".\.dupeDB","w")
existingFileName = []

for cKey in fGlobal.keys():
    keyList = list(fGlobal[cKey]['siblings'].keys())
    if len(keyList) > 1:
        wo = "File: " + cKey.replace('\\','/') + " has " + str(len(keyList)) + " possible dupes:\n\n"
        print(wo)
        dupeDB.writelines(wo)
        for dupeFile in fGlobal[cKey]['siblings'].keys():
            wo = "\t" + dupeFile
            print(wo)
            dupeDB.writelines(wo)
            dupeDB.write("\n")
dupeDB.close()
