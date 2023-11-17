from bs4 import BeautifulSoup
import re
import requests
from pandas import ExcelWriter
from pandas import read_csv
from pandas import DataFrame
import fileinput
import os
import win32api

view_all_gangs = {
    "ttb":"tsarbratva",
    "rdt":"reddragon",
    "gsb":"greenstreet",
    "vdt":"verdant",
    "vtb":"vietnamese",
    "sp":"southernpimps",
    "avispa":"avispa",
    "69":"69pier",
    "elc":"elloco"
}
parse_war_gangs={
    "ttb":"The Tsar Bratva",
    "rdt":"Red Dragon Triad",
    "gsb":"Green Street Bloods",
    "vdt":"Verdant Family",
    "vtb":"Vietnamese Boys",
    "sp":"Southern Pimps",
    "avispa":"Avispa Rifa",
    "69":"69 Pier Mobs",
    "elc":"El Loco Cartel"
}
wars =["wars/war1.csv","wars/war2.csv","wars/war3.csv","wars/war4.csv"]
def main():
    try:
        cnt=0
        asd= []
        turf_names=[]
        ##prompt
        date,gang = prompt()
        ## Sanctiuni scor
        sanctiuni_scor = input("Sanctionam pe scor? (y/n): ")
        if sanctiuni_scor == "y" or sanctiuni_scor == "yes" or "y" in sanctiuni_scor :
            sanctiuni_scoruri = True
        else:
            sanctiuni_scoruri = False
        ##
        regex_date = re.search(r'^(?:(?:31(\/|-|\.)(?:0?[13578]|1[02]))\1|(?:(?:29|30)(\/|-|\.)(?:0?[13-9]|1[0-2])\2))(?:(?:1[6-9]|[2-9]\d)?\d{2})$|^(?:29(\/|-|\.)0?2\3(?:(?:(?:1[6-9]|[2-9]\d)?(?:0[48]|[2468][048]|[13579][26])|(?:(?:16|[2468][048]|[3579][26])00))))$|^(?:0?[1-9]|1\d|2[0-8])(\/|-|\.)(?:(?:0?[1-9])|(?:1[0-2]))\4(?:(?:1[6-9]|[2-9]\d)?\d{2})$',str(date))
        while (regex_date == None):
            print('Date must be "DD.MM.YYYY"')
            date,gang = prompt()
            regex_date = re.search(r'^(?:(?:31(\/|-|\.)(?:0?[13578]|1[02]))\1|(?:(?:29|30)(\/|-|\.)(?:0?[13-9]|1[0-2])\2))(?:(?:1[6-9]|[2-9]\d)?\d{2})$|^(?:29(\/|-|\.)0?2\3(?:(?:(?:1[6-9]|[2-9]\d)?(?:0[48]|[2468][048]|[13579][26])|(?:(?:16|[2468][048]|[3579][26])00))))$|^(?:0?[1-9]|1\d|2[0-8])(\/|-|\.)(?:(?:0?[1-9])|(?:1[0-2]))\4(?:(?:1[6-9]|[2-9]\d)?\d{2})$',str(date))
        while gang.lower() not in view_all_gangs:
            print('Gang name Invalid')
            date,gang = prompt()
            
        links = get_war_link(date,view_all_gangs[gang.lower()])
            
        while (links == []):
            print(f'Gangul {gang.upper()} nu a avut waruri in data de {date}')
            date,gang= prompt()
            links = get_war_link(date,view_all_gangs[gang.lower()])
        links.sort()
        print(links)
        for x in links:
            asd.append(parse_war(parse_war_gangs[gang.lower()],x,cnt))
            cnt+=1
        ## got the wars/wars1..wars2..etc
        print("Getting Turf Names")
        for x in links:
            turf_names.append(get_turf(x))

        match len(links):
            case 1:
                min_sec1 = input(f"Secunde {turf_names[0]}: ")
                player_stats = todo(len(links),sanctiuni_scoruri,min_sec1)
            case 2:
                min_sec1 = input(f"Secunde {turf_names[0]}: ")
                min_sec2 = input(f"Secunde {turf_names[1]}: ")
                player_stats = todo(len(links),sanctiuni_scoruri,min_sec1,min_sec2)
            case 3:
                min_sec1 = input(f"Secunde {turf_names[0]}: ")
                min_sec2 = input(f"Secunde {turf_names[1]}: ")
                min_sec3 = input(f"Secunde {turf_names[2]}: ")
                player_stats = todo(len(links),sanctiuni_scoruri,min_sec1,min_sec2,min_sec3)
            case 4:
                min_sec1 = input(f"Secunde {turf_names[0]}: ")
                min_sec2 = input(f"Secunde {turf_names[1]}: ")
                min_sec3 = input(f"Secunde {turf_names[2]}: ")
                min_sec4 = input(f"Secunde {turf_names[3]}: ")
                player_stats = todo(len(links),sanctiuni_scoruri,min_sec1,min_sec2,min_sec3,min_sec4)
        ### Got the scrapper working and into a .csv, now work on the CSV
        with open("evidenta.csv", "a+") as f:
                    for x in player_stats:
                        try:
                            match len(links):
                                case 1:
                                    name,kills,deaths,kd,secunde, sanctiuneScor, sanctiunePrezenta =player_stats[x].values()
                                    f.write(f'{name} {kills} {kd} {secunde} "" "" "" "" "" "" "" "" "" "" {sanctiuneScor}{sanctiunePrezenta}  \n')
                                case 2:
                                    if len(player_stats[x]) == 7:
                                        name,kills,deaths,kd,secunde, sanctiuneScor, sanctiunePrezenta =player_stats[x].values()
                                        f.write(f'{name} {kills} {kd} {secunde} "" "" "" "" "" "" "" "" "" "" {sanctiuneScor}{sanctiunePrezenta}  \n')
                                    else: 
                                        name,kills,deaths,kd,secunde,kills1,deaths1,kd1,secunde1, sanctiuneScor, sanctiunePrezenta =player_stats[x].values()
                                        f.write(f'{name} {kills} {kd} {secunde} {kills1} {kd1} {secunde1} "" "" "" "" "" "" {sanctiuneScor} {sanctiunePrezenta} \n')
                                case 3:
                                    if len(player_stats[x]) == 7:
                                        name,kills,deaths,kd,secunde, sanctiuneScor, sanctiunePrezenta =player_stats[x].values()
                                        f.write(f'{name} {kills} {kd} {secunde} "" "" "" "" "" "" "" "" "" "" {sanctiuneScor}{sanctiunePrezenta}  \n')
                                    elif len(player_stats[x]) == 11:
                                        name,kills,deaths,kd,secunde,kills1,deaths1,kd1,secunde1, sanctiuneScor, sanctiunePrezenta =player_stats[x].values()
                                        f.write(f'{name} {kills} {kd} {secunde} {kills1} {kd1} {secunde1} "" "" "" "" "" "" {sanctiuneScor} {sanctiunePrezenta} \n')
                                    else:
                                        name,kills,deaths,kd,secunde,kills1,deaths1,kd1,secunde1,kills2,deaths2,kd2,secunde2, sanctiuneScor, sanctiunePrezenta =player_stats[x].values()
                                        f.write(f'{name} {kills} {kd} {secunde} {kills1} {kd1} {secunde1} {kills2} {kd2} {secunde2} "" "" "" {sanctiuneScor} {sanctiunePrezenta} \n')
                                case 4:
                                    if len(player_stats[x]) == 7:
                                        name,kills,deaths,kd,secunde, sanctiuneScor, sanctiunePrezenta =player_stats[x].values()
                                        f.write(f'{name} {kills} {kd} {secunde} "" "" "" "" "" "" "" "" "" "" {sanctiuneScor}{sanctiunePrezenta}  \n')
                                    elif len(player_stats[x]) == 11:
                                        name,kills,deaths,kd,secunde,kills1,deaths1,kd1,secunde1, sanctiuneScor, sanctiunePrezenta =player_stats[x].values()
                                        f.write(f'{name} {kills} {kd} {secunde} {kills1} {kd1} {secunde1} "" "" "" "" "" "" {sanctiuneScor} {sanctiunePrezenta} \n')
                                    elif len(player_stats[x]) == 15:
                                        name,kills,deaths,kd,secunde,kills1,deaths1,kd1,secunde1,kills2,deaths2,kd2,secunde2, sanctiuneScor, sanctiunePrezenta =player_stats[x].values()
                                        f.write(f'{name} {kills} {kd} {secunde} {kills1} {kd1} {secunde1} {kills2} {kd2} {secunde2} "" "" "" {sanctiuneScor} {sanctiunePrezenta} \n')
                                    else:
                                        name,kills,deaths,kd,secunde,kills1,deaths1,kd1,secunde1,kills2,deaths2,kd2,secunde2,kills3,deaths3,kd3,secunde3, sanctiuneScor, sanctiunePrezenta =player_stats[x].values()
                                        f.write(f'{name} {kills} {kd} {secunde} {kills1} {kd1} {secunde1} {kills2} {kd2} {secunde2} {kills3} {kd3} {secunde3} {sanctiuneScor} {sanctiunePrezenta} \n')
                        except ValueError:
                            f.write(f"Couldn't unpack values! \n")
        ### Got them from 4 csvs into 1 csv and now export to excel ###
        # df = pd.read_csv(txt_file, sep=" ",)
        # df.to_excel("color.xlsx",startcol=coloana_inceput,columns=["Nume","Scor","Secunde","Prezenta"])
        match len(links):
            case 1:
                writer = ExcelWriter('color.xlsx',mode='a', if_sheet_exists='overlay', engine='openpyxl')
                wb  = writer.book
                df = read_csv("evidenta.csv", sep=" ", names=["Nume","Kills","Scor","Secunde",'a', 'b', 'c', 'd', 'f', 'g' ,'i','k', 'y' ,'z',"sanctiuneScor","sanctiunePrezenta","x",])
                df.to_excel(writer,index=False, columns=["Nume","Kills","Scor","Secunde",'a', 'b', 'c', 'd', 'f', 'g','i','k', 'y' ,'z',"sanctiuneScor","sanctiunePrezenta","x"], header=["Nume","Kills","Scor","Secunde","","","","","","","","","","sanctiuneScor","sanctiunePrezenta","",""])
                wb.save(f'{gang}{date}.xlsx')
                wb.close()
            case 2:
                writer = ExcelWriter('color.xlsx',mode='a', if_sheet_exists='overlay', engine='openpyxl')
                wb  = writer.book
                df = read_csv("evidenta.csv", sep=" ", names=["Nume","Kills","Scor","Secunde","Kills2","Scor2","Secunde2",'a', 'b', 'c', 'd', 'f', 'g' ,"sanctiuneScor","sanctiunePrezenta","x",])
                df.to_excel(writer,index=False, columns=["Nume","Kills","Scor","Secunde","Kills2","Scor2","Secunde2",'a', 'b', 'c', 'd', 'f', 'g',"sanctiuneScor","sanctiunePrezenta","x"], header=["Nume","Kills","Scor","Secunde","Kills","Scor","Secunde","","","","","","","sanctiuneScor","sanctiunePrezenta","",])
                wb.save(f'{gang}{date}.xlsx')
                wb.close()
            case 3:
                writer = ExcelWriter('color.xlsx',mode='a', if_sheet_exists='overlay', engine='openpyxl')
                wb  = writer.book
                df = read_csv("evidenta.csv", sep=" ", names=["Nume","Kills","Scor","Secunde","Kills2","Scor2","Secunde2","Kills3","Scor3","Secunde3",'a','b','c',"sanctiuneScor","sanctiunePrezenta","x"])
                df.to_excel(writer,index=False, columns=["Nume","Kills","Scor","Secunde","Kills2","Scor2","Secunde2","Kills3","Scor3","Secunde3","a","b","c",'sanctiuneScor',"sanctiunePrezenta","x"], header=["Nume","Kills","Scor","Secunde","Kills","Scor","Secunde","Kills","Scor","Secunde","","","","sanctiuneScor","sanctiunePrezenta","",])
                wb.save(f'{gang}{date}.xlsx')
                wb.close()
            case 4:
                writer = ExcelWriter('color.xlsx',mode='a', if_sheet_exists='overlay', engine='openpyxl')
                wb  = writer.book
                df = read_csv("evidenta.csv", sep=" ", names=["Nume","Kills","Scor","Secunde","Kills2","Scor2","Secunde2","Kills3","Scor3","Secunde3","Kills4","Scor4","Secunde4",'sanctiuneScor',"sanctiunePrezenta"])
                df.to_excel(writer,index=True, index_label="Nume", columns=["Nume","Kills","Scor","Secunde","Kills2","Scor2","Secunde2","Kills3","Scor3","Secunde3","Kills4","Scor4","Secunde4",'sanctiuneScor',"sanctiunePrezenta"], header=["Kills","Scor","Secunde","Kills","Scor","Secunde","Kills","Scor","Secunde","Kills","Scor","Secunde",'sanctiuneScor',"sanctiunePrezenta","",])
                wb.save(f'{gang}{date}.xlsx')
                wb.close()
    
    # CLEANUP ###
        cleanup()
    except Exception:
        cleanup()
    finally:
        cleanup()
        ...



