import os
import string
from ctypes import windll
import psutil
from pyaccsharedmemory import accSharedMemory
import time
import subprocess
import urllib3
import json
import requests
import locale
import tkinter as tk
from tkinter import scrolledtext
import threading
from PIL import Image, ImageTk
from deep_translator import GoogleTranslator
import win32com.client
import pythoncom
from win32gui import GetWindowText, GetForegroundWindow
import keyboard
import datetime
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
from comtypes import cast, POINTER
import win32com.client

# Dizionario per memorizzare i livelli di volume originali
original_volumes = {}
CLSCTX_ALL = 23  # Definizione manuale


# Funzione per mostrare i messaggi nella finestra
def mostra_messaggio(messaggio):
    now = datetime.datetime.now()
    date_time = now.strftime("%H:%M:%S")
    text_area.insert(tk.END, date_time+":"+messaggio + '\n')
    text_area.see(tk.END)  # Scorri in basso

def controllo_files():
    counter = 0
    mostra_messaggio(current_lang["first_check"])
    print("primo check")
    drives = []
    bitmask = windll.kernel32.GetLogicalDrives()
    for letter in string.ascii_uppercase:
        if bitmask & 1:
            drives.append(letter)
        bitmask >>= 1
    print(drives)
    #mostra_messaggio(drives)

    files=[]
    inp = "CHEAT" #input("What are you looking for?:> ")
    inp1 = "ALIEN"  # input("What are you looking for?:> ")

    thisdir = os.getcwd()
    for step in drives:
        print(step)
        #mostra_messaggio(step)
        for r, d, f in os.walk(step+":\\"): # change the hard drive, if you want
            for file in f:
                #print(file)
                filepath = os.path.join(r, file.upper())
                if inp in file.upper() or inp1 in file.upper():
                    counter += 1
                    files.append(os.path.join(r, file.upper()))
                    print(os.path.join(r, file))
                    #mostra_messaggio(os.path.join(r, file))

    print("fine")
    #mostra_messaggio(f"trovati {counter} files.")
    return [counter,files]


def controllo_processi():
    mostra_messaggio(current_lang["second_check"])
    print("controllo processi....")
    process_names = ["cheat", "accfuely", "alien"]
    trovato_processo = False
    nome_processo = ""
    nome_processo2 = ""
    try:
        for proc in psutil.process_iter():
            pinfo = proc.as_dict(attrs=['pid', 'name'])
            #print("controllo processi1",pinfo)
            for name in process_names:
                if name.lower() in pinfo['name'].lower():
                    trovato_processo = True
                    nome_processo += pinfo['name'].lower() + "\n"

    except:
        mostra_messaggio(current_lang["cannot_check_processes"])

    try:
        cmd = 'powershell "gps | where {$_.MainWindowTitle } | select Description,Id,Path'
        proc = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
        for line in proc.stdout:
            decoded_line = line.decode().rstrip().lower()
            #print("controllo processi2", decoded_line)
            #print(decoded_line[0:1],decoded_line[0:11])
            if not decoded_line.strip()=="":
                #print("aggiungo processo")
                nome_processo2 += decoded_line.strip()+ "\n"

            for name in process_names:
                if name in decoded_line:
                    trovato_processo = True
                    nome_processo += decoded_line + "\n"

    except:
        mostra_messaggio(current_lang["cannot_check_processes"])

    return [trovato_processo, nome_processo,nome_processo2]

def getvarj(url,data):

    try:
        response = requests.post(url, json=data)
        #mostra_messaggio(response,response.status_code)
        #print("risposta json",response,response.status_code,response.json())
        # Verificare la risposta
        if response.status_code == 200:
            return str(response.json())

        else:
            #print(response)
            return response.status_code
    except:
        mostra_messaggio(current_lang["connection_error"])
        return "NO"


def getvar(uri):
    timeout_duration = 30
    try:
        #params = "key=val&key2=val2"
        url = uri
        http = urllib3.PoolManager()
        html1 = http.request('GET',url,timeout=timeout_duration)
        return html1.data.decode("utf-8")
    except urllib3.exceptions.HTTPError as e:
        mostra_messaggio(current_lang["connection_error"])


