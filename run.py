from .vues import app
from . import socketio


if __name__ == "__main__":
    socketio.run(app, debug=True)
    app.run(host="0.0.0.0", port=5000, debug=False)