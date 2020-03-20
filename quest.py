""" DOCSTRING """

import sys
import camelot

if len(sys.argv) > 2:
    print("USAGE : python3 quest.py [OPTIONAL_FILENAME]")
    sys.exit()

filename = "quests_for_question.pdf"
if len(sys.argv) == 2:
    filename = sys.argv[1]

# use camelot to read in spreadsheet values from PDF
tables = camelot.read_pdf(filename, split_text=True)

# Data will hold the data for each quest
class Data:
    """ Data will hold the data for each quest """
    def __init__(self, name, start, duration, reward):
        self.name = name
        self.start = start
        self.duration = duration
        self.reward = reward

# container to just hold and sort quest based on start day
# maxpossible is a size 32 array (for easy indexing based on day) that
#   holds the max rupees Link can earn on each day
# tracker holds names of quests he must take to obtain the value in maxpossible
container = []
maxpossible = []
tracker = []

# comparator function that will be used to sort container
def getstart(data):
    """ comparator function that will be used to sort container """
    return data.start

# From data read in by Camelot, store data in the class in container
for i in range(0, len(tables[0].df)):
    container.append(Data(tables[0].df.iloc[i][0], int(tables[0].df.iloc[i][1]),
                          int(tables[0].df.iloc[i][2]), int(tables[0].df.iloc[i][3])))

# sort container based on start date
container.sort(key=getstart)

# initialize maxpossible and tracker to size 32 (so we can index till day 31)
for i in range(0, 32):
    maxpossible.append(0)
    tracker.append([])

# in maxpossible, if we find a quest combination that yields more rupees than the previous,
#   update both maxpossible and tracker with relevant data
for stuff in container:
    mx = max(maxpossible[:stuff.start + 1])
    mx_idx = maxpossible.index(mx)

    cur_max = maxpossible[stuff.start + stuff.duration]
    if cur_max < mx + stuff.reward:
        maxpossible[stuff.start + stuff.duration] = mx + stuff.reward
        tracker[stuff.start + stuff.duration] = tracker[mx_idx].copy()
        tracker[stuff.start + stuff.duration].append(stuff.name)

# find thev value and list_index of the most income.
max_rupees = max(maxpossible)
idx = maxpossible.index(max_rupees)

print("MAX RUPEES :", max_rupees)
print("QUEST TO TAKE :")

for rpee in tracker[idx]:
    print(" ", rpee)