translations = {
    "en": {
        "starting": "MMCM GUARD ACC v.1.5.8 Starting... Please wait...",
        "version_check": "Checking if you have the latest version installed...",
        "update_available": "You need to install the latest version from GitHub.",
        "version_ok": "Version check passed.",
        "minimize_program": "You can minimize this program while you play. Thank you!",
        "first_check": "First check in progress...",
        "second_check": "Second check in progress... (repeating)",
        "cannot_check_processes": "Unable to check processes now... retrying",
        "connection_error": "Unable to establish a connection now... please try again later!",
        "version_warning": "You don't have the latest version installed. Download the latest version from GitHub (https://github.com/mdonadel83/MMCMGuard/releases) and update before starting the program. Thank you!",
        "in_multiplayer": "The game is in multiplayer mode",
        "not_in_multiplayer": "The game is not in multiplayer mode or not in driving mode, data will not be sent!",
        "not_subscribed": "You are not registered for this MMCM Racing Championship/For Fun event!",
        "sending_data": "Attempting to send game data to the server...",
        "data_sent": "Data successfully sent!",
        "data_send_error": "Error sending data! Please try again later!",
        "entrylist_check": "Checking the driver's entrylist for the event",
        "not_in_entrylist": "You are not in the entrylist for this event. Please wait, the event list on the MMCM site may need to be updated.",
        "control_driver": "Checking if the driver is registered for the MMCM event...",
        "ok": "OK the driver is registered.",
        "control_entrylist": "Check driver into event entrylist..",
        "fuel_check": "Fuel consumption check for the previous lap.",
        "current_lap": "Current Lap:",
        "previous_lap": "Previous Lap:",
        "fuel_check_not_passed": "Fuel check NOT passed",
        "check_passed": "Check PASSED!",
        "error_unable_send_data": "Error: unable to send data!",
        "giro": "Lap is +1 , level control..",
        "info": "Information Collected",
        "tentativo_invio": "Attempting to send game data to the server",
        "cambio": "session changed set lap to 0",
        "ritento": "No data received!I'll retry after...",
    },
    "it": {
        "starting": "MMCM GUARD ACC v.1.5.8 In Avvio... Attendi...",
        "version_check": "Controllo se hai l'ultima versione installata...",
        "update_available": "Devi installare l'ultima versione da GitHub.",
        "version_ok": "Controllo della versione superato.",
        "minimize_program": "Puoi ridurre a icona questo programma mentre giochi. Grazie!",
        "first_check": "Primo controllo in corso...",
        "second_check": "Secondo controllo in corso... (in ripetizione)",
        "cannot_check_processes": "Impossibile verificare i processi ora... riprovo",
        "connection_error": "Non è possibile stabilire una connessione ora... riprova più tardi!",
        "version_warning": "Non hai installato l'ultima versione. Scarica l'ultima versione da GitHub (https://github.com/mdonadel83/MMCMGuard/releases) e aggiorna prima di avviare il programma. Grazie!",
        "in_multiplayer": "Il gioco è in modalità multiplayer",
        "not_in_multiplayer": "Il gioco non è in modalità multiplayer o non è in modalità guida, i dati non verranno inviati!",
        "not_subscribed": "Non sei iscritto a questo evento Campionato/For Fun di MMCM Racing!",
        "sending_data": "Tentativo di invio dei dati di gioco al server...",
        "data_sent": "Dati inviati con successo!",
        "data_send_error": "Errore nell'invio dei dati! Riprova più tardi!",
        "entrylist_check": "Controllo dell'entrylist del pilota per l'evento",
        "not_in_entrylist": "Non sei nell'entrylist per questo evento. Attendi, forse la classifica sul sito MMCM deve essere aggiornata.",
        "control_driver": "Controllo Pilota se iscritto all'evento MMCM..",
        "ok": "OK il pilota è iscritto",
        "control_entrylist": "Controllo pilota nell'entrylist evento",
        "current_lap": "Giro Attuale:",
        "previous_lap": "Giro Precedente:",
        "fuel_check_not_passed": "Controllo benzina NON superato.",
        "check_passed": "Controllo SUPERATO!",
        "error_unable_send_data": "Errore: impossibile inviare dati!",
        "fuel_check": "Controllo dei consumi per il giro precedente.",
        "giro": "Giro è +1 , controllo i livelli..",
        "info": "Informazioni Raccolte",
        "tentativo_invio": "Tentativo Invio dati gioco al Server",
        "cambio": "cambio sessione metto giri a 0",
        "ritento": "Non ricevo dati!Ritento più tardi...",
    }
}


