# It would be way better to do this with API calls, but I'm not hammering the API for this nonsense
import pickle
import math
import tools

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
                if y.modCode & 258 == 0: # 258 == 0 for NM. 274 == 16 for HR. 322 == 64 for DT
                    FCSet.add(y.beatmapID)
    for y in FCSet:
        IDtoFCs[y] += 1
    if x == player:
        playerSet = FCSet
perYearList = []
for x in IDtoFCs:
    FCsPerYear = 525600*60*float(IDtoFCs[x])/(currentDate-IDToBeatmapSet[IDToBeatmap[x].beatmapSetID].date)
    FCsPerRootYear = float(IDtoFCs[x])/math.sqrt((currentDate-IDToBeatmapSet[IDToBeatmap[x].beatmapSetID].date)/525600/60)
    perYearList.append((x, FCsPerYear, FCsPerRootYear, IDtoFCs[x]))
perYearList.sort(key=lambda item: item[2])
file = open("html/rarestFCs.html", "w", encoding="utf-8")
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
    $(function(){
        $('table').tablesorter({
            usNumberFormat : false,
            sortReset      : true,
            sortRestart    : true
        });
    });
    </script>
    <title>Rarest FCs</title>
  </head>
  <body>
    <div class="content">
<p><a href="rankedSpecificFCs.html">Return to leaderboard</a></p>
<p><b>Rarest ranked CTB FCs</b></p>
<p>Sortable by total FCs (new maps are too close to the top), FCs per year (new maps are all at the bottom) & FCs per √year (a nice balance)</p>
<p>EZ/HT FCs don't count. All other mods count.</p>
<p>Only active users in the top 10k count. This isn't ideal, but at least provides a reasonable sample</p>
<div class="bp-wrapper">
  <table class="bp">
    <thead>
      <tr>
        <th>Map</th>
        <th>FCs</th>
        <th>FCs per<br>√year</th>
        <th>FCs per<br>year</th>
        <th>SR</th>
        <th>PP</th>
      </tr>
    </thead>
    <tbody>
""")
for x in perYearList:
    file.write("""      <tr""")
    if IDToBeatmapSet[IDToBeatmap[x[0]].beatmapSetID].date >= 1667223513:
        file.write(""" class="recent\"""")
    file.write(""">
        <td><a href="https://osu.ppy.sh/b/""")
    file.write(str(x[0]))
    file.write("""?m=2" target="_blank">""")
    file.write(IDToBeatmapSet[IDToBeatmap[x[0]].beatmapSetID].title+" ["+IDToBeatmap[x[0]].difficultyName)
    file.write("""]</a> </td>
        <td>""")
    file.write(str(x[3]))
    file.write("""</td>
        <td>""")
    file.write("{:.2f}".format(x[2]))
    file.write("""</td>
        <td>""")
    file.write("{:.2f}".format(x[1]))
    file.write("""</td>
        <td>""")
    file.write("{:.2f}".format(IDToBeatmap[x[0]].difficulty[0]))
    file.write("""</td>
        <td>""")
    file.write("{:.2f}".format(tools.catchPP(IDToBeatmap[x[0]].difficulty[0],IDToBeatmap[x[0]].maxCombo,IDToBeatmap[x[0]].maxCombo,0,tools.modifiedAR(IDToBeatmap[x[0]].AR,0),0,1)))
    file.write("""</td>
      </tr>""")