# CLEANUP ###
def cleanup():
    path_wars_OS = os.getcwd() +"/wars"
    path_wars = os.listdir(os.getcwd()+ "/wars")
    path_OS = os.getcwd()
    path = os.listdir(os.getcwd())
    for x in path_wars:
        if x.endswith(".csv"):
            os.remove(f"{path_wars_OS}/{x}")
    for x in path:
        if x.endswith(".csv"):
            os.remove(f"{path_OS}/{x}")
    return

def on_exit(signal_type):
    path_wars_OS = os.getcwd() +"/wars"
    path_wars = os.listdir(os.getcwd()+ "/wars")
    path_OS = os.getcwd()
    path = os.listdir(os.getcwd())
    for x in path_wars:
        if x.endswith(".csv"):
            os.remove(f"{path_wars_OS}/{x}")
    for x in path:
        if x.endswith(".csv"):
            os.remove(f"{path_OS}/{x}")
   
    
def prompt():
    date = input("Data: ")
    if "-" in date:
        date = date.replace("-",".")
    ## Input Validation Date
    date_wrong1 = re.search(r'^([0-9]{1})\.?\-?([0-9]*)\.?\-?([0-9]{4})$',str(date))
    if date_wrong1:
        date = f'0{date_wrong1.group(1)}.{date_wrong1.group(2)}.{date_wrong1.group(3)}'
    date_wrong2 = re.search(r'^([0-9]{2})\.?\-?([0-9]{1})\.?\-?([0-9]{4})$',str(date))
    if date_wrong2:
        date = f'{date_wrong2.group(1)}.0{date_wrong2.group(2)}.{date_wrong2.group(3)}'
    # print(date)
    print("Exemple Ganguri: ttb rdt gsb vdt vtb sp avispa 69 elc")
    gang = input("Gang: ")
    
    return date,gang
    
