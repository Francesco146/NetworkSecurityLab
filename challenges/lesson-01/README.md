# Lezione 1 — Challenge: il file che viaggia in chiaro

Questa è l'unica challenge della lezione 1. In aula la facciamo insieme:
8 minuti per provarci e 4 per la soluzione. Su Moodle resta come recupero per
gli assenti o per chi vuole rifarla.

**Obiettivo:** trasferire un file con Netcat, catturare il traffico e
ritrovare il contenuto del file in Wireshark.

**Nota:** la chat con `nc -l 1234` + `nc server 1234` è già full-duplex. Qui
non lavoriamo sulla direzione della chat: usiamo Netcat per un trasferimento
di file e vediamo che il contenuto viaggia in chiaro.

**Regole.** Lavora solo sui tuoi container. Non scansionare host esterni e non
usare la rete dell'aula per attaccare altri. Se qualcosa non funziona, chiedi:
è normale, Docker ha molti dettagli.

## Passi

1. Nel client, crea un file segreto (scegli tu il contenuto):

   ```bash
   docker exec -it client sh
   printf 'CCIT{...}\n' > /tmp/secret.txt
   ```

2. Nel server, mettiti in ascolto e scrivi ciò che arriva in un file:

   ```bash
   docker exec -it server sh
   nc -l 4444 > /tmp/received.txt
   ```

3. In un terzo terminale, avvia la cattura sul server:

   ```bash
   cd 01_first-communications
   mkdir -p captures
   docker run --rm --network container:server \
     -v "$PWD/captures:/caps" alpine:latest sh -c \
     'apk add --no-cache tcpdump >/dev/null && timeout -s INT 12 tcpdump -i eth0 -nn tcp port 4444 -c 20 -w /caps/file.pcap'
   ```

   Aspetta la riga `listening on eth0` prima di mandare il file.

4. Dal client, manda il file:

   ```bash
   docker exec -it client sh
   nc -w 2 server 4444 < /tmp/secret.txt
   ```

5. Controlla che il server abbia ricevuto il file:

   ```bash
   docker exec server sh -c 'cat /tmp/received.txt; md5sum /tmp/received.txt'
   ```

6. Apri `captures/file.pcap` in Wireshark, filtra `tcp.port == 4444`,
   tasto destro → `Follow` → `TCP Stream`.

## Cosa consegnare

- Screenshot di `Follow TCP Stream` con il contenuto del file.
- Il contenuto del file (o l'hash).
- Una frase: perché il file è leggibile in Wireshark? Cosa cambierebbe con
  TLS?

## Bonus (facoltativo)

Trasferisci un file binario e confronta gli hash:

```bash
# client
head -c 1024 /dev/urandom > /tmp/blob.bin
md5sum /tmp/blob.bin

# server: nuovo ascolto
nc -l 4445 > /tmp/blob.bin

# client
nc -w 2 server 4445 < /tmp/blob.bin
```

Poi confronta `md5sum` sui due lati. In Wireshark prova `Follow TCP Stream` →
`Save as...` → `Raw`.

## Pulizia

```bash
docker exec server sh -c 'rm -f /tmp/received.txt'
docker exec client sh -c 'rm -f /tmp/secret.txt /tmp/blob.bin'
```
