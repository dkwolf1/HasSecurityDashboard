from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import os

print("Starting FastAPI app...")

app = FastAPI(title="HasSecurityDash")

# Setup templates and static files
try:
    templates = Jinja2Templates(directory="/app/templates")
    app.mount("/static", StaticFiles(directory="/app/static"), name="static")
    print("Templates and static files mounted successfully")
except Exception as e:
    print(f"Error mounting templates: {e}")
    templates = None


@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    if templates:
        try:
            return templates.TemplateResponse("index.html", {"request": request})
        except Exception as e:
            print(f"Template error: {e}")
    
    # Fallback HTML response
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>HasSecurityDash</title>
        <script src="https://cdn.tailwindcss.com"></script>
        <script src="https://unpkg.com/lucide@latest"></script>
    </head>
    <body class="bg-gray-50">
        <div class="min-h-screen flex items-center justify-center">
            <div class="text-center">
                <h1 class="text-4xl font-bold text-blue-600 mb-4">🛡️ HasSecurityDash</h1>
                <p class="text-gray-600 mb-8">Security control and monitoring for Home Assistant</p>
                <div class="bg-white rounded-lg shadow p-6">
                    <h2 class="text-xl font-semibold mb-4">System Status</h2>
                    <div class="text-left space-y-2">
                        <p>✅ Backend API: Running</p>
                        <p>✅ FastAPI Server: Operational</p>
                        <p>✅ Health Check: <a href="/api/health" class="text-blue-600 hover:underline">Available</a></p>
                        <p>✅ API Endpoints: <a href="/api/security/score" class="text-blue-600 hover:underline">Security Score</a></p>
                        <p>⚠️ UI Templates: Loading from CDN</p>
                    </div>
                </div>
            </div>
        </div>
    </body>
    </html>
    """


@app.get("/api/health")
async def health():
    return {"status": "ok", "app": "HasSecurityDash", "version": "0.1.0"}


@app.get("/api/security/score")
async def get_security_score():
    return {
        "score": 75,
        "status": "good",
        "devices": 12,
        "open_ports": 3,
        "secured_services": 8,
        "threats": 1
    }


@app.get("/api/network/scan")
async def scan_network():
    return {
        "status": "completed",
        "devices": [
            {"ip": "192.168.1.1", "type": "router", "ports": [22, 80, 443]},
            {"ip": "192.168.1.100", "type": "desktop", "ports": [22, 80, 443, 8080]},
            {"ip": "192.168.1.105", "type": "mobile", "ports": [80, 443]}
        ],
        "open_ports": 3
    }


@app.get("/api/devices")
async def get_devices():
    return [
        {"name": "iPhone 13", "ip": "192.168.1.105", "type": "mobile", "status": "trusted", "last_seen": "2 hours ago"},
        {"name": "MacBook Pro", "ip": "192.168.1.102", "type": "laptop", "status": "trusted", "last_seen": "5 hours ago"},
        {"name": "Samsung TV", "ip": "192.168.1.108", "type": "tv", "status": "unknown", "last_seen": "1 day ago"}
    ]


@app.get("/api/alerts")
async def get_alerts():
    return [
        {"level": "critical", "title": "Unusual login attempt", "message": "Unknown IP address", "time": "10 minutes ago", "ip": "192.168.1.200"},
        {"level": "warning", "title": "Device without authentication", "message": "Connected without proper auth", "time": "1 hour ago", "ip": "192.168.1.150"},
        {"level": "info", "title": "New device joined", "message": "New device on network", "time": "2 hours ago", "ip": "192.168.1.105"}
    ]

print("FastAPI app created successfully!")
