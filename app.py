#NON ADAPTE A L'UTILISATION PAR PLUSIEURS PERSONNES (LES DONNEES D'UNE PERSONNE PEUVENT ÊTRE RECUPEREES)
#TODO : AJOUTER FONCTION DECONNEXION ECOLEDIRECTE ET SUPPRESSION DES VARIABLES APPELEE DES LE CHARGEMENT DE LA PAGE DE CONNEXION
from flask import Flask, render_template, request
from rewrite import connexion, EDT
import json
from datetime import datetime as dt

app = Flask(__name__)
isConnected = False

@app.route("/")
def menu():
    if isConnected:
        return render_template("menu.html")
    else:
        return render_template("login.html")

@app.route("/login", methods =["GET", "POST"])
def login():
    global isConnected, timelineEleve, EDTEleve, vieScolaireEleve, notesEleve
    if request.method == "POST":
        if isConnected:
            return render_template("menu.html")
        else:
            id = request.form.get("id")
            password = request.form.get("passw")
            isConnected = connexion(id, password)
            EDTEleve = EDT(avecTrous=False)
    return render_template("menu.html")

@app.route("/prochaincours")
def prochaincours():
    if isConnected:
        def coursPlusProche():
            global matiere, start_date, end_date, color, prof, salle
            json_object = json.loads(EDTEleve)
            now = dt.now()
            last_diff = now - dt.strptime("1900-01-01 00:00:00", '%Y-%m-%d %H:%M:%S') #set time diff to default high value
            if json_object['code'] == 200: #if EcoleDirecte response is correct
                try: #try to search next lesson
                    for cours in json_object['data']:
                        matiere = cours['matiere']
                        start_date = dt.strptime(cours['start_date'], '%Y-%m-%d %H:%M')
                        end_date = dt.strptime(cours['end_date'], '%Y-%m-%d %H:%M')
                        color = cours['color']
                        prof = cours['prof']
                        salle = cours['salle']
                        if start_date > now: #if lesson start_date is after now
                            diff = start_date - now
                            if diff < last_diff:
                                coursPlusProche = cours
                                last_diff = diff
                        else: 
                            pass #do nothing if lesson start_date is before now
                    #------Formatting values------
                    try:
                        salle = coursPlusProche['salle'].split(">")[1]
                    except:
                        salle = coursPlusProche['salle']
                        if salle =="":
                                salle = "Salle non définie"
                    prof = coursPlusProche['prof'].title()
                    color = coursPlusProche['color']
                    matiere = coursPlusProche['matiere'].title()
                    end_date = (str(dt.strptime(str(coursPlusProche['end_date']), '%Y-%m-%d %H:%M')).split(" ")[1]).split(":")[0] + ":" + (str(dt.strptime(str(coursPlusProche['end_date']), '%Y-%m-%d %H:%M')).split(" ")[1]).split(":")[1]
                    start_date = (str(dt.strptime(str(coursPlusProche['start_date']), '%Y-%m-%d %H:%M')).split(" ")[1]).split(":")[0] + ":" + (str(dt.strptime(str(coursPlusProche['start_date']), '%Y-%m-%d %H:%M')).split(" ")[1]).split(":")[1]
                    #                                                                                    ^ keep only H:M:S  ^ keep only hours                                                                         ^ keep only H:M:S  ^ keep only minutes 
                except UnboundLocalError: #if no lesson if found after current one
                    matiere = "Pas de prochain cours"
                    prof = ""
                    color = ""
                    salle = ""
                    end_date = ""
                    start_date = ""
                print(matiere + " de : " + str(start_date) + " jusqu'à : " + str(end_date) + " avec : " + prof + " en : " + salle)
        coursPlusProche()
        return render_template("prochaincours.html", varsCours = {'matiere':matiere, 'start_date':start_date, 'end_date':end_date, 'color':color, 'prof':prof, 'salle':salle})
    else:
        return render_template("login.html")
    
@app.route("/emploidutemps")
def emploidutemps():
    if isConnected:
        def edt():
            global coursTries
            json_object = json.loads(EDTEleve)
            if json_object['code'] == 200:
                data = json_object['data']
                sorted_data = sorted(data, key=lambda cours: cours['start_date'])
                coursTries = []
                for cours in sorted_data:
                    #FORMATTING VALUES
                    try:
                        salle = cours['salle'].split(">")[1]
                    except:
                        if cours['salle'] =="":
                            salle = "Salle non définie"
                        else:
                            salle = cours['salle']
                    prof = cours['prof'].title()
                    color = cours['color']
                    matiere = cours['matiere'].title()
                    end_date = (str(dt.strptime(str(cours['end_date']), '%Y-%m-%d %H:%M')).split(" ")[1]).split(":")[0] + ":" + (str(dt.strptime(str(cours['end_date']), '%Y-%m-%d %H:%M')).split(" ")[1]).split(":")[1]
                    start_date = (str(dt.strptime(str(cours['start_date']), '%Y-%m-%d %H:%M')).split(" ")[1]).split(":")[0] + ":" + (str(dt.strptime(str(cours['start_date']), '%Y-%m-%d %H:%M')).split(" ")[1]).split(":")[1]
                    #                                                                                    ^ keep only H:M:S  ^ keep only hours                                                                         ^ keep only H:M:S  ^ keep only minutes 
                    coursDict = {'matiere': matiere, 'prof': prof, 'start_date': start_date, 'end_date': end_date, 'salle': salle, 'color': color}
                    coursTries.append(coursDict)
        edt()
        return render_template("emploidutemps.html", coursTries=coursTries)
    else:
        return render_template("login.html")
    
if __name__ == "__main__":
    app.run(host='0.0.0.0')
