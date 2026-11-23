from pymodbus.client.sync import ModbusTcpClient

# Starter dello studente: lettura del PLC e prima scrittura.
# Completare la parte TODO e osservare l'HMI su http://localhost:8081.

plc = ModbusTcpClient("plc", port=502, timeout=2)
plc.connect()

levels = plc.read_input_registers(0, 3, unit=1)
coils = plc.read_coils(0, 12, unit=1)
print("Livelli:", levels.registers)
print("Pompe:", [coils.bits[0], coils.bits[2], coils.bits[4]])
print("Valvole:", [coils.bits[1], coils.bits[3], coils.bits[5]])
print("Allarmi:", [coils.bits[8], coils.bits[9], coils.bits[10]])

# TODO: accendi la pompa 1 e osserva il livello.
# plc.write_coil(0, True, unit=1)

plc.close()
