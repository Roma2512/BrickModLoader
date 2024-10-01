from subprocess import Popen, PIPE, CREATE_NO_WINDOW
from requests import get
from getpass import getuser
from os.path import exists

def downloadsteam(appid, contentid):
    global process
    args = ['c:/steamcmd/steamcmd.exe','+login anonymous',f'+workshop_download_item {appid} {contentid}','+quit']
    process = Popen(args, stdout=PIPE, errors='ignore',encoding="utf-8",creationflags=CREATE_NO_WINDOW)
    while True:
        if process.stdout.readline().strip() == '':
            break
        else:
            print(process.stdout.readline().strip())
def getworkshop(appid:int,page: int,days:int,sort:str, searh:str = None):
    if searh == '':
        request = get(f"https://steamcommunity.com/workshop/browse/?appid={appid}&browsesort={sort}&section=readytouseitems&days={days}&actualsort={sort}&p={page}")
    else:
        request = get(f"https://steamcommunity.com/workshop/browse/?appid={appid}&browsesort={sort}&section=readytouseitems&days={days}&actualsort={sort}&p={page}&searchtext={searh}")
    contents = []
    for i in range(30):
        try:
            content = request.text.split('<div class="workshopBrowseItems">')[1].split('<div data-panel="{&quot;type&quot;:&quot;PanelGroup&quot;}" class="workshopItem">')[i + 1]
            title = content.split('"title":"')[1].split('","')[0]
            id = content.split('"id":"')[1].split('","')[0]
            if exists(f"C:/Users/{getuser()}/AppData/Local/BrickRigs/SavedRemastered/Vehicles/{id}"):
                downloaded = True
            elif exists(f"C:/Users/{getuser()}/AppData/Local/BrickRigs/SavedRemastered/Vehicles/{title}"):
                downloaded = True
            else:
                downloaded = False
            contents.append({
                "id": id,
                "title": title,
                "imageurl": content.split('<img class="workshopItemPreviewImage " src="')[1].split('">')[0],
                "description": content.split('"description":"')[1].split('","')[0],
                "author": content.split('<a class="workshop_author_link"')[1].split('>')[1].split("</a></div>")[0].split("</a")[0],
                "downloaded": downloaded,
                })
            contents[i]['title'] = contents[i]['title'].encode().decode('unicode-escape')
            contents[i]['description'] = contents[i]['description'].encode().decode('unicode-escape')
        except:
            break
    return contents
def getworkshopslot(id: int):
    request = get(f"https://steamcommunity.com/sharedfiles/filedetails/?id={str(id)}&searchtext=")
    content = request.text
    try:
        img = content.split('<img id="previewImageMain" class="workshopItemPreviewImageMain" src="')[1].split('"/>')[0]
    except:
        img = content.split('<img id="previewImage" class="workshopItemPreviewImageEnlargeable" src="')[1].split('">')[0]
    title = content.split('<div class="workshopItemTitle">')[1].split('</div>')[0]
    if exists(f"C:/Users/{getuser()}/AppData/Local/BrickRigs/SavedRemastered/Vehicles/{id}"):
        downloaded = True
    elif exists(f"C:/Users/{getuser()}/AppData/Local/BrickRigs/SavedRemastered/Vehicles/{title}"):
        downloaded = True
    else:
        downloaded = False
    contents = {
        "id": id,
        "title": title,
        "imageurl": img,
        "description": content.split('<div class="workshopItemDescription" id="highlightContent">')[1].split('			</div>')[0],
        "authorname": content.split('<div class="friendBlockContent">\r\n\t\t\t\t')[1].split("<br>")[0],
        "downloaded": downloaded,
        }
    contents["description"] = contents["description"].replace("<br>", "\n").replace("<div>", "").replace("</div>","")
    return contents