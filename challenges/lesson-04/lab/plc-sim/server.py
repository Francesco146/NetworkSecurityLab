import threading
import time

from pymodbus.datastore import ModbusSequentialDataBlock, ModbusSlaveContext, ModbusServerContext
from pymodbus.server.sync import StartTcpServer

# Coils: 3 x (pump, valve), 3 alarms, 1 reset = 12
coils = [False] * 12
# Input registers: livelli vasca 1..3
levels = [80, 40, 60]

context = ModbusSlaveContext(
    co=ModbusSequentialDataBlock(0, coils),
    ir=ModbusSequentialDataBlock(0, levels),
    zero_mode=True,
)
server = ModbusServerContext(slaves={1: context}, single=False)


def simulation():
    while True:
        time.sleep(1)
        values = context.getValues(0x01, 0, 12)  # coils
        ir = context.getValues(0x04, 0, 3)       # input registers
        for i in range(3):
            pump = bool(values[2 * i])
            valve = bool(values[2 * i + 1])
            if pump:
                ir[i] += 5
            if valve:
                ir[i] -= 2
            ir[i] = max(0, min(100, ir[i]))
            if ir[i] > 90:
                values[8 + i] = True
        if values[11]:
            values[8] = values[9] = values[10] = False
            values[11] = False
        context.setValues(0x01, 0, values)
        context.setValues(0x04, 0, ir)


threading.Thread(target=simulation, daemon=True).start()
print("PLC simulator: Modbus TCP on 502, unit 1", flush=True)
StartTcpServer(context=server, address=("0.0.0.0", 502))