def parse_stats(atac_or_defend_players,player_stats,cnt):
    all_elements={}
    kills = []
    deaths = []
    kd = []
    secunde = []
    incrementer = 0
    counter2 = 0
    for z in range(len(atac_or_defend_players)):
        kills.append(player_stats[0+incrementer])
        deaths.append(player_stats[1+incrementer])
        kd.append(player_stats[2+incrementer])
        secunde.append(player_stats[3+incrementer])
        player = {
            "name":atac_or_defend_players[z],
            "kills":kills[z],
            "deaths":deaths[z],
            "kd":kd[z],
            "secunde":secunde[z]
        }
        all_elements[counter2] = player.copy()
        incrementer +=4
        counter2+=1
        # print(f"{atac_players[z]} Kills:{kills[z]}  Deaths:{deaths[z]},  KD:{kd[z]}  Secunde:{secunde[z]}")
        with open(wars[cnt], "a+") as f:
            f.write(f"{atac_or_defend_players[z]},{kills[z]},{deaths[z]},{kd[z]},{secunde[z]}\n")
    # with open("bla3.csv", "a+") as f:
    #     f.write(f"OVER##########################\n")
        # file = pd.read_csv ('bla3.csv')
        # file.to_excel ('xl.xlsx', index = None, header=True)
    cnt+=1
    return all_elements
        
            
