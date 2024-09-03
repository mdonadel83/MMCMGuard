import os
import string
from ctypes import windll
import psutil
from pyaccsharedmemory import accSharedMemory
import time
import subprocess
import urllib3


now = time.time()
cont=0
versione=1.3
print("MMCM GUARD ACC v.1.3 In Avvio Attendi...")
print("PUOI RIDURRE AD ICONA QUESTO PROGRAMMA MENTRE GIOCHI.GRAZIE!")
def controllo_files():
    counter = 0
    print("Primo controllo In esecuzione...")

    drives = []
    bitmask = windll.kernel32.GetLogicalDrives()
    for letter in string.ascii_uppercase:
        if bitmask & 1:
            drives.append(letter)
        bitmask >>= 1

    #print(drives)

    files=[]
    inp = "CHEAT" #input("What are you looking for?:> ")
    thisdir = os.getcwd()
    for step in drives:
        #print(step)
        for r, d, f in os.walk(step+":\\"): # change the hard drive, if you want
            for file in f:
                filepath = os.path.join(r, file.upper())
                if inp in file.upper():
                    counter += 1
                    files.append(os.path.join(r, file.upper()))
                    #print(os.path.join(r, file))

    #print(f"trovati {counter} files.")
    return [counter,files]

def controllo_processi():
    print("Secondo controllo In esecuzione...(in ripetizione)")

    listOfProcessObjects = []
    # Iterate over the all the running process
    processName="cheat"
    processName1="ACCFuely"
    trovato_processo=False
    nome_processo=""
    for proc in psutil.process_iter():

        pinfo = proc.as_dict(attrs=['pid', 'name', 'create_time', 'status'])
        # Check if process name contains the given name string.
        #print(pinfo['name'].lower())
        if processName1.lower() in pinfo['name'].lower():
            trovato_processo=True
            nome_processo+=pinfo['name'].lower()+chr(13)+chr(10)
        if processName.lower() in pinfo['name'].lower():
            trovato_processo=True
            nome_processo+=pinfo['name'].lower()+chr(13)+chr(10)

    cmd = 'powershell "gps | where {$_.MainWindowTitle } | select Description,Id,Path'
    proc = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
    for line in proc.stdout:
        if not line.decode()[0].isspace():
            #print(line.decode().rstrip())
            # only print lines that are not empty
            # decode() is necessary to get rid of the binary string (b')
            # rstrip() to remove `\r\n`
            #print(line.decode().rstrip())
            if processName.lower() in line.decode().rstrip().lower():
                trovato_processo = True
                nome_processo += line.decode().rstrip().lower() + chr(13) + chr(10)
            if processName1.lower() in line.decode().rstrip().lower():
                trovato_processo = True
                nome_processo += line.decode().rstrip().lower() + chr(13) + chr(10)
    #print(nome_processo,trovato_processo)
    return [trovato_processo,nome_processo]

def getvar(uri):
    timeout_duration = 30
    try:
        #params = "key=val&key2=val2"
        url = uri
        http = urllib3.PoolManager()
        html1 = http.request('GET',url)
        return html1.data.decode("utf-8")
    except urllib3.exceptions.HTTPError as e:
        print('Richiesta connessione fallita!Errore:', e.reason)


sessione=""
descrizione=""
giro_precedente=0
campionato_in_corso=""
giro=0
dati_files = controllo_files()
#print(dati_files[0])
if int(dati_files[0]) > 0:
    #print("trovati files sospetti")
    descrizione = "Esistono "+str(int(dati_files[0]))+" files sospetti:"
    for files in dati_files[1]:
        descrizione +=files+chr(13)+chr(10)
    #print(descrizione)
