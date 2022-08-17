from Code.ExaLogParser import *
from argparse import ArgumentParser
from pathlib import Path
from os import listdir,remove

parser = ArgumentParser()
parser.add_argument("-d", "--directory", help="Change the default directory of the log file")
parser.add_argument("-k", "--keep", help="Keep the .csv file after the script concludes (Default is to remove it).", action="store_true")
args = parser.parse_args()

path = args.directory
if not path:
    path = str(Path.home() / "Downloads")
    csvFiles = []
    for file in listdir(path):
        if file.endswith(".csv"):
            csvFiles.append(file)
    if len(csvFiles) == 0:
        print("No .csv files found in Downloads directory. Try downloading a log file or specify a custom path with -d.")
        exit(0)
    elif len(csvFiles) == 1:
        path += "\\" + csvFiles[0]
    else:
        print("Multiple .csv files found in downloads directory, please specify your desired file.")
        for file in csvFiles:
            print("[" + str(csvFiles.index(file)) + "] " + file)
        selection = int(input("Select file: "))
        path += "\\" + csvFiles[selection]

scoringEvents = getScoringEvents(path)
selectedEvents = filterScoringEvents(scoringEvents)
# print(selectedEvents)
for event in selectedEvents:
    print(event["Risk Reason"])
# Delete the log file after using it if the -k flag is not used
if not args.keep:
    remove(path)