def parse_war(gang,link,cnt):
    true_elements = {}
    attacker = False
    defender = False
    atac_players=[]
    defend_players=[]
    player_stats=[]
    r = requests.get(link)
    soup = BeautifulSoup(r.text,'html.parser')
    war_top = soup.find("div", class_='viewWarTop')
    a = war_top.find_all('a')
    if gang in a[0]:
        attacker = True
        print("Attacker!")
    else:
        defender = True
        print("Defender")
        ### Part1
    
    if attacker:
        attacker_players = soup.find("div", id='viewWarAttackerPlayers')
        tr = attacker_players.find_all('tr')
        for x in tr:
            a = x.find_all('a')
            nume_jucator = re.search(r'\/players\/general\/([\.\$\_\?@\[]*\w+[_\.@\[]*\w*[\.@\]]*\w*)"',str(a))
            if nume_jucator:
                atac_players.append(nume_jucator.group(1))
            td = x.find_all('td')
            for y in td:
                scor = re.search(r'<td>(-?[0-9]+)<\/td>',str(y))
                if scor:
                    player_stats.append(scor.group(1))
                    ########################################
        true_elements = parse_stats(atac_players,player_stats,cnt)
        
    
    

    elif defender:
        defender_players = soup.find("div", id='viewWarDefenderPlayers')
        tr = defender_players.find_all('tr')
        for x in tr:
            a = x.find_all('a')
            nume_jucator = re.search(r'\/players\/general\/([\.\$\_\?@\[]*\w+[_\.@\[]*\w*[\.@\]]*\w*)"',str(a))
            if nume_jucator:
                defend_players.append(nume_jucator.group(1))
            td = x.find_all('td')
            for y in td:
                scor = re.search(r'<td>(-?[0-9]+)<\/td>',str(y))
                if scor:
                    player_stats.append(scor.group(1))
                    ########################################
        true_elements=parse_stats(defend_players,player_stats,cnt)
    return true_elements
    print("######################################################################################################")
    # if attacker:
    #     for x in atac_players:
    #         print(x)
    # elif defender:
    #     for x in defend_players:
    #         print(x)

