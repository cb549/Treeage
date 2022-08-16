import pandas
import os

# Description: Extracts scoring events from the event log csv
#   Default dir value for now is C:\\Users\\us86497\\Documents\\Treeage\\Data\\TestLogs\\
#   Eventually this will be changed to C:\\Users\\us86497\\Downloads, plan to add a flag that gives the user an option to change the path
# Input: path to the event log csv file
# Returns: a list of the scoring events
def getScoringEvents(path='C:\\Users\\us86497\\Documents\\Treeage\\Data\\TestLogs\\'):
    events = pandas.read_csv(path + 'fbfs01.csv', header=0)
    scoringEvents = []

    for index,event in events.iterrows():
        # Check if the risk reason is NaN
        #   True: We don't care about that event, move on
        #   False: Save the event to the scoring events list
        if pandas.isna(event["Risk Reason"]):
            continue
        else:
            scoringEvents.append(event)
    return scoringEvents

# Description: parses the scoring events and presents them to the user, asks what events they are intersted in
# Input: list of scoring events from the event log file
# Returns: a list of events selected by the user
def filterScoringEvents(scoringEvents):
    # First, the events need to be sorted in order of their score value
    for event in scoringEvents:
        riskReasons = event["Risk Reason"]
        scoreIndexStart = 0
        score = 0
        # Risk reason strings are structured as follows: "Reason1 for score (score);Reason2 for score (score)"
        # Some have multiple scoring reasons, some do not
        # While loop iterates through the risk reason string and combines all score values until no more score values are detected
        while riskReasons.find('(',scoreIndexStart) != -1:
            scoreIndexStart = riskReasons.find('(',scoreIndexStart)+1
            scoreIndexStop = riskReasons.find(')',scoreIndexStart)
            score += int(riskReasons[scoreIndexStart:scoreIndexStop])
        # Add a score key, value pair to the dictionary of the specific event log
        event["Score"] = score

    index = 1
    print("Option\t\tScore\t\tRisk Reason")
    for event in scoringEvents:
        print("[" + str(index) + "]\t\t10\t\t" + event["Risk Reason"])
        index+=1
    print("\nSelect events you wish to include in the report by typing the event's correspoding option value into the terminal.")
    print("Multiple events can be selected at a time by entering each number in a single line separated by commas\n")
    options = input("Options: ")


scoringEvents = getScoringEvents()
eventsOfInterest = filterScoringEvents(scoringEvents)
# print(eventsOfInterest)