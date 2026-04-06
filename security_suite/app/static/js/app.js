// Initialize Lucide icons
lucide.createIcons();

// Section navigation
function showSection(sectionId) {
    // Hide all sections
    const sections = ['dashboard', 'network', 'devices', 'alerts', 'settings'];
    sections.forEach(id => {
        const section = document.getElementById(id);
        if (section) {
            section.classList.add('hidden');
        }
    });
    
    // Show selected section
    const selectedSection = document.getElementById(sectionId);
    if (selectedSection) {
        selectedSection.classList.remove('hidden');
    }
    
    // Update navigation buttons
    const buttons = document.querySelectorAll('nav button');
    buttons.forEach(button => {
        button.classList.remove('text-white', 'bg-blue-600');
        button.classList.add('text-gray-700', 'hover:text-gray-900', 'hover:bg-gray-100');
    });
    
    event.target.classList.remove('text-gray-700', 'hover:text-gray-900', 'hover:bg-gray-100');
    event.target.classList.add('text-white', 'bg-blue-600');
    
    // Initialize section-specific content
    if (sectionId === 'dashboard') {
        initializeDashboard();
    } else if (sectionId === 'network') {
        initializeNetwork();
    } else if (sectionId === 'devices') {
        initializeDevices();
    } else if (sectionId === 'alerts') {
        initializeAlerts();
    }
}

// Dashboard initialization
function initializeDashboard() {
    // Initialize security chart
    const ctx = document.getElementById('securityChart');
    if (ctx && !ctx.chart) {
        ctx.chart = new Chart(ctx, {
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
                    y: {
                        beginAtZero: true,
                        max: 100
                    }
                }
            }
        });
    }
}

// Network section
function initializeNetwork() {
    // Placeholder for network initialization
}

function startNetworkScan() {
    const button = event.target;
    button.disabled = true;
    button.innerHTML = '<i data-lucide="loader" class="w-4 h-4 inline mr-2 animate-spin"></i>Scanning...';
    lucide.createIcons();
    
    // Simulate network scan
    setTimeout(() => {
        const resultsDiv = document.getElementById('scanResults');
        resultsDiv.innerHTML = `
            <div class="mt-4 space-y-3">
                <div class="bg-green-50 border border-green-200 rounded-md p-3">
                    <div class="flex items-center">
                        <i data-lucide="check-circle" class="w-5 h-5 text-green-600 mr-2"></i>
                        <span class="text-sm font-medium text-green-800">Scan completed successfully</span>
                    </div>
                    <div class="mt-2 text-sm text-green-700">
                        Found 12 devices, 3 open ports detected
                    </div>
                </div>
                <div class="grid grid-cols-1 md:grid-cols-2 gap-3">
                    <div class="border border-gray-200 rounded-md p-3">
                        <div class="flex items-center justify-between">
                            <span class="text-sm font-medium">192.168.1.1</span>
                            <span class="text-xs bg-green-100 text-green-800 px-2 py-1 rounded">Router</span>
                        </div>
                        <div class="text-xs text-gray-500 mt-1">Ports: 22, 80, 443</div>
                    </div>
                    <div class="border border-gray-200 rounded-md p-3">
                        <div class="flex items-center justify-between">
                            <span class="text-sm font-medium">192.168.1.100</span>
                            <span class="text-xs bg-blue-100 text-blue-800 px-2 py-1 rounded">Desktop</span>
                        </div>
                        <div class="text-xs text-gray-500 mt-1">Ports: 22, 80, 443, 8080</div>
                    </div>
                </div>
            </div>
        `;
        resultsDiv.classList.remove('hidden');
        lucide.createIcons();
        
        button.disabled = false;
        button.innerHTML = '<i data-lucide="search" class="w-4 h-4 inline mr-2"></i>Start Network Scan';
    }, 3000);
}

