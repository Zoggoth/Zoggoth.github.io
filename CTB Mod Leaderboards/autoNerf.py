import math
import tools
import pickle

oneYearAgo = tools.oneYearAgo
oneMonthAgo = tools.oneMonthAgo


def printPlays(plays, IDToBeatmap, IDToBeatmapSet, IDToUser, user=0, count=100):
    file = open("html/AutoNerf/{}.html".format(user), "w")
    username = IDToUser[user].name
    file.write("""<!DOCTYPE html>
    <html lang="en">
      <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width">
        <link rel="stylesheet" href="https://unpkg.com/ress/dist/ress.min.css">
    <link rel="stylesheet" href="../../../style.css">
        <title>{}'s AutoNerfed plays</title>
      </head>
      <body>
        <div class="content">
    <p><a href="../AutoNerf.html">Return to leaderboard</a></p>
    <br>
    <p><b>{}</b></p>
    <div class="bp-wrapper">
      <table class="bp">
        <thead>
          <tr>
            <th class="text-left">#</th>
            <th>Map name</th>
            <th>Mods</th>
            <th>Miss</th>
            <th>Combo</th>
            <th>PP</th>
          </tr>
        </thead>
        <tbody>""".format(username, username))
    rank = 1
    done = set()
    for play in plays:
        if rank > count:
            break
        if play.beatmapID not in done:
            done.add(play.beatmapID)
            file.write("""
                    <tr""")
            if play.date >= oneMonthAgo:
                file.write(""" class="recent\"""")
            file.write(""">
                    <td>{}</td>
                    <td><a href="https://osu.ppy.sh/b/{}?m=2" target="_blank">{} [{}]</a> </td>
                    <td>""".format(rank, play.beatmapID, IDToBeatmapSet[IDToBeatmap[play.beatmapID].beatmapSetID].title,
                                   IDToBeatmap[play.beatmapID].difficultyName))
            file.write(tools.modCodeToText(play.modCode))
            file.write("""</td>
                    <td>{}</td>
                    <td>{}/{}x</td>
                    <td><b>{:.2f}pp</b></td>""".format(play.misses, play.combo, IDToBeatmap[play.beatmapID].maxCombo, play.pp[1]))
            file.write("""
          </tr>""")
            rank += 1
    file.write("""
    </tbody>
  </table>
</div>
  </div>
  </body>
</html>""")
    file.close()


def printNerf(nerfList, IDToBeatmap, IDToBeatmapSet, globalBuff):
    file = open("html/AutoNerf/farm.html", "w")
    file.write("""<!DOCTYPE html>
    <html lang="en">
      <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width">
        <link rel="stylesheet" href="https://unpkg.com/ress/dist/ress.min.css">
    <link rel="stylesheet" href="../../../style.css">
        <script
          src="https://code.jquery.com/jquery-3.6.0.min.js"
          integrity="sha256-/xUj+3OJU5yExlq6GSYGSHk7tPXikynS7ogEvDej/m4="
          crossorigin="anonymous"></script>
        <script type="text/javascript" src="../../../Mottie-tablesorter/js/jquery.tablesorter.js"></script>
        <script>
        $(function(){{
            $('table').tablesorter({{
                usNumberFormat : false,
                sortReset      : true,
                sortRestart    : true
            }});
        }});
        </script>
        <title>Nerfed Farm Maps</title>
      </head>
      <body>
        <div class="content">
    <p><a href="../AutoNerf.html">Return to leaderboard</a></p>
    <br>
    <p><b>Nerfed Farm Maps</b></p>
    <p>Note that all maps get buffed to keep total pp the same, so some of these maps will be buffed, just less buffed than the average map</p>    
    <div class="bp-wrapper">
      <table class="bp">
        <thead>
          <tr>
            <th data-lockedorder="asc" class="text-left">#</th>
            <th data-sorter="false">Map name</th>
            <th data-sorter="false">Mods</th>
            <th data-lockedorder="desc">PP</th>
            <th data-sorter="false">Nerf</th>
          </tr>
        </thead>
        <tbody>
    """)
    rank = 1
    for ((ID, mod), nerfs) in nerfList:
        if nerfs == 0:
            break
        beatmap = IDToBeatmap[ID]
        beatmapSet = IDToBeatmapSet[beatmap.beatmapSetID]
        title = beatmapSet.title
        difficultyName = beatmap.difficultyName
        modName = tools.modCodeToText(mod)
        SR = beatmap.difficulty[tools.modCodeToDifficultyCode(mod)]
        mcombo = beatmap.maxCombo
        AR = tools.modifiedAR(beatmap.AR, mod)
        pp = tools.catchPP(SR, mcombo, mcombo, 0, AR, mod, 1)
        newpp = pp * globalBuff * (1 - nerfs / 1000)
        file.write("""	  <tr >
        <td>{}</td>
        <td><a href="https://osu.ppy.sh/b/{}?m=2" target="_blank">{} [{}]</a> </td>
        <td>{}</td>
        <td><b>{:.2f}pp</b></td>
        <td>{:.1f}%</td>
      </tr>
""".format(rank, ID, title, difficultyName, modName, newpp, nerfs/10))
        rank += 1
    file.write("""    </tbody>
  </table>
</div>
  </div>
  </body>
</html>""")


