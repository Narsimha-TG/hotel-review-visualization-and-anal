from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/api/config', methods=['GET'])
def get_button_config():
    return jsonify({
        "buttons": [
            {"id": "analyze", "color": "#FF5733"},
            {"id": "export", "color": "#33FF57"},
            {"id": "refresh", "color": "#3357FF"},
            {"id": "settings", "color": "#F333FF"}
        ]
    })

if __name__ == '__main__':
    app.run(debug=True)