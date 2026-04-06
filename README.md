# HasSecurityDash

Security control for Home Assistant OS 2026.4

## Features

### 🎯 Dashboard & Overview
- **Security Score Ring** - Visual security status indicator (0-100)
- **Real-time Statistics** - Active devices, open ports, secured services, threat count
- **Security Trend Chart** - Historical security data visualization
- **Recent Activity Timeline** - Live security events and notifications
- **Color-coded Status** - Green/Yellow/Red threat levels

### 🔍 Network Security
- **Network Scanner** - LAN device discovery and port scanning
- **Open Port Detection** - Identify vulnerable network services
- **Network Topology Mapping** - Visual network structure overview
- **Intrusion Detection** - Monitor for unusual network activity

### 📱 Device Management
- **Device Discovery** - Automatic detection of connected devices
- **Device Classification** - Router, desktop, mobile, IoT devices
- **Trust Management** - Mark devices as trusted/unknown/threatening
- **Connection History** - Track when devices join/leave network
- **Device Fingerprinting** - Identify device types and manufacturers

### 🚨 Security Alerts
- **Real-time Notifications** - Instant security threat warnings
- **Alert Prioritization** - Critical, Warning, Info levels
- **Threat Intelligence** - Automated security analysis
- **Custom Alert Rules** - Configure your own security triggers
- **Email/Push Notifications** - Integration with notification systems

### 🔐 Password & Authentication
- **Password Strength Checker** - Analyze Home Assistant account security
- **Authentication Monitoring** - Track login attempts and failures
- **Multi-factor Authentication** - MFA status and recommendations
- **User Account Audit** - Review all Home Assistant users

### 🏠 Home Assistant Integration
- **Entity Security Monitoring** - Check automation security
- **Integration Scanner** - Audit third-party integrations
- **Configuration Analysis** - Review HA settings for vulnerabilities
- **Automation Security** - Check for unsafe automations
- **Backup Security** - Monitor backup encryption and access

### 📊 Logging & Reporting
- **Security Event Log** - Complete audit trail of all security events
- **Export Reports** - Generate PDF/CSV security reports
- **Historical Analytics** - Long-term security trend analysis
- **Compliance Reports** - Security compliance documentation

### ⚙️ Configuration & Settings
- **Scan Frequency Control** - Configure automated scan intervals
- **Alert Threshold Settings** - Customize sensitivity levels
- **Network Configuration** - Set scan ranges and exclusions
- **User Preferences** - Language, notifications, dashboard layout
- **API Access Control** - Manage external API access

## Installation

1. Add this repository to Home Assistant:
   - Settings → Add-ons → Add-on Store → Three dots → Add repository
   - Enter: `https://github.com/dkwolf1/HasSecurityDash`

2. Install "Security Suite" from the store

3. Configure the add-on with your preferred settings

## Requirements

- Home Assistant OS 2026.4+
- Host network access enabled
- Read/write access to Home Assistant configuration

## Architecture

- **Frontend**: Modern responsive web interface with TailwindCSS
- **Backend**: FastAPI with Python 3
- **Database**: SQLite for local data storage
- **Container**: Docker-based deployment

## Security & Privacy

- All security analysis runs locally on your Home Assistant
- No data is transmitted to external services
- Full control over what gets monitored and logged
- Open source for complete transparency

## Contributing

Contributions are welcome! Please feel free to submit pull requests or open issues for bugs and feature requests.

## License

This project is licensed under the MIT License - see the LICENSE file for details.
