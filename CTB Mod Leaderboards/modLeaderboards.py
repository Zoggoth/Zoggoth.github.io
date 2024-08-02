import tools
import pickle

oneMonthAgo = tools.oneMonthAgo
oneYearAgo = tools.oneYearAgo
dateName = tools.dateName


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
    file = open("html/{}/farm.html".format(name), "w")
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
    <title>{} Farm Maps</title>
  </head>
  <body>
    <div class="content">
<p><a href="../{}.html">Return to leaderboard</a></p>
<br>
<p><b>{} Farm Maps (Click on PP or Farm Score to sort)</b></p>    
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
""".format(name, name, name))
    rank = 0
    for x in farmMaps[:count]:
        rank += 1
        file.write("""	  <tr >
        <td>{}</td>
        <td><a href="https://osu.ppy.sh/b/{}?m=2" target="_blank">{} [{}]</a> </td>
        <td>{}</td>
        <td><b>{:.2f}pp</b></td>
        <td>{:.2f}</td>
      </tr>
""".format(rank, x[0], IDToBeatmapSet[IDToBeatmap[x[0]].beatmapSetID].title, IDToBeatmap[x[0]].difficultyName, tools.modCodeToText(x[1]), IDAndModToPPAndScore[x][0], IDAndModToPPAndScore[x][1]))
    file.write("""    </tbody>
  </table>
</div>
  </div>
  </body>
</html>""")


def printPlays(plays, IDToBeatmap, IDToBeatmapSet, IDToUser, name, user=0, count=100, multiuser=False):
    beatmapIDtoUserList = {}
    beatmapIDtoPP = {}
    beatmapIDtoDate = {}
    if multiuser:
        for x in plays:
            if x.beatmapID in beatmapIDtoUserList:
                if x.pp > beatmapIDtoPP[x.beatmapID] - 0.01:
                    beatmapIDtoUserList[x.beatmapID].append(x.userID)
                    beatmapIDtoDate[x.beatmapID] = min(beatmapIDtoDate[x.beatmapID], x.date)
            else:
                beatmapIDtoUserList[x.beatmapID] = [x.userID]
                beatmapIDtoPP[x.beatmapID] = x.pp
                beatmapIDtoDate[x.beatmapID] = x.date
    plays = playFilter(plays)
    pp = ppCalculate(plays, count)
    filename = "html/{}/".format(name)
    if multiuser:
        filename += "all.html"
    else:
        filename += "{}.html".format(user)
    file = open(filename, "w")
    username = "Everyone" if multiuser else IDToUser[user].name
    file.write("""<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width">
    <link rel="stylesheet" href="https://unpkg.com/ress/dist/ress.min.css">
<link rel="stylesheet" href="../../../style.css">
    <title>{}'s {} plays</title>
  </head>
  <body>
    <div class="content">
<p><a href="../{}.html">Return to leaderboard</a></p>
<br>
<p><b>{} ({:.2f} pp)</b></p>
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
""".format(username, name, ("index" if name == "Total" else name), username, pp))
    if multiuser:
        file.write("""<th>Player</th>
""")
    file.write("""      </tr>
    </thead>
    <tbody>""")
    rank = 1
    for x in plays[:count]:
        file.write("""
        <tr""")
        if multiuser:
            if beatmapIDtoDate[x.beatmapID] >= oneMonthAgo:
                file.write(""" class="recent\"""")
        else:
            if x.date >= oneMonthAgo:
                file.write(""" class="recent\"""")
        file.write(""">
        <td>{}</td>
        <td><a href="https://osu.ppy.sh/b/{}?m=2" target="_blank">{} [{}]</a> </td>
        <td>""".format(rank, x.beatmapID, IDToBeatmapSet[IDToBeatmap[x.beatmapID].beatmapSetID].title, IDToBeatmap[x.beatmapID].difficultyName))
        if multiuser:
            if len(beatmapIDtoUserList[x.beatmapID]) > 1:
                file.write(tools.modCodeToText((x.modCode & 1370)))
            else:
                file.write(tools.modCodeToText(x.modCode))
        else:
            file.write(tools.modCodeToText(x.modCode))
        file.write("""</td>
        <td>{}</td>
        <td>{}/{}x</td>
        <td><b>{:.2f}pp</b></td>""".format(x.misses, x.combo, IDToBeatmap[x.beatmapID].maxCombo, x.pp))
        if multiuser:
            if len(beatmapIDtoUserList[x.beatmapID])>5:
                usernameList = "Several People"
            else:
                usernameList = ""
                for y in beatmapIDtoUserList[x.beatmapID]:
                    usernameList += "{} & ".format(IDToUser[y].name)
                usernameList = usernameList[:-3]
            file.write("<td>{}</td>".format(usernameList))
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


def modLeaderboard(name, userIDToPlays, IDToUser, countryCodes, IDToBeatmap, IDToBeatmapSet, includeMods=0, excludeMods=0, count=2000, banSet=None):
    if banSet is None:
        banSet = {}
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
        recent = False
        for y in filteredPlays[0:100]:
            if y.date >= oneYearAgo:
                recent = True
                break
        printPlays(filteredPlays, IDToBeatmap, IDToBeatmapSet, IDToUser, name, x[0])
        filteredCountrySet.add(IDToUser[x[0]].country)
        if not recent:
            continue
        # totalpp = IDToUser[x[0]].pp
        totalpp = ppCalculate(filteredPlays)
        multiplier = float(1)
        for y in filteredPlays:
            if (y.beatmapID, y.modCode & 1370) in IDAndModToPPAndScore:
                IDAndModToPPAndScore[(y.beatmapID, y.modCode & 1370)][0] = max(IDAndModToPPAndScore[(y.beatmapID, y.modCode & 1370)][0], y.pp)
                IDAndModToPPAndScore[(y.beatmapID, y.modCode & 1370)][1] = IDAndModToPPAndScore[(y.beatmapID, y.modCode & 1370)][1] + y.pp*multiplier/totalpp
            else:
                IDAndModToPPAndScore[(y.beatmapID, y.modCode & 1370)] = [y.pp, y.pp*multiplier/totalpp]
            multiplier *= .95
    farmMaps = sorted(IDAndModToPPAndScore, key=lambda item: IDAndModToPPAndScore[item][1], reverse=True)
    printFarmMaps(farmMaps, IDAndModToPPAndScore, IDToBeatmap, IDToBeatmapSet, name)
    filteredCountryList = sorted(filteredCountrySet, key=lambda item: countryCodes[item])
    banListString = ""
    if hasBanList:
        banListString = "<p>Banlist</p>"
        for x in banSet:
            banListString += """\n<p><a href="https://osu.ppy.sh/b/{}?m=2" target="_blank">{} [{}]</a></p>""".format(x, IDToBeatmapSet[IDToBeatmap[x].beatmapSetID].title, IDToBeatmap[x].difficultyName)
    IDToStoredData = {}
    lastMonth = []
    try:
        file = open("last month/previous{}.pkl".format(name), "rb")
        lastMonth = pickle.load(file)
        file.close()
    except:
        lastMonth = []
    file = open("html/{}.html".format(name), "w", encoding="utf-8")
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
    <title>{} pp ranking</title>
  </head>
  <body>
    <div class="content">
