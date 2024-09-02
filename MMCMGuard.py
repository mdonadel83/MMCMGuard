import os
import string
from ctypes import windll
import psutil
from pyaccsharedmemory import accSharedMemory
import mysql.connector
from mysql.connector import Error
import time
import subprocess

now = time.time()
cont=0
versione=1.1
print("MMCM GUARD ACC v.1.1 In Avvio Attendi...")
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
    inp = "cheat" #input("What are you looking for?:> ")
    thisdir = os.getcwd()
    for step in drives:
        #print(step)
        for r, d, f in os.walk(step+":\\"): # change the hard drive, if you want
            for file in f:
                filepath = os.path.join(r, file)
                if inp in file:
                    counter += 1
                    files.append(os.path.join(r, file))
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
while True:

    if time.time() > now + 60:
        controllo_proc=controllo_processi()
        if controllo_proc[0]:
            processi=True
        else:
            processi=False


        now = time.time()

        asm = accSharedMemory()
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
                    mydb = mysql.connector.connect(host="Your IP",
                                                   database="Your DB",
                                                   user="Your User",
                                                   password="Your Pass",
                                                   port="Your Port",
                                                   auth_plugin='Your Plugin')

                    if mydb.is_connected():

                        sql1 = "SELECT nome_pilota,cognome_pilota,numero_pilota,acc_campionato_in_corso.campionato FROM acc_champ_player,acc_campionato_in_corso where nome_pilota='" + nome_pilota.strip()+"' and cognome_pilota='"+cognome_pilota.strip()+"' and nome_campionato=acc_campionato_in_corso.campionato"

                        mycursor = mydb.cursor()
                        mycursor.execute(sql1)
                        records = mycursor.fetchall()
                        controllo_consumi_ok=True

                        if mycursor.rowcount:
                            if len(records) > 0:
                                for row in records:
                                    numero_driver = row[2]
                                    nome_pilota=row[0]
                                    cognome_pilota=row[1]
                                    campionato_in_corso=row[3]
                                print("Giro Attuale:",sm.Graphics.completed_lap,"Giro Precedente:",giro)
                                if sm.Graphics.completed_lap > giro:
                                    giro_precedente = giro
                                    giro = sm.Graphics.completed_lap
                                    if giro > 0 and online:
                                        print("Giro è +1 , controllo i livelli..")
                                        # Verifico il giro precedente del pilota per i consumi
                                        sql1 = "SELECT fuel FROM acc_guard where nome_pilota='" + nome_pilota + "' and cognome_pilota='" + cognome_pilota + "' and numero_pilota="+str(numero_driver)+" and giro="+str(giro_precedente)+" and sessione='"+sessione+"' and last_mod_data=CURDATE() LIMIT 1" #and pista='"+pista.strip()+"' da verificare perchè non mi scrive la pista come vorrei...
                                        mycursor = mydb.cursor()
                                        mycursor.execute(sql1)
                                        records1 = mycursor.fetchall()
                                        #print(sql1)
                                        #print(records1)
                                        for row1 in records1:
                                            if row1[0]==benza:
                                                print("controllo benzina NON superato")
                                                controllo_consumi_ok=False
                                                descrizione=+" ------ CONSUMI NON OK, PILOTA SOTTO CONTROLLO!! ------"

                                print("Invio dati gioco al Server")
                                if processi or len(descrizione)>0:
                                    #print("sospetto")
                                    sql1 = "INSERT INTO acc_guard (last_mod_data,last_mod_ora,nome_pilota,cognome_pilota,numero_pilota,connesso,pista,sessione,fuel,descrizione,processi,driver_in_visione,danni,pressure,slip,wheel_angular_s,tyre_core_temp,suspension_travel,is_in_pit_lane,fuel_rate,nome_campionato,giro,desc_processi,versione) VALUES (CURDATE(),CURTIME(),%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
                                    val = (nome_pilota.strip(), cognome_pilota.strip(), numero_driver, online, pista.strip(), sessione, benza,descrizione,("Processo cheatengine/ACCFuely attivo!!" if processi else ""),1,str(danni),str(pressure),str(slip),str(wheel_angular_s),str(tyre_core_temp),str(suspension_travel),is_in_pit_lane,consumi,campionato_in_corso,giro,controllo_proc[1],versione)

                                else:
                                    #print("inserisco")
                                    sql1 = "INSERT INTO acc_guard (last_mod_data,last_mod_ora,nome_pilota,cognome_pilota,numero_pilota,connesso,pista,sessione,fuel,danni,pressure,slip,wheel_angular_s,tyre_core_temp,suspension_travel,is_in_pit_lane,fuel_rate,nome_campionato,giro,desc_processi,versione) VALUES (CURDATE(),CURTIME(),%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
                                    val = (nome_pilota.strip(),cognome_pilota.strip(),numero_driver,online,pista.strip(),sessione,benza,str(danni),str(pressure),str(slip),str(wheel_angular_s),str(tyre_core_temp),str(suspension_travel),is_in_pit_lane,consumi,campionato_in_corso,giro,controllo_proc[1],versione)

                                # print(sql1)
                                mycursor = mydb.cursor()
                                mycursor.execute(sql1, val)
                                mydb.commit()

                except Error as e:
                    print("Error while connecting to MySQL", e)
                finally:
                    if (mydb.is_connected()):
                        mycursor.close()
                        mydb.close()

        asm.close()
