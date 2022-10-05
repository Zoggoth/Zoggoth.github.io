import tools
import pickle


def playFilter(playList, includeMods=0, excludeMods=0):
    mapSet = set()
    output = []
    for x in playList:
        if x.beatmapID not in mapSet:
            if (x.modCode & includeMods) == includeMods:
                if (x.modCode & excludeMods) == 0:
                    mapSet.add(x.beatmapID)
                    output.append(x)
    return output


def ppCalculate(playList, count=100):
    multiplier = float(1)
    output = float(0)
    for x in playList[:count]:
        output += x.pp*multiplier
        multiplier *= 0.95
    return output


def printFarmMaps(farmMaps, IDAndModToPPAndScore, IDToBeatmap, IDToBeatmapSet, name, count=1000):
    file = open("html/"+name+"/farm.html", "w")
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
    $(function(){
        $('table').tablesorter({
            usNumberFormat : false,
            sortReset      : true,
            sortRestart    : true
        });
    });
    </script>
    <title>"""+name+""" Farm Maps</title>
  </head>
  <body>
    <div class="content">
<p><a href="../"""+name+""".html">Return to leaderboard</a></p>
<br>
<p><b>"""+name+""" Farm Maps (Click on PP or Farm Score to sort)</b></p>    
<div class="bp-wrapper">
  <table class="bp">
    <thead>
      <tr>
        <th data-lockedorder="asc" class="text-left">#</th>
        <th data-sorter="false">Map name</th>
        <th data-sorter="false">Mods</th>
        <th data-lockedorder="desc">PP</th>
        <th data-lockedorder="desc">Farm Score</th>
      </tr>
    </thead>
    <tbody>
""")
    rank = 0
    for x in farmMaps[:count]:
        rank += 1
        file.write("""	  <tr >
        <td>"""+str(rank)+"""</td>
        <td><a href="https://osu.ppy.sh/b/"""+str(x[0])+"""?m=2" target="_blank">"""+IDToBeatmapSet[IDToBeatmap[x[0]].beatmapSetID].title+" ["+IDToBeatmap[x[0]].difficultyName+"""]</a> </td>
        <td>"""+tools.modCodeToText(x[1])+"""</td>
        <td><b>"""+"{:.2f}".format(IDAndModToPPAndScore[x][0])+"""pp</b></td>
        <td>"""+"{:.2f}".format(IDAndModToPPAndScore[x][1])+"""</td>
      </tr>
""")
    file.write("""    </tbody>
  </table>
</div>
  </div>
  </body>
</html>""")


def printPlays(plays, IDToBeatmap, IDToBeatmapSet, IDToUser, name, user=0, count=100, multiuser=False):
    beatmapIDtoUserList = {}
    beatmapIDtoPP = {}
    if multiuser:
        for x in plays:
            if x.beatmapID in beatmapIDtoUserList:
                if x.pp > beatmapIDtoPP[x.beatmapID] - 0.01:
                    beatmapIDtoUserList[x.beatmapID].append(x.userID)
            else:
                beatmapIDtoUserList[x.beatmapID] = [x.userID]
                beatmapIDtoPP[x.beatmapID] = x.pp
    plays = playFilter(plays)
    pp = ppCalculate(plays)
    filename = "html/" + name + "/"
    if multiuser:
        filename += "all.html"
    else:
        filename += str(user) + ".html"
    file = open(filename, "w")
    username = "Everyone" if multiuser else IDToUser[user].name
    file.write("""<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width">
    <link rel="stylesheet" href="https://unpkg.com/ress/dist/ress.min.css">
<link rel="stylesheet" href="../../../style.css">
    <title>""" + username +"'s " + name + """ plays</title>
  </head>
  <body>
    <div class="content">
<p><a href="../""" + ("index" if name == "Total" else name) + """.html">Return to leaderboard</a></p>
<br>
<p><b>""" + username + " (" + "{:.2f}".format(pp) + """ pp)</b></p>
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
""")
    if multiuser:
        file.write("""<th>Player</th>
""")
    file.write("""      </tr>
    </thead>
    <tbody>""")
    rank = 1
    for x in plays[:count]:
        file.write("""
        <tr>
        <td>"""+str(rank)+"""</td>
        <td><a href="https://osu.ppy.sh/b/"""+str(x.beatmapID)+"""?m=2" target="_blank">"""+IDToBeatmapSet[IDToBeatmap[x.beatmapID].beatmapSetID].title+" ["+IDToBeatmap[x.beatmapID].difficultyName+"""]</a> </td>
        <td>""")
        if multiuser:
            if len(beatmapIDtoUserList[x.beatmapID]) > 1:
                file.write(tools.modCodeToText((x.modCode & 1370)))
            else:
                file.write(tools.modCodeToText(x.modCode))
        else:
            file.write(tools.modCodeToText(x.modCode))
        file.write("""</td>
        <td>"""+str(x.misses)+"""</td>
        <td>"""+str(x.combo)+"/"+str(IDToBeatmap[x.beatmapID].maxCombo)+"""x</td>
        <td><b>"""+"{:.2f}".format(x.pp)+"""pp</b></td>""")
        if multiuser:
            if len(beatmapIDtoUserList[x.beatmapID])>5:
                usernameList = "Several People"
            else:
                usernameList = ""
                for y in beatmapIDtoUserList[x.beatmapID]:
                    usernameList += IDToUser[y].name + " & "
                usernameList = usernameList[:-3]
            file.write("<td>"+usernameList+"</td>")
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


