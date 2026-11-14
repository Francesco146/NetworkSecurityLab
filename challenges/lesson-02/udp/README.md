# Lezione 2 — Bonus: lo scanner UDP

Il nostro scanner Scapy della lezione è TCP. Questo è un esercizio
facoltativo per scrivere uno scanner **UDP** e capire perché UDP è diverso.

## Perché UDP non è TCP

UDP non ha handshake. Non c'è un SYN-ACK che ci dice «la porta è aperta».
Dobbiamo interpretare le risposte:

| Risposta | Stato |
| --- | --- |
| Un datagramma UDP di risposta | **open** |
| ICMP type 3, code 3 (port unreachable) | **closed** |
| Nessuna risposta entro il timeout | **open\|filtered** |

`open|filtered` è ambiguo: la porta può essere aperta con un servizio che non
risponde, oppure filtrata da un firewall. In UDP non possiamo distinguerle
con una singola sonda.

## Cosa devi fare

1. Avvia il laboratorio:

   ```bash
   cd challenges/lesson-02/udp
   docker compose up -d --build
   ```

2. Guarda lo starter:

   ```bash
   docker exec -it udp-scanner python /work/starter.py
   ```

3. Completa `starter.py`: per ogni porta del range **5554–5557**, classifica
   la risposta come `open`, `closed` o `open|filtered`. Per `open` stampa
   anche il payload ricevuto.

4. Trova il servizio che risponde e il servizio che ascolta in silenzio.

5. Facoltativo: cattura il traffico e aprilo in Wireshark.

   ```bash
   docker exec -d udp-scanner sh -c \
     'timeout -s INT 8 tcpdump -i eth0 -nn "udp or icmp" -w /work/captures/udp.pcap'
   docker exec -it udp-scanner python /work/starter.py
   ```

   Apri `challenges/lesson-02/udp/captures/udp.pcap` in Wireshark.

## Cosa devi consegnare

1. L'output per le quattro porte, con lo stato e, per la porta aperta, il
   payload.
2. Due–cinque righe: perché una porta UDP chiusa si riconosce dall'ICMP,
   mentre una porta silenziosa resta `open|filtered`?
3. Facoltativo: uno screenshot di Wireshark con la richiesta UDP e la
   risposta (o l'ICMP port unreachable).

## Bonus

Prova a scansionare un range più ampio, per esempio `5500–5600`. Vedrai
molte più porte `open|filtered` del previsto. Perché? C'entra il rate limit
degli ICMP port unreachable del kernel, non il numero di servizi. Spiega
questo effetto in due righe.

## Regole

- Scansiona solo `udp-target`, il container della challenge o macchine tue.
- Non usare questo scanner contro host esterni.
- Non serve `sudo`: il container `udp-scanner` ha già i permessi.
- Non modificare il target: il punto è classificare le risposte, non
  aggirarlo.

## Se qualcosa non va

- `docker compose` non parte: Docker è avviato? La porta 5555 è occupata?
- `udp-scanner` non risolve `udp-target`: sei nella rete `udp-lab`?
- Tutte le porte sono `open|filtered`: il target è acceso? Hai usato il
  range giusto?
- Il pcap è vuoto: hai avviato `tcpdump` prima della scansione?