asm = accSharedMemory()
while True:

    if time.time() > now + 60:
        controllo_proc=controllo_processi()
        if controllo_proc[0]:
            processi=True
        else:
            processi=False


        now = time.time()


        sm = asm.read_shared_memory()

        if (sm is not None):
            #print("entro")
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
            sessione_in_corso=str(sm.Graphics.session_type).strip()
            if sessione_in_corso == "Qualify":
                sessione_in_corso = "Qualifica"
            if sessione_in_corso == "Pratice":
                sessione_in_corso = "Pratica"
            if sessione_in_corso == "Race":
                sessione_in_corso = "Gara"

            pista=str(sm.Static.track).strip()
            if not sessione==sessione_in_corso:
                print("cambio sessione metto giri a 0")
                giro=0
                sessione=sessione_in_corso

            """
            print(sm.Graphics.session_type)
            if sm.Graphics.session_type==-1:
                sessione="Non conosciuta"
            if sm.Graphics.session_type == 0:
                sessione = "Pratiche"
            if sm.Graphics.session_type == 1:
                sessione = "Qualifica"
            if sm.Graphics.session_type == 2:
                sessione = "Gara"
            if sm.Graphics.session_type == 3:
                sessione = "HotLap"
            if sm.Graphics.session_type == 4:
                sessione = "Time Attack"
            if sm.Graphics.session_type == 5:
                sessione = "Drift"
            if sm.Graphics.session_type == 6:
                sessione = "Drag"
            if sm.Graphics.session_type == 7:
                sessione = "HotStint"
            if sm.Graphics.session_type == 8:
                sessione = "HotLapSuperPole"
            """

            #print(online,nome_pilota.strip(),cognome_pilota.strip(),consumi,benza,giro,danni,pressure,slip,wheel_angular_s,tyre_core_temp,suspension_travel)
            if online:
                print("Il gioco è in multiplayer")
                try:
                    print("Controllo Pilota se iscritto all'evento MMCM..")
                    risp = getvar("https://yoursite/api/controllo_pilota.php?nome=" + nome_pilota.strip()+"&cognome="+cognome_pilota.strip())
                    #print(risp)
                    if risp.find("OK") > -1:
                        print("OK Iscritto")
                        numero_driver=int(risp[risp.find("num") + 5:risp.find("champ")])
                        campionato_in_corso=risp[risp.find("champ") + 7:]
                        #print(risp[risp.find("num") + 5:risp.find("champ")])
                        #print(risp[risp.find("champ") + 7:])

                        print("Giro Attuale:",sm.Graphics.completed_lap,"Giro Precedente:",giro)
                        if sm.Graphics.completed_lap > giro:
                            giro_precedente = giro
                            giro = sm.Graphics.completed_lap
                            if giro > 0 and online:
                                print("Giro è +1 , controllo i livelli..")
                                # Verifico il giro precedente del pilota per i consumi
                                risp = getvar(
                                    "https://yoursite/api/controllo_benza.php?nome=" + nome_pilota.strip() + "&cognome=" + cognome_pilota.strip()+"&num="+str(numero_driver)+"&giroprec="+str(giro_precedente)+"&sess="+sessione)
                                if risp.find("OK") > -1:
                                    print("Informazioni Raccolte")
                                    print(float(risp[risp.find("Fuel") + 6:]))

                                    if float(risp[risp.find("Fuel") + 6:])==benza:
                                        print("controllo benzina NON superato")
                                        controllo_consumi_ok=False
                                        descrizione=+" ------ CONSUMI NON OK, PILOTA SOTTO CONTROLLO!! ------"
                                    else:
                                        print("Controllo SUPERATO!")

                        print("Tentativo Invio dati gioco al Server")
                        risp = getvar(
                            "https://yoursite/api/inserimento_dati.php?nome=" + nome_pilota.strip() + "&cognome=" + cognome_pilota.strip() + "&num=" + str(
                                numero_driver) + "&online=" + ("1" if online else "0") + "&pista=" + pista.strip()+"&sess="+sessione+"&benza="+str(benza)+"&desc="+descrizione+"&proc="+("Processo cheatengine/ACCFuely attivo!!" if processi else "")+"&drivvisio="+("1" if processi or len(descrizione)>0 else "0")+"&danni="+str(danni)+"&press="+str(pressure)+"&slip="+str(slip)+"&wheel="+str(wheel_angular_s)+"&tyret="+str(tyre_core_temp)+"&susptrav="+str(suspension_travel)+"&pit="+("1" if is_in_pit_lane else "0")+"&consumi="+str(consumi)+"&campcorso="+campionato_in_corso+"&giro="+str(giro)+"&descproc="+controllo_proc[1]+"&ver="+str(versione))
                        if risp.find("OK") > -1:
                            print("Inviati!")
                        else:
                            print("Errore su invio!Riprovare più tardi!")
                    else:
                        print("Non sei iscritto a questo Campionato/For Fun di MMCM Racing!")

                except:
                    print("Errore impossibile inviare dati!")
            else:
                print("Il gioco non è in modalità multiplayer e non è in modalità Guida, non invio dati!")


        sm.close()