<p><a href="index.html">Return to main page</a></p>
<br>
<p>Osu!catch pp from {} plays.</p>
<p>Data taken from top 10,000 players.</p>
<p>Doesn't include bonus pp.</p>
""".format(name, name))
    if name != "Loved":
        file.write("""<p>Doesn't include Loved maps.</p>
        """)
    file.write("""<p>If player has multiple scores on the same map, only the highest pp play is used for calculation.</p>
<p>Click someone's name to see their top ranks.</p>
""")
    if hasBanList:
        file.write("""<p>There is a separate leaderboard that bans the {} most overweighted maps. Click the top of the table to sort.</p>
""".format(len(banSet)))
    file.write("""<p>Using {} data. Data is released once a month at <a href="https://data.ppy.sh/">data.ppy.sh</a>, used with permission</p>
<p><a href="{}/all.html">Top 200 plays overall</a></p>
<p><a href="{}/farm.html">Top 1000 farm maps</a></p>
<div class="search_field">
  <input id="user_search_text" type="text" placeholder="Search by username...">
  <input id="user_search_button" type="button" value="search">
  <span>(Case-insensitive)</span>
</div>
<div class="search_field">
  <label for="country_ranking">Filter by country:</label>
  <select id="country_ranking">
    <option value="all" selected>All country</option>
""".format(dateName, name, name))
    for x in filteredCountryList:
        file.write("""    <option value="{}">{}</option>
""".format(countryCodes[x].replace(" ", "_"), countryCodes[x]))
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
        <th data-lockedorder="desc">PP</th>""")
    if hasBanList:
        file.write("""
        <th data-lockedorder="desc">Filtered<br>PP</th>
        <th data-lockedorder="asc" class="text-left">#</th>""")
    file.write("""      </tr>
    </thead>
    <tbody>
""")
    rank = 1
    for x in IDToPP[:count]:
        file.write("""      <tr class="{}">
        <td>{}""".format(countryCodes[IDToUser[x[0]].country].replace(" ", "_"), rank))
        if x[0] in lastMonth:
            change = lastMonth[x[0]][0] - rank
            if change == 0:
                file.write(""" <span class="rank_no_change">(→)</span>""")
            if change > 0:
                file.write(""" <span class="rank_up">(+{})</span>""".format(change))
            if change < 0:
                file.write(""" <span class="rank_down">({})</span>""".format(change))
        else:
            file.write(""" <span class="rank_new">(New)</span>""")
        file.write("""</td>
        <td class="user_name">
          <a href="{}/{}.html">{}</a>
        </td>
        <td>{:.2f}""".format(name, x[0], IDToUser[x[0]].name, x[1]))
        if x[0] in lastMonth:
            change = x[1] - lastMonth[x[0]][1]
            if change == 0:
                file.write(""" <span class="rank_no_change">(+0)</span>""")
            if change < 0:
                file.write(""" <span class="rank_down">({:.2f})</span>""".format(change))
            if change > 0:
                if change < 50:
                    file.write(""" <span class="pp_50">(+{:.2f})</span>""".format(change))
                else:
                    if change < 100:
                        file.write(""" <span class="pp_100">(+{:.2f})</span>""".format(change))
                    else:
                        if change < 200:
                            file.write(""" <span class="rank_new">(+{:.2f})</span>""".format(change))
                        else:
                            file.write(""" <span class="rank_up">(+{:.2f})</span>""".format(change))
        if hasBanList:
            file.write("""</td>
        <td>{:.2f}""".format(IDToBannedPP[x[0]]))
            if x[0] in lastMonth:
                change = IDToBannedPP[x[0]] - lastMonth[x[0]][3]
                if change == 0:
                    file.write(""" <span class="rank_no_change">(+0)</span>""")
                if change < 0:
                    file.write(""" <span class="rank_down">({:.2f})</span>""".format(change))
                if change > 0:
                    if change < 50:
                        file.write(""" <span class="pp_50">(+{:.2f})</span>""".format(change))
                    else:
                        if change < 100:
                            file.write(""" <span class="pp_100">(+{:.2f})</span>""".format(change))
                        else:
                            if change < 200:
                                file.write(""" <span class="rank_new">(+{:.2f})</span>""".format(change))
                            else:
                                file.write(""" <span class="rank_up">(+{:.2f})</span>""".format(change))
            file.write("""</td>
        <td>{}""".format(banRanked[x[0]]))
            if x[0] in lastMonth:
                change = lastMonth[x[0]][2] - banRanked[x[0]]
                if change == 0:
                    file.write(""" <span class="rank_no_change">(→)</span>""")
                if change > 0:
                    file.write(""" <span class="rank_up">(+{})</span>""".format(change))
                if change < 0:
                    file.write(""" <span class="rank_down">({})</span>""".format(change))
            else:
                file.write(""" <span class="rank_new">(New)</span>""")
        file.write("""</td>
      </tr>""")
        if hasBanList:
            IDToStoredData[x[0]] = (rank, x[1], banRanked[x[0]], IDToBannedPP[x[0]])
        else:
            IDToStoredData[x[0]] = (rank, x[1])
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
    file.close()
    file = open("this month/previous{}.pkl".format(name), "wb")
    pickle.dump(IDToStoredData, file)
    file.close()


