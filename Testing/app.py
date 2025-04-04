from flask import Flask, render_template, jsonify
from sensor_data import parse_input
from system import System

app = Flask(__name__)

# Constants
FILE_PATH = 'non-variable-input-flows.xlsx'

@app.route("/")
def index():
    return render_template("simulation.html")

@app.route("/simulate")
def simulate():
    system = System(
        recycling_volume=4.0,
        bta_volume=0.3,
        btb_volume=2.0,
        recycling_pressure=2,
        bta_pressure=0.5,
        btb_pressure=2,
        compressor_speed=50,
        valve_BA=0,
        valve_BB=1
    )

    flowrates = parse_input(FILE_PATH)
    system.changes_in_tanks(flowrates, 0)

    return jsonify({
        "bta": {
            "volume": system.bta_volume,
            "pressure": system.pressure_threshold('bta'),
            "valve": "OPEN" if system.valve_BA > 0 else "CLOSED"
        },
        "btb": {
            "volume": system.btb_volume,
            "pressure": system.pressure_threshold('btb'),
            "valve": "OPEN" if system.valve_BB > 0 else "CLOSED"
        },
        "recycle": {
            "volume": system.recycling_volume,
            "pressure": system.pressure_threshold('recycling'),
            "compressor_speed": system.compressor_speed,
            "methane_output": round(system.compressor_speed * 0.00046, 3)
        }
    })

if __name__ == "__main__":
    app.run(debug=True)
