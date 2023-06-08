import requests
import json
import datetime

def error_code_handling(code):
    global isConnected
    if code == 200:
        print("Connexion réussie !")
        isConnected = True
    elif code == 505:
        print("Mauvais identifiant ou mot de passe\nVérifiez les identifiants et mot de passe et réessayez")
    elif code == 520:
        print("Token invalide\nRegenerez votre token en vous reconnectant")
    elif code == 525:
        print("Token expiré\nRegenerez votre token en vous reconnectant")
    elif code == 40129:
        print("Format JSON invalide\nRéessayez. Si cela continue contactez le support technique")
    else:
        print("Code d'erreur inconnu\nRéessayez. Si cela continue contactez le support technique")



def connexion(identifiant, motdepasse):
    #-----VARIABLES-----#
    global isConnected, userID, token
    endpoint = "https://api.ecoledirecte.com/v3/login.awp"
    isConnected = False
    userID = None
    token = None
    #-----END VARIABLES-----#
    #-----SEND REQUEST, RECV DATA-----#
    payload = {
        "uuid": "",
        "identifiant": identifiant,
        "motdepasse": motdepasse,
        "isReLogin": False
    }
    headers = {
        'Content-Type': 'text/plain',
        'user-agent': 'baguetteLand'
    }
    response = requests.request("POST", endpoint, headers=headers, data="data=" + json.dumps(payload))
    json_response = json.dumps(response.json(), indent=4, sort_keys=True)
    json_response_dict = json.loads(json_response)
    code = json_response_dict["code"]
    error_code_handling(code)
    #-----END SEND REQUEST, RECV DATA-----#
    #-----RETRV TOKEN-----#
    if isConnected:
        token = json_response_dict["token"]
        foundID = False
        while foundID == False:
                for a in json_response_dict:
                    if "data" in a:
                            for b in json_response_dict[a]:
                                if "accounts" in b:
                                        for c in json_response_dict[a][b]:
                                            if 'id' in c:
                                                    userID = c['id']
                                                    foundID = True
                                                    break					
    else:
        pass
    return isConnected
    #-----END RETRV TOKEN-----#



def timeline():
    endpoint = "https://api.ecoledirecte.com/v3/Eleves/"+ str(userID) + "/timeline.awp?verbe=get"
    payload = "data={\r\n}"
    headers = {
        'X-Token': token,
        'Content-Type': 'text/plain',
        'user-agent': 'baguetteLand'
    }
    global timelineResponse, json_timeline_response
    timelineResponse = requests.request("POST", endpoint, headers=headers, data=payload)
    json_timeline_response = json.dumps(timelineResponse.json(), indent=4, sort_keys=True)
    json_timeline_response_dict = json.loads(json_timeline_response)
    code = json_timeline_response_dict["code"]
    error_code_handling(code)
    return json_timeline_response



def EDT(dateDebut=(datetime.date.today()), dateFin=(datetime.date.today()), avecTrous:bool=False): #[AAAA-MM-JJ] FORMAT FOR DATES
    endpoint = "https://api.ecoledirecte.com/v3/E/"+ str(userID) + "/emploidutemps.awp?verbe=get"
    payload = {
        "dateDebut": str(dateDebut),
        "dateFin": str(dateFin),
        "avecTrous": avecTrous
    }
    headers = {
        'X-Token': token,
        'Content-Type': 'text/plain',
        'user-agent': 'baguetteLand'
    }
    global EDTResponse, json_EDT_response
    EDTResponse = requests.request("POST", endpoint, headers=headers, data="data=" + json.dumps(payload))
    json_EDT_response = json.dumps(EDTResponse.json(), indent=4, sort_keys=False)
    json_EDT_response_dict = json.loads(json_EDT_response)
    code = json_EDT_response_dict["code"]
    error_code_handling(code)
    return json_EDT_response



def vieScolaire():
    endpoint = "https://api.ecoledirecte.com/v3/Eleves/"+ str(userID) + "/viescolaire.awp?verbe=get"
    payload = "data={\r\n}"
    headers = {
        'X-Token': token,
        'Content-Type': 'text/plain',
        'user-agent': 'baguetteLand'
    }
    global vieScolaireResponse, json_vieScolaire_response
    vieScolaireResponse = requests.request("POST", endpoint, headers=headers, data=payload)
    json_vieScolaire_response = json.dumps(vieScolaireResponse.json(), indent=4, sort_keys=True)
    json_vieScolaire_response_dict = json.loads(json_vieScolaire_response)
    code = json_vieScolaire_response_dict["code"]
    error_code_handling(code)
    return json_vieScolaire_response



def notes():
    endpoint = "https://api.ecoledirecte.com/v3/Eleves/"+ str(userID) + "/notes.awp?verbe=get"
    payload = "data={\r\n}"
    headers = {
        'X-Token': token,
        'Content-Type': 'text/plain',
        'user-agent': 'baguetteLand'
    }
    global notesResponse, json_notes_response
    notesResponse = requests.request("POST", endpoint, headers=headers, data=payload)
    json_notes_response = json.dumps(notesResponse.json(), indent=4, sort_keys=True)
    json_notes_response_dict = json.loads(json_notes_response)
    code = json_notes_response_dict["code"]
    error_code_handling(code)
    return json_notes_response



def cahierDeTexte(): #DO NOT USE, RETURNS A HTML LOADING PAGE
    endpoint = "https://api.ecoledirecte.com/v3/Eleves/"+ str(userID) + "/cahierdetextes.awp?verbe=get"
    payload = "data={\r\n}"
    headers = {
        'X-Token': token,
        'Content-Type': 'text/plain',
        'user-agent': 'baguetteLand'
    }
    global CDTResponse, json_CDT_response
    CDTResponse = requests.request("POST", endpoint, headers=headers, data=payload)
    json_CDT_response = json.dumps(CDTResponse.json(), indent=4, sort_keys=False)
    json_CDT_response_dict = json.loads(json_CDT_response)
    code = json_CDT_response_dict["code"]
    error_code_handling(code)