file.write("""
    </tbody>
  </table>
</div>
  </div>
  </body>
</html>""")
file.close()
# Would technically be faster to do above, but it just looks like a mess
file = open("IDToUser.pkl", "rb")
IDToUser = pickle.load(file)
file.close()
playerName = IDToUser[player].name
playerFCs = open("playerFCs.html", "w", encoding="utf-8")
playerNonFCs = open("playerNonFCs.html", "w", encoding="utf-8")
playerFCs.write("""<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width">
    <link rel="stylesheet" href="https://unpkg.com/ress/dist/ress.min.css">
<link rel="stylesheet" href="../style.css">
    <script
      src="https://code.jquery.com/jquery-3.6.0.min.js"
      integrity="sha256-/xUj+3OJU5yExlq6GSYGSHk7tPXikynS7ogEvDej/m4="
      crossorigin="anonymous"></script>
    <script type="text/javascript" src="../Mottie-tablesorter/js/jquery.tablesorter.js"></script>
    <script>
    $(function(){
        $('table').tablesorter({
            usNumberFormat : false,
            sortReset      : true,
            sortRestart    : true
        });
    });
    </script>
    <title>"""+playerName+"""'s FCs</title>
  </head>
  <body>
    <div class="content">
<p><b>"""+playerName+"""'s FCs</b></p>
<div class="bp-wrapper">
  <table class="bp">
    <thead>
      <tr>
        <th>Map</th>
        <th>FCs</th>
        <th>FCs per<br>√year</th>
        <th>FCs per<br>>year</th>
        <th>SR</th>
        <th>PP</th>
      </tr>
    </thead>
    <tbody>
""")
playerNonFCs.write("""<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width">
    <link rel="stylesheet" href="https://unpkg.com/ress/dist/ress.min.css">
<link rel="stylesheet" href="../style.css">
    <script
      src="https://code.jquery.com/jquery-3.6.0.min.js"
      integrity="sha256-/xUj+3OJU5yExlq6GSYGSHk7tPXikynS7ogEvDej/m4="
      crossorigin="anonymous"></script>
    <script type="text/javascript" src="../Mottie-tablesorter/js/jquery.tablesorter.js"></script>
    <script>
    $(function(){
        $('table').tablesorter({
            usNumberFormat : false,
            sortReset      : true,
            sortRestart    : true
        });
    });
    </script>
    <title>"""+playerName+"""'s To Do list</title>
  </head>
  <body>
    <div class="content">
<p><b>"""+playerName+"""'s To Do list</b></p>
<div class="bp-wrapper">
  <table class="bp">
    <thead>
      <tr>
        <th>Map</th>
        <th>FCs</th>
        <th>FCs per<br>√year</th>
        <th>FCs per<br>>year</th>
        <th>SR</th>
        <th>PP</th>
      </tr>
    </thead>
    <tbody>
""")
for x in perYearList:
    if x[0] in playerSet:
        playerFCs.write("""      <tr""")
        if IDToBeatmapSet[IDToBeatmap[x[0]].beatmapSetID].date >= 1667223513:
            playerFCs.write(""" class="recent\"""")
        playerFCs.write(""">
                        <td><a href="https://osu.ppy.sh/b/""")
        playerFCs.write(str(x[0]))
        playerFCs.write("""?m=2" target="_blank">""")
        playerFCs.write(IDToBeatmapSet[IDToBeatmap[x[0]].beatmapSetID].title + " [" + IDToBeatmap[x[0]].difficultyName)
        playerFCs.write("""]</a> </td>
                        <td>""")
        playerFCs.write(str(x[3]))
        playerFCs.write("""</td>
                        <td>""")
        playerFCs.write("{:.2f}".format(x[2]))
        playerFCs.write("""</td>
                        <td>""")
        playerFCs.write("{:.2f}".format(x[1]))
        playerFCs.write("""</td>
                        <td>""")
        playerFCs.write("{:.2f}".format(IDToBeatmap[x[0]].difficulty[0]))
        playerFCs.write("""</td>
                        <td>""")
        playerFCs.write("{:.2f}".format(
            tools.catchPP(IDToBeatmap[x[0]].difficulty[0], IDToBeatmap[x[0]].maxCombo, IDToBeatmap[x[0]].maxCombo, 0, tools.modifiedAR(IDToBeatmap[x[0]].AR,0), 0, 1)))
        playerFCs.write("""</td>
                      </tr>""")
    else:
        playerNonFCs.write("""      <tr""")
        if IDToBeatmapSet[IDToBeatmap[x[0]].beatmapSetID].date >= 1667223513:
            playerNonFCs.write(""" class="recent\"""")
        playerNonFCs.write(""">
                        <td><a href="https://osu.ppy.sh/b/""")
        playerNonFCs.write(str(x[0]))
        playerNonFCs.write("""?m=2" target="_blank">""")
        playerNonFCs.write(IDToBeatmapSet[IDToBeatmap[x[0]].beatmapSetID].title + " [" + IDToBeatmap[x[0]].difficultyName)
        playerNonFCs.write("""]</a> </td>
                        <td>""")
        playerNonFCs.write(str(x[3]))
        playerNonFCs.write("""</td>
                        <td>""")
        playerNonFCs.write("{:.2f}".format(x[2]))
        playerNonFCs.write("""</td>
                        <td>""")
        playerNonFCs.write("{:.2f}".format(x[1]))
        playerNonFCs.write("""</td>
                        <td>""")
        playerNonFCs.write("{:.2f}".format(IDToBeatmap[x[0]].difficulty[0]))
        playerNonFCs.write("""</td>
                        <td>""")
        playerNonFCs.write("{:.2f}".format(
            tools.catchPP(IDToBeatmap[x[0]].difficulty[0], IDToBeatmap[x[0]].maxCombo, IDToBeatmap[x[0]].maxCombo, 0, tools.modifiedAR(IDToBeatmap[x[0]].AR,0), 0, 1)))
        playerNonFCs.write("""</td>
                      </tr>""")
playerNonFCs.write("""
    </tbody>
  </table>
</div>
  </div>
  </body>
</html>""")
playerFCs.write("""
    </tbody>
  </table>
</div>
  </div>
  </body>
</html>""")
playerFCs.close()
playerNonFCs.close()