file = open("userIDToRankedPlays.pkl", "rb")
userIDToRankedPlays = pickle.load(file)
file.close()
file = open("IDToBeatmap.pkl", "rb")
IDToBeatmap = pickle.load(file)
file.close()
file = open("IDToBeatmapSet.pkl", "rb")
IDToBeatmapSet = pickle.load(file)
file.close()
file = open("IDToUser.pkl", "rb")
IDToUser = pickle.load(file)
file.close()
active = {}
activeCount = 0
for (ID, plays) in userIDToRankedPlays.items():
    if len(plays) < 200:
        active[ID] = False
        continue
    else:
        active[ID] = False
        for play in plays[:100]:
            if play.date >= oneYearAgo:
                active[ID] = True
                activeCount += 1
                break
farmScore = {}
originalPPSum = 0
originalPlays = {}
for (ID,plays) in userIDToRankedPlays.items():
    for play in plays:
        modCode = (play.modCode | 1) - 1
        beatmap = IDToBeatmap[play.beatmapID]
        SR = beatmap.difficulty[tools.modCodeToDifficultyCode(play.modCode)]
        mcombo = beatmap.maxCombo
        AR = tools.modifiedAR(beatmap.AR,play.modCode)
        accuracy = 1-(play.misses + play.drpmiss)/beatmap.accuracyTotal
        newpp = tools.catchPP(SR, play.combo, mcombo, play.misses, AR, modCode, accuracy)
        play.pp = (newpp,newpp)
        if play.modCode & 66 == 66:
            play.modCode += 64
    plays.sort(key=lambda item: item.pp[1], reverse=True)
    originalPlays[ID] = plays
    plays = plays[:500]
    userIDToRankedPlays[ID] = plays
    if not active[ID]:
        continue
    totalpp = 0
    multiplier = 1
    done = set()
    count = 0
    for play in plays:
        if play.beatmapID not in done:
            done.add(play.beatmapID)
            totalpp += play.pp[1] * multiplier
            multiplier *= .95
            count += 1
            if count >= 200:
                break
    originalPPSum += totalpp
    multiplier = 1
    done = set()
    count = 0
    for play in plays:
        if play.beatmapID not in done:
            done.add(play.beatmapID)
            mapModPair = (play.beatmapID, play.modCode & 66)
            farm = play.pp[1] * multiplier/totalpp
            farm = farm*10000/activeCount
            farmScore[mapModPair] = farmScore.get(mapModPair, 0) + farm
            multiplier *= .95
            count += 1
            if count >= 200:
                break
fixed = False
timesNerfed = {}
currentPPSum = 0
while not fixed:
    currentPPSum = 0
    for (IDMod,score) in farmScore.items():
        if score >= 2.5:
            timesNerfed[IDMod] = timesNerfed.get(IDMod,0) + 10
        elif score >= 2:
            timesNerfed[IDMod] = timesNerfed.get(IDMod, 0) + 1
    farmScore = {}
    for (ID,plays) in userIDToRankedPlays.items():
        for play in plays:
            IDMod = (play.beatmapID, play.modCode & 66)
            nerfFraction = 1 - timesNerfed.get(IDMod, 0)/1000
            play.pp = (play.pp[0], play.pp[0]*nerfFraction)
        plays.sort(key=lambda item: item.pp[1], reverse=True)
        userIDToRankedPlays[ID] = plays
        if not active[ID]:
            continue
        totalpp = 0
        multiplier = 1
        done = set()
        count = 0
        for play in plays:
            if play.beatmapID not in done:
                done.add(play.beatmapID)
                totalpp += play.pp[1] * multiplier
                multiplier *= .95
                count += 1
                if count >= 200:
                    break
        currentPPSum += totalpp
        multiplier = 1
        done = set()
        count = 0
        for play in plays:
            if play.beatmapID not in done:
                done.add(play.beatmapID)
                mapModPair = (play.beatmapID, play.modCode & 66)
                farm = play.pp[1] * multiplier / totalpp
                farm = farm*10000/activeCount
                farmScore[mapModPair] = farmScore.get(mapModPair, 0) + farm
                multiplier *= .95
                count += 1
                if count >= 200:
                    break
    overCount = 0
    for (ID,score) in farmScore.items():
        if score >= 2:
            overCount += 1
            if score >= 2.005:
                overCount += 10
    if overCount <=10:
        fixed = True
    print(overCount)