def modLeaderboard(name, userIDToPlays, IDToUser, countryCodes, IDToBeatmap, IDToBeatmapSet, includeMods=0, excludeMods=0, count=2000, banSet={}):
    IDToPP = []
    allPlays = []
    hasBanList = False
    if len(banSet) != 0:
        hasBanList = True
        IDToBannedPP = {}
    for x in userIDToPlays:
        filteredPlays = playFilter(userIDToPlays[x], includeMods=includeMods, excludeMods=excludeMods)
        allPlays.extend(filteredPlays[0:100])
        IDToPP.append((x, ppCalculate(filteredPlays)))
        if hasBanList:
            banFilteredPlays = filteredPlays
            for y in banFilteredPlays[0:100+len(banSet)]:
                if y.beatmapID in banSet:
                    filteredPlays.remove(y)
            IDToBannedPP[x] = ppCalculate(banFilteredPlays)
    if hasBanList:
        banSorted = sorted(IDToBannedPP, key=lambda item: IDToBannedPP[item], reverse=True)
        banRanked = {}
        rank = 1
        for x in banSorted:
            banRanked[x] = rank
            rank += 1
    allPlays.sort(key=lambda item: item.pp, reverse=True)
    printPlays(allPlays, IDToBeatmap, IDToBeatmapSet, IDToUser, name, count=200, multiuser=True)
    IDToPP.sort(key=lambda item: item[1], reverse=True)
    filteredCountrySet = set()
    IDAndModToPPAndScore = {}
    for x in IDToPP[:count]:
        filteredPlays = playFilter(userIDToPlays[x[0]], includeMods=includeMods, excludeMods=excludeMods)
        totalpp = ppCalculate(filteredPlays)
        multiplier = float(1)
        for y in filteredPlays:
            if (y.beatmapID, y.modCode & 1370) in IDAndModToPPAndScore:
                IDAndModToPPAndScore[(y.beatmapID, y.modCode & 1370)][0] = max(IDAndModToPPAndScore[(y.beatmapID, y.modCode & 1370)][0], y.pp)
                IDAndModToPPAndScore[(y.beatmapID, y.modCode & 1370)][1] = IDAndModToPPAndScore[(y.beatmapID, y.modCode & 1370)][1] + y.pp*multiplier/totalpp
            else:
                IDAndModToPPAndScore[(y.beatmapID, y.modCode & 1370)] = [y.pp, y.pp*multiplier/totalpp]
            multiplier *= .95
        printPlays(filteredPlays, IDToBeatmap, IDToBeatmapSet, IDToUser, name, x[0])
        filteredCountrySet.add(IDToUser[x[0]].country)
    farmMaps = sorted(IDAndModToPPAndScore, key=lambda item: IDAndModToPPAndScore[item][1], reverse=True)
    printFarmMaps(farmMaps, IDAndModToPPAndScore, IDToBeatmap, IDToBeatmapSet, name)
    filteredCountryList = sorted(filteredCountrySet, key=lambda item: countryCodes[item])
    banListString = ""
    if hasBanList:
        banListString = "<p>Banlist</p>"
        for x in banSet:
            banListString += """\n<p><a href="https://osu.ppy.sh/b/"""+str(x)+"""?m=2" target="_blank">"""+IDToBeatmapSet[IDToBeatmap[x].beatmapSetID].title+" ["+IDToBeatmap[x].difficultyName+"""]</a></p>"""
    file = open("html/"+name+".html", "w")
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
    <title>"""+name+""" pp ranking</title>
  </head>
  <body>
    <div class="content">
