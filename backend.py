from typing import List, Any
from flask import Flask, request, render_template,redirect
from shutil import move,rmtree
from wget import download
from getpass import getuser
from zipfile import ZipFile
from os import mkdir,remove
from os.path import exists
from steamlib import *
from shutil import rmtree
notifications = []

app = Flask(__name__)
@app.route('/vehicles')
def vehiles():
    global workshopinfo,day,page,browsesort,search, notifications
    print(notifications)
    if request.args.get('browsesort') is None:browsesort = "trend"
    else:browsesort = request.args.get('browsesort')
    try:
        if request.args.get('page') is None: page = 1
        else:
            if int(request.args.get('page')) < 1:
                page = 1
            else:
                page = int(request.args.get('page'))
    except:page = 1
    if request.args.get('search') is None: search = ''
    else:search = request.args.get('search')
    if request.args.get('day') is None: day = -1
    else:day = int(request.args.get('day'))
    workshopinfo = getworkshop(552100, page, day, browsesort,search)
    for mod in range(len(workshopinfo)):
        if len(workshopinfo[mod]['title']) > 20:
            workshopinfo[mod]['title'] = workshopinfo[mod]['title'][:20]
            workshopinfo[mod]['title'] += "..."
    return render_template("vehicles.html", vehicles=workshopinfo, page=page,search=search, notifications=notifications)
@app.route('/vehicle')
def vehicle():
    global notifications
    id = int(request.args.get("id"))
    description = getworkshopslot(id)['description']
    renderdescrip = description.split("\n")
    return render_template("vehicle.html", vehicle=getworkshopslot(id), description=renderdescrip, notifications=notifications)
@app.route('/downloadvehicle')
def downloadvehicle():
    global workshopinfo, notifications
    if exists("C:/steamcmd/crashhandler.dll"):
        workshopinfo = getworkshopslot(int(request.args.get('id')))
        print(workshopinfo)
        if exists(f"C:/Users/{getuser()}/AppData/Local/BrickRigs/SavedRemastered/Vehicles/{workshopinfo['id']}"):
            rmtree(f"C:/Users/{getuser()}/AppData/Local/BrickRigs/SavedRemastered/Vehicles/{workshopinfo['id']}")
        else:
            try:
                downloadsteam(552100, workshopinfo['id'])
                if exists(f"C:/Users/{getuser()}/AppData/Local/BrickRigs/SavedRemastered/Vehicles/{workshopinfo['id']}"):
                    rmtree(f"C:/Users/{getuser()}/AppData/Local/BrickRigs/SavedRemastered/Vehicles/{workshopinfo['id']}")
                    mkdir(f"C:/Users/{getuser()}/AppData/Local/BrickRigs/SavedRemastered/Vehicles/{workshopinfo['id']}")
                else:
                    try:
                        mkdir(f"C:/Users/{getuser()}/AppData/Local/BrickRigs/SavedRemastered/Vehicles/{workshopinfo['title']}")
                        dirname = workshopinfo['title']
                    except:
                        mkdir(f"C:/Users/{getuser()}/AppData/Local/BrickRigs/SavedRemastered/Vehicles/{workshopinfo['id']}")
                        dirname = workshopinfo['id']
                    try:
                        download(workshopinfo['imageurl'],f"C:/Users/{getuser()}/AppData/Local/BrickRigs/SavedRemastered/Vehicles/{dirname}/Preview.png")
                    except:
                        print("(!) Невозможно загрузить изображение")
                    try:
                        move(f"C:/steamcmd/steamapps/workshop/content/552100/{workshopinfo['id']}/Vehicle.brv",f"C:/Users/{getuser()}/AppData/Local/BrickRigs/SavedRemastered/Vehicles/{workshopinfo['title']}")
                    except:
                        move(f"C:/steamcmd/steamapps/workshop/content/552100/{workshopinfo['id']}/Vehicle.brv",f"C:/Users/{getuser()}/AppData/Local/BrickRigs/SavedRemastered/Vehicles/{workshopinfo['id']}")
                    rmtree(f"C:/steamcmd/steamapps/workshop/content/552100/{workshopinfo['id']}")
                    notifications = []
                    notifications.append({"type": "lime", "text": f"Постройка {workshopinfo['title']} загружена!"})
            except:
                notifications = []
                notifications.append({"type": "red", "text": "Ошибка загрузки!"})
    else:
        if exists("tempfile"):
            rmtree("tempfile")
        mkdir("tempfile")
        download("https://steamcdn-a.akamaihd.net/client/installer/steamcmd.zip", "tempfile/steamcmd.zip")
        if exists("c:/steamcmd"):
            rmtree("c:/steamcmd")
        with ZipFile("tempfile/steamcmd.zip", 'r') as f:
            f.extractall("c:/steamcmd")
        args = ['c:/steamcmd/steamcmd.exe', '+quit']
        process = Popen(args, stdout=PIPE, errors='ignore', encoding="utf-8", creationflags=CREATE_NO_WINDOW)
        rmtree("tempfile")
    if request.args.get('redirect') == "vehicles":
        return redirect(f"/vehicles?page{page}&search={search}")
    else:
        return redirect(f"/vehicle?id={workshopinfo['id']}")
@app.route('/deletevehicle')
def deletevehicle():
    global notifications
    vehicle = getworkshopslot(int(request.args.get('id')))
    title = vehicle["title"]
    id = vehicle["id"]
    if exists(f"C:/Users/{getuser()}/AppData/Local/BrickRigs/SavedRemastered/Vehicles/{id}"):
        try:
            rmtree(f"C:/Users/{getuser()}/AppData/Local/BrickRigs/SavedRemastered/Vehicles/{id}")
        except:
            remove(f"C:/Users/{getuser()}/AppData/Local/BrickRigs/SavedRemastered/Vehicles/{id}")
        notifications = []
        notifications.append({"type": "red", "text": "Машина удалена!"})
    elif exists(f"C:/Users/{getuser()}/AppData/Local/BrickRigs/SavedRemastered/Vehicles/{title}"):
        try:
            rmtree(f"C:/Users/{getuser()}/AppData/Local/BrickRigs/SavedRemastered/Vehicles/{title}")
        except:
            remove(f"C:/Users/{getuser()}/AppData/Local/BrickRigs/SavedRemastered/Vehicles/{title}")
        notifications = []
        notifications.append({"type": "red", "text": "Машина удалена!"})
    else:
        notifications = []
        notifications.append({"type": "red", "text": "Ошибка удаления!"})
    if request.args.get('redirect') == "vehicles":
        return redirect(f"/vehicles?page{page}&search={search}")
    else:
        return redirect(f"/vehicle?id={id}")
app.run(host='0.0.0.0', port=5000, debug=True)
