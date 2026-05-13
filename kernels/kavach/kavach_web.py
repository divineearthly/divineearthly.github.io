from flask import Flask, render_template_string, request
import kavach_core

app = Flask(__name__)
kavach = kavach_core.KAVACH()

HTML = """<!DOCTYPE html>
<html><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>KAVACH — Cyber Defense</title>
<style>
body{font-family:system-ui;background:#06060f;color:#d0d0e0;padding:20px;text-align:center}
h1{color:#e94560;font-size:32px}
.card{background:#0d0d20;border:1px solid #1a1a3a;border-radius:14px;padding:20px;margin:16px auto;max-width:650px;text-align:left}
h3{color:#f0b040}pre{background:#000;padding:14px;border-radius:8px;font-size:12px;color:#4ecca3;overflow-x:auto}
.clean{color:#4ecca3}.threat{color:#e94560}textarea{width:100%;padding:12px;background:#1a1a3a;color:#fff;border:1px solid #2a2a5a;border-radius:8px;font-size:14px;min-height:80px;resize:vertical}
button{width:100%;padding:14px;background:#e94560;color:#fff;border:none;border-radius:8px;font-weight:700;font-size:16px;cursor:pointer;margin-top:8px}
</style></head><body>
<h1>🔴 KAVACH</h1>
<p>Sovereign Cyber Defense Intelligence — Vedic Sutras Based</p>
""" + f"""
<div class="card"><h3>Defense Status</h3><pre>Total Incidents: {len(kavach.audit_log)}
Status: ACTIVE SHIELD 🛡️</pre></div>
""" + """
<div class="card"><h3>Scan Input</h3>
<form method="POST"><textarea name="data" placeholder="Paste any text, code, or log to scan for threats...">""" + (request.form.get('data', '') if request.method == 'POST' else '') + """</textarea>
<button>🔍 Scan for Threats</button></form></div>
""" + (f"""<div class="card"><h3>Scan Result</h3><pre>{chr(10).join([f"{'⚠️' if t['severity'] in ['CRITICAL','HIGH'] else 'ℹ️'} {t['severity']}: {t['type']}" for t in kavach.scan(request.form.get('data',''))] if request.method == 'POST' and request.form.get('data') else []) or 'Enter data and click Scan'}</pre></div>""" if request.method == 'POST' else "") + """
<p><a href="https://divineearthly.github.io" style="color:#f0b040">Divine Earthly Hub</a></p>
</body></html>"""

@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template_string(HTML)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=7860)
