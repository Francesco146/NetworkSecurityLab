#!/bin/sh
# Servizio segreto della challenge della lezione 2.
# Gira dentro il container scanme; risponde con il flag a chi si connette.
while true; do
  echo 'CCIT{s3rv1z10_s3gr3t0}' | nc -l -p 31337
done
