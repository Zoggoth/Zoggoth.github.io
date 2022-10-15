import pickle
import tools

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
FCset = set()
for x in userIDToRankedPlays[usercode]:
    if x.misses == 0:
        if x.modCode & 258 == 0:
            FCset.add(x.beatmapID)
file = open("IDToBeatmap.pkl", "rb")
IDToBeatmap = pickle.load(file)
file.close()
todo = []
for x in IDToBeatmap:
    if IDToBeatmap[x].mode == 2:
        if IDToBeatmap[x].status <= 2:
            if IDToBeatmap[x].ID not in FCset:
                todo.append((IDToBeatmap[x], tools.catchPP(IDToBeatmap[x].difficulty[0], IDToBeatmap[x].maxCombo, IDToBeatmap[x].maxCombo, 0, IDToBeatmap[x].AR, 0, 1)))
todo.sort(key=lambda item: item[1])
file = open("IDToBeatmapSet.pkl", "rb")
IDToBeatmapSet = pickle.load(file)
file.close()
for x in todo:
    print("{:.2f}".format(x[0].difficulty[0]) + "* " + "{:.2f}".format(x[1]) + " pp: " + IDToBeatmapSet[x[0].beatmapSetID].artist + " - " + IDToBeatmapSet[x[0].beatmapSetID].title + " [" + x[0].difficultyName + "]")
