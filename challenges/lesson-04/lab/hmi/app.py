from flask import Flask, jsonify, render_template, request

from pymodbus.client.sync import ModbusTcpClient

app = Flask(__name__)


def client():
    return ModbusTcpClient("plc", port=502, timeout=2)


def read_state():
    c = client()
    try:
        if not c.connect():
            return {"ok": False, "error": "PLC non raggiungibile"}
        ir = c.read_input_registers(0, 3, unit=1)
        coils = c.read_coils(0, 12, unit=1)
        if ir.isError() or coils.isError():
            return {"ok": False, "error": "errore Modbus"}
        return {
            "ok": True,
            "tanks": [
                {
                    "level": ir.registers[i],
                    "pump": coils.bits[2 * i],
                    "valve": coils.bits[2 * i + 1],
                    "alarm": coils.bits[8 + i],
                }
                for i in range(3)
            ],
        }
    finally:
        c.close()


def write_coil(address, value):
    c = client()
    try:
        if not c.connect():
            return False
        return not c.write_coil(address, bool(value), unit=1).isError()
    finally:
        c.close()


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/api/state")
def state():
    return jsonify(read_state())


@app.route("/api/pump", methods=["POST"])
def pump():
    tank = int(request.form.get("tank", "0"))
    value = request.form.get("value", "false").lower() == "true"
    return jsonify({"ok": write_coil(2 * tank, value)})


@app.route("/api/valve", methods=["POST"])
def valve():
    tank = int(request.form.get("tank", "0"))
    value = request.form.get("value", "false").lower() == "true"
    return jsonify({"ok": write_coil(1 + 2 * tank, value)})


@app.route("/api/reset", methods=["POST"])
def reset():
    return jsonify({"ok": write_coil(11, True)})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8081)
