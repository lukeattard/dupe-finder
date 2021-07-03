from os import walk
from os import stat

def get_files(mypath):
    fileDB = open(r"./.tmpList","w")
    f = []
    try:
        for (dirpath, dirnames, filenames) in walk(mypath):
            print('Processing:', dirpath)
        
            for file in filenames:
                try:
                    fullpath = dirpath + '/'+ file
                    fdict = { 'filename': file, 'path': fullpath, 'size': (stat(fullpath)).st_size, 'modified': (stat(fullpath)).st_mtime }
                    f.append(fdict)
                    fKey = file + " " + str(stat(fullpath).st_size)
                    fGlobal[fKey] = { 'filename': file, 'path': fullpath, 'size': (stat(fullpath)).st_size, 'modified': (stat(fullpath)).st_mtime, 'siblings': fdict, 'printed': 0}
                    fGlobal[fKey]['siblings'][fullpath] = fdict
                    #fileDB.write(str(fdict))
                    #fileDB.write("\n")
                except Exception as lerr:
                    print("Error with: ", dirpath,"Error: ",lerr)
                    continue
    except Exception as err:
        print("Error with: ", dirpath,"Error: ",err)
    fileDB.close()
    return f

fGlobal = {}
files =  get_files('/mnt/f/')

dupeDB = open(r"./.dupeDB","w")
existingFileName = []

for file in files:
    existingFileName.append("FileName:")
    for tmp in files:
        if (file['filename'] == tmp['filename']) and (file['size'] == tmp['size']) :
            #print("Here: ", type(tmp))
            lKey = file['filename'] + " " + str(file['size'])
            fGlobal[lKey]['siblings'][tmp['path']] = tmp
            #if existingFileName.count(file['filename']) < 1:
                #print("herer2: ",fGlobal[tmp['path']]['siblings'])
            #    existingFileName.append(file['filename'])
    keyList = fGlobal[lKey]['siblings'].keys()
    if len(keyList) > 1 and fGlobal[lKey]['printed'] == 0:
        print("Possible dupes found for: ", lKey, f"\n")
        fGlobal[lKey]['printed'] = 1
        for dupe in keyList:
            print(fGlobal[lKey]['siblings'][dupe]['path'])
        # if len(siblings) > 0:
        # print('Potential duplication for file', file['filename'])
        # for f in siblings:
            # #print('\tSize:', f['size'], '\tModified:', f['modified'], '\tPath:', f['path'])
            # dupeRecord = { 'file': file['filename'], 'path': f['path'], 'size': f['size'], 'modified': f['modified'] }
            # #print(str(dupeRecord))
            # dupeDB.write(str(dupeRecord))
            # dupeDB.write("\n")
    #for dup in fGlobal:
        #fGlobal[dup]['siblings'] = list(dict.fromkeys(fGlobal[dup]['siblings']))
        #print (fGlobal[dup]['siblings'])
       #print(f"\n\n")
for dup in fGlobal:
    keyList = fGlobal[dup]['siblings'].keys()
    if len(keyList) > 1:
        print("Possible dupes found for: ", dup, f"\n")
        for dupe in keyList:
            print(fGlobal[dup]['siblings'][dupe]['path'])
dupeDB.close()