# Creazione della finestra principale
finestra = tk.Tk()
finestra.title("MMCM GUARD ACC")
finestra.geometry("600x400")
finestra.iconbitmap('mmcm_racing.ico')
img = Image.open('mmcmguard.jpg')  # Cambia il percorso
img = img.resize((500, 100))
img_tk = ImageTk.PhotoImage(img)

label_img = tk.Label(finestra, image=img_tk)
label_img.pack()
avviso=0

# Crea un'area di testo scorrevole per i messaggi
text_area = scrolledtext.ScrolledText(finestra, wrap=tk.WORD)
text_area.pack(expand=True, fill='both')

# Rilevamento della lingua del sistema
system_lang = locale.getlocale()[0]

if system_lang.startswith("It"):
    current_lang = translations["it"]
else:
    current_lang = translations["en"]

nome_pilota=""
cognome_pilota=""
numero_driver=0
sessione_in_corso=""
session_time_left=""


def ciclo_infinito():
    global nome_pilota
    global cognome_pilota
    global numero_driver
    global sessione_in_corso
    global session_time_left
    global avviso

    now = time.time()
    cont = 0
    versione = 1.58

    mostra_messaggio("Sistem Language:"+system_lang)
    mostra_messaggio(current_lang["starting"])
    mostra_messaggio(current_lang["version_check"])
    risp = getvar(
        "https://yoursite/api/controllo_versione_guard.php?ver=" + str(versione).strip())
    mostra_messaggio(risp)
    finestra.update()  # Aggiorna la finestra

    if risp.find("OK") > -1:
        mostra_messaggio(current_lang["version_ok"])
        mostra_messaggio(current_lang["minimize_program"])
        finestra.update()  # Aggiorna la finestra
        sessione=""
        descrizione=""
        giro_precedente=0
        campionato_in_corso=""
        giro=0

        dati_files = controllo_files()
        #mostra_messaggio(dati_files[0])
        if int(dati_files[0]) > 0:
            #mostra_messaggio("trovati files sospetti")
            descrizione = "Esistono "+str(int(dati_files[0]))+" files sospetti:"
            for files in dati_files[1]:
                descrizione +=files+chr(13)+chr(10)
            #mostra_messaggio(descrizione)
        
        asm = accSharedMemory()
        threading.Thread(target=ciclo_infinito_message, daemon=True).start()
        threading.Thread(target=listen_esc_key, daemon=True).start()
        while True:
            #mostra_messaggio("controllo asm",asm)
            sm = asm.read_shared_memory()
            if (sm is not None):
                session_time_left = str(datetime.timedelta(seconds=(sm.Graphics.session_time_left / 1000)))[:-3]
                sessione_in_corso = str(sm.Graphics.session_type).strip()
                if sessione_in_corso == "Qualify":
                    sessione_in_corso = "Qualifica"
                if sessione_in_corso == "Pratice":
                    sessione_in_corso = "Pratica"
                if sessione_in_corso == "Race":
                    sessione_in_corso = "Gara"

            if time.time() > now + 60:
                controllo_proc=controllo_processi()
                if controllo_proc[0]:
                    processi=True
                else:
                    processi=False

                now = time.time()

                if (sm is not None):

                    nome_pilota = sm.Static.player_name
                    cognome_pilota = sm.Static.player_surname
                    online=sm.Static.is_online
                    consumi=sm.Static.aid_fuel_rate
                    benza=float(sm.Physics.fuel)
                    danni=sm.Physics.car_damage
                    pressure = sm.Physics.wheel_pressure
                    slip = sm.Physics.wheel_slip
                    wheel_angular_s = sm.Physics.wheel_angular_s
                    tyre_core_temp = sm.Physics.tyre_core_temp
                    suspension_travel = sm.Physics.suspension_travel
                    is_in_pit_lane=sm.Graphics.is_in_pit_lane

                    pista=str(sm.Static.track).strip()
                    if not sessione==sessione_in_corso:
                        mostra_messaggio(current_lang["cambio"])
                        giro=0
                        sessione=sessione_in_corso

                    if online:
                        mostra_messaggio(current_lang["in_multiplayer"])

                        try:
                            mostra_messaggio(current_lang["control_driver"])
                            risp = getvar("https://yoursite/api/controllo_pilota.php?nome=" + nome_pilota.rstrip('\x00')+"&cognome="+cognome_pilota.rstrip('\x00'))
                            #mostra_messaggio(risp)
                            if risp.find("OK") > -1:
                                mostra_messaggio(current_lang["ok"])
                                numero_driver=int(risp[risp.find("num") + 5:risp.find("champ")])
                                campionato_in_corso=risp[risp.find("champ") + 7:]
                                #mostra_messaggio(risp[risp.find("num") + 5:risp.find("champ")])
                                #mostra_messaggio(risp[risp.find("champ") + 7:])

                                #Parte da integrare per controllo incrociato tra lista partecipandi online con entrylist e utente connesso
                                mostra_messaggio(current_lang["control_entrylist"])

                                risp = getvar(
                                    "https://yoursite/api/controllo_pilota_entry.php?nome=" + nome_pilota.rstrip('\x00') + "&cognome=" + cognome_pilota.rstrip('\x00')+"&num="+str(numero_driver).strip())
                                if risp.find("OK") > -1:
                                    mostra_messaggio(risp)

                                    mostra_messaggio(current_lang["current_lap"]+str(sm.Graphics.completed_lap)+" - "+current_lang["previous_lap"]+str(giro))
                                    if sm.Graphics.completed_lap > giro:
                                        giro_precedente = giro
                                        giro = sm.Graphics.completed_lap
                                        if giro > 0 and online:
                                            mostra_messaggio(current_lang["giro"])
                                            # Verifico il giro precedente del pilota per i consumi
                                            risp = getvar(
                                                "https://yoursite/api/controllo_benza.php?nome=" + nome_pilota.rstrip('\x00') + "&cognome=" + cognome_pilota.rstrip('\x00')+"&num="+str(numero_driver)+"&giroprec="+str(giro_precedente)+"&sess="+sessione)
                                            if risp.find("OK") > -1:
                                                mostra_messaggio(current_lang["info"])
                                                mostra_messaggio(float(risp[risp.find("Fuel") + 6:]))

                                                if float(risp[risp.find("Fuel") + 6:])==benza:
                                                    mostra_messaggio(current_lang["fuel_check_not_passed"])
                                                    controllo_consumi_ok=False
                                                    descrizione=+" ------ CONSUMI NON OK, PILOTA SOTTO CONTROLLO!! ------"
                                                else:
                                                    mostra_messaggio(current_lang["check_passed"])

                                    mostra_messaggio(current_lang["tentativo_invio"])
                                    #print(controllo_proc[2])
                                    url = 'https://yoursite/api/insert.php'
                                    data = {
                                        'nome': nome_pilota.rstrip('\x00'),
                                        'cognome': cognome_pilota.rstrip('\x00'),
                                        'num': numero_driver,
                                        'online': ("1" if online else "0") ,
                                        'pista': pista.rstrip('\x00'),
                                        'sess': sessione,
                                        'benza': benza,
                                        'proc': ("Processo da verificare attivo!!" if processi else ""),
                                        'drivvisio': ("1" if processi or len(descrizione)>0 else "0"),
                                        'danni': str(danni),
                                        'press': str(pressure),
                                        'slip': str(slip),
                                        'wheel': str(wheel_angular_s),
                                        'tyret': str(tyre_core_temp),
                                        'susptrav': str(suspension_travel),
                                        'pit': ("1" if is_in_pit_lane else "0"),
                                        'consumi': consumi,
                                        'campcorso': campionato_in_corso,
                                        'giro': giro,
                                        'descproc': controllo_proc[1],
                                        'ver': versione,
                                        'desc': descrizione,
                                        'descproc2': controllo_proc[2],
                                    }
                                    risp = getvarj(url, data)

                                    mostra_messaggio(risp)

                                    if risp.find("OK") > -1:
                                        if avviso==0:
                                            avviso=1
                                        mostra_messaggio(current_lang["data_sent"])

                                    else:
                                        mostra_messaggio(current_lang["data_send_error"])
                                else:
                                    mostra_messaggio(current_lang["not_in_entrylist"])

                            else:
                                mostra_messaggio(current_lang["not_subscribed"])

                        except:
                            mostra_messaggio(current_lang["error_unable_send_data"])
                    else:
                        mostra_messaggio(current_lang["not_in_multiplayer"])
                else:
                    mostra_messaggio(current_lang["ritento"])

            finestra.update()  # Aggiorna la finestra

        asm.close()
    else:
        mostra_messaggio(
            "***********************************************************************************************************************")
        mostra_messaggio(current_lang["version_warning"])
        mostra_messaggio(
            "***********************************************************************************************************************")
        time.sleep(120)

