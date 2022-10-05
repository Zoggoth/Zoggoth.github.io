import re
import tools
import pickle
import modLeaderboards

file = open("osu_beatmaps.sql", "r", encoding="utf-8")
text = file.read()
file.close()
capture = re.findall(r"\((\d+),(\d+),\d+,'[^']*?(?:\\'[^']*?)*','[0-f]*','([^']*?(?:\\'[^']*?)*)',(?:\d+(?:\.\d+)?,){9}(\d+(?:\.\d+)?),(\d),(\d)", text)
IDToBeatmap = {}
for x in capture:
    beatmap = tools.beatmap()
    beatmap.ID = int(x[0])
    beatmap.beatmapSetID = int(x[1])
    beatmap.difficultyName = x[2].replace(r"\'", "'")
    beatmap.AR = float(x[3])
    beatmap.mode = int(x[4])
    beatmap.status = int(x[5])
    beatmap.difficulty = {}
    IDToBeatmap[beatmap.ID] = beatmap
IDToBeatmap[2536330].difficulty = {0: 12.60, 2: 10.54, 16: 15.02, 64: 15.15, 66: 12.63, 80: 18.08, 256: 11.43, 258: 9.58, 272: 13.58}
file = open("osu_beatmap_difficulty.sql", "r")
text = file.read()
file.close()
capture = re.findall(r"\((\d+),2,(\d+),(\d+(?:\.\d+)?)", text)
for x in capture:
    IDToBeatmap[int(x[0])].difficulty[int(x[1])] = float(x[2])
file = open("osu_beatmapsets.sql", "r", encoding="utf-8", errors="replace")
text = file.read()
file.close()
capture = re.findall(r"\((\d+),\d+,\d+,'([^']*?(?:\\'[^']*?)*)',(?:NULL|'[^']*?(?:\\'[^']*?)*'),'([^']*?(?:\\'[^']*?)*)',", text)
IDToBeatmapSet = {}
for x in capture:
    beatmapSet = tools.beatmapSet()
    beatmapSet.ID = int(x[0])
    beatmapSet.artist = x[1].replace(r"\'", "'")
    beatmapSet.title = x[2].replace(r"\'", "'")
    IDToBeatmapSet[beatmapSet.ID] = beatmapSet
file = open("Country Codes.txt", "r")
text = file.read().split("\n")
file.close()
countryCodes = {}
for x in range(round(len(text)/2)):
    countryCodes[text[2*x]] = text[2*x+1]
file = open("osu_user_stats_fruits.sql", "r")
text = file.read()
file.close()
capture = re.findall(r"\((\d+),\d+,\d+,\d+,\d+,\d+,\d+,\d+(?:\.\d+)?,\d+,\d+,\d+,\d+,\d+,\d+,\d+,\d+,\d+,\d+(?:\.\d+)?,\d+,\d+,\d+,\d+,'(\w\w)',(\d+(?:\.\d+)?),(\d+)", text)
IDToUser = {}
for x in capture:
    user = tools.user()
    user.ID = int(x[0])
    user.country = x[1]
    if user.country not in countryCodes:
        print("Country " + user.country + " missing")
        countryCodes[user.country] = user.country
    user.pp = float(x[2])
    user.ppRank = int(x[3])
    IDToUser[user.ID] = user
file = open("sample_users.sql", "r")
text = file.read()
file.close()
capture = re.findall(r"\((\d+),'([^']*)'", text)
for x in capture:
    IDToUser[int(x[0])].name = x[1]
file = open("osu_scores_fruits_high.sql", "r")
text = file.read()
file.close()
capture = re.findall(r"\((\d+),(\d+),(\d+),(\d+),(\d+),'(\wH?)',(\d+),(\d+),(\d+),(\d+),\d+,(\d+),\d,(\d+),'[^']*',(\d+(?:\.\d+)?|NULL)", text)
userIDToRankedPlays = {}
userIDToLovedPlays = {}
for x in capture:
    safe = True
    play = tools.play()
    play.ID = int(x[0])
    play.beatmapID = int(x[1])
    play.userID = int(x[2])
    play.score = int(x[3])
    play.combo = int(x[4])
    play.rank = x[5]
    play.misses = int(x[9])
    play.drpmiss = int(x[10])
    try:
        IDToBeatmap[play.beatmapID].maxCombo = int(x[7]) + int(x[8]) + int(x[9])
        IDToBeatmap[play.beatmapID].accuracyTotal = IDToBeatmap[play.beatmapID].maxCombo + int(x[6]) + int(x[10])
    except Exception as e:
        print(e)
        print(x)
        continue
    play.modCode = int(x[11])
    if x[12] != "NULL":
        play.pp = float(x[12])
        if play.userID not in userIDToRankedPlays:
            userIDToRankedPlays[play.userID] = []
        userIDToRankedPlays[play.userID].append(play)
    else:
        if IDToBeatmap[play.beatmapID].maxCombo == 0:
            play.pp = 0
        else:
            try:
                SR = IDToBeatmap[play.beatmapID].difficulty[tools.modCodeToDifficultyCode(play.modCode)]
            except:
                SR = 0
                print("Missing SR: " + str(play.beatmapID))
            maxCombo = IDToBeatmap[play.beatmapID].maxCombo
            AR = tools.modifiedAR(IDToBeatmap[play.beatmapID].AR, play.modCode)
            Acc = 1-(play.misses+play.drpmiss)/IDToBeatmap[play.beatmapID].accuracyTotal
            play.pp = tools.catchPP(SR, play.combo, maxCombo, play.misses, AR, play.modCode, Acc)
            if play.userID not in userIDToLovedPlays:
                userIDToLovedPlays[play.userID] = []
            userIDToLovedPlays[play.userID].append(play)
