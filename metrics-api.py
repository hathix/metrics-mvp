import os
from models import metrics
from flask import Flask, send_from_directory, jsonify, request

app = Flask(__name__, static_folder='frontend/build')

# Serve React App
@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve(path):
    if path != "" and os.path.exists("frontend/build/" + path):
        return send_from_directory('frontend/build', path)
    else:
        return send_from_directory('frontend/build', 'index.html')

# hello world
@app.route('/metrics', methods=['GET'])
def index():
    route_id = str(request.args.get('route_id'))
    if route_id is None:
        route_id = '12'
    stop_id = str(request.args.get('stop_id'))
    if stop_id is None:
        stop_id = '4970'
    date = request.args.get('date')
    if date is None:
        date = "2019-02-01"
    direction = request.args.get('direction')
    if direction is None:
    	direction = "O"
    directionString = "inbound"
    if direction is "O":
    	directionString = "outbound"
    print(":)", route_id, stop_id, date, direction)    
    return "average waiting time at stop " + stop_id + " for route " + route_id + "  on " + date + " going " + directionString + " is " + str(metrics.get_average_waiting_time(
        stop_id=stop_id,
        route_id=route_id,
        direction="O",
        date_range=[date],
        # use the last month; calculate it and turn it into timestamps
        # date_range=[d.date().strftime("%Y-%m-%d") for d in
        # pd.date_range(pd.datetime.today(), periods=30).tolist()]
        time_range=("09:00", "10:00")))

# sanity check route
@app.route('/ajaxCall', methods=['POST'])
def ping_pong():
    return jsonify('I just made an ajax call :)')

if __name__ == '__main__':
    app.run(use_reloader=True, port=5000, threaded=True)