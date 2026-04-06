from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
import os
import asyncio
from datetime import datetime
from security_scanner import scanner

print("Starting FastAPI app...")

app = FastAPI(title="HasSecurityDash")

# Mount static files
app.mount("/static", StaticFiles(directory="/app/static"), name="static")
print("Static files mounted successfully")


@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    # Serve the complete HTML directly
    return """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>HasSecurityDash - Security Suite for Home Assistant</title>
        <script src="https://cdn.tailwindcss.com"></script>
        <script src="https://unpkg.com/lucide@latest"></script>
        <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
        <style>
            .security-score-ring {
                transform: rotate(-90deg);
                transform-origin: 50% 50%;
            }
            .animate-pulse-slow {
                animation: pulse 3s cubic-bezier(0.4, 0, 0.6, 1) infinite;
            }
        </style>
    </head>
    <body class="bg-gray-50 text-gray-900">
        <!-- Header -->
        <header class="bg-white shadow-sm border-b border-gray-200">
            <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
                <div class="flex justify-between items-center h-16">
                    <div class="flex items-center">
                        <i data-lucide="shield-search" class="w-8 h-8 text-blue-600 mr-3"></i>
                        <h1 class="text-xl font-semibold text-gray-900">HasSecurityDash</h1>
                    </div>
                    <nav class="flex space-x-4">
                        <button class="px-3 py-2 rounded-md text-sm font-medium text-white bg-blue-600" onclick="showSection('dashboard')">
                            Dashboard
                        </button>
                        <button class="px-3 py-2 rounded-md text-sm font-medium text-gray-700 hover:text-gray-900 hover:bg-gray-100" onclick="showSection('network')">
                            Network
                        </button>
                        <button class="px-3 py-2 rounded-md text-sm font-medium text-gray-700 hover:text-gray-900 hover:bg-gray-100" onclick="showSection('devices')">
                            Devices
                        </button>
                        <button class="px-3 py-2 rounded-md text-sm font-medium text-gray-700 hover:text-gray-900 hover:bg-gray-100" onclick="showSection('alerts')">
                            Alerts
                        </button>
                        <button class="px-3 py-2 rounded-md text-sm font-medium text-gray-700 hover:text-gray-900 hover:bg-gray-100" onclick="showSection('settings')">
                            Settings
                        </button>
                    </nav>
                </div>
            </div>
        </header>

        <!-- Main Content -->
        <main class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
            <!-- Dashboard Section -->
            <section id="dashboard" class="space-y-6">
                <!-- Security Score Overview -->
                <div class="bg-white rounded-lg shadow p-6">
                    <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
                        <!-- Security Score -->
                        <div class="text-center">
                            <div class="relative inline-flex items-center justify-center">
                                <svg class="w-32 h-32">
                                    <circle cx="64" cy="64" r="56" stroke="#e5e7eb" stroke-width="12" fill="none"></circle>
                                    <circle cx="64" cy="64" r="56" stroke="#10b981" stroke-width="12" fill="none"
                                            stroke-dasharray="351.86" stroke-dashoffset="88" class="security-score-ring"></circle>
                                </svg>
                                <div class="absolute">
                                    <div class="text-3xl font-bold text-gray-900" id="security-score">75</div>
                                    <div class="text-sm text-gray-500">Score</div>
                                </div>
                            </div>
                            <div class="mt-4">
                                <span class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-green-100 text-green-800" id="security-status">
                                    <i data-lucide="shield" class="w-3 h-3 mr-1"></i>
                                    Good
                                </span>
                            </div>
                        </div>

                        <!-- Quick Stats -->
                        <div class="md:col-span-2 grid grid-cols-2 gap-4">
                            <div class="bg-blue-50 rounded-lg p-4">
                                <div class="flex items-center">
                                    <i data-lucide="wifi" class="w-8 h-8 text-blue-600 mr-3"></i>
                                    <div>
                                        <div class="text-2xl font-semibold text-gray-900" id="device-count">12</div>
                                        <div class="text-sm text-gray-600">Active Devices</div>
                                    </div>
                                </div>
                            </div>
                            <div class="bg-yellow-50 rounded-lg p-4">
                                <div class="flex items-center">
                                    <i data-lucide="alert-triangle" class="w-8 h-8 text-yellow-600 mr-3"></i>
                                    <div>
                                        <div class="text-2xl font-semibold text-gray-900" id="open-ports">3</div>
                                        <div class="text-sm text-gray-600">Open Ports</div>
                                    </div>
                                </div>
                            </div>
                            <div class="bg-green-50 rounded-lg p-4">
                                <div class="flex items-center">
                                    <i data-lucide="lock" class="w-8 h-8 text-green-600 mr-3"></i>
                                    <div>
                                        <div class="text-2xl font-semibold text-gray-900" id="secured-services">8</div>
                                        <div class="text-sm text-gray-600">Secured Services</div>
                                    </div>
                                </div>
                            </div>
                            <div class="bg-red-50 rounded-lg p-4">
                                <div class="flex items-center">
                                    <i data-lucide="alert-circle" class="w-8 h-8 text-red-600 mr-3"></i>
                                    <div>
                                        <div class="text-2xl font-semibold text-gray-900" id="threats">1</div>
                                        <div class="text-sm text-gray-600">Threats Detected</div>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>

                <!-- Recent Activity -->
                <div class="bg-white rounded-lg shadow">
                    <div class="px-6 py-4 border-b border-gray-200">
                        <h2 class="text-lg font-medium text-gray-900">Recent Activity</h2>
                    </div>
                    <div class="p-6">
                        <div class="space-y-4" id="activity-list">
                            <!-- Activity items will be loaded here -->
                        </div>
                    </div>
                </div>

                <!-- Security Chart -->
                <div class="bg-white rounded-lg shadow">
                    <div class="px-6 py-4 border-b border-gray-200">
                        <h2 class="text-lg font-medium text-gray-900">Security Trend</h2>
                    </div>
                    <div class="p-6">
                        <canvas id="securityChart" width="400" height="200"></canvas>
                    </div>
                </div>
            </section>

            <!-- Network Section -->
            <section id="network" class="space-y-6 hidden">
                <div class="bg-white rounded-lg shadow p-6">
                    <h2 class="text-lg font-medium text-gray-900 mb-4">Network Scanner</h2>
                    <div class="space-y-4">
                        <button onclick="startNetworkScan()" class="bg-blue-600 text-white px-4 py-2 rounded-md hover:bg-blue-700">
                            <i data-lucide="search" class="w-4 h-4 inline mr-2"></i>
                            Start Network Scan
                        </button>
                        <div id="scanResults" class="hidden">
                            <!-- Scan results will appear here -->
                        </div>
                    </div>
                </div>
            </section>

            <!-- Devices Section -->
            <section id="devices" class="space-y-6 hidden">
                <div class="bg-white rounded-lg shadow p-6">
                    <h2 class="text-lg font-medium text-gray-900 mb-4">Connected Devices</h2>
                    <div id="deviceList" class="space-y-3">
                        <!-- Device list will appear here -->
                    </div>
                </div>
            </section>

            <!-- Alerts Section -->
            <section id="alerts" class="space-y-6 hidden">
                <div class="bg-white rounded-lg shadow p-6">
                    <h2 class="text-lg font-medium text-gray-900 mb-4">Security Alerts</h2>
                    <div id="alertsList" class="space-y-3">
                        <!-- Alerts will appear here -->
                    </div>
                </div>
            </section>

            <!-- Settings Section -->
            <section id="settings" class="space-y-6 hidden">
                <div class="bg-white rounded-lg shadow p-6">
                    <h2 class="text-lg font-medium text-gray-900 mb-4">Security Settings</h2>
                    <div class="space-y-4">
                        <div>
                            <label class="block text-sm font-medium text-gray-700">Scan Frequency</label>
                            <select class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500">
                                <option>Every 5 minutes</option>
                                <option>Every 15 minutes</option>
                                <option>Every 30 minutes</option>
                                <option>Every hour</option>
                            </select>
                        </div>
                        <div>
                            <label class="block text-sm font-medium text-gray-700">Alert Level</label>
                            <select class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500">
                                <option>All alerts</option>
                                <option>Warnings and above</option>
                                <option>Critical only</option>
                            </select>
                        </div>
                        <button class="bg-blue-600 text-white px-4 py-2 rounded-md hover:bg-blue-700">
                            Save Settings
                        </button>
                    </div>
                </div>
            </section>
        </main>

        <script>
            // Initialize Lucide icons
            lucide.createIcons();

            // Section navigation
            function showSection(sectionId) {
                const sections = ['dashboard', 'network', 'devices', 'alerts', 'settings'];
                sections.forEach(id => {
                    const section = document.getElementById(id);
                    if (section) section.classList.add('hidden');
                });
                
                const selectedSection = document.getElementById(sectionId);
                if (selectedSection) selectedSection.classList.remove('hidden');
                
                // Update navigation buttons
                const buttons = document.querySelectorAll('nav button');
                buttons.forEach(button => {
                    button.classList.remove('text-white', 'bg-blue-600');
                    button.classList.add('text-gray-700', 'hover:text-gray-900', 'hover:bg-gray-100');
                });
                
                event.target.classList.remove('text-gray-700', 'hover:text-gray-900', 'hover:bg-gray-100');
                event.target.classList.add('text-white', 'bg-blue-600');
                
                // Initialize section-specific content
                if (sectionId === 'dashboard') loadDashboard();
                if (sectionId === 'devices') loadDevices();
                if (sectionId === 'alerts') loadAlerts();
            }

            // Load dashboard data
            async function loadDashboard() {
                try {
                    const response = await fetch('/api/security/score');
                    const data = await response.json();
                    
                    document.getElementById('security-score').textContent = data.score;
                    document.getElementById('device-count').textContent = data.devices;
                    document.getElementById('open-ports').textContent = data.open_ports;
                    document.getElementById('secured-services').textContent = data.secured_services;
                    document.getElementById('threats').textContent = data.threats;
                    
                    // Update status
                    const statusEl = document.getElementById('security-status');
                    if (data.score >= 80) {
                        statusEl.className = 'inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-green-100 text-green-800';
                        statusEl.innerHTML = '<i data-lucide="shield" class="w-3 h-3 mr-1"></i>Good';
                    } else if (data.score >= 60) {
                        statusEl.className = 'inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-yellow-100 text-yellow-800';
                        statusEl.innerHTML = '<i data-lucide="shield" class="w-3 h-3 mr-1"></i>Warning';
                    } else {
                        statusEl.className = 'inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-red-100 text-red-800';
                        statusEl.innerHTML = '<i data-lucide="shield" class="w-3 h-3 mr-1"></i>Critical';
                    }
                    lucide.createIcons();
                    
                    // Load activity
                    loadActivity();
                    
                    // Initialize chart
                    initChart();
                } catch (error) {
                    console.error('Error loading dashboard:', error);
                }
            }

            // Load recent activity
            async function loadActivity() {
                const activities = [
                    {icon: 'user-plus', color: 'blue', title: 'New device connected', desc: 'iPhone 13 - 192.168.1.105', time: '2 min ago'},
                    {icon: 'shield-check', color: 'green', title: 'Security scan completed', desc: 'Network scan finished successfully', time: '15 min ago'},
                    {icon: 'alert-triangle', color: 'yellow', title: 'Unusual activity detected', desc: 'Multiple failed login attempts', time: '1 hour ago'}
                ];
                
                const activityList = document.getElementById('activity-list');
                activityList.innerHTML = activities.map(activity => `
                    <div class="flex items-center justify-between">
                        <div class="flex items-center">
                            <div class="flex-shrink-0">
                                <i data-lucide="${activity.icon}" class="w-5 h-5 text-${activity.color}-600"></i>
                            </div>
                            <div class="ml-3">
                                <p class="text-sm font-medium text-gray-900">${activity.title}</p>
                                <p class="text-sm text-gray-500">${activity.desc}</p>
                            </div>
                        </div>
                        <div class="text-sm text-gray-500">${activity.time}</div>
                    </div>
                `).join('');
                
                lucide.createIcons();
            }

            // Initialize security chart
            function initChart() {
                const ctx = document.getElementById('securityChart');
                if (!ctx) return;
                
                new Chart(ctx, {
                    type: 'line',
                    data: {
                        labels: ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'],
                        datasets: [{
                            label: 'Security Score',
                            data: [65, 70, 68, 75, 73, 75, 75],
                            borderColor: 'rgb(59, 130, 246)',
                            backgroundColor: 'rgba(59, 130, 246, 0.1)',
                            tension: 0.4
                        }]
                    },
                    options: {
                        responsive: true,
                        maintainAspectRatio: false,
                        scales: {
                            y: { beginAtZero: true, max: 100 }
                        }
                    }
                });
            }

            // Network scan
            async function startNetworkScan() {
                const button = event.target;
                const originalText = button.innerHTML;
                button.disabled = true;
                button.innerHTML = '<i data-lucide="loader" class="w-4 h-4 inline mr-2 animate-spin"></i>Scanning...';
                lucide.createIcons();
                
                const resultsDiv = document.getElementById('scanResults');
                
                try {
                    // Show scanning progress
                    resultsDiv.innerHTML = `
                        <div class="mt-4 space-y-3">
                            <div class="bg-blue-50 border border-blue-200 rounded-md p-3">
                                <div class="flex items-center">
                                    <i data-lucide="search" class="w-5 h-5 text-blue-600 mr-2 animate-pulse"></i>
                                    <span class="text-sm font-medium text-blue-800">Discovering hosts on network...</span>
                                </div>
                                <div class="mt-2">
                                    <div class="w-full bg-blue-200 rounded-full h-2">
                                        <div class="bg-blue-600 h-2 rounded-full animate-pulse" style="width: 30%"></div>
                                    </div>
                                </div>
                            </div>
                        </div>
                    `;
                    resultsDiv.classList.remove('hidden');
                    lucide.createIcons();
                    
                    try {
                        const response = await fetch('/api/network/scan');
                    
                    // Check if response is ok
                    if (!response.ok) {
                        throw new Error(`HTTP ${response.status}: ${response.statusText}`);
                    }
                    
                    // Check content type
                    const contentType = response.headers.get('content-type');
                    if (!contentType || !contentType.includes('application/json')) {
                        const text = await response.text();
                        console.error('Non-JSON response:', text);
                        throw new Error('Server returned non-JSON response');
                    }
                    
                    const data = await response.json();
                    console.log('Scan data received:', data);
                        
                        if (data.status === 'error') {
                            throw new Error(data.error || 'Scan failed');
                        }
                        
                        // Show scan results
                        resultsDiv.innerHTML = `
                            <div class="mt-4 space-y-3">
                                <div class="bg-green-50 border border-green-200 rounded-md p-3">
                                    <div class="flex items-center justify-between">
                                        <div class="flex items-center">
                                            <i data-lucide="check-circle" class="w-5 h-5 text-green-600 mr-2"></i>
                                            <span class="text-sm font-medium text-green-800">Scan completed successfully</span>
                                        </div>
                                        <span class="text-xs text-green-600">Security Score: ${data.security_score}/100</span>
                                    </div>
                                    <div class="mt-2 text-sm text-green-700">
                                        Found ${data.devices.length} devices, ${data.open_ports} open ports detected
                                    </div>
                                </div>
                                
                                ${data.devices.length > 0 ? `
                                    <div class="space-y-2">
                                        <h3 class="text-sm font-medium text-gray-900">Discovered Devices</h3>
                                        <div class="grid grid-cols-1 md:grid-cols-2 gap-3">
                                            ${data.devices.map(device => `
                                                <div class="border border-gray-200 rounded-md p-3 ${device.security_level === 'critical' ? 'border-red-300 bg-red-50' : device.security_level === 'high_risk' ? 'border-orange-300 bg-orange-50' : device.security_level === 'medium_risk' ? 'border-yellow-300 bg-yellow-50' : 'border-green-300 bg-green-50'}">
                                                    <div class="flex items-center justify-between mb-2">
                                                        <span class="text-sm font-medium">${device.hostname || device.ip}</span>
                                                        <span class="text-xs px-2 py-1 rounded ${device.security_level === 'critical' ? 'bg-red-100 text-red-800' : device.security_level === 'high_risk' ? 'bg-orange-100 text-orange-800' : device.security_level === 'medium_risk' ? 'bg-yellow-100 text-yellow-800' : 'bg-green-100 text-green-800'}">
                                                            ${device.security_level.replace('_', ' ').toUpperCase()}
                                                        </span>
                                                    </div>
                                                    <div class="text-xs text-gray-600 mb-2">${device.ip}</div>
                                                    ${device.ports.length > 0 ? `
                                                        <div class="space-y-1">
                                                            <div class="text-xs font-medium text-gray-700">Open Ports:</div>
                                                            <div class="flex flex-wrap gap-1">
                                                                ${device.ports.map(port => `
                                                                    <span class="text-xs bg-gray-100 text-gray-800 px-2 py-1 rounded">${port}</span>
                                                                `).join('')}
                                                            </div>
                                                        </div>
                                                    ` : '<div class="text-xs text-gray-500">No open ports detected</div>'}
                                                    ${device.vulnerabilities > 0 ? `
                                                        <div class="mt-2 text-xs text-red-600">
                                                            <i data-lucide="alert-triangle" class="w-3 h-3 inline mr-1"></i>
                                                            ${device.vulnerabilities} vulnerabilities found
                                                        </div>
                                                    ` : ''}
                                                </div>
                                            `).join('')}
                                        </div>
                                    </div>
                                ` : '<div class="text-sm text-gray-500">No devices found on network</div>'}
                                
                                ${data.vulnerabilities && data.vulnerabilities.length > 0 ? `
                                    <div class="space-y-2">
                                        <h3 class="text-sm font-medium text-gray-900">Security Issues Found</h3>
                                        <div class="space-y-2">
                                            ${data.vulnerabilities.map(vuln => `
                                                <div class="border-l-4 border-${vuln.severity === 'critical' ? 'red' : vuln.severity === 'high' ? 'orange' : 'yellow'}-500 bg-${vuln.severity === 'critical' ? 'red' : vuln.severity === 'high' ? 'orange' : 'yellow'}-50 p-3">
                                                    <div class="flex items-start">
                                                        <i data-lucide="${vuln.severity === 'critical' ? 'alert-circle' : vuln.severity === 'high' ? 'alert-triangle' : 'info'}" class="w-4 h-4 text-${vuln.severity === 'critical' ? 'red' : vuln.severity === 'high' ? 'orange' : 'yellow'}-600 mr-2 mt-0.5"></i>
                                                        <div class="flex-1">
                                                            <div class="text-sm font-medium text-${vuln.severity === 'critical' ? 'red' : vuln.severity === 'high' ? 'orange' : 'yellow'}-800">
                                                                ${vuln.service} (Port ${vuln.port})
                                                            </div>
                                                            <div class="text-xs text-${vuln.severity === 'critical' ? 'red' : vuln.severity === 'high' ? 'orange' : 'yellow'}-700 mt-1">
                                                                ${vuln.description}
                                                            </div>
                                                            <div class="text-xs text-${vuln.severity === 'critical' ? 'red' : vuln.severity === 'high' ? 'orange' : 'yellow'}-600 mt-1">
                                                                💡 ${vuln.recommendation}
                                                            </div>
                                                        </div>
                                                    </div>
                                                </div>
                                            `).join('')}
                                        </div>
                                    </div>
                                ` : ''}
                                
                                ${data.recommendations && data.recommendations.length > 0 ? `
                                    <div class="space-y-2">
                                        <h3 class="text-sm font-medium text-gray-900">Security Recommendations</h3>
                                        <div class="space-y-2">
                                            ${data.recommendations.map(rec => `
                                                <div class="bg-blue-50 border border-blue-200 rounded-md p-3">
                                                    <div class="flex items-start">
                                                        <i data-lucide="shield-check" class="w-4 h-4 text-blue-600 mr-2 mt-0.5"></i>
                                                        <div class="text-sm text-blue-800">${rec}</div>
                                                    </div>
                                                </div>
                                            `).join('')}
                                        </div>
                                    </div>
                                ` : ''}
                                
                                <div class="text-xs text-gray-500 mt-4">
                                    Scan completed at: ${new Date(data.scan_time).toLocaleString()}
                                </div>
                            </div>
                        `;
                        resultsDiv.classList.remove('hidden');
                        lucide.createIcons();
                        
                        // Update dashboard if needed
                        if (typeof loadDashboard === 'function') {
                            loadDashboard();
                        }
                        
                    } catch (error) {
                        console.error('Scan error:', error);
                        resultsDiv.innerHTML = `
                            <div class="mt-4">
                                <div class="bg-red-50 border border-red-200 rounded-md p-3">
                    // Show scan results
                    resultsDiv.innerHTML = `
                        <div class="mt-4 space-y-3">
                            <div class="bg-green-50 border border-green-200 rounded-md p-3">
                                <div class="flex items-center justify-between">
                                    <div class="flex items-center">
                                        <i data-lucide="check-circle" class="w-5 h-5 text-green-600 mr-2"></i>
                                        <span class="text-sm font-medium text-green-800">Scan completed successfully</span>
                                    </div>
                                    <span class="text-xs text-green-600">Security Score: ${data.security_score}/100</span>
                                </div>
                                <div class="mt-2 text-sm text-green-700">
                                    Found ${data.devices.length} devices, ${data.open_ports} open ports detected
                                </div>
                            </div>
                            
                            ${data.devices.length > 0 ? `
                                <div class="space-y-2">
                                    <h3 class="text-sm font-medium text-gray-900">Discovered Devices</h3>
                                    <div class="grid grid-cols-1 md:grid-cols-2 gap-3">
                                        ${data.devices.map(device => `
                                            <div class="border border-gray-200 rounded-md p-3 ${device.security_level === 'critical' ? 'border-red-300 bg-red-50' : device.security_level === 'high_risk' ? 'border-orange-300 bg-orange-50' : device.security_level === 'medium_risk' ? 'border-yellow-300 bg-yellow-50' : 'border-green-300 bg-green-50'}">
                                                <div class="flex items-center justify-between mb-2">
                                                    <span class="text-sm font-medium">${device.hostname || device.ip}</span>
                                                    <span class="text-xs px-2 py-1 rounded ${device.security_level === 'critical' ? 'bg-red-100 text-red-800' : device.security_level === 'high_risk' ? 'bg-orange-100 text-orange-800' : device.security_level === 'medium_risk' ? 'bg-yellow-100 text-yellow-800' : 'bg-green-100 text-green-800'}">
                                                        ${device.security_level.replace('_', ' ').toUpperCase()}
                                                    </span>
                                                </div>
                                                <div class="text-xs text-gray-600 mb-2">${device.ip}</div>
                                                ${device.ports.length > 0 ? `
                                                    <div class="space-y-1">
                                                        <div class="text-xs font-medium text-gray-700">Open Ports:</div>
                                                        <div class="flex flex-wrap gap-1">
                                                            ${device.ports.map(port => `
                                                                <span class="text-xs bg-gray-100 text-gray-800 px-2 py-1 rounded">${port}</span>
                                                            `).join('')}
                                                        </div>
                                                    </div>
                                                ` : '<div class="text-xs text-gray-500">No open ports detected</div>'}
                                                ${device.vulnerabilities > 0 ? `
                                                    <div class="mt-2 text-xs text-red-600">
                                                        <i data-lucide="alert-triangle" class="w-3 h-3 inline mr-1"></i>
                                                        ${device.vulnerabilities} vulnerabilities found
                                                    </div>
                                                ` : ''}
                                            </div>
                                        `).join('')}
                                    </div>
                                </div>
                            ` : '<div class="text-sm text-gray-500">No devices found on network</div>'}
                            
                            ${data.vulnerabilities && data.vulnerabilities.length > 0 ? `
                                <div class="space-y-2">
                                    <h3 class="text-sm font-medium text-gray-900">Security Issues Found</h3>
                                    <div class="space-y-2">
                                        ${data.vulnerabilities.map(vuln => `
                                            <div class="border-l-4 border-${vuln.severity === 'critical' ? 'red' : vuln.severity === 'high' ? 'orange' : 'yellow'}-500 bg-${vuln.severity === 'critical' ? 'red' : vuln.severity === 'high' ? 'orange' : 'yellow'}-50 p-3">
                                                <div class="flex items-start">
                                                    <i data-lucide="${vuln.severity === 'critical' ? 'alert-circle' : vuln.severity === 'high' ? 'alert-triangle' : 'info'}" class="w-4 h-4 text-${vuln.severity === 'critical' ? 'red' : vuln.severity === 'high' ? 'orange' : 'yellow'}-600 mr-2 mt-0.5"></i>
                                                    <div class="flex-1">
                                                        <div class="text-sm font-medium text-${vuln.severity === 'critical' ? 'red' : vuln.severity === 'high' ? 'orange' : 'yellow'}-800">
                                                            ${vuln.service} (Port ${vuln.port})
                                                        </div>
                                                        <div class="text-xs text-${vuln.severity === 'critical' ? 'red' : vuln.severity === 'high' ? 'orange' : 'yellow'}-700 mt-1">
                                                            ${vuln.description}
                                                        </div>
                                                        <div class="text-xs text-${vuln.severity === 'critical' ? 'red' : vuln.severity === 'high' ? 'orange' : 'yellow'}-600 mt-1">
                                                            💡 ${vuln.recommendation}
                                                        </div>
                                                    </div>
                                                </div>
                                            </div>
                                        `).join('')}
                                    </div>
                                </div>
                            ` : ''}
                            
                            ${data.recommendations && data.recommendations.length > 0 ? `
                                <div class="space-y-2">
                                    <h3 class="text-sm font-medium text-gray-900">Security Recommendations</h3>
                                    <div class="space-y-2">
                                        ${data.recommendations.map(rec => `
                                            <div class="bg-blue-50 border border-blue-200 rounded-md p-3">
                                                <div class="flex items-start">
                                                    <i data-lucide="shield-check" class="w-4 h-4 text-blue-600 mr-2 mt-0.5"></i>
                                                    <div class="text-sm text-blue-800">${rec}</div>
                                                </div>
                                            </div>
                                        `).join('')}
                                    </div>
                                </div>
                            ` : ''}
                            
                            <div class="text-xs text-gray-500 mt-4">
                                Scan completed at: ${new Date(data.scan_time).toLocaleString()}
                            </div>
                        </div>
                    `;
                    resultsDiv.classList.remove('hidden');
                    lucide.createIcons();
                    
                    // Update dashboard if needed
                    if (typeof loadDashboard === 'function') {
                        loadDashboard();
                    }
                    
                } catch (error) {
                    console.error('Scan error:', error);
                    resultsDiv.innerHTML = `
                        <div class="mt-4">
                            <div class="bg-red-50 border border-red-200 rounded-md p-3">
                                <div class="flex items-center">
                                    <i data-lucide="x-circle" class="w-5 h-5 text-red-600 mr-2"></i>
                                    <span class="text-sm font-medium text-red-800">Scan failed</span>
                                </div>
                                <div class="mt-2 text-sm text-red-700">
                                    ${error.message}
                                </div>
                            </div>
                        </div>
                    `;
                    resultsDiv.classList.remove('hidden');
                    lucide.createIcons();
                } finally {
                    button.disabled = false;
                    button.innerHTML = originalText;
                    lucide.createIcons();
                }
            }

            // Load devices
            async function loadDevices() {
                try {
                    const response = await fetch('/api/devices');
                    const devices = await response.json();
                    
                    const deviceList = document.getElementById('deviceList');
                    deviceList.innerHTML = devices.map(device => `
                        <div class="flex items-center justify-between p-3 border border-gray-200 rounded-md">
                            <div class="flex items-center">
                                <i data-lucide="smartphone" class="w-5 h-5 text-blue-600 mr-3"></i>
                                <div>
                                    <div class="text-sm font-medium">${device.name}</div>
                                    <div class="text-xs text-gray-500">${device.ip} • Connected ${device.last_seen}</div>
                                </div>
                            </div>
                            <span class="text-xs bg-${device.status === 'trusted' ? 'green' : 'yellow'}-100 text-${device.status === 'trusted' ? 'green' : 'yellow'}-800 px-2 py-1 rounded">
                                ${device.status}
                            </span>
                        </div>
                    `).join('');
                    
                    lucide.createIcons();
                } catch (error) {
                    console.error('Error loading devices:', error);
                }
            }

            // Load alerts
            async function loadAlerts() {
                try {
                    const response = await fetch('/api/alerts');
                    const alerts = await response.json();
                    
                    const alertsList = document.getElementById('alertsList');
                    alertsList.innerHTML = alerts.map(alert => `
                        <div class="border-l-4 border-${alert.level === 'critical' ? 'red' : alert.level === 'warning' ? 'yellow' : 'blue'}-500 bg-${alert.level === 'critical' ? 'red' : alert.level === 'warning' ? 'yellow' : 'blue'}-50 p-4">
                            <div class="flex items-center">
                                <i data-lucide="${alert.level === 'critical' ? 'alert-circle' : alert.level === 'warning' ? 'alert-triangle' : 'info'}" class="w-5 h-5 text-${alert.level === 'critical' ? 'red' : alert.level === 'warning' ? 'yellow' : 'blue'}-600 mr-2"></i>
                                <div class="flex-1">
                                    <h3 class="text-sm font-medium text-${alert.level === 'critical' ? 'red' : alert.level === 'warning' ? 'yellow' : 'blue'}-800">${alert.title}</h3>
                                    <div class="mt-1 text-sm text-${alert.level === 'critical' ? 'red' : alert.level === 'warning' ? 'yellow' : 'blue'}-700">
                                        ${alert.message}
                                    </div>
                                    <div class="mt-2 text-xs text-${alert.level === 'critical' ? 'red' : alert.level === 'warning' ? 'yellow' : 'blue'}-600">
                                        ${alert.time} • ${alert.ip}
                                    </div>
                                </div>
                            </div>
                        </div>
                    `).join('');
                    
                    lucide.createIcons();
                } catch (error) {
                    console.error('Error loading alerts:', error);
                }
            }

            // Initialize dashboard on load
            document.addEventListener('DOMContentLoaded', function() {
                loadDashboard();
            });

            // Simulate real-time updates
            setInterval(() => {
                const scoreEl = document.getElementById('security-score');
                if (scoreEl && Math.random() > 0.8) {
                    const currentScore = parseInt(scoreEl.textContent);
                    const newScore = Math.max(60, Math.min(100, currentScore + Math.floor(Math.random() * 5) - 2));
                    scoreEl.textContent = newScore;
                }
            }, 10000);
        </script>
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


@app.get("/api/network/test")
async def test_scan():
    """Test endpoint to verify JSON response works"""
    return {
        "status": "test",
        "message": "JSON response test",
        "timestamp": datetime.now().isoformat()
    }


@app.get("/api/network/scan")
async def scan_network(network_range: str = "192.168.1.0/24"):
    """Perform real security scan of network"""
    try:
        print(f"Starting security scan for network: {network_range}")
        
        # Perform real security scan
        scan_results = await scanner.scan_network_security(network_range)
        
        print(f"Scan results: {scan_results}")
        
        if 'error' in scan_results:
            return {
                "status": "error",
                "error": scan_results['error'],
                "scan_time": scan_results.get('scan_time')
            }
        
        # Format results for UI
        devices = []
        for device in scan_results['devices']:
            device_info = {
                "ip": device['ip'],
                "hostname": device.get('hostname', device['ip']),
                "type": device.get('security_level', 'unknown'),
                "ports": [port['port'] for port in device.get('open_ports', [])],
                "services": device.get('services', []),
                "vulnerabilities": len(device.get('vulnerabilities', [])),
                "security_level": device.get('security_level', 'unknown')
            }
            devices.append(device_info)
        
        result = {
            "status": "completed",
            "scan_time": scan_results['scan_time'],
            "network_range": scan_results['network_range'],
            "devices": devices,
            "open_ports": sum(len(device.get('open_ports', [])) for device in scan_results['devices']),
            "vulnerabilities": scan_results['vulnerabilities'],
            "security_score": scan_results['security_score'],
            "recommendations": scan_results['recommendations']
        }
        
        print(f"Returning result: {result}")
        return result
        
    except Exception as e:
        print(f"Network scan error: {str(e)}")
        import traceback
        traceback.print_exc()
        return {
            "status": "error",
            "error": str(e),
            "scan_time": datetime.now().isoformat()
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