def YMDvsTheWorld(YMDID, userIDToPlays, IDToUser, IDToBeatmap, IDToBeatmapSet, includeMods=0, excludeMods=0, count=200):
    allPlays = []
    for x in userIDToPlays:
        if x == YMDID:
            YMDPlays = playFilter(userIDToPlays[x], includeMods, excludeMods)
            printPlays(YMDPlays, IDToBeatmap, IDToBeatmapSet, IDToUser, "Total", YMDID, count)
        else:
            filteredPlays = playFilter(userIDToPlays[x], includeMods=includeMods, excludeMods=excludeMods)
            allPlays.extend(filteredPlays[0:count])
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
    IDToStoredData = {}
    lastMonth = []
    try:
        file = open("last month/previousRanked.pkl", "rb")
        lastMonth = pickle.load(file)
        file.close()
    except:
        lastMonth = []
    file = open("html/rankedSpecificFCs.html", "w", encoding="utf-8")
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
    <p>Overwritten plays (a NM FC & a HR choke) still count as FCing, even if the FC comes after the choke.</p>
    <p>Lists of missing FCs are not currently provided, as most users have several thousand.</p>
    <p>In addition to total FCs, there is also a leaderboard that only tracks "difficult" plays. Click the top of the table to sort</p>
    <p>This allows users to compete without playing 4000 Cups/Salads/Platters.</p>
    <p>I arbitrarily chose 3.5* as the cutoff.</p>
    <p> It's approximately the border between Platter & Rain, and includes <a href="http://osu.ppy.sh/b/283299">several</a> <a href="http://osu.ppy.sh/b/369758">maps</a> <a href="https://osu.ppy.sh/b/2905286">that I</a> <a href="http://osu.ppy.sh/b/177970">found</a> <a href="https://osu.ppy.sh/b/2385749">difficult</a>.</p>
    <p><a href="rarestFCs.html">Rarest FCs</a></p>
    <p>Using {} data. Data is released once a month at <a href="https://data.ppy.sh/">data.ppy.sh</a>, used with permission</p>
    <div class="search_field">
      <input id="user_search_text" type="text" placeholder="Search by username...">
      <input id="user_search_button" type="button" value="search">
      <span>(Case-insensitive)</span>
    </div>
    <div class="search_field">
      <label for="country_ranking">Filter by country:</label>
      <select id="country_ranking">
        <option value="all" selected>All country</option>
    """.format(dateName))
    for x in filteredCountryList:
        file.write("""    <option value="{}">{}</option>
    """.format(countryCodes[x].replace(" ", "_"), countryCodes[x]))
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
            <th data-lockedorder="desc">Total FCs<br>(out of {})</th>
            <th data-lockedorder="desc">Rain+ FCs<br>(out of {})</th>
            <th data-lockedorder="asc" class="text-left">#</th>
          </tr>
        </thead>
        <tbody>
    """.format(len(allSet), len(rainSet)))
    rank = 1
    for x in userScores[:count]:
        file.write("""      <tr class="{}">
            <td>{}""".format(countryCodes[IDToUser[x[0]].country].replace(" ", "_"),rank))
        if x[0] in lastMonth:
            change = lastMonth[x[0]][0] - rank
            if change == 0:
                file.write(""" <span class="rank_no_change">(→)</span>""")
            if change > 0:
                file.write(""" <span class="rank_up">(+{})</span>""".format(change))
            if change < 0:
                file.write(""" <span class="rank_down">({})</span>""".format(change))
        else:
            file.write(""" <span class="rank_new">(New)</span>""")
        file.write("""</td>
            <td class="user_name">
              <a>{}</a>
            </td>
            <td>{} ({:.2f}%)""".format(IDToUser[x[0]].name, x[1], 100*x[1]/len(allSet)))
        if x[0] in lastMonth:
            change = x[1]/len(allSet) - lastMonth[x[0]][1]
            if change >= 0:
                if change >= 0.0095:
                    file.write(""" <span class="rank_up">(+{:.1f}%)</span>""".format(100*change))
                else:
                    file.write(""" <span class="pp_100">(+{:.1f}%)</span>""".format(100*change))
            else:
                file.write(""" <span class="rank_down">({:.1f}%)</span>""".format(100*change))
        file.write("""</td>
            <td>{} ({:.2f}%)""".format(x[2], 100*x[2]/len(rainSet)))
        if x[0] in lastMonth:
            change = x[2]/len(rainSet) - lastMonth[x[0]][3]
            if change >= 0:
                if change >= 0.0095:
                    file.write(""" <span class="rank_up">(+{:.1f}%)</span>""".format(100*change))
                else:
                    file.write(""" <span class="pp_100">(+{:.1f}%)</span>""".format(100*change))
            else:
                file.write(""" <span class="rank_down">({:.1f}%)</span>""".format(100*change))
        file.write("""</td>
            <td>{}""".format(IDtoRainRank[x[0]]))
        if x[0] in lastMonth:
            change = lastMonth[x[0]][2] - IDtoRainRank[x[0]]
            if change == 0:
                file.write(""" <span class="rank_no_change">(→)</span>""")
            if change > 0:
                file.write(""" <span class="rank_up">(+{})</span>""".format(change))
            if change < 0:
                file.write(""" <span class="rank_down">({})</span>""".format(change))
        else:
            file.write(""" <span class="rank_new">(New)</span>""")
        file.write("""</td>
          </tr>
""")
        IDToStoredData[x[0]] = (rank, x[1]/len(allSet), IDtoRainRank[x[0]], x[2]/len(rainSet))
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
    file.close()
    file = open("this month/previousRanked.pkl", "wb")
    pickle.dump(IDToStoredData, file)
    file.close()
    import fcsPerYear

