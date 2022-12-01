import pickle

usercode = input("User number or name: ")
usingNumber = True
try:
    usercode = int(usercode)
except:
    usingNumber = False
if not usingNumber:
    file = open("IDToUser.pkl", "rb")
    IDToUser = pickle.load(file)
    file.close()
    for x in IDToUser:
        if IDToUser[x].name.upper() == str(usercode).upper():
            usercode = x
if isinstance(usercode, str):
    print("Couldn't find username")
    print("Check user is top 10,000, check spelling or try user number")
    exit()
file = open("userIDToRankedPlays.pkl", "rb")
userIDToRankedPlays = pickle.load(file)
file.close()
file = open("userIDToLovedPlays.pkl", "rb")
userIDToLovedPlays = pickle.load(file)
file.close()
file = open("IDToBeatmap.pkl", "rb")
IDToBeatmap = pickle.load(file)
file.close()
allplays = []
try:
    allplays = userIDToRankedPlays[usercode] + userIDToLovedPlays[usercode]
except:
    print("Couldn't find user")
    print("Check user is top 10,000 & check spelling")
    exit()
IDToTopScore = {}
for x in allplays:
    if x.beatmapID in IDToTopScore:
        if x.score > IDToTopScore[x.beatmapID].score:
            IDToTopScore[x.beatmapID] = x
    else:
        IDToTopScore[x.beatmapID] = x
topScoreList = sorted(IDToTopScore.items(), key=lambda item: item[1].misses, reverse=True)
topScoreList.sort(key=lambda item: item[1].rank[0])
currentrank = ""
misses = False
count = 0
for x in topScoreList:
    if IDToBeatmap[x.beatmapID].status == 1:
        count += 1
    if x[1].rank[0] == "X":
        exit()
    if x[1].rank[0] != currentrank:
        currentrank = x[1].rank[0]
        print(currentrank + " ranks")
        if currentrank == "S":
            if x[1].misses:
                print("With misses")
                misses = True
            else:
                print("Without misses")
                misses = False
    if misses:
        if not x[1].misses:
            print("Without misses")
            misses = False
    print("https://osu.ppy.sh/scores/fruits/" + str(x[1].ID))
print(count)