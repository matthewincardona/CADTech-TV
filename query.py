import json
import csv
import os
import re

#filepath to this script
SCRIPTPATH = os.path.dirname(os.path.realpath(__file__))

#this is the folder that holds all the raw json data
RAWDIR = SCRIPTPATH + "/files/"

#this is the folder that holds all the final schedule
CSVDIR = SCRIPTPATH + "/schedule/"
# dates = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]

count = 5
set = []
bigSet = {"Monday": {}, "Tuesday": {}, "Wednesday": {}, "Thursday": {}, "Friday": {}}
MARKER = "X"
NULLVAULE = ""
CURRENTYEAR = "2024"

STARTMARK = "07:00:00"
ENDMARK = "23:00:00"
csvSet = {"Monday": [], "Tuesday": [], "Wednesday": [], "Thursday": [], "Friday": []}
header = []
rowEntry = []
rowEntry.append("")
rowEntry.append(STARTMARK)

#Make bigSet that parse the data from json
for filename in os.listdir(RAWDIR):

    if filename[0] == ".":
        continue
    file = RAWDIR + filename
    token = filename.split(".")
    filename = token[0]
    f = open(file)
    data = json.load(f)

    #add the class to the bigSet (so that classes that doesn't have class for a day still shows up)
    for date in bigSet:
        if (filename not in bigSet[date].keys()):
            bigSet[date][filename]=[]

    for entry in data["data"]:
        #The json files includes both fall and spring semester, so need to update that
        if(entry.get("date").split("-")[0] == CURRENTYEAR):
            if(re.search("\D{4}\s*\d{3}",entry.get("meeting"))):
                if (entry.get("start") != "00:00:00"):

                    #get start time
                    startTimeMark = entry.get("start")
                    token = startTimeMark.split(":")

                    #round up to nearest 10th min
                    if token[1][1] == "5":
                        startTimeMark = token[0] + ":" + str(int(token[1]) + 5 )+ ":" + token[2]

                    #get end time
                    endTimeMark = entry.get("end")
                    token = endTimeMark.split(":")

                    #round down to nearest 10th min
                    if token[1][1] == "5":
                        endTimeMark = token[0] + ":" + str(int(token[1]) - 5 )+ ":" + token[2]

                    set = [startTimeMark,endTimeMark]
                    date = entry.get("day")

                    if(date in bigSet):
                        if (set not in bigSet[date][filename]):
                            bigSet[date][filename].append(set)
    f.close()

# making the header
while (STARTMARK != ENDMARK):
    token = STARTMARK.split(":")
    if ((int(token[1]) + 10) == 60):
        temp = int(token[0]) + 1
        if (temp < 10):
            temp = "0" + str(temp)
        STARTMARK = str(temp) + ":00:" + token[2]
    else:
        STARTMARK = token[0] + ":" + str(int(token[1]) + 10 )+ ":" + token[2]
    rowEntry.append(STARTMARK)
header = rowEntry
length = len(header)

#Make the class times into a 2d matrix
for date in bigSet:
    for classes in bigSet[date].keys():
        rowEntry = [NULLVAULE] * length
        rowEntry[0] = classes
        bigSet[date][classes].sort()
        IndexList = []
        count = 0
        indexCounter = 0
        marking = False
        for i in range (0,len(bigSet[date][classes])):
            startTimeMark = header.index(bigSet[date][classes][i][0])
            endTimeMark = header.index(bigSet[date][classes][i][1])
            if(startTimeMark in IndexList):
                firstToken = IndexList.pop()
            else:
                IndexList.append(startTimeMark)
            IndexList.append(endTimeMark)
        while (count < length):
            if(IndexList != []):
                if (indexCounter % 2 == 0):
                    if (count == IndexList[indexCounter]):
                        indexCounter += 1
                        marking = True
                elif(indexCounter % 2 == 1):
                    if(count == IndexList[indexCounter]):
                        indexCounter += 1
                        if(indexCounter == len(IndexList)):
                            indexCounter = 0
                        marking = False
            if (marking):
                rowEntry[count] = MARKER
            count += 1
        csvSet[date].append(rowEntry)

#write the data to csv files
for date in csvSet:
    CSVFileName = CSVDIR + date + ".csv"
    with open(CSVFileName, "w") as csvFile:
        csvWriter = csv.writer(csvFile, delimiter=",")
        csvWriter.writerow(header)
        csvSet[date].sort()
        for rows in csvSet[date]:
            csvWriter.writerow(rows)