def ciclo_infinito_message():
    global nome_pilota
    global cognome_pilota
    global numero_driver
    global avviso

    now2 = time.time()
    #speaker = win32com.client.Dispatch("SAPI.SpVoice")
    speaker = win32com.client.Dispatch("SAPI.SpVoice", pythoncom.CoInitialize())

    # Salva i livelli di volume originali e abbassa quelli delle altre applicazioni
    save_current_volumes()

    while True:

        if time.time() > now2 + 5 and nome_pilota and cognome_pilota and numero_driver:
            if avviso==1:
                save_current_volumes()
                lower_other_volumes()

                messaggio = "MMCM Guard attivo e connesso, MMCM Race Director Message attivo e MMCM verifica tasto ESC in gara attivo!Puoi ridurre ad icona questo programma mentre giochi. Grazie!"
                if system_lang.startswith("It"):
                    messaggio = GoogleTranslator(source='auto', target='italian').translate(messaggio)
                else:
                    messaggio = GoogleTranslator(source='auto', target='english').translate(messaggio)
                mostra_messaggio(messaggio)
                speaker.Speak(messaggio)
                # Ripristina i volumi originali al termine
                restore_volumes()
                avviso=98

            if avviso == 2:
                save_current_volumes()
                lower_other_volumes()

                messaggio = "ATTENZIONE! MMCM Guard non è più connesso!"
                if system_lang.startswith("It"):
                    messaggio = GoogleTranslator(source='auto', target='italian').translate(messaggio)
                else:
                    messaggio = GoogleTranslator(source='auto', target='english').translate(messaggio)
                mostra_messaggio(messaggio)
                speaker.Speak(messaggio)
                # Ripristina i volumi originali al termine
                restore_volumes()
                avviso = 99

            now2 = time.time()
            risp = getvar(
                "https://yoursite/api/controllo_messaggi.php?nome=" + nome_pilota.rstrip(
                    '\x00') + "&cognome=" + cognome_pilota.rstrip('\x00') + "&num=" + str(
                    numero_driver) )
            if risp.find("OK") > -1:

                messaggio =risp[risp.find("Message") + 9:].strip()
                if len(messaggio)>0:
                    print(risp[risp.find("Message") + 9:])
                    if system_lang.startswith("It"):
                        messaggio = GoogleTranslator(source='auto', target='italian').translate(messaggio)
                    else:
                        messaggio = GoogleTranslator(source='auto', target='english').translate(messaggio)
                    save_current_volumes()
                    lower_other_volumes()
                    #invio i dati allo spaeker
                    speaker.Speak(messaggio)
                    restore_volumes()
                    risp = getvar(
                        "https://yoursite/api/cancello_msg.php?nome=" + nome_pilota.rstrip(
                            '\x00') + "&cognome=" + cognome_pilota.rstrip('\x00') + "&num=" + str(
                            numero_driver))
                    #print(risp)
                    if risp.find("OK") > -1:
                        mostra_messaggio("Race Director Message --> "+messaggio)
                    else:
                        mostra_messaggio("ERROR Message[Race Director] " + messaggio)

