import math
import datetime

# All the stuff that needs to be updated once a month
# Also, remember to put the "this month" data into the "last month" folder
# It's a giant hassle if you forget to do this
oneMonthAgo = 1701352469
oneYearAgo = oneMonthAgo - 525600*60
dateName = "1st January 2023"


class beatmapSet:
    ID = 0
    artist = ""  # There's also a unicode one
    title = ""  # ""
    date = datetime.datetime(1970, 1, 1)

    def __repr__(self):
        return str(self.ID) + " " + self.artist + " " + self.title
    # Beatmap sets also have a user_id & a status, but in general they can be overriden with the beatmap ones
    # The .sql file has a lot of raw binary, so it may be genuinely tricky to pick up anything after that


class beatmap:
    ID = 0
    beatmapSetID = 0
    difficultyName = ""
    length = 0
    AR = 0  # Beatmaps have aim, speed, strain etc. but only AR is included here for pp calculation purposes
    HP = 0
    CS = 0
    mode = 0  # 0: standard, 1: taiko, 2: catch, 3: mania
    status = 0  # 1: ranked, 2: approved, 3: qualified, 4: Loved (including TAG4)
    difficulty = {}  # EZ/NM/HR * HT/NM/DT = 9 possible difficulties
    maxCombo = 0
    accuracyTotal = 0

    def __repr__(self):
        return str(self.ID) + " " + str(self.beatmapSetID) + " " + self.difficultyName + " " + str(self.AR) + " " + str(self.mode) + " " + str(self.status) + " " + str(self.difficulty) + " " + str(self.maxCombo) + " " + str(self.accuracyTotal)
    # There's a whole bunch of things like CS or BPM that people could feasibly want to filter by
    # The only one I might actually do is mapper (user_id)


class user:
    ID = 0
    name = ""
    country = ""
    pp = 0
    ppRank = 0

    def __repr__(self):
        return str(self.ID) + " " + self.name + " " + self.country + " " + str(self.pp) + " " + str(self.ppRank)


class play:
    ID = 0
    beatmapID = 0
    userID = 0
    score = 0
    combo = 0
    rank = ""
    misses = 0
    drpmiss = 0
    modCode = 0
    pp = 0
    date = datetime.datetime(1970, 1, 1)

    def __repr__(self):
        return str(self.ID) + " " + str(self.beatmapID) + " " + str(self.userID) + " " + str(self.score) + " " + str(self.combo) + " " + self.rank + " " + str(self.misses) + " " + str(self.drpmiss) + " " + str(self.modCode) + " " + str(self.pp)


def modCodeToText(modCode):
    output = []
    if modCode == 0:
        return "+None"
    if modCode & 1:
        output += ",NF"
    if modCode & 2:
        output += ",EZ"
    if modCode & 8:
        output += ",HD"
    if modCode & 16:
        output += ",HR"
    if modCode & 64:
        if modCode & 512:
            output += ",NC"
        else:
            output += ",DT"
    if modCode & 256:
        output += ",HT"
    if modCode & 1024:
        output += ",FL"
    if modCode & 32:
        if modCode & 16384:
            output += ",PF"
        else:
            output += ",SD"
    if not output:
        return "+None"
    output[0] = "+"
    return "".join(output)


# You should probably keep everything in mod codes until the last moment, but it's possible this'll be useful
def textToModCode(modtext):
    output = 0
    mods = modtext.split(",")
    mods[0] = mods[0][1:]
    for x in mods:
        if x == "NF":
            output += 1
        if x == "EZ":
            output += 2
        if x == "HD":
            output += 8
        if x == "HR":
            output += 16
        if x == "SD":
            output += 32
        if x == "DT":
            output += 64
        if x == "HT":
            output += 256
        if x == "NC":
            output += 512 + 64
        if x == "FL":
            output += 1024
        if x == "PF":
            output += 16384 + 32
    return output


# Ignores everything except HR, EZ, DT & HT. Used for difficulty calculation
def modCodeToDifficultyCode(modCode):
    return modCode & 338


def modifiedAR(AR, modCode):
    if modCode & 16:
        AR *= 1.4
        AR = min(AR, 10)
    if modCode & 2:
        AR *= 0.5
    if AR > 5:
        ms = 1950-AR*150
    else:
        ms = 1800-AR*120
    if modCode & 64:
        ms = ms/1.5
    if modCode & 256:
        ms = ms/0.75
    if ms > 1200:
        AR = 15 - ms/120
    else:
        AR = 13 - ms/150
    return AR


# I couldn't find the official code so this is a modified version of PakaChan's
def catchPP(SR, combo, mCombo, misses, AR, modCode, accuracy):
    pp = float((max(5*SR/0.0049, 5)-4)**2)/100000
    lengthbonus = (0.95 + 0.3 * min(1.0, mCombo/2500.0) + (0 if mCombo <= 2500 else math.log10(mCombo/2500.0) * 0.475))
    pp *= lengthbonus
    pp *= 0.97**misses
    pp *= (combo/mCombo)**.8
    arbonus = 1
    if AR > 9:
        arbonus += 0.1 * (AR - 9.0)
    if AR > 10:
        arbonus += 0.1 * (AR - 10.0)
    if AR < 8:
        arbonus += 0.025 * (8.0 - AR)
    pp *= arbonus
    if modCode & 8:
        if AR > 10:
            pp *= 1.01 + 0.04 * (11 - AR)
        else:
            pp *= 1.05 + 0.075 * (10 - AR)
    pp *= accuracy ** 5.5
    if modCode & 1024:
        pp *= 1.35 * lengthbonus
    if modCode & 1:
        pp *= .9
    return pp