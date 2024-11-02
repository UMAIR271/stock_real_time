from flask import Flask, render_template
from flask_socketio import SocketIO
import asyncio
from script import main  # Adjust this import according to your package structure
import threading

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app, cors_allowed_origins="*")

@app.route('/')
def index():
    """Serve the index HTML file."""
    return render_template('index.html')

def start_async_tasks():
    """Start background tasks in a separate thread."""
    thread = threading.Thread(target=background_fetch_and_emit)
    thread.start()

def background_fetch_and_emit():
    """Set up and run the event loop for async tasks."""
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(fetch_data_and_emit())

async def fetch_data_and_emit():
    """Continuously fetch data asynchronously and emit using SocketIO."""
    while True:
        results = await main()  # Your async function that fetches data
        for data_type, data in results:
            socketio.emit('data_update', {'type': data_type, 'data': data}, namespace='/test')
        await asyncio.sleep(3)  # Wait for 1 second before fetching new data

@socketio.on('connect', namespace='/test')
def test_connect():
    """Handle client connections and start emitting data."""
    print('Client connected')
    start_async_tasks()

if __name__ == '__main__':
    # Run Flask application with SocketIO integration
    socketio.run(app, debug=True, host='0.0.0.0', port=5000)
