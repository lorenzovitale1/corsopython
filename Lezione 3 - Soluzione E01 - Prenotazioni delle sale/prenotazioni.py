class Prenotazione:                           # Definisce la classe che rappresenta una prenotazione.
    def __init__(self, sala, ore):            # Riceve la nuova istanza (self), il nome della sala e il numero di ore.
        self.sala = sala                      # Memorizza il nome della sala su questa prenotazione.
        self.ore = ore                        # Memorizza la durata in ore sulla stessa prenotazione.

    def minuti(self):                         # Definisce il metodo che calcola la durata di questa prenotazione.
        return self.ore * 60                  # Converte le ore in minuti e restituisce il risultato a chi ha chiamato il metodo.
