import csv                                    # Importa il modulo standard per leggere e scrivere righe CSV.
from pathlib import Path                      # Importa Path per indicare i percorsi dei due file.
import prenotazioni                           # Carica il nostro modulo prenotazioni.py dalla stessa cartella dello script.

prova = prenotazioni.Prenotazione("Prova", 2)  # Nel modulo prenotazioni usa la classe Prenotazione per creare un esempio di due ore.
print("Minuti di prova:", prova.minuti())     # Chiama il metodo sull’esempio e mostra 120 minuti.

origine = Path("richieste_sale.csv")          # Indica il CSV da leggere nella cartella di lavoro.
destinazione = Path("minuti_sale.csv")        # Indica il nome del report che il programma creerà nella stessa cartella.
totali = {}                                   # Prepara un dizionario: ogni chiave sarà una sala, ogni valore il suo totale in minuti.
scarti = 0                                    # Parte da zero prenotazioni scartate.

with origine.open(encoding="utf-8", newline="") as ingresso:  # Apre il CSV in lettura. with lo chiude a fine blocco e newline="" lascia gestire i fine riga a csv.
    lettore = csv.reader(ingresso)            # Prepara il lettore: ogni riga sarà una lista di stringhe.
    next(lettore, None)                       # Consuma la prima riga, sala,ore. Se il file è vuoto, next restituisce None.
    for riga in lettore:                      # Visita una prenotazione per volta a partire dalla prima riga di dati.
        if len(riga) < 2:                     # Controlla se manca la seconda colonna, quella delle ore.
            scarti += 1                       # Conta la riga incompleta come uno scarto.
            continue                          # Passa alla riga successiva prima di provare a leggere le ore.
        try:                                  # Prova a convertire il testo della durata in un numero intero.
            ore = int(riga[1])                # Legge la seconda colonna: per esempio, la stringa "2" diventa il numero 2.
        except ValueError:                    # Gestisce una durata illeggibile, come il punto interrogativo di Rossa.
            scarti += 1                       # Aggiunge uno scarto per la durata illeggibile.
            continue                          # Passa alla riga seguente senza creare una prenotazione.
        if ore <= 0:                          # Controlla se le ore sono zero o negative.
            scarti += 1                       # Conta anche questa durata come uno scarto.
            continue                          # Passa alla riga seguente senza sommare minuti.
        voce = prenotazioni.Prenotazione(riga[0], ore)  # Crea una prenotazione valida con la sala della prima colonna e le ore convertite.
        if voce.sala in totali:               # Verifica se è già presente un totale per questa sala.
            totali[voce.sala] += voce.minuti()  # Aggiunge al totale precedente i minuti della nuova prenotazione.
        else:                                 # Gestisce la prima prenotazione valida di questa sala.
            totali[voce.sala] = voce.minuti()  # Registra i primi minuti della sala nel dizionario.

with destinazione.open("w", encoding="utf-8", newline="") as uscita:  # Apre il report in scrittura. La modalità "w" lo ricrea a ogni esecuzione.
    scrittore = csv.writer(uscita)            # Prepara lo scrittore CSV collegato al file di uscita.
    scrittore.writerow(["sala", "minuti"])    # Scrive l’intestazione con i nomi delle due colonne.
    for sala, minuti in totali.items():       # Prende dal dizionario una sala e il suo totale per volta.
        scrittore.writerow([sala, minuti])    # Scrive una riga del report con la sala e i suoi minuti.

with destinazione.open(encoding="utf-8", newline="") as uscita:  # Riapre il report appena scritto per controllare il contenuto salvato.
    for riga in csv.reader(uscita):           # Legge tutte le righe del report, compresa l’intestazione.
        print(riga)                           # Mostra a schermo la riga appena riletta.
print("Scarti:", scarti)                      # Mostra il numero complessivo di prenotazioni scartate.
