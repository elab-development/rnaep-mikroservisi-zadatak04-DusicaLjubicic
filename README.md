[![Review Assignment Due Date](https://classroom.github.com/assets/deadline-readme-button-22041afd0340ce965d47ae6ef1cefeee28c7c493a6346c4f15d667ab976d596c.svg)](https://classroom.github.com/a/6F6ro7qq)
# Domaći zadatak 04 Proširenje i orkestracije mikroservisne arhitekture

Potrebno je unaprediti koncept loose coupling-a u distribuiranoj mikroservisnoj arhitekturi, primeniti standarde za konfiguraciju web aplikacije i dokerizovati aplikaciju u celosti. 

Postojeći sistem se sastoji od dva mikroservisa: Inventory (upravljanje zalihama) i Payment (obrada porudžbina). Servisi komuniciraju sinhrono putem HTTP protokola prilikom provere dostupnosti proizvoda, dok se asinhrona komunikacija i kompenzacione transakcije obavljaju putem Redis Streams mehanizma.

## Refaktorisanje
Trenutna implementacija u `payment/main.py` sadrži "hardkodovanu" URL adresu inventory servisa.

- Izmestite sve fiksne parametre (adrese servisa, portove i Redis kredencijale) iz koda u `.env` datoteke.
- U aplikaciji implementirajte učitavanje ovih vrednosti koristeći sistemske promenljive okruženja (preporuka: koristiti `pydantic-settings`).

## Dokerizacija aplikacije

Aplikacija mora postati prenosiva i nezavisna od lokalnog okruženja.
- Kreirajte Dockerfile datoteke za oba mikroservisa (inventory i payment), vodeći računa o instalaciji zavisnosti definisanih u requirements.txt.
- Definišite jedinstvenu docker-compose.yml datoteku koja će podizati ceo sistem:
- Kontejner za Redis bazu podataka.
- Kontejnere za oba mikroservisa.
- Kontejnere za njihove potrošače (consumers).

**Važno**: Komunikacija između servisa unutar Docker mreže mora se odvijati preko naziva kontejnera (npr. http://inventory:8000), a ne preko localhost adrese.

## Implementacija novog servisa: Notification Service

Potrebno je demonstrirati prednost arhitekture zasnovane na događajima (event-driven architecture).
- Razvijte novi, potpuno nezavisan mikroservis pod nazivom notification.
- Ovaj servis ne treba da ima sopstvene API endpoint-e, već isključivo proces u pozadini (consumer.py).
- Servis mora da se pridruži postojećim Redis stream-ovima: order_completed i refund_order.
- Za svaki pročitani događaj, servis treba da simulira slanje obaveštenja ispisom poruke u konzolu (npr. "Obaveštenje: Porudžbina {id} je uspešno kreirana i plaćena").
- Novi servis takođe mora biti uključen u docker-compose.yml orkestraciju.

![#f03c15](https://placehold.co/15x15/f03c15/f03c15.png) `#**Rok za predaju gotovog domaćeg zadatka je 5. maj 2026. godine.**`
