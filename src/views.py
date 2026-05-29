import os
import sys
import time
import subprocess
import threading
from flask import Blueprint, render_template, jsonify, send_from_directory, abort, request

bp = Blueprint("views", __name__)

class CPUStressor:
    def __init__(self):
        self.processes = []
        self.start_time = None
        self.duration = 0
        self.requested_cores = 0
        self.lock = threading.Lock()

    def start(self, num_cores=2, duration=10):
        with self.lock:
            self._stop_unlocked()  # Clean up any existing processes
            
            # Max core protection and duration limit
            num_cores = max(1, min(num_cores, 8))
            duration = max(1, min(duration, 30))
            
            self.duration = duration
            self.requested_cores = num_cores
            self.start_time = time.time()
            
            python_executable = sys.executable
            # Heavy CPU math calculation script
            script = f"""
import time
start = time.time()
while time.time() - start < {duration}:
    _ = 12345.67 * 89012.34
"""
            for _ in range(num_cores):
                try:
                    # CREATE_NO_WINDOW (0x08000000) prevents command prompt windows on Windows
                    creationflags = 0
                    if sys.platform == "win32":
                        creationflags = 0x08000000
                    p = subprocess.Popen([python_executable, "-c", script], creationflags=creationflags)
                    self.processes.append(p)
                except Exception as e:
                    print(f"Error starting stress process: {e}")

    def stop(self):
        with self.lock:
            self._stop_unlocked()

    def _stop_unlocked(self):
        for p in self.processes:
            try:
                p.terminate()
                p.wait(timeout=0.2)
            except Exception:
                try:
                    p.kill()
                except Exception:
                    pass
        self.processes = []
        self.start_time = None
        self.duration = 0
        self.requested_cores = 0

    def get_status(self):
        with self.lock:
            # Filter out finished processes
            self.processes = [p for p in self.processes if p.poll() is None]
            active_count = len(self.processes)
            
            if active_count == 0:
                return {
                    "status": "idle",
                    "active_cores": 0,
                    "remaining_time": 0,
                    "requested_cores": 0,
                    "duration": 0
                }
            
            elapsed = time.time() - self.start_time if self.start_time else 0
            remaining = max(0, self.duration - elapsed)
            
            if remaining <= 0:
                self._stop_unlocked()
                active_count = 0
                remaining = 0
                
            return {
                "status": "stressing" if active_count > 0 else "idle",
                "active_cores": active_count,
                "remaining_time": round(remaining, 1),
                "requested_cores": self.requested_cores,
                "duration": self.duration
            }

stressor = CPUStressor()

IMAGE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "data", "images"))
TEXT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "data", "texts"))

@bp.route("/")
def index():
    """Render the landing page of the Flask application."""
    return render_template("index.html")

@bp.route("/api/health")
def health():
    """Health check endpoint for monitoring."""
    return jsonify({
        "status": "healthy",
        "service": "Flask Demo App",
        "port": 19191,
        "version": "1.0.0"
    })

@bp.route("/feature1/<picture_name>")
def feature1(picture_name):
    """Retrieve an image by name from the data/images directory."""
    try:
        return send_from_directory(IMAGE_DIR, picture_name)
    except FileNotFoundError:
        abort(404, description="Image not found")

@bp.route("/feature2/<file_name>")
def feature2(file_name):
    """Retrieve the text content of a txt file by name from the data/texts directory."""
    # Ensure secure path and prevent directory traversal
    safe_path = os.path.abspath(os.path.join(TEXT_DIR, file_name))
    if not safe_path.startswith(TEXT_DIR):
        abort(403, description="Access denied")
    
    if not os.path.isfile(safe_path) or not file_name.endswith(".txt"):
        abort(404, description="Text file not found")
        
    try:
        with open(safe_path, "r", encoding="utf-8") as f:
            content = f.read()
        return content, 200, {"Content-Type": "text/plain; charset=utf-8"}
    except Exception:
        abort(500, description="Internal server error reading file")

@bp.route("/api/cpu/stress/start", methods=["POST"])
def cpu_stress_start():
    """Start CPU stress background subprocesses."""
    data = request.get_json() or {}
    cores = int(data.get("cores", 2))
    duration = int(data.get("duration", 10))
    
    stressor.start(num_cores=cores, duration=duration)
    return jsonify({
        "status": "success",
        "message": f"Started CPU stress on {cores} cores for {duration} seconds.",
        "details": stressor.get_status()
    })

@bp.route("/api/cpu/stress/stop", methods=["POST"])
def cpu_stress_stop():
    """Stop all active CPU stress background subprocesses."""
    stressor.stop()
    return jsonify({
        "status": "success",
        "message": "Stopped all active CPU stress processes.",
        "details": stressor.get_status()
    })

@bp.route("/api/cpu/stress/status", methods=["GET"])
def cpu_stress_status():
    """Get the current CPU stress status."""
    return jsonify(stressor.get_status())