<p><a href="index.html">Return to main page</a></p>
<br>
<p>Osu!catch pp from """+name+""" plays.</p>
<p>Data taken from top 10,000 players.</p>
<p>Doesn't include bonus pp.</p>
""")
    if name != "Loved":
        file.write("""<p>Doesn't include Loved maps.</p>
        """)
    file.write("""<p>If player has multiple scores on the same map, only the highest pp play is used for calculation.</p>
<p>Click someone's name to see their top ranks.</p>
""" +
("""<p>There is a separate leaderboard that bans the """ + str(len(banSet)) + """ most overweighted maps. Click the top of the table to sort.</p>
""" if hasBanList else "")
+ """<p>Using 1st October 2022 data. Data is released once a month at <a href="https://data.ppy.sh/">data.ppy.sh</a>, used with permission</p>
<p><a href=\""""+name+"""/all.html">Top 200 plays overall</a></p>
<p><a href=\""""+name+"""/farm.html">Top 1000 farm maps</a></p>
<div class="search_field">
  <input id="user_search_text" type="text" placeholder="Search by username...">
  <input id="user_search_button" type="button" value="search">
  <span>(Case-insensitive)</span>
</div>
<div class="search_field">
  <label for="country_ranking">Filter by country:</label>
  <select id="country_ranking">
    <option value="all" selected>All country</option>
""")
    for x in filteredCountryList:
        file.write("""    <option value=\""""+countryCodes[x].replace(" ", "_")+"""">"""+countryCodes[x]+"""</option>
""")
    file.write("""  </select>
</div>
<div class="search_field">
  <input id="reset" type="button" value="Clear search result">
</div>
<div id="ranking-wrapper">
  <table table class="tablesorter">
    <thead>
      <tr>
        <th data-lockedorder="asc" class="text-left">#</th>
        <th data-sorter="false" id="user_name_head">Name</th>
        <th data-lockedorder="desc">PP</th>""" + ("""
        <th data-lockedorder="desc">Filtered<br>PP</th>
        <th data-lockedorder="asc" class="text-left">#</th>""" if hasBanList else "") +
"""      </tr>
    </thead>
    <tbody>
""")
    rank = 1
    for x in IDToPP[:count]:
        file.write("""      <tr class=\""""+countryCodes[IDToUser[x[0]].country].replace(" ", "_")+"""">
        <td>"""+str(rank)+"""</td>
        <td class="user_name">
          <a href=\""""+name+"/"+str(x[0])+""".html">"""+IDToUser[x[0]].name+"""</a>
        </td>
        <td>"""+"{:.2f}".format(x[1])+(("""</td>
        <td>"""+"{:.2f}".format(IDToBannedPP[x[0]])+"""</td>
        <td>"""+str(banRanked[x[0]])) if hasBanList else "")+"""</td>
      </tr>""")
        rank += 1
    file.write("""    </tbody>
  </table>
</div>
  </div>"""+banListString+"""
  </body>
<script>
  "use strict";
  window.addEventListener('pageshow', () => {
    $("#country_ranking").val("all");
    $("#user_search_text").val("");
  });
  $(() => {
    const escapeRegExp = (string) => string.replace(/[.*+?^${}()|[\]\\\\]/g, '\\\\$&');
    const resetTable = () => $("tr").removeClass('hide');
    let isNameFiltered = false;
    let isCountryFiltered = false;
    $("#user_search_button").on("click", () => {
      if(isNameFiltered) {
        resetTable();
      }
      const search_text = $("#user_search_text").val();
      $(".user_name a").each((_, e) => {
        const user_elem = $(e);
        const user_parent = user_elem.closest("tr");
        const val = user_elem.text().toUpperCase();
        if (val.match(escapeRegExp(search_text.toUpperCase()))) {
          user_parent.removeClass('hide');
        } else {
          user_parent.addClass('hide');
        }
      });
      isNameFiltered = true;
    });

    $("#reset").on("click", () => {
      resetTable();
      $("#country_ranking").val("all");
      $("#user_search_text").val("");
    });

    $("#country_ranking").on("change", () => {
      if (isCountryFiltered) {
        resetTable();
      }
      const selected_country = $("#country_ranking").val();
      if (selected_country === "all") {
        resetTable();
      } else {
        $("tbody tr").each((_, e) => {
          const user_row = $(e);
          if (user_row.attr("class") === selected_country) {
            user_row.removeClass('hide');
          } else {
            user_row.addClass('hide');
          }
        });
        isCountryFiltered = true;
      }
    });
  });
</script>
</html>""")