globalBuff = originalPPSum/currentPPSum
userIDToRankedPlays = originalPlays
farmScore = {}
IDToPP = {}
file = open("outputFixPlayers.txt", "w")
for (ID,plays) in userIDToRankedPlays.items():
    for play in plays:
        IDMod = (play.beatmapID, play.modCode & 66)
        nerfFraction = 1 - timesNerfed.get(IDMod, 0) / 1000
        play.pp = (play.pp[0], play.pp[0] * globalBuff * nerfFraction)
        if play.modCode & 128 == 128:
            play.modCode -= 64
    plays.sort(key=lambda item: item.pp[1], reverse=True)
    printPlays(plays, IDToBeatmap, IDToBeatmapSet, IDToUser, ID)
    totalpp = 0
    multiplier = 1
    done = set()
    count = 0
    for play in plays:
        if play.beatmapID not in done:
            done.add(play.beatmapID)
            totalpp += play.pp[1] * multiplier
            multiplier *= .95
            count += 1
            if count >= 200:
                break
    if active[ID]:
        multiplier = 1
        done = set()
        count = 0
        for play in plays:
            if play.beatmapID not in done:
                done.add(play.beatmapID)
                mapModPair = (play.beatmapID, play.modCode & 66)
                farm = play.pp[1] * multiplier/totalpp
                farm = farm*10000/activeCount
                farmScore[mapModPair] = farmScore.get(mapModPair, 0) + farm
                multiplier *= .95
                count += 1
                if count >= 200:
                    break
    bonuspp = 1250 * (1 - math.pow(0.9994, len(plays))) / 3
    totalpp += bonuspp
    IDToPP[ID] = totalpp
    username = IDToUser[ID].name
    oldpp = IDToUser[ID].pp
    file.write("{}£{:.1f}£{:.1f}\n".format(username, oldpp, totalpp))
file.close()
sortedUsers = sorted(IDToPP.items(),key=lambda item: item[1], reverse=True)
rank = 1
file = open("html/AutoNerf.html", "w")
file.write("""<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width">
    <link rel="stylesheet" href="https://unpkg.com/ress/dist/ress.min.css">
<link rel="stylesheet" href="../../style.css">
<script
  src="https://code.jquery.com/jquery-3.6.0.min.js"
  integrity="sha256-/xUj+3OJU5yExlq6GSYGSHk7tPXikynS7ogEvDej/m4="
  crossorigin="anonymous"></script>
    <script type="text/javascript" src="../../Mottie-tablesorter/js/jquery.tablesorter.js"></script>
    <script>
    $(function(){{
        $('table').tablesorter({{
            usNumberFormat : false,
            sortReset      : true,
            sortRestart    : true
        }});
    }});
    </script>
    <title>AutoNerfed pp ranking</title>
  </head>
  <body>
    <div class="content">
<p><a href="index.html">Return to main page</a></p>
<br>
  <p>All farm maps are <a href="AutoNerf/farm.html" target="_blank">nerfed</a> until there are no farm maps</p>
  <p>Then all maps are given a {:.2f}% buff to keep average pp the same</p>
  <p>Also I got rid of NF nerf because I don't like it</p>
    <div class="bp-wrapper">
      <table class="bp">
        <thead>
          <tr>
            <th data-lockedorder="asc" class="text-left">#</th>
            <th data-sorter="false">user</th>
            <th data-lockedorder="desc">AutoNerfed pp</th>
            <th data-lockedorder="desc">Current pp</th>
            <th data-lockedorder="asc" class="text-left">#</th>
          </tr>
        </thead>
        <tbody>""".format(100*(globalBuff-1)))
for (ID,pp) in sortedUsers:
    file.write("""<tr>
                    <td>{}</td>
                    <td><a href="AutoNerf/{}.html" target="_blank">{}</a> </td>
                    <td>{:.2f}</td>
                    <td>{:.2f}</td>
                    <td>{}</td>
          </tr>""".format(rank, ID, IDToUser[ID].name, pp, IDToUser[ID].pp, IDToUser[ID].ppRank))
    rank += 1
file.write("""    </tbody>
  </table>
</div>""")
file.close()
sortedFarm = sorted(farmScore.items(),key=lambda item: item[1], reverse=True)
sortedNerfs = sorted(timesNerfed.items(), key=lambda item: item[1], reverse=True)
printNerf(sortedNerfs,IDToBeatmap,IDToBeatmapSet,globalBuff)
file = open("outputFixFarm.txt", "w")
for ((ID, mod), score) in sortedFarm:
    beatmap = IDToBeatmap[ID]
    beatmapSet = IDToBeatmapSet[beatmap.beatmapSetID]
    title = beatmapSet.title
    difficultyName = beatmap.difficultyName
    if mod & 128 == 128:
        mod -= 64
    modName = tools.modCodeToText(mod)
    nerfs = timesNerfed.get((ID, mod),0)
    SR = beatmap.difficulty[tools.modCodeToDifficultyCode(mod)]
    mcombo = beatmap.maxCombo
    AR = tools.modifiedAR(beatmap.AR, mod)
    pp = tools.catchPP(SR, mcombo, mcombo, 0, AR, mod, 1)
    newpp = pp * globalBuff * (1-nerfs/1000)
    file.write("{}£{} [{}]£{}£{:.2f}£-{:.1f}%£{:.2f}\n".format(ID, title, difficultyName, modName, newpp, nerfs/10, score))
file.close()