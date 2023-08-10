import requests
import json
import re

def fetch(arg):
    if arg:
        response = requests.get("https://statsnite.com/api/btd/v3/towers")
        print(response)

        data = json.loads(response.text)

        with open("towers_raw.json", "w") as f:
            json.dump(data, f, indent = 4)

        return data

    else:
        with open("towers_raw.json", "r") as f:
            data = json.load(f)
        return data

def getEffect(data, stats, effect):
    damage = r"[+\-]?[0-9]+[dD]"
    pierce = r"[+\-]?[0-9]+[pP]"
    attackSpeed = r"[0-9]*[.]*[0-9]+%[sS]"
    range = r"[+\-]?[0-9]+[rR]"

    damage_search = re.findall(damage, data)
    pierce_search = re.findall(pierce, data)
    attackSpeed_search = re.findall(attackSpeed, data)
    range_search = re.findall(range, data)
    findings = damage_search + pierce_search + attackSpeed_search + range_search
    if len(findings) > 0:
        if len(damage_search) > 0:
            damage_search = damage_search[0].strip("d")
            stats["damage"] = int(damage_search)  + int(stats["damage"])
        if len(pierce_search) > 0:
            pierce_search = pierce_search[0].strip("p")
            stats["pierce"] = int(pierce_search) + int(stats["pierce"])
        if len(attackSpeed_search) > 0:
            attackSpeed_search = str(attackSpeed_search[0]).strip("%s")
            if float(attackSpeed_search) < 0:
                attackSpeed_search = 1 + float(attackSpeed_search)
            stats["attackSpeed"] = float(stats["attackSpeed"]) * (float(attackSpeed_search)/100)
        if len(range_search) > 0:
            range_search = range_search[0].strip("r")
            if "Infinite" not in str(stats["range"]):
                stats["range"] = int(range_search)  + int(stats["range"])
    else:
        effect.append(data)

data = fetch(False)

with open("towers.json", "r") as f:
    towers = json.load(f)

