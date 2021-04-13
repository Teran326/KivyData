from database import *

db = Database(dbtype='sqlite', dbname='data.db')

rasa = Rasa()
rasa.nazev_rasy = 'Člověk'
db.create_rasa(rasa)

popis = Popis()
popis.popis = "'Nájemný zabiják monster, který na svých bedrech nosí dva meče.' \
                    ' Jeden stříbrný na monstra a ten druhý ocelový. Svým způsobem taky na monstra.'"
db.create_popis(popis)

povolani = Povolani()
povolani.nazev_povolani = 'Zaklínač'
povolani.rasa_id = rasa.nazev_rasy
povolani.popis_id = popis.popis

db.create_povolani(povolani)
