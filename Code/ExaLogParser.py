from pandas import read_csv,isna
import re

'''
Description: Extracts scoring events from the event log csv
  Default dir value for now is C:\\Users\\us86497\\Documents\\TestLogs\\
  Eventually this will be changed to C:\\Users\\us86497\\Downloads, plan to add a flag that gives the user an option to change the path
Input: path to the event log csv file
Returns: a list of the scoring events
'''
def getScoringEvents(path):
    events = read_csv(path, header=0)
    scoringEvents = []

    for _,event in events.iterrows():
        # Check if the risk reason is NaN
        #   True: We don't care about that event, move on
        #   False: Save the event to the scoring events list
        if isna(event["Risk Reason"]):
            continue
        else:
            scoringEvents.append(event)
    return scoringEvents

'''
Description: parses the scoring events and presents them to the user, asks what events they are intersted in
Input: list of scoring events from the event log file
Returns: a list of events selected by the user
'''
def filterScoringEvents(scoringEvents):
    # First, the events need to be sorted in order of their score value
    # Start by extracting the scores from the risk reasons in each event data structure and adding it as a new key,value pair
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
        # Add a score key, value pair to the dictionary of the current event log
        event["Score"] = score
    # Sort the list by the score key
    scoringEvents.sort(key=lambda x: x.Score, reverse=True)

    index = 1
    print("Option\t\tScore\t\tRisk Reason")
    for event in scoringEvents:
        print("[" + str(index) + "]\t\t" + str(event["Score"]) + "\t\t" + event["Risk Reason"])
        index+=1
    print("\nSpecify desired logs with corresponding value, list of comma separated values, or range of values (ex. 1-5)")
    selections = input("Selections: ").split(',')
    selectionsset = set([ ])
    # Iterate through the user's input, if int(x) generates a ValueError that means it is a range (lower-upper)
    for x in selections:
        try:
            singleSet = set([int(x)])
            selectionsset = selectionsset.union(singleSet)
        except ValueError:
            # Remove the 'x-y' value from selections, we only want integers in the set
            r = [ int(val) for val in x.split('-') ]
            # Using sets to avoid duplicate values, generate a range of values and union them with the rest of the selections
            # Lower bound of range must be less then the upper bound
            selectionsset = selectionsset.union(set([ val for val in range(r[0],r[1]+1) ] if r[0] < r[1] else []))
    selections = list(selectionsset)
    # dropna() is used to remove null values from the data
    selectedEvents = [ scoringEvents[index].dropna() for index in selections ]
    return selectedEvents


