# Lezione 4 — Laboratorio impianto a tre vasche

Laboratorio locale al posto di HoneyICS. Il PLC è un simulatore Modbus;
l'HMI è una pagina web; l'attaccante è il container `attacker`.

## Avvio

```bash
cd challenges/lesson-04/lab
docker compose up -d --build
docker compose ps
```

Attesi: `plc`, `hmi`, `attacker` Up. HMI: <http://localhost:8081>.
Modbus: `localhost:502`.

## Cosa c'è

- tre vasche con livelli, pompe, valvole, allarmi;
- HMI senza autenticazione (voluto);
- un client `starter.py` nel container `attacker`;
- `tcpdump` nel container `attacker` per la cattura;
- nessun dato esterno, nessun HoneyICS.

## Registri

| Indirizzo | Tipo | Significato |
| --- | --- | --- |
| IR 0–2 | input registers | livelli vasca 1–3 |
| Coil 0 | coil | pompa 1 |
| Coil 1 | coil | valvola 1 |
| Coil 2/3 | coil | pompa/valvola 2 |
| Coil 4/5 | coil | pompa/valvola 3 |
| Coil 8–10 | coil | allarmi 1–3 |
| Coil 11 | coil | reset allarmi |

## Leggere

```bash
docker exec -it attacker python /app/starter.py
```

Lo starter legge livelli e coils. Per scrivere, crea il tuo script con
`easymodbus==1.4.0` sul host oppure modifica una copia dello starter.

## Catturare

```bash
docker exec -d attacker tcpdump -i eth0 -nn tcp port 502 -w /tmp/modbus.pcap
# fai la lettura/scrittura
docker cp attacker:/tmp/modbus.pcap captures/modbus.pcap
```

Apri il pcap in Wireshark: filtro `modbus`, `modbus.func_code == 5`.

## Challenge

Obiettivo: portare la vasca 1 in allarme/overflow con una scrittura Modbus
non autenticata, poi fermare la pompa e resettare gli allarmi. Consegna
screenshot HMI, pcap e spiegazione.

## Regole

- Solo laboratorio locale.
- Non contattare dispositivi trovati su Shodan/Censys.
- Non modificare il PLC per aggirare la challenge.
