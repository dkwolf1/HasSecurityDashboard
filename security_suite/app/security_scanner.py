import socket
import ssl
import subprocess
import ipaddress
from datetime import datetime, timedelta
from typing import List, Dict, Any
import asyncio
import json
import re

class SecurityScanner:
    def __init__(self):
        self.security_ports = {
            21: 'FTP - Often unencrypted',
            22: 'SSH - Check for weak passwords',
            23: 'Telnet - Unencrypted protocol',
            25: 'SMTP - Check for open relay',
            53: 'DNS - Potential DNS poisoning',
            80: 'HTTP - Unencrypted web traffic',
            110: 'POP3 - Unencrypted email',
            135: 'Windows RPC - Potential exploits',
            139: 'NetBIOS - Windows sharing',
            143: 'IMAP - Unencrypted email',
            443: 'HTTPS - Verify SSL/TLS',
            445: 'SMB - Potential exploits',
            993: 'IMAPS - Encrypted email',
            995: 'POP3S - Encrypted email',
            1433: 'MSSQL - Database access',
            1521: 'Oracle - Database access',
            3306: 'MySQL - Database access',
            3389: 'RDP - Remote desktop',
            5432: 'PostgreSQL - Database access',
            5900: 'VNC - Remote desktop',
            8080: 'HTTP-Alt - Web services',
            8443: 'HTTPS-Alt - Web services'
        }
        
    async def scan_network_security(self, network_range: str = "192.168.1.0/24") -> Dict[str, Any]:
        """Perform comprehensive security scan of network"""
        try:
            print(f"Starting security scan for network: {network_range}")
            
            results = {
                'scan_time': datetime.now().isoformat(),
                'network_range': network_range,
                'devices': [],
                'vulnerabilities': [],
                'security_score': 100,
                'recommendations': []
            }
            
            # Discover hosts using simple ping sweep
            hosts = await self._discover_hosts(network_range)
            print(f"Found {len(hosts)} hosts: {hosts}")
            
            # Scan each host for security issues
            for host in hosts:
                print(f"Scanning host: {host}")
                host_result = await self._scan_host_security(host)
                results['devices'].append(host_result)
                results['vulnerabilities'].extend(host_result.get('vulnerabilities', []))
            
            # Calculate security score
            results['security_score'] = self._calculate_security_score(results['vulnerabilities'])
            results['recommendations'] = self._generate_recommendations(results['vulnerabilities'])
            
            print(f"Scan completed. Security score: {results['security_score']}")
            return results
            
        except Exception as e:
            print(f"Scan error: {str(e)}")
            return {'error': str(e), 'scan_time': datetime.now().isoformat()}
    
    async def _discover_hosts(self, network_range: str) -> List[str]:
        """Discover active hosts on network using ping"""
        try:
            network = ipaddress.ip_network(network_range)
            hosts = []
            
            # Limit to first 20 IPs to avoid long scans
            ip_list = list(network.hosts())[:20]
            
            for ip in ip_list:
                try:
                    # Simple ping check
                    proc = await asyncio.create_subprocess_exec(
                        'ping', '-c', '1', '-W', '1', str(ip),
                        stdout=asyncio.subprocess.DEVNULL,
                        stderr=asyncio.subprocess.DEVNULL
                    )
                    await proc.wait()
                    
                    if proc.returncode == 0:
                        hosts.append(str(ip))
                        print(f"Host found: {ip}")
                except Exception as e:
                    print(f"Ping error for {ip}: {e}")
                    continue
            
            return hosts
        except Exception as e:
            print(f"Host discovery error: {e}")
            return []
    
    async def _scan_host_security(self, host: str) -> Dict[str, Any]:
        """Perform security scan on individual host"""
        host_info = {
            'ip': host,
            'hostname': self._resolve_hostname(host),
            'open_ports': [],
            'vulnerabilities': [],
            'services': [],
            'security_level': 'unknown'
        }
        
        try:
            print(f"Scanning ports on {host}")
            
            # Simple port scan for common ports
            common_ports = [21, 22, 23, 25, 53, 80, 110, 135, 139, 143, 443, 445, 993, 995, 1433, 1521, 3306, 3389, 5432, 5900, 8080, 8443]
            
            for port in common_ports:
                if await self._is_port_open(host, port):
                    service_info = {
                        'port': port,
                        'protocol': 'tcp',
                        'state': 'open',
                        'service': self._guess_service(port),
                        'version': '',
                        'security_risk': self._assess_port_security(port)
                    }
                    host_info['open_ports'].append(service_info)
                    host_info['services'].append(service_info['service'])
                    
                    # Check for vulnerabilities
                    vulns = self._check_port_vulnerabilities(port, host)
                    host_info['vulnerabilities'].extend(vulns)
                    
                    print(f"Port {port} open on {host} - {service_info['service']}")
            
            # SSL/TLS certificate analysis for HTTPS ports
            if any(port in [443, 8443] for port_info in host_info['open_ports'] for port_info in [port_info] if port_info['port'] == port_info['port']):
                ssl_vulns = await self._analyze_ssl_certificates(host)
                host_info['vulnerabilities'].extend(ssl_vulns)
            
            # Determine security level
            host_info['security_level'] = self._determine_security_level(host_info['vulnerabilities'])
            
            print(f"Host {host} security level: {host_info['security_level']}")
            
        except Exception as e:
            print(f"Host scan error for {host}: {e}")
            host_info['error'] = str(e)
        
        return host_info
    
    async def _is_port_open(self, host: str, port: int) -> bool:
        """Check if port is open"""
        try:
            future = asyncio.open_connection(host, port)
            reader, writer = await asyncio.wait_for(future, timeout=2)
            writer.close()
            await writer.wait_closed()
            return True
        except:
            return False
    
    def _guess_service(self, port: int) -> str:
        """Guess service based on port number"""
        service_map = {
            21: 'ftp', 22: 'ssh', 23: 'telnet', 25: 'smtp', 53: 'dns',
            80: 'http', 110: 'pop3', 135: 'rpc', 139: 'netbios', 143: 'imap',
            443: 'https', 445: 'smb', 993: 'imaps', 995: 'pop3s',
            1433: 'mssql', 1521: 'oracle', 3306: 'mysql', 3389: 'rdp',
            5432: 'postgresql', 5900: 'vnc', 8080: 'http-alt', 8443: 'https-alt'
        }
        return service_map.get(port, 'unknown')
    
    def _resolve_hostname(self, ip: str) -> str:
        """Resolve hostname from IP"""
        try:
            hostname = socket.gethostbyaddr(ip)[0]
            return hostname
        except:
            return ip
    
    def _assess_port_security(self, port: int) -> str:
        """Assess security risk of open port"""
        if port in self.security_ports:
            risk_desc = self.security_ports[port]
            
            # High risk ports
            if port in [21, 23, 135, 139, 445]:
                return f'HIGH RISK: {risk_desc}'
            
            # Medium risk ports
            elif port in [25, 53, 80, 110, 143, 3389, 5900]:
                return f'MEDIUM RISK: {risk_desc}'
            
            # Low risk (but still check)
            else:
                return f'LOW RISK: {risk_desc}'
        
        return 'UNKNOWN SERVICE'
    
    def _check_port_vulnerabilities(self, port: int, host: str) -> List[Dict]:
        """Check for specific vulnerabilities on port"""
        vulnerabilities = []
        
        # Check for default credentials on common services
        if port == 22:
            vulnerabilities.append({
                'type': 'weak_authentication',
                'severity': 'medium',
                'port': port,
                'service': 'SSH',
                'description': 'SSH service detected - verify strong passwords and disable root login',
                'recommendation': 'Use key-based authentication, disable password auth, change default port'
            })
        
        elif port == 80:
            vulnerabilities.append({
                'type': 'unencrypted_protocol',
                'severity': 'high',
                'port': port,
                'service': 'HTTP',
                'description': 'Unencrypted HTTP traffic detected',
                'recommendation': 'Redirect to HTTPS, implement HSTS, use secure cookies'
            })
        
        elif port in [21, 23]:
            vulnerabilities.append({
                'type': 'insecure_protocol',
                'severity': 'critical',
                'port': port,
                'service': self._guess_service(port),
                'description': f'Insecure protocol {self._guess_service(port)} detected',
                'recommendation': 'Disable protocol, use encrypted alternatives (SFTP, SSH, HTTPS)'
            })
        
        elif port == 3389:
            vulnerabilities.append({
                'type': 'remote_desktop',
                'severity': 'high',
                'port': port,
                'service': 'RDP',
                'description': 'Remote Desktop Protocol exposed',
                'recommendation': 'Use VPN access, enable Network Level Authentication, use strong passwords'
            })
        
        elif port in [3306, 5432, 1433, 1521]:
            vulnerabilities.append({
                'type': 'database_exposure',
                'severity': 'critical',
                'port': port,
                'service': self._guess_service(port),
                'description': f'Database service {self._guess_service(port)} exposed to network',
                'recommendation': 'Restrict database access to localhost, use firewall rules, implement strong authentication'
            })
        
        return vulnerabilities
    
    async def _analyze_ssl_certificates(self, host: str) -> List[Dict]:
        """Analyze SSL/TLS certificates for security issues"""
        vulnerabilities = []
        
        try:
            print(f"Analyzing SSL certificate for {host}:443")
            
            # Check HTTPS certificate
            context = ssl.create_default_context()
            context.check_hostname = False
            context.verify_mode = ssl.CERT_NONE
            
            # Use socket with timeout
            with socket.create_connection((host, 443), timeout=5) as sock:
                with context.wrap_socket(sock, server_hostname=host) as ssock:
                    cert = ssock.getpeercert()
                    
                    if cert:
                        # Check certificate expiration
                        not_after = cert.get('notAfter', '')
                        if not_after:
                            # Parse date format from SSL cert
                            try:
                                date_str = not_after.replace(' GMT', '')
                                expiry_date = datetime.strptime(date_str, '%b %d %H:%M:%S %Y')
                                
                                if expiry_date < datetime.now():
                                    vulnerabilities.append({
                                        'type': 'expired_certificate',
                                        'severity': 'critical',
                                        'service': 'HTTPS',
                                        'description': f'SSL certificate expired on {expiry_date}',
                                        'recommendation': 'Renew SSL certificate immediately'
                                    })
                                
                                elif expiry_date < datetime.now() + timedelta(days=30):
                                    vulnerabilities.append({
                                        'type': 'expiring_certificate',
                                        'severity': 'medium',
                                        'service': 'HTTPS',
                                        'description': f'SSL certificate expires on {expiry_date}',
                                        'recommendation': 'Renew SSL certificate soon'
                                    })
                                
                                else:
                                    print(f"SSL certificate valid until {expiry_date}")
                                    
                            except ValueError as e:
                                print(f"Could not parse certificate date: {e}")
                        
                        # Check cipher
                        cipher = ssock.cipher()
                        if cipher and ('RC4' in str(cipher) or 'MD5' in str(cipher)):
                            vulnerabilities.append({
                                'type': 'weak_encryption',
                                'severity': 'high',
                                'service': 'HTTPS',
                                'description': f'Weak cipher suite detected: {cipher}',
                                'recommendation': 'Configure server to use strong cipher suites only'
                            })
                    else:
                        print("No certificate found")
        
        except Exception as e:
            print(f"SSL analysis error for {host}: {e}")
            vulnerabilities.append({
                'type': 'ssl_error',
                'severity': 'medium',
                'service': 'HTTPS',
                'description': f'SSL/TLS configuration issue: {str(e)}',
                'recommendation': 'Check SSL certificate and configuration'
            })
        
        return vulnerabilities
    
    def _determine_security_level(self, vulnerabilities: List[Dict]) -> str:
        """Determine overall security level based on vulnerabilities"""
        if not vulnerabilities:
            return 'secure'
        
        critical_count = len([v for v in vulnerabilities if v['severity'] == 'critical'])
        high_count = len([v for v in vulnerabilities if v['severity'] == 'high'])
        
        if critical_count > 0:
            return 'critical'
        elif high_count > 2:
            return 'high_risk'
        elif high_count > 0:
            return 'medium_risk'
        else:
            return 'low_risk'
    
    def _calculate_security_score(self, vulnerabilities: List[Dict]) -> int:
        """Calculate overall security score (0-100)"""
        if not vulnerabilities:
            return 100
        
        score = 100
        
        # Deduct points based on severity
        for vuln in vulnerabilities:
            if vuln['severity'] == 'critical':
                score -= 25
            elif vuln['severity'] == 'high':
                score -= 15
            elif vuln['severity'] == 'medium':
                score -= 10
            elif vuln['severity'] == 'low':
                score -= 5
        
        return max(0, score)
    
    def _generate_recommendations(self, vulnerabilities: List[Dict]) -> List[str]:
        """Generate security recommendations based on vulnerabilities"""
        recommendations = []
        
        # Group vulnerabilities by type
        types = {}
        for vuln in vulnerabilities:
            vuln_type = vuln['type']
            if vuln_type not in types:
                types[vuln_type] = []
            types[vuln_type].append(vuln)
        
        # Generate recommendations for each type
        if 'insecure_protocol' in types:
            recommendations.append("DISABLE INSECURE PROTOCOLS: Disable Telnet, FTP, and other unencrypted protocols. Use SSH, SFTP, HTTPS instead.")
        
        if 'unencrypted_protocol' in types:
            recommendations.append("IMPLEMENT HTTPS: Redirect all HTTP traffic to HTTPS. Implement HSTS and secure cookies.")
        
        if 'weak_authentication' in types:
            recommendations.append("STRENGTHEN AUTHENTICATION: Use key-based authentication for SSH, implement strong password policies, enable 2FA where possible.")
        
        if 'database_exposure' in types:
            recommendations.append("SECURE DATABASES: Restrict database access to localhost only. Use firewall rules to block external access.")
        
        if 'expired_certificate' in types or 'expiring_certificate' in types:
            recommendations.append("UPDATE SSL CERTIFICATES: Renew expired or expiring SSL certificates. Use automated renewal.")
        
        if 'weak_encryption' in types:
            recommendations.append("UPGRADE ENCRYPTION: Disable weak cipher suites. Use TLS 1.2+ and strong encryption algorithms.")
        
        if 'remote_desktop' in types:
            recommendations.append("SECURE REMOTE ACCESS: Use VPN for remote desktop access. Enable Network Level Authentication and strong passwords.")
        
        return recommendations

# Global scanner instance
scanner = SecurityScanner()
