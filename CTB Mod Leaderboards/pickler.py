import re
import time

import tools
import pickle
import modLeaderboards

file = open("osu_beatmaps.sql", "r", encoding="utf-8")
text = file.read()
file.close()
capture = re.finditer(r"\((?P<ID>\d+),(?P<SetID>\d+),\d+,'[^']*?(?:\\'[^']*?)*','[0-f]*','(?P<DiffName>[^']*?(?:\\'[^']*?)*)',(?P<Length>\d+(?:\.\d+)?),(?:\d+(?:\.\d+)?,){5}(?P<HP>\d+(?:\.\d+)?),(?P<CS>\d+(?:\.\d+)?),\d+(?:\.\d+)?,(?P<AR>\d+(?:\.\d+)?),(?P<Mode>\d),(?P<Status>\d)", text)
IDToBeatmap = {}
for x in capture:
    beatmap = tools.beatmap()
    beatmap.ID = int(x["ID"])
    beatmap.beatmapSetID = int(x["SetID"])
    beatmap.difficultyName = x["DiffName"].replace(r"\'", "'")
    beatmap.length = int(x["Length"])
    beatmap.AR = float(x["AR"])
    beatmap.HP = float(x["HP"])
    beatmap.CS = float(x["CS"])
    beatmap.mode = int(x["Mode"])
    beatmap.status = int(x["Status"])
    beatmap.difficulty = {}
    IDToBeatmap[beatmap.ID] = beatmap
IDToBeatmap[2536330].difficulty = {0: 12.60, 2: 10.54, 16: 15.02, 64: 15.15, 66: 12.63, 80: 18.08, 256: 11.43, 258: 9.58, 272: 13.58}
file = open("osu_beatmap_difficulty.sql", "r")
text = file.read()
file.close()
capture = re.finditer(r"\((?P<ID>\d+),2,(?P<ModCode>\d+),(?P<SR>\d+(?:\.\d+)?)", text)
for x in capture:
    IDToBeatmap[int(x["ID"])].difficulty[int(x["ModCode"])] = float(x["SR"])
file = open("osu_beatmapsets.sql", "r", encoding="utf-8", errors="replace")
text = file.read()
file.close()
capture = re.finditer(r"\((?P<ID>\d+),\d+,\d+,'(?P<Artist>[^']*?(?:\\'[^']*?)*)',(?:NULL|'[^']*?(?:\\'[^']*?)*'),'(?P<Title>[^']*?(?:\\'[^']*?)*)',(?:NULL|'[^']*?(?:\\'[^']*?)*'),'[^']*?(?:\\'[^']*?)*','[^']*?(?:\\'[^']*?)*','[^']*?(?:\\'[^']*?)*',\d,\d,\d,\d+(?:\.\d+)?,\d+,\d+,(?:\d+|NULL),'(?P<Date>[^']+)", text)
IDToBeatmapSet = {}
for x in capture:
    beatmapSet = tools.beatmapSet()
    beatmapSet.ID = int(x["ID"])
    beatmapSet.artist = x["Artist"].replace(r"\'", "'")
    beatmapSet.title = x["Title"].replace(r"\'", "'")
    beatmapSet.date = time.mktime(time.strptime(x["Date"], '%Y-%m-%d %H:%M:%S'))
    IDToBeatmapSet[beatmapSet.ID] = beatmapSet
file = open("Country Codes.txt", "r", encoding="utf-8")
text = file.read().split("\n")
file.close()
countryCodes = {}
for x in range(round(len(text)/2)):
    countryCodes[text[2*x]] = text[2*x+1]
file = open("osu_user_stats_fruits.sql", "r")
text = file.read()
file.close()
capture = re.finditer(r"\((?P<ID>\d+),\d+,\d+,\d+,\d+,\d+,\d+,\d+(?:\.\d+)?,\d+,\d+,\d+,\d+,\d+,-?\d+,\d+,\d+,\d+,\d+(?:\.\d+)?,\d+,\d+,\d+,\d+,'(?P<Country>\w\w)',(?P<PP>\d+(?:\.\d+)?),(?P<Rank>\d+)", text)
IDToUser = {}
for x in capture:
    user = tools.user()
    user.ID = int(x["ID"])
    user.country = x["Country"]
    if user.country not in countryCodes:
        print("Country " + user.country + " missing")
        countryCodes[user.country] = user.country
    user.pp = float(x["PP"])
    user.ppRank = int(x["Rank"])
    IDToUser[user.ID] = user