// Devices section
function initializeDevices() {
    const deviceList = document.getElementById('deviceList');
    if (deviceList.children.length === 0) {
        deviceList.innerHTML = `
            <div class="space-y-3">
                <div class="flex items-center justify-between p-3 border border-gray-200 rounded-md">
                    <div class="flex items-center">
                        <i data-lucide="smartphone" class="w-5 h-5 text-blue-600 mr-3"></i>
                        <div>
                            <div class="text-sm font-medium">iPhone 13</div>
                            <div class="text-xs text-gray-500">192.168.1.105 • Connected 2 hours ago</div>
                        </div>
                    </div>
                    <span class="text-xs bg-green-100 text-green-800 px-2 py-1 rounded">Trusted</span>
                </div>
                <div class="flex items-center justify-between p-3 border border-gray-200 rounded-md">
                    <div class="flex items-center">
                        <i data-lucide="laptop" class="w-5 h-5 text-gray-600 mr-3"></i>
                        <div>
                            <div class="text-sm font-medium">MacBook Pro</div>
                            <div class="text-xs text-gray-500">192.168.1.102 • Connected 5 hours ago</div>
                        </div>
                    </div>
                    <span class="text-xs bg-green-100 text-green-800 px-2 py-1 rounded">Trusted</span>
                </div>
                <div class="flex items-center justify-between p-3 border border-gray-200 rounded-md">
                    <div class="flex items-center">
                        <i data-lucide="tv" class="w-5 h-5 text-purple-600 mr-3"></i>
                        <div>
                            <div class="text-sm font-medium">Samsung TV</div>
                            <div class="text-xs text-gray-500">192.168.1.108 • Connected 1 day ago</div>
                        </div>
                    </div>
                    <span class="text-xs bg-yellow-100 text-yellow-800 px-2 py-1 rounded">Unknown</span>
                </div>
            </div>
        `;
        lucide.createIcons();
    }
}

// Alerts section
function initializeAlerts() {
    const alertsList = document.getElementById('alertsList');
    if (alertsList.children.length === 0) {
        alertsList.innerHTML = `
            <div class="space-y-3">
                <div class="border-l-4 border-red-500 bg-red-50 p-4">
                    <div class="flex items-center">
                        <i data-lucide="alert-circle" class="w-5 h-5 text-red-600 mr-2"></i>
                        <div class="flex-1">
                            <h3 class="text-sm font-medium text-red-800">Critical Security Alert</h3>
                            <div class="mt-1 text-sm text-red-700">
                                Unusual login attempt detected from unknown IP address
                            </div>
                            <div class="mt-2 text-xs text-red-600">
                                10 minutes ago • 192.168.1.200
                            </div>
                        </div>
                    </div>
                </div>
                <div class="border-l-4 border-yellow-500 bg-yellow-50 p-4">
                    <div class="flex items-center">
                        <i data-lucide="alert-triangle" class="w-5 h-5 text-yellow-600 mr-2"></i>
                        <div class="flex-1">
                            <h3 class="text-sm font-medium text-yellow-800">Warning</h3>
                            <div class="mt-1 text-sm text-yellow-700">
                                Device connected without authentication
                            </div>
                            <div class="mt-2 text-xs text-yellow-600">
                                1 hour ago • 192.168.1.150
                            </div>
                        </div>
                    </div>
                </div>
                <div class="border-l-4 border-blue-500 bg-blue-50 p-4">
                    <div class="flex items-center">
                        <i data-lucide="info" class="w-5 h-5 text-blue-600 mr-2"></i>
                        <div class="flex-1">
                            <h3 class="text-sm font-medium text-blue-800">Information</h3>
                            <div class="mt-1 text-sm text-blue-700">
                                New device joined the network
                            </div>
                            <div class="mt-2 text-xs text-blue-600">
                                2 hours ago • 192.168.1.105
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        `;
        lucide.createIcons();
    }
}

// Initialize dashboard on load
document.addEventListener('DOMContentLoaded', function() {
    initializeDashboard();
});

// Simulate real-time updates
setInterval(() => {
    // Update security score occasionally
    const scoreElement = document.querySelector('.text-3xl.font-bold');
    if (scoreElement && Math.random() > 0.8) {
        const currentScore = parseInt(scoreElement.textContent);
        const newScore = Math.max(60, Math.min(100, currentScore + Math.floor(Math.random() * 5) - 2));
        scoreElement.textContent = newScore;
        
        // Update ring color based on score
        const ring = document.querySelector('.security-score-ring');
        if (newScore >= 80) {
            ring.setAttribute('stroke', '#10b981'); // green
        } else if (newScore >= 60) {
            ring.setAttribute('stroke', '#f59e0b'); // yellow
        } else {
            ring.setAttribute('stroke', '#ef4444'); // red
        }
        
        // Update ring stroke-dashoffset
        const circumference = 2 * Math.PI * 56;
        const offset = circumference - (newScore / 100) * circumference;
        ring.setAttribute('stroke-dashoffset', offset);
    }
}, 10000);
