import datetime
import csv
import os

#return a dict(str:bool) of all the class and if it's avaliable or not, if it returns and empty dict then it means that it's the weekend and all rooms are avaliable
#true means open, false means close
def GetClassAvailability():
    CSVDIR = os.path.dirname(os.path.realpath(__file__)) + "/schedule/"
    DATES = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
    MARKER = "X"
    ClassAvailability = {} 
    DateTimeNow = datetime.datetime.now() #it's being weird

    #only for weekday not weekend
    if(DateTimeNow.weekday()<5):
        #open files
        CSVFileName = CSVDIR + DATES[DateTimeNow.weekday()] + ".csv"
        with open(CSVFileName) as csvFile:
            csvReader = csv.reader(csvFile,delimiter=",")

            #grab the current time
            TimeHeader = next(csvReader)
            hour = str(DateTimeNow.hour)
            if hour == "0":
                hour = "00"
            minute = str(DateTimeNow.minute-DateTimeNow.minute%10)
            if minute == "0": 
                minute = "00"
            
            #grab the index of the time
            TimeIndex = TimeHeader.index(hour + ":" + minute + ":00")

            #add it to the dict
            for row in csvReader:
                if(row[TimeIndex] == MARKER):
                    ClassAvailability[row[0]] = False
                else:
                    ClassAvailability[row[0]] = True
    return(ClassAvailability)

#prints out the dict of class availability
print(GetClassAvailability())