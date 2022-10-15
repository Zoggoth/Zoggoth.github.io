# It would be way better to do this with API calls, but I'm not hammering the API for this nonsense
import pickle
import math

player = 2799946
file = open("userIDToRankedPlays.pkl", "rb")
userIDToRankedPlays = pickle.load(file)
file.close()
file = open("IDToBeatmap.pkl", "rb")
IDToBeatmap = pickle.load(file)
file.close()
file = open("IDToBeatmapSet.pkl", "rb")
IDToBeatmapSet = pickle.load(file)
file.close()
IDtoFCs = {}
for x in IDToBeatmap:
    if IDToBeatmap[x].mode == 2:
        if IDToBeatmap[x].status <= 2:
            IDtoFCs[x] = 0
currentDate = 0
playerSet = set()
for x in userIDToRankedPlays:
    FCSet = set()
    for y in userIDToRankedPlays[x]:
        currentDate = max(currentDate, y.date)
        if y.beatmapID in IDtoFCs:
            if y.misses == 0:
                if y.modCode & 258 == 0:
                    FCSet.add(y.beatmapID)
    for y in FCSet:
        IDtoFCs[y] += 1
    if x == player:
        playerSet = FCSet
perYearList = []
for x in IDtoFCs:
    FCsPerYear = 31556952*float(IDtoFCs[x])/(currentDate-IDToBeatmapSet[IDToBeatmap[x].beatmapSetID].date)
    FCsPerRootYear = float(IDtoFCs[x])/math.sqrt((currentDate-IDToBeatmapSet[IDToBeatmap[x].beatmapSetID].date)/31556952)
    perYearList.append((x, FCsPerYear, FCsPerRootYear))
perYearList.sort(key=lambda item: item[1])
file = open("FCsPerYear.txt", "w")
file.write("Non-EZ/HT FCs per year since ranked.\nOverweights new maps. This is fixed in FCsPerRootYear.txt.\nOnly counts FCs by the top 10k. Fixing requires a new data source.\n\n")
file2 = open("PlayerFCsPerYear.txt", "w")
rank = 1
for x in perYearList:
    file.write(str(rank) + " - {:.2f}".format(IDToBeatmap[x[0]].difficulty[0]) + "* " + IDToBeatmapSet[IDToBeatmap[x[0]].beatmapSetID].artist + " - " + IDToBeatmapSet[IDToBeatmap[x[0]].beatmapSetID].title + " [" + IDToBeatmap[x[0]].difficultyName + "]: " + "{:.2f}".format(x[1])+"\n")
    if x[0] in playerSet:
        file2.write(str(rank) + " - {:.2f}".format(IDToBeatmap[x[0]].difficulty[0]) + "* " + IDToBeatmapSet[IDToBeatmap[x[0]].beatmapSetID].artist + " - " + IDToBeatmapSet[IDToBeatmap[x[0]].beatmapSetID].title + " [" + IDToBeatmap[x[0]].difficultyName + "]: " + "{:.2f}".format(x[1]) + "\n")
    rank += 1
file.close()
file2.close()
perYearList.sort(key=lambda item: item[2])
file = open("FCsPerRootYear.txt", "w")
file.write("Non-EZ/HT FCs/sqrt(years since ranked).\nTop is weird maps (why I made this). Bottom is farm maps.\nThe actual curve could be anything concave & increasing, but sqrt's easy to implement.\nStill has much of the same problems as FCsPerYear.txt\n\n")
file2 = open("PlayerFCsPerRootYear.txt", "w")
rank = 1
for x in perYearList:
    file.write(str(rank) + " - {:.2f}".format(IDToBeatmap[x[0]].difficulty[0]) + "* " + IDToBeatmapSet[IDToBeatmap[x[0]].beatmapSetID].artist + " - " + IDToBeatmapSet[IDToBeatmap[x[0]].beatmapSetID].title + " [" + IDToBeatmap[x[0]].difficultyName + "]: " + "{:.2f}".format(x[2])+"\n")
    if x[0] in playerSet:
        file2.write(str(rank) + " - {:.2f}".format(IDToBeatmap[x[0]].difficulty[0]) + "* " + IDToBeatmapSet[IDToBeatmap[x[0]].beatmapSetID].artist + " - " + IDToBeatmapSet[IDToBeatmap[x[0]].beatmapSetID].title + " [" + IDToBeatmap[x[0]].difficultyName + "]: " + "{:.2f}".format(x[2]) + "\n")
    rank += 1
file.close()
file2.close()