def YMDvsTheWorld(YMDID, userIDToPlays, IDToUser, countryCodes, IDToBeatmap, IDToBeatmapSet, includeMods=0, excludeMods=0, count=200):
    IDToPP = []
    allPlays = []
    for x in userIDToPlays:
        if x == YMDID:
            YMDPlays = playFilter(userIDToPlays[x], includeMods, excludeMods)
            printPlays(YMDPlays, IDToBeatmap, IDToBeatmapSet, IDToUser, "Total", YMDID, count)
        else:
            filteredPlays = playFilter(userIDToPlays[x], includeMods=includeMods, excludeMods=excludeMods)
            allPlays.extend(filteredPlays[0:100])
            IDToPP.append((x, ppCalculate(filteredPlays)))
    allPlays.sort(key=lambda item: item.pp, reverse=True)
    printPlays(allPlays, IDToBeatmap, IDToBeatmapSet, IDToUser, "Total", count=count, multiuser=True)


def specificFCsLeaderboard(userIDToPlays, IDToUser, IDToBeatmap, countryCodes, count=2000):
    allSet = set()
    rainSet = set()
    for x in IDToBeatmap:
        if IDToBeatmap[x].mode == 2:
            if IDToBeatmap[x].status < 3:
                if IDToBeatmap[x].difficulty[0] >= float(3.495):
                    rainSet.add(x)
                allSet.add(x)
    userScores = []
    for x in userIDToPlays:
        userAllSet = set()
        userRainSet = set()
        for y in userIDToPlays[x]:
            if y.misses == 0:
                if y.modCode & 258 == 0:
                    if y.beatmapID in allSet:
                        userAllSet.add(y.beatmapID)
                    if y.beatmapID in rainSet:
                        userRainSet.add(y.beatmapID)
        userScores.append([x, len(userAllSet), len(userRainSet)])
    userScores.sort(key=lambda item: item[1], reverse=True)
    userScores.sort(key=lambda item: item[2], reverse=True)
    IDtoRainRank = {}
    rank = 1
    for x in userScores:
        IDtoRainRank[x[0]] = rank
        rank += 1
    userScores.sort(key=lambda item: item[1], reverse=True)
    filteredCountrySet = set()
    for x in userScores[0:count]:
        filteredCountrySet.add(IDToUser[x[0]].country)
    filteredCountryList = sorted(filteredCountrySet, key=lambda item: countryCodes[item])
    file = open("html/rankedSpecificFCs.html", "w")
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
        <title>
    Ranked Specific FCs ranking</title>
      </head>
      <body>
        <div class="content">
    <p><a href="index.html">Return to main page</a></p>
    <br>
    <p>Ranking based on total number of ranked ctb maps each user has FCd.</p>
    <p>Data taken from top 10,000 players.</p>
    <p>HT/EZ FCs do not count (even if EZ makes the map harder).</p>
    <p>Overwritten plays (a NM FC & a HR choke) do count.</p>
    <p>Lists of missing FCs are not currently provided, as most users have several thousand.</p>
    <p>In addition to total FCs, there is also a leaderboard that only tracks "difficult" plays. Click the top of the table to sort</p>
    <p>This allows users to compete without playing 3000 Cups/Salads/Platters.</p>
    <p>I arbitrarily chose 3.5* as the cutoff.</p>
    <p> It's approximately the border between Platter & Rain, and includes <a href="http://osu.ppy.sh/b/283299">several</a> <a href="http://osu.ppy.sh/b/369758">maps</a> <a href="https://osu.ppy.sh/b/2905286">that I</a> <a href="http://osu.ppy.sh/b/177970">found</a> <a href="https://osu.ppy.sh/b/2385749">difficult</a>.</p>
    <p>Using 1st October 2022 data. Data is released once a month at <a href="https://data.ppy.sh/">data.ppy.sh</a>, used with permission</p>
    <div class="search_field">
      <input id="user_search_text" type="text" placeholder="Search by username...">
      <input id="user_search_button" type="button" value="search">
      <span>(Case-insensitive)</span>
    </div>
    <div class="search_field">
      <label for="country_ranking">Filter by country:</label>
      <select id="country_ranking">
        <option value="all" selected>All country</option>
    """)
    for x in filteredCountryList:
        file.write("""    <option value=\"""" + countryCodes[x].replace(" ", "_") + """">""" + countryCodes[x] + """</option>
    """)
    file.write("""  </select>
    </div>
    <div class="search_field">
      <input id="reset" type="button" value="Clear search result">
    </div>
    <div id="ranking-wrapper">
      <table class="tablesorter">
        <thead>
          <tr>
            <th data-lockedorder="asc" class="text-left">#</th>
            <th data-sorter="false" id="user_name_head">Name</th>
            <th data-lockedorder="desc">Total FCs<br>(out of """+str(len(allSet))+""")</th>
            <th data-lockedorder="desc">Rain+ FCs<br>(out of """+str(len(rainSet))+""")</th>
            <th data-lockedorder="asc" class="text-left">#</th>
          </tr>
        </thead>
        <tbody>
    """)
    rank = 1
    for x in userScores[:count]:
        file.write("""      <tr class=\"""" + countryCodes[IDToUser[x[0]].country].replace(" ", "_") + """">
            <td>""" + str(rank) + """</td>
            <td class="user_name">
              <a>""" + IDToUser[x[0]].name + """</a>
            </td>
            <td>""" + str(x[1]) + " ("+"{:.2f}".format(100*x[1]/len(allSet))+"""%)</td>
            <td>""" + str(x[2]) + " ("+"{:.2f}".format(100*x[2]/len(rainSet))+"""%)</td>
            <td>""" + str(IDtoRainRank[x[0]])+"""</td>
          </tr>
""")
        rank += 1
    file.write("""    </tbody>
      </table>
    </div>
      </div>
      </body>
    <script>
      "use strict";
      window.addEventListener('pageshow', () => {
        $("#country_ranking").val("all");
        $("#user_search_text").val("");
      });
      $(() => {
        const escapeRegExp = (string) => string.replace(/[.*+?^${}()|[\]\\\\]/g, '\\\\$&');
        const resetTable = () => $("tr").removeClass('hide');
        let isNameFiltered = false;
        let isCountryFiltered = false;
        $("#user_search_button").on("click", () => {
          if(isNameFiltered) {
            resetTable();
          }
          const search_text = $("#user_search_text").val();
          $(".user_name a").each((_, e) => {
            const user_elem = $(e);
            const user_parent = user_elem.closest("tr");
            const val = user_elem.text().toUpperCase();
            if (val.match(escapeRegExp(search_text.toUpperCase()))) {
              user_parent.removeClass('hide');
            } else {
              user_parent.addClass('hide');
            }
          });
          isNameFiltered = true;
        });

        $("#reset").on("click", () => {
          resetTable();
          $("#country_ranking").val("all");
          $("#user_search_text").val("");
        });

        $("#country_ranking").on("change", () => {
          if (isCountryFiltered) {
            resetTable();
          }
          const selected_country = $("#country_ranking").val();
          if (selected_country === "all") {
            resetTable();
          } else {
            $("tbody tr").each((_, e) => {
              const user_row = $(e);
              if (user_row.attr("class") === selected_country) {
                user_row.removeClass('hide');
              } else {
                user_row.addClass('hide');
              }
            });
            isCountryFiltered = true;
          }
        });
      });
    </script>
    </html>""")


# file = open("userIDToLovedPlays.pkl", "rb")
# userIDToPlays = pickle.load(file)
# file.close()
# file = open("IDToUser.pkl", "rb")
# IDToUser = pickle.load(file)
# file.close()
# file = open("countryCodes.pkl", "rb")
# countryCodes = pickle.load(file)
# file.close()
# file = open("IDToBeatmap.pkl", "rb")
# IDToBeatmap = pickle.load(file)
# file.close()
# file = open("IDToBeatmapSet.pkl", "rb")
# IDToBeatmapSet = pickle.load(file)
# file.close()