def rankedSpecificPasses(userIDToPlays, IDToUser, IDToBeatmap, countryCodes, count=2000):
    DMCA = set()
    try:
        file = open("DMCA.txt","r")
        text = file.read().split("\n")
        for x in text:
            DMCA.add(int(x))
    except:
        DMCA = set()
    allSet = set()
    for x in IDToBeatmap:
        if IDToBeatmap[x].mode == 2:
            if IDToBeatmap[x].status < 3:
                if IDToBeatmap[x].beatmapSetID not in DMCA:
                    allSet.add(x)
    userScores = []
    for x in userIDToPlays:
        userAllSet = set()
        for y in userIDToPlays[x]:
            if y.beatmapID in allSet:
                if y.modCode & 1 == 0:
                    userAllSet.add(y.beatmapID)
                else:
                    accuracyTotal = IDToBeatmap[y.beatmapID].accuracyTotal
                    missTotal = y.misses + y.drpmiss
                    if missTotal/accuracyTotal <= .5:
                        userAllSet.add(y.beatmapID)
        userScores.append([x, len(userAllSet)])
    userScores.sort(key=lambda item: item[1], reverse=True)
    filteredCountrySet = set()
    for x in userScores[0:count]:
        filteredCountrySet.add(IDToUser[x[0]].country)
    filteredCountryList = sorted(filteredCountrySet, key=lambda item: countryCodes[item])
    IDToStoredData = {}
    lastMonth = []
    try:
        file = open("last month/previousSpecificPasses.pkl", "rb")
        lastMonth = pickle.load(file)
        file.close()
    except:
        lastMonth = []
    file = open("html/rankedSpecificPasses.html", "w", encoding="utf-8")
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
        <title>
    Ranked Specific Passes</title>
      </head>
      <body>
        <div class="content">
    <p><a href="index.html">Return to main page</a></p>
    <br>
    <p>Ranking based on total number of ranked ctb maps passed.</p>
    <p>Data taken from top 10,000 players.</p>
    <p>Any ranked mod is allowed (so no Auto, Relax, ScoreV2 etc.)</p>
    <p>If you are aiming for 100%, please see <a href="rules.html">here</a>. tl;dr Don't AFK. Just play the way you normally do.</p>
    <p>Using {} data. Data is released once a month at <a href="https://data.ppy.sh/">data.ppy.sh</a>, used with permission</p>
    <div class="search_field">
      <input id="user_search_text" type="text" placeholder="Search by username...">
      <input id="user_search_button" type="button" value="search">
      <span>(Case-insensitive)</span>
    </div>
    <div class="search_field">
      <label for="country_ranking">Filter by country:</label>
      <select id="country_ranking">
        <option value="all" selected>All country</option>
    """.format(dateName))
    for x in filteredCountryList:
        file.write("""    <option value="{}">{}</option>
    """.format(countryCodes[x].replace(" ", "_"), countryCodes[x]))
    file.write("""  </select>
    </div>
    <div class="search_field">
      <input id="reset" type="button" value="Clear search result">
    </div>
    <div id="ranking-wrapper">
      <table class="tablesorter">
        <thead>
          <tr>
            <th data-sorter="false" class="text-left">#</th>
            <th data-sorter="false" id="user_name_head">Name</th>
            <th data-sorter="false">Passes<br>(out of {})</th>
          </tr>
        </thead>
        <tbody>
    """.format(len(allSet)))
    rank = 1
    for x in userScores[:count]:
        file.write("""      <tr class="{}">
            <td>{}""".format(countryCodes[IDToUser[x[0]].country].replace(" ", "_"),rank))
        if x[0] in lastMonth:
            change = lastMonth[x[0]][0] - rank
            if change == 0:
                file.write(""" <span class="rank_no_change">(→)</span>""")
            if change > 0:
                file.write(""" <span class="rank_up">(+{})</span>""".format(change))
            if change < 0:
                file.write(""" <span class="rank_down">({})</span>""".format(change))
        else:
            file.write(""" <span class="rank_new">(New)</span>""")
        file.write("""</td>
            <td class="user_name">
              <a>{}</a>
            </td>
            <td>{} ({:.2f}%)""".format(IDToUser[x[0]].name, x[1], 100*x[1]/len(allSet)))
        if x[0] in lastMonth:
            change = x[1]/len(allSet) - lastMonth[x[0]][1]
            if change >= 0:
                if change >= 0.0095:
                    file.write(""" <span class="rank_up">(+{:.1f}%)</span>""".format(100*change))
                else:
                    file.write(""" <span class="pp_100">(+{:.1f}%)</span>""".format(100*change))
            else:
                file.write(""" <span class="rank_down">({:.1f}%)</span>""".format(100*change))
        IDToStoredData[x[0]] = (rank, x[1] / len(allSet))
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
    file.close()
    file = open("this month/previousSpecificPasses.pkl", "wb")
    pickle.dump(IDToStoredData, file)
    file.close()


def number1s(userIDToRankedPlays, userIDToLovedPlays, IDToUser, countryCodes, count = 2000):
    mapAndCountryToBest = {}
    for x in userIDToRankedPlays:
        country = IDToUser[x].country
        for y in userIDToRankedPlays[x]:
            if mapAndCountryToBest.get((y.beatmapID, country), 0) == 0:
                mapAndCountryToBest[(y.beatmapID, country)] = [y.score, [x]]
            elif mapAndCountryToBest[(y.beatmapID, country)][0] < y.score:
                mapAndCountryToBest[(y.beatmapID, country)] = [y.score, [x]]
            elif mapAndCountryToBest[(y.beatmapID, country)][0] == y.score:
                mapAndCountryToBest[(y.beatmapID, country)][1].append(x)
            if mapAndCountryToBest.get((y.beatmapID, "All"), 0) == 0:
                mapAndCountryToBest[(y.beatmapID, "All")] = [y.score, [x]]
            elif mapAndCountryToBest[(y.beatmapID, "All")][0] < y.score:
                mapAndCountryToBest[(y.beatmapID, "All")] = [y.score, [x]]
            elif mapAndCountryToBest[(y.beatmapID, "All")][0] == y.score:
                mapAndCountryToBest[(y.beatmapID, "All")][1].append(x)
    for x in userIDToLovedPlays:
        country = IDToUser[x].country
        for y in userIDToLovedPlays[x]:
            if mapAndCountryToBest.get((y.beatmapID, country), 0) == 0:
                mapAndCountryToBest[(y.beatmapID, country)] = [y.score, [x]]
            elif mapAndCountryToBest[(y.beatmapID, country)][0] < y.score:
                mapAndCountryToBest[(y.beatmapID, country)] = [y.score, [x]]
            elif mapAndCountryToBest[(y.beatmapID, country)][0] == y.score:
                mapAndCountryToBest[(y.beatmapID, country)][1].append(x)
            if mapAndCountryToBest.get((y.beatmapID, "All"), 0) == 0:
                mapAndCountryToBest[(y.beatmapID, "All")] = [y.score, [x]]
            elif mapAndCountryToBest[(y.beatmapID, "All")][0] < y.score:
                mapAndCountryToBest[(y.beatmapID, "All")] = [y.score, [x]]
            elif mapAndCountryToBest[(y.beatmapID, "All")][0] == y.score:
                mapAndCountryToBest[(y.beatmapID, "All")][1].append(x)
    IDToCountry1s = {}
    IDToGlobal1s = {}
    for x in mapAndCountryToBest:
        if x[1] == "All":
            setversion = set()
            for y in mapAndCountryToBest[x][1]:
                setversion.add(y)
            for y in setversion:
                IDToGlobal1s[y] = IDToGlobal1s.get(y, 0) + 1
        else:
            setversion = set()
            for y in mapAndCountryToBest[x][1]:
                setversion.add(y)
            for y in setversion:
                IDToCountry1s[y] = IDToCountry1s.get(y, 0) + 1
    top2000Country = sorted(IDToCountry1s, key=lambda item: IDToCountry1s[item], reverse=True)
    top2000Country = top2000Country[:count]
    IDToCountryRank = {}
    rank = 1
    for x in top2000Country:
        IDToCountryRank[x] = rank
        rank += 1
    top2000Country.sort(key=lambda item: IDToGlobal1s.get(item,0), reverse=True)
    IDToGlobalRank = {}
    rank = 1
    for x in top2000Country:
        IDToGlobalRank[x] = rank
        rank += 1
    filteredCountrySet = set()
    for x in top2000Country:
        filteredCountrySet.add(IDToUser[x].country)
    filteredCountryList = sorted(filteredCountrySet, key=lambda item: countryCodes[item])
    IDToStoredData = {}
    lastMonth = []
    try:
        file = open("last month/previousNumber1s.pkl", "rb")
        lastMonth = pickle.load(file)
        file.close()
    except:
        lastMonth = []
    file = open("html/number1s.html", "w", encoding="utf-8")
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
        <title>
    Number 1s ranking</title>
      </head>
      <body>
        <div class="content">
    <p><a href="index.html">Return to main page</a></p>
    <br>
    <p>Ranking based on total number of first places</p>
    <p>If 2 people have the same score, they both get first (normally goes to whoever set the score first)</p>
    <p>Data taken from top 10,000 players.</p>
    <p>Using {} data. Data is released once a month at <a href="https://data.ppy.sh/">data.ppy.sh</a>, used with permission</p>
    <div class="search_field">
      <input id="user_search_text" type="text" placeholder="Search by username...">
      <input id="user_search_button" type="button" value="search">
      <span>(Case-insensitive)</span>
    </div>
    <div class="search_field">
      <label for="country_ranking">Filter by country:</label>
      <select id="country_ranking">
        <option value="all" selected>All country</option>
    """.format(dateName))
    for x in filteredCountryList:
        file.write("""    <option value="{}">{}</option>
    """.format(countryCodes[x].replace(" ", "_"), countryCodes[x]))
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
                <th data-lockedorder="desc">Global #1s</th>
                <th data-lockedorder="desc">Country #1s</th>
                <th data-lockedorder="asc" class="text-left">#</th>
              </tr>
            </thead>
            <tbody>
        """)
    for x in top2000Country:
        file.write("""      <tr class="{}">
                <td>{}""".format(countryCodes[IDToUser[x].country].replace(" ", "_"),IDToGlobalRank[x]))
        if x in lastMonth:
            change = lastMonth[x][0] - IDToGlobalRank[x]
            if change == 0:
                file.write(""" <span class="rank_no_change">(→)</span>""")
            if change > 0:
                file.write(""" <span class="rank_up">(+{})</span>""".format(change))
            if change < 0:
                file.write(""" <span class="rank_down">({})</span>""".format(change))
        else:
            file.write(""" <span class="rank_new">(New)</span>""")
        file.write("""</td>
                <td class="user_name">
                  <a>{}</a>
                </td>
                <td>{}""".format(IDToUser[x].name,IDToGlobal1s.get(x,0)))
        if x in lastMonth:
            change = IDToGlobal1s.get(x,0) - lastMonth[x][1]
            if change == 0:
                file.write(""" <span class="rank_no_change">(→)</span>""")
            if change > 0:
                file.write(""" <span class="rank_up">(+{})</span>""".format(change))
            if change < 0:
                file.write(""" <span class="rank_down">({})</span>""".format(change))
        file.write("""</td>
                <td>{}""".format(IDToCountry1s[x]))
        if x in lastMonth:
            change = IDToCountry1s[x] - lastMonth[x][3]
            if change == 0:
                file.write(""" <span class="rank_no_change">(→)</span>""")
            if change > 0:
                file.write(""" <span class="rank_up">(+{})</span>""".format(change))
            if change < 0:
                file.write(""" <span class="rank_down">({})</span>""".format(change))
        file.write("""</td>
                <td>{}""".format(IDToCountryRank[x]))
        if x in lastMonth:
            change = lastMonth[x][2] - IDToCountryRank[x]
            if change == 0:
                file.write(""" <span class="rank_no_change">(→)</span>""")
            if change > 0:
                file.write(""" <span class="rank_up">(+{})</span>""".format(change))
            if change < 0:
                file.write(""" <span class="rank_down">({})</span>""".format(change))
        else:
            file.write(""" <span class="rank_new">(New)</span>""")
        file.write("""</td>
              </tr>
    """)
        IDToStoredData[x] = (IDToGlobalRank[x], IDToGlobal1s.get(x,0), IDToCountryRank[x], IDToCountry1s[x])
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
    file.close()
    file = open("this month/previousNumber1s.pkl", "wb")
    pickle.dump(IDToStoredData, file)
    file.close()

def hundrethPlay(userIDToPlays, IDToUser, IDToBeatmap, countryCodes, count=2000):
    IDToScore = {}
    IDToConvertScore = {}
    for x in userIDToPlays:
        filteredPlays = playFilter(userIDToPlays[x], includeMods=0, excludeMods=0)
        totalCount = 0
        convertCount = 0
        for y in filteredPlays:
            totalCount += 1
            if IDToBeatmap[y.beatmapID].mode == 0:
                convertCount += 1
            if totalCount == 100:
                IDToScore[x] = y.pp
            if convertCount == 100:
                IDToConvertScore[x] = y.pp
                break
        if convertCount < 100:
            IDToConvertScore[x] = convertCount - 100
        if totalCount < 100:
            IDToScore[x] = totalCount - 100
    top2000Total = sorted(IDToScore, key=lambda item: IDToConvertScore[item], reverse=True)
    IDToConvertRank = {}
    rank = 1
    for x in top2000Total:
        IDToConvertRank[x] = rank
        rank += 1
    top2000Total.sort(key=lambda item: IDToScore[item], reverse=True)
    top2000Total = top2000Total[:count]
    IDToTotalRank = {}
    rank = 1
    for x in top2000Total:
        IDToTotalRank[x] = rank
        rank += 1
    filteredCountrySet = set()
    for x in top2000Total:
        filteredCountrySet.add(IDToUser[x].country)
    filteredCountryList = sorted(filteredCountrySet, key=lambda item: countryCodes[item])
    IDToStoredData = {}
    lastMonth = []
    try:
        file = open("last month/previous100s.pkl", "rb")
        lastMonth = pickle.load(file)
        file.close()
    except:
        lastMonth = []
    file = open("html/100play.html", "w", encoding="utf-8")
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
            <title>
        100th play ranking</title>
          </head>
          <body>
            <div class="content">
        <p><a href="index.html">Return to main page</a></p>
        <br>
        <p>Ranking based on users 100th best play & 100th best convert</p>
        <p>Doesn't include Loved maps.</p>
        <p>Data taken from top 10,000 players.</p>
        <p>Using {} data. Data is released once a month at <a href="https://data.ppy.sh/">data.ppy.sh</a>, used with permission</p>
        <div class="search_field">
          <input id="user_search_text" type="text" placeholder="Search by username...">
          <input id="user_search_button" type="button" value="search">
          <span>(Case-insensitive)</span>
        </div>
        <div class="search_field">
          <label for="country_ranking">Filter by country:</label>
          <select id="country_ranking">
            <option value="all" selected>All country</option>
        """.format(dateName))
    for x in filteredCountryList:
        file.write("""    <option value="{}">{}</option>
        """.format(countryCodes[x].replace(" ", "_"), countryCodes[x]))
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
                    <th data-lockedorder="desc">100th play</th>
                    <th data-sorter="false">100th convert</th>
                    <th data-lockedorder="asc" class="text-left">#</th>
                  </tr>
                </thead>
                <tbody>
            """)
    for x in top2000Total:
        file.write("""      <tr class="{}">
                    <td>{}""".format(countryCodes[IDToUser[x].country].replace(" ", "_"),IDToTotalRank[x]))
        if x in lastMonth:
            change = lastMonth[x][2] - IDToTotalRank[x]
            if change == 0:
                file.write(""" <span class="rank_no_change">(→)</span>""")
            if change > 0:
                file.write(""" <span class="rank_up">(+{})</span>""".format(change))
            if change < 0:
                file.write(""" <span class="rank_down">({})</span>""".format(change))
        else:
            file.write(""" <span class="rank_new">(New)</span>""")
        file.write("""</td>
                    <td class="user_name">
                      <a>{}</a>
                    </td>
                    <td>{:.2f}""".format(IDToUser[x].name, IDToScore.get(x, 0)))
        if x in lastMonth:
            change = IDToScore.get(x, 0) - lastMonth[x][1]
            if change == 0:
                file.write(""" <span class="rank_no_change">(→)</span>""")
            if change > 0:
                file.write(""" <span class="rank_up">(+{:.2f})</span>""".format(change))
            if change < 0:
                file.write(""" <span class="rank_down">({:.2f})</span>""".format(change))
        file.write("""</td>
                    <td>{:.2f}""".format(IDToConvertScore[x]))
        if x in lastMonth:
            change = IDToConvertScore[x] - lastMonth[x][3]
            if change == 0:
                file.write(""" <span class="rank_no_change">(→)</span>""")
            if change > 0:
                file.write(""" <span class="rank_up">(+{:.2f})</span>""".format(change))
            if change < 0:
                file.write(""" <span class="rank_down">({:.2f})</span>""".format(change))
        file.write("""</td>
                    <td>{}""".format(IDToConvertRank[x]))
        if x in lastMonth:
            change = lastMonth[x][0] - IDToConvertRank[x]
            if change == 0:
                file.write(""" <span class="rank_no_change">(→)</span>""")
            if change > 0:
                file.write(""" <span class="rank_up">(+{})</span>""".format(change))
            if change < 0:
                file.write(""" <span class="rank_down">({})</span>""".format(change))
        else:
            file.write(""" <span class="rank_new">(New)</span>""")
        file.write("""</td>
                  </tr>
        """)
        IDToStoredData[x] = (IDToConvertRank[x], IDToScore.get(x, 0), IDToTotalRank[x], IDToConvertScore[x])
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
    file.close()
    file = open("this month/previous100s.pkl", "wb")
    pickle.dump(IDToStoredData, file)
    file.close()

def totalPasses(userIDToPlays, IDToUser, IDToBeatmap, countryCodes, count=2000):
    mapCount = 0
    for (_, y) in IDToBeatmap.items():
        if y.mode & 2 == 0:
            if y.status == 1:
                mapCount += 1
    IDToScore = {}
    for (x, y) in userIDToPlays.items():
        userpassed = set()
        for z in y:
            if z.modCode & 1 == 0:
                if IDToBeatmap[z.beatmapID].status == 1:
                    userpassed.add(z.beatmapID)
        IDToScore[x] = userpassed.__len__()
    sortedScores = sorted(IDToScore.items(), key=lambda item: item[1], reverse=True)
    filteredCountrySet = set()
    for (x, _) in sortedScores[:count]:
        filteredCountrySet.add(IDToUser[x].country)
    filteredCountryList = sorted(filteredCountrySet, key=lambda item: countryCodes[item])
    IDToStoredData = {}
    lastMonth = []
    try:
        file = open("last month/previousPasses.pkl", "rb")
        lastMonth = pickle.load(file)
        file.close()
    except:
        lastMonth = []
    file = open("html/passes.html", "w", encoding="utf-8")
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
        <title>Total Passes</title>
      </head>
      <body>
        <div class="content">
    <p><a href="index.html">Return to main page</a></p>
    <br>
    <p>Ranking based on total passes (out of {} ranked maps)</p>
    <p>Data taken from top 10,000 players.</p>
    <p>Doesn't include Loved maps.</p>
    <p>Using {} data. Data is released once a month at <a href="https://data.ppy.sh/">data.ppy.sh</a>, used with permission</p>
    <p>EZ/HT are allowed. NF is not allowed.</p>
    <div class="search_field">
      <input id="user_search_text" type="text" placeholder="Search by username...">
      <input id="user_search_button" type="button" value="search">
      <span>(Case-insensitive)</span>
    </div>
    <div class="search_field">
      <label for="country_ranking">Filter by country:</label>
      <select id="country_ranking">
        <option value="all" selected>All country</option>
    """.format(mapCount, dateName))
    for x in filteredCountryList:
        file.write("""    <option value="{}">{}</option>
    """.format(countryCodes[x].replace(" ", "_"), countryCodes[x]))
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
        <th data-lockedorder="desc">Passes</th>      </tr>
                   </thead>
                   <tbody>
               """)
    rank = 1
    for (x, y) in sortedScores[:count]:
        file.write("""      <tr class="{}">
        <td>{}""".format(countryCodes[IDToUser[x].country].replace(" ", "_"),rank))
        if x in lastMonth:
            change = lastMonth[x][0] - rank
            if change == 0:
                file.write(""" <span class="rank_no_change">(→)</span>""")
            if change > 0:
                file.write(""" <span class="rank_up">(+{})</span>""".format(change))
            if change < 0:
                file.write(""" <span class="rank_down">({})</span>""".format(change))
        else:
            file.write(""" <span class="rank_new">(New)</span>""")
        file.write("""</td>
        <td class="user_name">
          {}
        </td>
        <td>{}""".format(IDToUser[x].name, y))
        if x in lastMonth:
            change = y - lastMonth[x][1]
            if change == 0:
                file.write(""" <span class="rank_no_change">(+0)</span>""")
            if change < 0:
                file.write(""" <span class="rank_down">({})</span>""".format(change))
            if change > 0:
                if change < 50:
                    file.write(""" <span class="pp_50">(+{})</span>""".format(change))
                else:
                    if change < 100:
                        file.write(""" <span class="pp_100">(+{})</span>""".format(change))
                    else:
                        if change < 200:
                            file.write(""" <span class="rank_new">(+{})</span>""".format(change))
                        else:
                            file.write(""" <span class="rank_up">(+{})</span>""".format(change))
        file.write("""</td>
      </tr>""")
        IDToStoredData[x] = (rank, y)
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
    file.close()
    file = open("this month/previousPasses.pkl", "wb")
    pickle.dump(IDToStoredData, file)
    file.close()

def specificScore(userIDToRankedPlays, userIDToLovedPlays, IDToUser, IDToBeatmap, countryCodes, count=2000):
    IDToRankedScore = {}
    for (x,y) in userIDToRankedPlays.items():
        beatmapIDToScore = {}
        for z in y:
            beatmapID = z.beatmapID
            if IDToBeatmap[beatmapID].mode == 2:
                score = z.score
                oldScore = beatmapIDToScore.get(beatmapID,0)
                beatmapIDToScore[beatmapID] = max(score, oldScore)
        scoreSum = 0
        for (_,z) in beatmapIDToScore.items():
            scoreSum += z
        IDToRankedScore[x] = scoreSum
    IDToTotalScore = IDToRankedScore.copy()
    for (x,y) in userIDToLovedPlays.items():
        beatmapIDToScore = {}
        for z in y:
            beatmapID = z.beatmapID
            if IDToBeatmap[beatmapID].mode == 2:
                score = z.score
                oldScore = beatmapIDToScore.get(beatmapID,0)
                beatmapIDToScore[beatmapID] = max(score, oldScore)
        scoreSum = 0
        for (_,z) in beatmapIDToScore.items():
            scoreSum += z
        IDToTotalScore[x] += scoreSum
    for (x,y) in IDToRankedScore.items():
        IDToRankedScore[x] = round(y/1000000000, 2)
    for (x,y) in IDToTotalScore.items():
        IDToTotalScore[x] = round(y/1000000000, 2)
    sortedScores = sorted(IDToRankedScore.items(), key=lambda item: item[1], reverse=True)
    IDToRankedRank = {}
    rank = 1
    for (x,y) in sortedScores:
        IDToRankedRank[x] = rank
        rank += 1
    sortedScores = sorted(IDToTotalScore.items(), key=lambda item: item[1], reverse=True)
    filteredCountrySet = set()
    for (x, _) in sortedScores[:count]:
        filteredCountrySet.add(IDToUser[x].country)
    filteredCountryList = sorted(filteredCountrySet, key=lambda item: countryCodes[item])
    IDToStoredData = {}
    lastMonth = []
    try:
        file = open("last month/previousSpecificScore.pkl", "rb")
        lastMonth = pickle.load(file)
        file.close()
    except:
        lastMonth = []
    file = open("html/specificScore.html", "w", encoding="utf-8")
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
        <title>Catch-only Score</title>
      </head>
      <body>
        <div class="content">
    <p><a href="index.html">Return to main page</a></p>
    <br>
    <p>Total of players highest scoring play on each map</p>
    <p>Data taken from top 10,000 players.</p>
    <p>Using {} data. Data is released once a month at <a href="https://data.ppy.sh/">data.ppy.sh</a>, used with permission</p>
    <div class="search_field">
      <input id="user_search_text" type="text" placeholder="Search by username...">
      <input id="user_search_button" type="button" value="search">
      <span>(Case-insensitive)</span>
    </div>
    <div class="search_field">
      <label for="country_ranking">Filter by country:</label>
      <select id="country_ranking">
        <option value="all" selected>All country</option>
    """.format(dateName))
    for x in filteredCountryList:
        file.write("""    <option value="{}">{}</option>
    """.format(countryCodes[x].replace(" ", "_"), countryCodes[x]))
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
        <th data-lockedorder="desc">Total</th>
        <th data-lockedorder="desc">Ranked</th>
        <th data-lockedorder="asc" class="text-left">#</th>      </tr>
                   </thead>
                   <tbody>
               """)
    rank = 1
    for (x, y) in sortedScores[:count]:
        file.write("""      <tr class="{}">
        <td>{}""".format(countryCodes[IDToUser[x].country].replace(" ", "_"),rank))
        if x in lastMonth:
            change = lastMonth[x][0] - rank
            if change == 0:
                file.write(""" <span class="rank_no_change">(→)</span>""")
            if change > 0:
                file.write(""" <span class="rank_up">(+{})</span>""".format(change))
            if change < 0:
                file.write(""" <span class="rank_down">({})</span>""".format(change))
        else:
            file.write(""" <span class="rank_new">(New)</span>""")
        file.write("""</td>
        <td class="user_name">
          {}
        </td>
        <td>{:.2f}B""".format(IDToUser[x].name, y))
        if x in lastMonth:
            change = y - lastMonth[x][1]
            if change == 0:
                file.write(""" <span class="rank_no_change">(+0)</span>""")
            if change < 0:
                file.write(""" <span class="rank_down">({})</span>""".format(change))
            if change > 0:
                if change < 50:
                    file.write(""" <span class="pp_50">(+{})</span>""".format(change))
                else:
                    if change < 100:
                        file.write(""" <span class="pp_100">(+{})</span>""".format(change))
                    else:
                        if change < 200:
                            file.write(""" <span class="rank_new">(+{})</span>""".format(change))
                        else:
                            file.write(""" <span class="rank_up">(+{})</span>""".format(change))
        file.write("""</td>
        <td>{:.2f}B""".format(IDToRankedScore[x]))
        if x in lastMonth:
            change = IDToRankedScore[x] - lastMonth[x][3]
            if change == 0:
                file.write(""" <span class="rank_no_change">(+0)</span>""")
            if change < 0:
                file.write(""" <span class="rank_down">({})</span>""".format(change))
            if change > 0:
                if change < 50:
                    file.write(""" <span class="pp_50">(+{})</span>""".format(change))
                else:
                    if change < 100:
                        file.write(""" <span class="pp_100">(+{})</span>""".format(change))
                    else:
                        if change < 200:
                            file.write(""" <span class="rank_new">(+{})</span>""".format(change))
                        else:
                            file.write(""" <span class="rank_up">(+{})</span>""".format(change))
        file.write("""</td>
                    <td>{}""".format(IDToRankedRank[x]))
        if x in lastMonth:
            change = lastMonth[x][2] - IDToRankedRank[x]
            if change == 0:
                file.write(""" <span class="rank_no_change">(→)</span>""")
            if change > 0:
                file.write(""" <span class="rank_up">(+{})</span>""".format(change))
            if change < 0:
                file.write(""" <span class="rank_down">({})</span>""".format(change))
        file.write("""</td>
      </tr>""")
        IDToStoredData[x] = (rank, y, IDToRankedRank[x], IDToRankedScore[x])
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
    file.close()
    file = open("this month/previousSpecificScore.pkl", "wb")
    pickle.dump(IDToStoredData, file)
    file.close()

if __name__ == "__main__":
    file = open("userIDToLovedPlays.pkl", "rb")
    userIDToLovedPlays = pickle.load(file)
    file.close()
    file = open("userIDToRankedPlays.pkl", "rb")
    userIDToRankedPlays = pickle.load(file)
    file.close()
    file = open("IDToUser.pkl", "rb")
    IDToUser = pickle.load(file)
    file.close()
    file = open("countryCodes.pkl", "rb")
    countryCodes = pickle.load(file)
    file.close()
    file = open("IDToBeatmap.pkl", "rb")
    IDToBeatmap = pickle.load(file)
    file.close()
    file = open("IDToBeatmapSet.pkl", "rb")
    IDToBeatmapSet = pickle.load(file)
    file.close()
    specificScore(userIDToRankedPlays=userIDToRankedPlays,userIDToLovedPlays=userIDToLovedPlays,IDToUser=IDToUser,IDToBeatmap=IDToBeatmap,countryCodes=countryCodes)
    # modLeaderboard("EZ", includeMods=2, userIDToPlays=userIDToRankedPlays, IDToUser=IDToUser, countryCodes=countryCodes, IDToBeatmap=IDToBeatmap, IDToBeatmapSet=IDToBeatmapSet)
    # modLeaderboard("HD", includeMods=8, userIDToPlays=userIDToRankedPlays, IDToUser=IDToUser, countryCodes=countryCodes, IDToBeatmap=IDToBeatmap, IDToBeatmapSet=IDToBeatmapSet)
    # modLeaderboard("HR", includeMods=16, userIDToPlays=userIDToRankedPlays, IDToUser=IDToUser, countryCodes=countryCodes, IDToBeatmap=IDToBeatmap, IDToBeatmapSet=IDToBeatmapSet)
    # modLeaderboard("DT", includeMods=64, userIDToPlays=userIDToRankedPlays, IDToUser=IDToUser, countryCodes=countryCodes, IDToBeatmap=IDToBeatmap, IDToBeatmapSet=IDToBeatmapSet)
    # modLeaderboard("HT", includeMods=256, userIDToPlays=userIDToRankedPlays, IDToUser=IDToUser, countryCodes=countryCodes, IDToBeatmap=IDToBeatmap, IDToBeatmapSet=IDToBeatmapSet)
    # modLeaderboard("FL", includeMods=1024, userIDToPlays=userIDToRankedPlays, IDToUser=IDToUser, countryCodes=countryCodes, IDToBeatmap=IDToBeatmap, IDToBeatmapSet=IDToBeatmapSet)
    # modLeaderboard("NM", excludeMods=1370, userIDToPlays=userIDToRankedPlays, IDToUser=IDToUser, countryCodes=countryCodes, IDToBeatmap=IDToBeatmap, IDToBeatmapSet=IDToBeatmapSet)
    # modLeaderboard("Loved", userIDToPlays=userIDToLovedPlays, IDToUser=IDToUser, countryCodes=countryCodes, IDToBeatmap=IDToBeatmap, IDToBeatmapSet=IDToBeatmapSet, banSet={1529757, 2572147, 1257904, 2571858, 1267365, 1165130})
    # YMDvsTheWorld(4158549, userIDToPlays=userIDToRankedPlays, IDToUser=IDToUser, IDToBeatmap=IDToBeatmap, IDToBeatmapSet=IDToBeatmapSet)
    # specificFCsLeaderboard(userIDToPlays=userIDToRankedPlays, IDToUser=IDToUser, IDToBeatmap=IDToBeatmap, countryCodes=countryCodes)
    # rankedSpecificPasses(userIDToPlays=userIDToRankedPlays, IDToUser=IDToUser, IDToBeatmap=IDToBeatmap, countryCodes=countryCodes)
    # number1s(userIDToRankedPlays, userIDToLovedPlays, IDToUser, countryCodes)
    # hundrethPlay(userIDToPlays=userIDToRankedPlays, IDToUser=IDToUser, IDToBeatmap=IDToBeatmap, countryCodes=countryCodes)
    # totalPasses(userIDToPlays=userIDToRankedPlays, IDToUser=IDToUser, IDToBeatmap=IDToBeatmap, countryCodes=countryCodes)
    # userIDToConvertPlays = {}
    # for x in userIDToRankedPlays:
    #     convertsOnly = []
    #     for y in userIDToRankedPlays[x]:
    #         if IDToBeatmap[y.beatmapID].mode == 0:
    #             convertsOnly.append(y)
    #     userIDToConvertPlays[x] = convertsOnly
    # modLeaderboard("Convert", userIDToPlays=userIDToConvertPlays, IDToUser=IDToUser, countryCodes=countryCodes, IDToBeatmap=IDToBeatmap, IDToBeatmapSet=IDToBeatmapSet)