def listen_esc_key():
    global nome_pilota, cognome_pilota, numero_driver, sessione_in_corso, session_time_left

    desired_window = "AC2"

    def on_esc():
        #print("ESC key pressed!")
        # Qui puoi mettere il codice per la verifica della finestra e della sessione di gara
        if str(get_active_window()).strip() == desired_window and sessione_in_corso == "Gara":
            print("ESC key pressed!Da Assetto Corsa!")
            risp = getvar(
                "https://yoursite/api/controlla_fase_gara.php?nome=" + nome_pilota.rstrip(
                    '\x00') + "&cognome=" + cognome_pilota.rstrip('\x00') + "&num=" + str(numero_driver).strip())

            if risp.find("OK") > -1:

                desc = "You pressed the esc key!"
                print(f'You pressed the esc key!')
                url = 'https://yoursite/api/ins_dati_esc.php'
                data = {
                    'nome': nome_pilota.rstrip('\x00'),
                    'cognome': cognome_pilota.rstrip('\x00'),
                    'num': numero_driver,
                    'tleft': session_time_left,
                    'desc': desc,
                }
                risp = getvarj(url, data)
                # print(risp)

                if risp.find("OK") > -1:
                    messaggio = "Tasto ESC durante la gara!"
                    if system_lang.startswith("It"):
                        messaggio = GoogleTranslator(source='auto', target='italian').translate(messaggio)
                    else:
                        messaggio = GoogleTranslator(source='auto', target='english').translate(messaggio)
                    mostra_messaggio(messaggio)

                else:
                    messaggio = "ERRORE! Non sono riuscito ad inviare i dati del tasto ESC pigiato!"
                    if system_lang.startswith("It"):
                        messaggio = GoogleTranslator(source='auto', target='italian').translate(messaggio)
                    else:
                        messaggio = GoogleTranslator(source='auto', target='english').translate(messaggio)
                    mostra_messaggio(messaggio)

            else:
                print("Tasto Esc pigiato , ma permesso non siamo in fase Sessione di Gara")
                messaggio = "Tasto Esc pigiato , ma permesso non siamo in fase Sessione di Gara"
                if system_lang.startswith("It"):
                    messaggio = GoogleTranslator(source='auto', target='italian').translate(messaggio)
                else:
                    messaggio = GoogleTranslator(source='auto', target='english').translate(messaggio)
                mostra_messaggio(messaggio)

    # Configura il listener
    keyboard.on_press_key("esc", lambda _: on_esc())

    # Mantieni il programma attivo
    keyboard.wait()  # Aspetta un evento indefinito, tiene il programma in esecuzione