def get_war_link(date,gang):
    dates=[]
    links=[]
    primul=""
    found = []
    pages=[]
    i=0
    day,month,year = date.split(".")
    # Get X where "Page 1 of X"
    r = requests.get(f"https://www.rpg.b-zone.ro/wars/viewall/gang/{gang}")
    soup = BeautifulSoup((r.text), 'html.parser')
    pagination = soup.find("span", class_="showJumper")
    rgx = re.search(r'Page 1 of ([0-9]{3})',str(pagination))
    if rgx:
        iterate = rgx.group(1)
    for x in range(int(iterate)):
        i+=1
        pages.append(i)
    ##
    for x in pages:
        r = requests.get(f"https://www.rpg.b-zone.ro/wars/viewall/gang/{gang}/{x}")
        soup = BeautifulSoup((r.text), 'html.parser')
        print("Page: ",x)
        table_full = soup.find("div", class_="tableFull")
        tr = table_full.find_all('tr')
        for x in tr:
            td = x.find_all("td")
            for d in td:
                regex = re.search(r'([0-9]{2}\.[0-9]{2}\.[0-9]{4})',str(d))
                if regex:
                    pageDay,pageMonth,pageYear = regex.group(1).split(".") 
                    if regex.group(1) == date:
                        found.append("found")
                        primul = found.index("found")
                        dates.append(x)
                        # if len(dates) == 4:
                        #         for link in dates:
                        #             regex2 = re.search(r'\/([0-9]{5})',str(link))
                        #             if regex2:
                        #                 links.append(f"https://www.rpg.b-zone.ro/wars/view/{regex2.group(1)}")
                        #         return links
                    elif pageMonth < month and pageYear == year or pageYear < year:
                        return links
                    else:
                        found.append("cold")
                        if primul or primul == 0:
                            if found[primul+found.count("found")] == "cold":
                                for link in dates:
                                    regex2 = re.search(r'\/([0-9]{5})',str(link))
                                    if regex2:
                                        links.append(f"https://www.rpg.b-zone.ro/wars/view/{regex2.group(1)}")
                                return links
                                
    #print(f'Gangul {gang.upper()} nu a avut waruri in data de {date}')                              
    return links