file = open("sample_users.sql", "r")
text = file.read()
file.close()
capture = re.finditer(r"\((?P<ID>\d+),'(?P<Name>[^']*)'", text)
for x in capture:
    IDToUser[int(x["ID"])].name = x["Name"]
file = open("osu_scores_fruits_high.sql", "r")
text = file.read()
file.close()
capture = re.finditer(r"\((?P<PlayID>\d+),(?P<BeatmapID>\d+),(?P<UserID>\d+),(?P<Score>\d+),(?P<Combo>\d+),'(?P<Rank>\wH?)',(?P<n50>\d+),(?P<n100>\d+),(?P<n300>\d+),(?P<Miss>\d+),\d+,(?P<DrpMiss>\d+),\d,(?P<ModCode>\d+),'(?P<Date>[^']*)',(?P<PP>\d+(?:\.\d+)?|NULL)", text)
userIDToRankedPlays = {}
userIDToLovedPlays = {}
for x in capture:
    safe = True
    play = tools.play()
    play.ID = int(x["PlayID"])
    play.beatmapID = int(x["BeatmapID"])
    play.userID = int(x["UserID"])
    play.score = int(x["Score"])
    play.combo = int(x["Combo"])
    play.rank = x["Rank"]
    play.misses = int(x["Miss"])
    play.drpmiss = int(x["DrpMiss"])
    try:
        IDToBeatmap[play.beatmapID].maxCombo = int(x["n100"]) + int(x["n300"]) + int(x["Miss"])
        IDToBeatmap[play.beatmapID].accuracyTotal = IDToBeatmap[play.beatmapID].maxCombo + int(x["n50"]) + int(x["DrpMiss"])
    except Exception as e:
        print(e)
        print(x[0])
        continue
    play.modCode = int(x["ModCode"])
    play.date = time.mktime(time.strptime(x["Date"], '%Y-%m-%d %H:%M:%S'))
    if x["PP"] != "NULL":
        play.pp = float(x["PP"])
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
modLeaderboards.YMDvsTheWorld(4158549, userIDToPlays=userIDToRankedPlays, IDToUser=IDToUser, IDToBeatmap=IDToBeatmap, IDToBeatmapSet=IDToBeatmapSet)
modLeaderboards.specificFCsLeaderboard(userIDToPlays=userIDToRankedPlays, IDToUser=IDToUser, IDToBeatmap=IDToBeatmap, countryCodes=countryCodes)
modLeaderboards.rankedSpecificPasses(userIDToPlays=userIDToRankedPlays, IDToUser=IDToUser, IDToBeatmap=IDToBeatmap, countryCodes=countryCodes)
modLeaderboards.number1s(userIDToRankedPlays, userIDToLovedPlays, IDToUser, countryCodes)
modLeaderboards.hundrethPlay(userIDToPlays=userIDToRankedPlays, IDToUser=IDToUser, IDToBeatmap=IDToBeatmap, countryCodes=countryCodes)
modLeaderboards.totalPasses(userIDToPlays=userIDToRankedPlays, IDToUser=IDToUser, IDToBeatmap=IDToBeatmap, countryCodes=countryCodes)
userIDToConvertPlays = {}
for x in userIDToRankedPlays:
    convertsOnly = []
    for y in userIDToRankedPlays[x]:
        if IDToBeatmap[y.beatmapID].mode == 0:
            convertsOnly.append(y)
    userIDToConvertPlays[x] = convertsOnly
modLeaderboards.modLeaderboard("Convert", userIDToPlays=userIDToConvertPlays, IDToUser=IDToUser, countryCodes=countryCodes, IDToBeatmap=IDToBeatmap, IDToBeatmapSet=IDToBeatmapSet)
import autoNerf