for x in userIDToRankedPlays:
    userIDToRankedPlays[x].sort(key=lambda item: item.pp, reverse=True)
for x in userIDToLovedPlays:
    userIDToLovedPlays[x].sort(key=lambda item: item.pp, reverse=True)
file = open("IDToBeatmap.pkl", "wb")
pickle.dump(IDToBeatmap, file)
file.close()
file = open("IDToBeatmapSet.pkl", "wb")
pickle.dump(IDToBeatmapSet, file)
file.close()
file = open("IDToUser.pkl", "wb")
pickle.dump(IDToUser, file)
file.close()
file = open("userIDToRankedPlays.pkl", "wb")
pickle.dump(userIDToRankedPlays, file)
file.close()
file = open("userIDToLovedPlays.pkl", "wb")
pickle.dump(userIDToLovedPlays, file)
file.close()
file = open("countryCodes.pkl", "wb")
pickle.dump(countryCodes, file)
file.close()
modLeaderboards.modLeaderboard("EZ", includeMods=2, userIDToPlays=userIDToRankedPlays, IDToUser=IDToUser, countryCodes=countryCodes, IDToBeatmap=IDToBeatmap, IDToBeatmapSet=IDToBeatmapSet)
modLeaderboards.modLeaderboard("HD", includeMods=8, userIDToPlays=userIDToRankedPlays, IDToUser=IDToUser, countryCodes=countryCodes, IDToBeatmap=IDToBeatmap, IDToBeatmapSet=IDToBeatmapSet)
modLeaderboards.modLeaderboard("HR", includeMods=16, userIDToPlays=userIDToRankedPlays, IDToUser=IDToUser, countryCodes=countryCodes, IDToBeatmap=IDToBeatmap, IDToBeatmapSet=IDToBeatmapSet)
modLeaderboards.modLeaderboard("DT", includeMods=64, userIDToPlays=userIDToRankedPlays, IDToUser=IDToUser, countryCodes=countryCodes, IDToBeatmap=IDToBeatmap, IDToBeatmapSet=IDToBeatmapSet)
modLeaderboards.modLeaderboard("HT", includeMods=256, userIDToPlays=userIDToRankedPlays, IDToUser=IDToUser, countryCodes=countryCodes, IDToBeatmap=IDToBeatmap, IDToBeatmapSet=IDToBeatmapSet)
modLeaderboards.modLeaderboard("FL", includeMods=1024, userIDToPlays=userIDToRankedPlays, IDToUser=IDToUser, countryCodes=countryCodes, IDToBeatmap=IDToBeatmap, IDToBeatmapSet=IDToBeatmapSet)
modLeaderboards.modLeaderboard("NM", excludeMods=1370, userIDToPlays=userIDToRankedPlays, IDToUser=IDToUser, countryCodes=countryCodes, IDToBeatmap=IDToBeatmap, IDToBeatmapSet=IDToBeatmapSet)
modLeaderboards.modLeaderboard("Loved", userIDToPlays=userIDToLovedPlays, IDToUser=IDToUser, countryCodes=countryCodes, IDToBeatmap=IDToBeatmap, IDToBeatmapSet=IDToBeatmapSet, banSet={1529757, 2572147, 1257904, 2571858, 1267365, 1165130})
modLeaderboards.YMDvsTheWorld(4158549, userIDToPlays=userIDToRankedPlays, IDToUser=IDToUser, countryCodes=countryCodes, IDToBeatmap=IDToBeatmap, IDToBeatmapSet=IDToBeatmapSet)
modLeaderboards.specificFCsLeaderboard(userIDToPlays=userIDToRankedPlays, IDToUser=IDToUser, IDToBeatmap=IDToBeatmap, countryCodes=countryCodes)