for data_set in data:
    tower = None
    try:
        tower = towers[data_set["id"]]
    except Exception as e:
        towers[data_set["id"]] = {"paths":{}}
        tower = towers[data_set["id"]]
    #adding cost
    tower["cost"] = data_set["cost"]

    #adding base stats
    tower["stats"] = data_set["stats"]
    tower["type"] =  data_set["type"]

    #adding upgrade paths
    paths = (data_set["paths"])
    path_names = [path for path in paths]
    path_tuples = [(1, 0, 0), (0, 1, 0), (0, 0, 1), (1, 0, 1), (0, 1, 1), (0, 2, 1), (2, 0, 1), (1, 1, 0), (0, 1, 1), (0, 1, 2), (2, 1, 2), (1, 1, 0), (1, 0, 1), (1, 0, 2), (1, 2, 0), (2, 0, 0), (0, 2, 0), (0, 0, 2), (1, 0, 2), (0, 1, 2), (0, 2, 2), (2, 0, 2), (1, 2, 0), (0, 2, 1), (0, 2, 2), (2, 2, 2), (2, 1, 0), (2, 0, 1), (2, 0, 2), (2, 2, 0), (3, 0, 0), (0, 3, 0), (0, 0, 3), (1, 0, 3), (0, 1, 3), (0, 2, 3), (2, 0, 3), (1, 3, 0), (0, 3, 1), (0, 3, 2), (2, 3, 2), (3, 1, 0), (3, 0, 1), (3, 0, 2), (3, 2, 0), (4, 0, 0), (0, 4, 0), (0, 0, 4), (1, 0, 4), (0, 1, 4), (0, 2, 4), (2, 0, 4), (1, 4, 0), (0, 4, 1), (0, 4, 2), (2, 4, 2), (4, 1, 0), (4, 0, 1), (4, 0, 2), (4, 2, 0), (5, 0, 0), (0, 5, 0), (0, 0, 5), (1, 0, 5), (0, 1, 5), (0, 2, 5), (2, 0, 5), (1, 5, 0), (0, 5, 1), (0, 5, 2), (2, 5, 2), (5, 1, 0), (5, 0, 1), (5, 0, 2), (5, 2, 0)]
    for path in path_tuples:

        ## TODO: Add effects parser

        cost = tower["cost"].copy()
        stats = tower["stats"].copy()
        effects = []

        if "N/A" in str(stats["attackSpeed"]):
            stats["attackSpeed"] = 0

        if "N/A" in str(stats["damage"]):
            stats["damage"] = 0

        if "N/A" in str(stats["range"]):
            stats["range"] = 0

        if "N/A" in str(stats["pierce"]):
            stats["pierce"] = 0

        #path1
        if not path[0] == 0:
            for i in range(path[0]):
                stat = paths[path_names[0]][i]
                cost["easy"] += stat["cost"]["easy"]
                cost["medium"] += stat["cost"]["medium"]
                cost["hard"] += stat["cost"]["hard"]
                cost["impoppable"] += stat["cost"]["impoppable"]
                for effect in (stat["effects"]):
                    getEffect(effect, stats, effects)


        #path2
        if not path[1] == 0:
            for i in range(path[1]):
                stat = paths[path_names[1]][i]
                cost["easy"] += stat["cost"]["easy"]
                cost["medium"] += stat["cost"]["medium"]
                cost["hard"] += stat["cost"]["hard"]
                cost["impoppable"] += stat["cost"]["impoppable"]
                for effect in (stat["effects"]):
                    getEffect(effect, stats, effects)

        #path3
        if not path[2] == 0:
            for i in range(path[2]):
                stat = paths[path_names[2]][i]
                cost["easy"] += stat["cost"]["easy"]
                cost["medium"] += stat["cost"]["medium"]
                cost["hard"] += stat["cost"]["hard"]
                cost["impoppable"] += stat["cost"]["impoppable"]
                for effect in (stat["effects"]):
                    getEffect(effect, stats, effects)

        #cost per pop, lower is better

        dps = 0
        try:
            dps = int(stats["damage"])/float(stats["attackSpeed"])
        except Exception as e:
            pass

        cpd = 0
        try:
            cpd = {value : float(cost[value]) / float(stats["damage"]) for value in cost}
        except Exception as e:
            pass

        tower["paths"][str(path)] = {"cost" : cost, "DPS" : dps, "Cost_per_damage" : cpd, "stats" : stats, "effects": effects}

with open("towers.json", "w") as f:
    try:
        json.dump(towers, f, indent = 4)
    except Exception as e:
        print(e)


break_con = False
difficulty = ""

print("> 1: easy")
print("> 2: medium")
print("> 3: hard")
print("> 4: impoppable")
feedback = input("> ")

diff_list = ["","easy", "medium","hard","impoppable"]
difficulty = diff_list[int(feedback)]

while True:
    feedback = input("> ")
    if "CPD" in feedback:
        DPS = []
        for tower in towers:
            for path in towers[tower]["paths"]:
                path_data = towers[tower]["paths"][path]
                DPS.append([path, tower, {"cost": path_data["cost"][difficulty], "DPS" : path_data["DPS"]}])

        #SORT
        DPS_sorted = []
        location = 0
        for i in range(len(DPS)):
            highscore = 0
            highscore_data = DPS[0]
            for item in DPS:
                if int(item[2]["DPS"]) > highscore:
                    highscore = int(item[2]["DPS"])
                    highscore_data = item
                if (int(item[2]["DPS"]) == highscore):
                    try:
                        if (item[2]["cost"] < highscore_data[2]["cost"]):
                            highscore = int(item[2]["DPS"])
                            highscore_data = item
                    except Exception as e:
                        highscore = int(item[2]["DPS"])
                        highscore_data = item
            DPS_sorted.append(highscore_data)
            DPS.remove(highscore_data)

        for value in DPS_sorted:
            print(value)

    if "CPD" in feedback:
        CPD = []
        for tower in towers:
            for path in towers[tower]["paths"]:
                path_data = towers[tower]["paths"][path]
                CPD.append([path, {"cost": path_data["cost"][difficulty], "CPD" : path_data["CPD"][difficulty]}])

    if feedback in towers:
        try:
            print(towers[feedback])

        except Exception as e:
            print(towers.keys())