def todo(link_length,sanctiuni_scoruri,min_sec1=0,min_sec2=0,min_sec3=0,min_sec4=0):
    names =set()
    counter = 0
    n=0
    player_stats = {}
    path = os.listdir(os.getcwd()+"/wars")
    csv_path = []
    print("Number of Wars: ",link_length)
    for x in path:
        if x.endswith(".csv"):
            csv_path.append(f"wars/{x}")

    with fileinput.input(files=csv_path, encoding="utf-8") as f:
        for line in f:
            filename = f.filename()
            name,kills,deaths,kd,secunde = line.strip('\n').split(",")
            if name not in names:
                match filename:
                    case "wars/war1.csv":
                        player = {
                        "name":name,
                        "kills":kills,
                        "deaths":deaths,
                        "kd":kd,
                        "secunde":secunde if int(secunde) >= int(min_sec1) else "(ABSENT)",
                        
                        }
                        names.add(name)
                        player_stats[name] = player.copy()
                    case "wars/war2.csv":
                        player = {
                        "name":name,
                        "kills":kills,
                        "deaths":deaths,
                        "kd":kd,
                        "secunde":secunde if int(secunde) >= int(min_sec2) else "(ABSENT)",
                        
                        }
                        names.add(name)
                        player_stats[name] = player.copy()
                    case "wars/war3.csv":
                        player = {
                        "name":name,
                        "kills":kills,
                        "deaths":deaths,
                        "kd":kd,
                        "secunde":secunde if int(secunde) >= int(min_sec3) else "(ABSENT)",
                        
                        }
                        names.add(name)
                        player_stats[name] = player.copy()
                    case "wars/war4.csv":
                        player = {
                        "name":name,
                        "kills":kills,
                        "deaths":deaths,
                        "kd":kd,
                        "secunde":secunde if int(secunde) >= int(min_sec4) else "(ABSENT)",
                        
                        }
                        names.add(name)
                        player_stats[name] = player.copy()
        
            else:
                match filename:
                    case "wars/war1.csv":
                        player_stats[name].update({
                            f"kills{n}":kills,
                            f"deaths{n}":deaths,
                            f"kd{n}":kd,
                            f"secunde{n}":secunde if int(secunde) >= int(min_sec1) else "(ABSENT)",
                            
                        })
                        n+=1
                    case "wars/war2.csv":
                        player_stats[name].update({
                            f"kills{n}":kills,
                            f"deaths{n}":deaths,
                            f"kd{n}":kd,
                            f"secunde{n}":secunde if int(secunde) >= int(min_sec2) else "(ABSENT)",
                            
                        })
                        n+=1
                    case "wars/war3.csv":
                        player_stats[name].update({
                            f"kills{n}":kills,
                            f"deaths{n}":deaths,
                            f"kd{n}":kd,
                            f"secunde{n}":secunde if int(secunde) >= int(min_sec3) else "(ABSENT)",
                            
                        })
                        n+=1
                    case "wars/war4.csv":
                        player_stats[name].update({
                            f"kills{n}":kills,
                            f"deaths{n}":deaths,
                            f"kd{n}":kd,
                            f"secunde{n}":secunde if int(secunde) >= int(min_sec4) else "(ABSENT)",
        
                        })
                        n+=1
            #     for x in range(len(player_stats)):
            #         if player_stats[x]['name'] == name:
            #             player_stats[x].update({
            #             "kills1":kills,
            #             "deaths1":deaths,
            #             "kd1":kd,
            #             "secunde1":secunde
            #             })
    
        # if player_stats[x].count("(ABSENT)" == 2):
        #     player_stats[x].update({
        #         f"SANCTIONAT"
        #     })
    sanctiune = 0
    sanctionam_amenda_1_4 = []
    sanctionam_AV_amenda= []
    sanctionamFW = []
    sanctionam_amenda =[]
    sanctionam_AV = []
     ###sanctiuni scor
    amenda_scor_5 = []
    amenda_scor_10 = []
    fw_15 = []
    ## Vedem pe cine sa sanctionam dar nu modificam pt. ca "List length can't change during iteration"
    match link_length:
        case 1:
            for x in player_stats:
                sanctiune = 0
                for y in player_stats[x].values():
                    if y == "(ABSENT)":
                        sanctiune +=1
                    if sanctiune == 1:
                        sanctionamFW.append(f"{player_stats[x]['name']}")
        case 2:
            for x in player_stats:
                sanctiune = 0
                for y in player_stats[x].values():
                    if y == "(ABSENT)":
                        sanctiune +=1
                if sanctiune == 1:
                    sanctionam_AV_amenda.append(f"{player_stats[x]['name']}")
                elif sanctiune == 2:
                    sanctionamFW.append(f"{player_stats[x]['name']}")

        case 3:
            for x in player_stats:
                sanctiune = 0
                for y in player_stats[x].values():
                    if y == "(ABSENT)":
                        sanctiune +=1
                if sanctiune == 1:
                    sanctionam_AV.append(f"{player_stats[x]['name']}")
                elif sanctiune == 2:
                    sanctionam_AV_amenda.append(f"{player_stats[x]['name']}")
                elif sanctiune == 3:
                    sanctionamFW.append(f"{player_stats[x]['name']}")
            
        case 4:
            for x in player_stats:
                sanctiune = 0
                for y in player_stats[x].values():
                    if y == "(ABSENT)":
                        sanctiune +=1
                if sanctiune == 1:
                    sanctionam_amenda_1_4.append(f"{player_stats[x]['name']}")
                elif sanctiune == 2:
                    sanctionam_AV.append(f"{player_stats[x]['name']}")
                elif sanctiune == 3:
                    sanctionam_AV_amenda.append(f"{player_stats[x]['name']}")
                elif sanctiune == 4:
                    sanctionamFW.append(f"{player_stats[x]['name']}")
        
    for x in player_stats:
            player_stats[x].update({
                "sanctiuneScor":"",
            })
    ### SANCTIUNI SCORURI
    if sanctiuni_scoruri == True:
        for x in player_stats:
            for y in player_stats[x]:
                kdregex = re.search(r'(kd[0-9]*)',str(y))
                if kdregex:
                    if -5 >= int(player_stats[x][y]) >=-9 :
                        amenda_scor_5.append(f"{player_stats[x]['name']}")
                    elif -10 >= int(player_stats[x][y]) >=-14 :
                        amenda_scor_10.append(f"{player_stats[x]['name']}")
                    elif int(player_stats[x][y]) <=-15:
                        fw_15.append(player_stats[x]['name'])
        
        
        for membru in player_stats:
            if membru in amenda_scor_5 and membru in amenda_scor_10:
                player_stats[membru].update({
                    "sanctiuneScor":f'"Amenda ${amenda_scor_5.count(membru) *25 + amenda_scor_10.count(membru)*30}k"'
                })

            elif membru in amenda_scor_5:
                    player_stats[membru].update({
                        "sanctiuneScor":f'"Amenda ${amenda_scor_5.count(membru) * 25}k"'
                        })
            elif membru in amenda_scor_10:
                    player_stats[membru].update({
                        "sanctiuneScor":f'"Amenda ${amenda_scor_10.count(membru) * 30}k"'
                        })
        for membru in fw_15:
                player_stats[membru].update({
                    "sanctiuneScor":f'"FW"'
                    })
            
           ## Punem sanctiunea la fiecare sa nu fie probleme la Pandas.to_excel.
    
            
    for x in player_stats:
        player_stats[x].update({
            "sanctiunePrezenta":"",
        })
    ### Adaugam sanctiunile in player stats.
    for membru in sanctionamFW:
        player_stats[membru].update({
            "sanctiunePrezenta":'"FW"'
        })

    for membru in sanctionam_AV:
        player_stats[membru].update({
            "sanctiunePrezenta":'"AV"'
        })

    for membru in sanctionam_amenda_1_4:
        player_stats[membru].update({
            "sanctiunePrezenta":'"Amenda $25k"'
        })
        
    for membru in sanctionam_AV_amenda:
        player_stats[membru].update({
            "sanctiunePrezenta":'"AV + Amenda $50k"'
        })
        
    # print(player_stats)
    return player_stats
        
def get_turf(link):
    r = requests.get(link)
    soup = BeautifulSoup((r.text), 'html.parser')
    war_page = soup.find("div", class_="viewWarPage")
    turf_div = war_page.find('div', style='text-align: center')
    turf = re.search(r'Turf:\s+(\w+\s*\w*\s*\w*)<br\/>',str(turf_div))

    
    return turf.group(1)
                
    
if __name__ == "__main__":
    win32api.SetConsoleCtrlHandler(on_exit,True)
    main()