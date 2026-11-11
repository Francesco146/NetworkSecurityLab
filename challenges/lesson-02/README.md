# Lezione 2 — Il servizio segreto

Questa cartella contiene la challenge facoltativa della lezione 2. Il
container `scanme` espone alcuni servizi; uno è **segreto** e risponde su una
porta alta. Il tuo compito è trovarlo, connetterti e leggere il messaggio.

**Regola:** scansiona solo `scanme`, il container della challenge o macchine
tue. Non scansionare la rete dell'aula o host che non controlli.

## Cosa ti serve

- Docker avviato.
- Wireshark installato.
- Nessun permesso di amministratore: Nmap, Netcat e tcpdump sono già nel
  container `scapy-challenge`.

## Avvio

```bash
cd challenges/lesson-02
docker compose up -d --build
```

La prima volta il build può richiedere un minuto. Controlla:

```bash
docker compose ps
```

Devono essere `Up` `scanme-challenge` e `scapy-challenge`.

## Scansione

```bash
docker exec scapy-challenge nmap -p 1-40000 scanme
```

Nel risultato cerca le porte `open`. Una è il servizio segreto, su una porta
alta. Non fermarti alle prime porte: il range 1–100 non basta.

## Connessione

Sostituisci `<porta>` con il numero che hai trovato:

```bash
docker exec scapy-challenge sh -c 'printf "" | nc -w 2 scanme <porta>'
```

Il servizio risponde con un messaggio che inizia per `CCIT{`.

## Cattura

```bash
docker exec -d scapy-challenge sh -c \
  'timeout -s INT 6 tcpdump -i eth0 -nn tcp port <porta> -c 20 -w /caps/secret.pcap'
docker exec scapy-challenge sh -c 'printf "" | nc -w 2 scanme <porta>'
```

Il pcap finisce in `challenges/lesson-02/captures/secret.pcap`. Aprilo in
Wireshark, filtra `tcp.port == <porta>` e usa `Follow TCP Stream`.

## Cosa consegnare

1. Screenshot di Nmap con la porta alta aperta.
2. Il messaggio ricevuto.
3. Screenshot di Wireshark con il messaggio in `Follow TCP Stream`.
4. Due–cinque righe: perché uno scanner 1–100 non trova il servizio? Che
   differenza c'è tra porta aperta, chiusa e filtrata?

## Pulizia

```bash
docker compose down
```

## Se qualcosa non va

- `docker compose` non parte: Docker è avviato? La porta 31337 è occupata?
- Nmap non trova la porta: hai usato `-p 1-40000` o `-p-`?
- `nc` non risponde: il servizio accetta una connessione alla volta; riprova.
- Pcap vuoto: avvia `tcpdump` prima della connessione.
- Wireshark non vede il traffico: apri il pcap salvato, non catturare
  dall'host.
