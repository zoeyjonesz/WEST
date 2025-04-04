import eventlet
eventlet.monkey_patch()

from flask import Flask, render_template
from flask_socketio import SocketIO
from system import System
from sensor_data import parse_input
import time

app = Flask(__name__)
socketio = SocketIO(app)

# Constants
FILE_PATH = 'non-variable-input-flows.xlsx'
FULLY_OPEN = 1
FULLY_CLOSED = 0
SPEED_INCREMENT = 20
BTA_VALVE_INITIAL = 0.5
BTB_VALVE_INITIAL = 0.5

@app.route('/')
def index():
    return render_template('dashboard.html')

@socketio.on('connect')
def handle_connect():
    print("Client connected")
    socketio.start_background_task(simulate_system)

def simulate_system():
    system = System(
        recycling_volume = 0,
        bta_volume = 0,
        btb_volume = 0,
        recycling_pressure = 2,
        bta_pressure = 0.5,
        btb_pressure = 2,
        compressor_speed = 100,
        valve_BA = BTA_VALVE_INITIAL,
        valve_BB = BTB_VALVE_INITIAL
    )

    flowrates = parse_input(FILE_PATH)
    flow_rate_index = 1

    system.update_volume()

    while (system.pressure_threshold('recycling') == 'MOD' and
           system.pressure_threshold('bta') == 'LO' and
           system.pressure_threshold('btb') == 'HI'):

        if system.valve_BB != FULLY_OPEN:
            system.adjust_valve_position('BB', FULLY_OPEN)

        if system.compressor_speed < (system.max_compressor_speed - SPEED_INCREMENT):
            system.adjust_compressor_speed(SPEED_INCREMENT)

        if system.valve_BA != FULLY_CLOSED:
            system.adjust_valve_position('BA', FULLY_CLOSED)

        original_recycle_pressure = system.recycling_pressure

        system.changes_in_tanks(flowrates, flow_rate_index)
        flow_rate_index += 10

        recycle_pressure_change = system.recycling_pressure - original_recycle_pressure

        if recycle_pressure_change < 0:
            system.changes_in_tanks(flowrates, flow_rate_index)
            flow_rate_index += 10
        elif recycle_pressure_change >= 0 and system.compressor_speed <= (system.max_compressor_speed - SPEED_INCREMENT):
            system.adjust_compressor_speed(SPEED_INCREMENT)

        # Emit updated pressures to the frontend
        socketio.emit('pressure_update', {
            'recycle': system.recycling_pressure,
            'bta': system.bta_pressure,
            'btb': system.btb_pressure
        })

        time.sleep(1)

if __name__ == '__main__':
    socketio.run(app, debug=True)