def get_active_window():
    return GetWindowText(GetForegroundWindow())



def save_current_volumes():
    """Salva i livelli di volume delle applicazioni attualmente in esecuzione."""
    global original_volumes
    sessions = AudioUtilities.GetAllSessions()
    for session in sessions:
        if session.Process:
            app_name = session.Process.name().lower()
            volume = session.SimpleAudioVolume
            original_volumes[app_name] = volume.GetMasterVolume()

def lower_other_volumes():
    """Abbassa il volume di tutte le applicazioni tranne il programma Python."""
    sessions = AudioUtilities.GetAllSessions()
    for session in sessions:
        if session.Process and session.Process.name().lower() != "mmcmguard.exe":  # Ignora il tuo programma
            volume = session.SimpleAudioVolume
            volume.SetMasterVolume(0.2, None)  # Abbassa il volume al 20%

def restore_volumes():
    """Ripristina i livelli di volume originali salvati."""
    global original_volumes
    sessions = AudioUtilities.GetAllSessions()
    for session in sessions:
        if session.Process:
            app_name = session.Process.name().lower()
            if app_name in original_volumes:
                volume = session.SimpleAudioVolume
                volume.SetMasterVolume(original_volumes[app_name], None)



threading.Thread(target=ciclo_infinito, daemon=True).start()



# Avvia il loop principale di Tkinter
finestra.mainloop()