from urllib.request import urlopen
import re
from datetime import datetime
import sys

# global list of housing blocks
groups = []

def main(num):
    global groups
    filename = "selection.txt"
    readf(filename)
    filec(num)
    print(count_groups(num))

def filec(num):
    f = open("output.txt", "w")
    f.write("Time: " + str(datetime.now()) + "\n")
    count, counttogo = count_groups(num)
    i = 1
    for x in count:
        f.write("Number of " + str(i) + " person Blocks: " + str(x) + "\n")
        i += 1
    f.write("\n")
    i = 1
    for x in counttogo:
        f.write("Number of " + str(i) + " person Blocks left to pick before " + str(num) + ": " + str(x) + "\n")
        i += 1
    appts = readavail()
    f.write("\n")
    f.write("Number of Coles towers quad left not on second floor: " + str(appts))

# Method scrapes bowdoin websites and counts the number of tower appartments are available 
def readavail():
    page = urlopen("https://webapi.bowdoin.edu/starrez/BowdoinLottery.html")
    html_bytes = page.read()
    html = html_bytes.decode("utf-8")
    towers = re.findall("<div><strong>Room: </strong> <span>Tow-\w+</span></div>", html)
    badtowers = re.findall("<div><strong>Room: </strong> <span>Tow-02\w+</span></div>", html)
    return (len(towers) - len(badtowers))

# Reads text file with housing lottery info
def readf(filename):
    global groups
    file = open(filename, 'r', encoding="utf8")
    currgroup = 1
    groupsize = 1
    for x in file:
        info = x.split(" ")
        if int(info[0]) == currgroup:
            groupsize += 1
        else:
            group = Group(info[0], groupsize, info[2])
            groups.append(group)
            groupsize = 1
            currgroup += 1

# Counts blocks of different sizes
def count_groups(num):
    global groups
    count = [0,0,0,0,0,0,0,0]
    counttogo = [0,0,0,0,0,0,0,0]
    time = str(datetime.now()).split(" ")
    currtime = int(time[1][0:2] + time[1][3:5])
    for group in groups:
        strtime = group.time
        grouptime = int(strtime[0:2] + strtime[3:5])
        if grouptime > currtime and int(group.rank) < num:
            counttogo[group.size - 1] = counttogo[group.size - 1] + 1
        count[group.size - 1] = count[group.size - 1] + 1
    return count,  counttogo

# Group class stores important information about a group
class Group:
    def __init__(self, rank, size, time):
        self.rank = rank
        self.size = size
        self.time = time

    def __str__(self):
        toreturn = str(self.rank)  + " " + str(self.size) + " " + str(self.time)
        return toreturn
    
# Input the number of block
if __name__ == "__main__":
    main(sys.argv[1])
    