from flask import Flask, request, redirect, url_for, session, render_template_string, flash, jsonify
from flask_cors import CORS
from datetime import datetime

app = Flask(__name__)
app.secret_key = "AquaShield_AI_2026"
CORS(app)  # Enables cross-origin requests for citizen complaint form submission

# Sample Initial Incidents Data
INCIDENTS = [
    {"id":1,"location":"MG Road Junction","water":46,"department":"Traffic Department","status":"Road Restricted","risk":"HIGH","description":"Heavy water accumulation. Traffic should be avoided.","officer":"Amit Sharma","reported":"11:10 AM"},
    {"id":2,"location":"Railway Underpass","water":22,"department":"Municipal Department","status":"Under Review","risk":"MEDIUM","description":"Waterlogging detected near the underpass.","officer":"Neha Verma","reported":"10:55 AM"},
    {"id":3,"location":"Bus Stand Road","water":8,"department":"Road Department","status":"Resolved","risk":"LOW","description":"Minor water accumulation.","officer":"Rohan Patel","reported":"10:20 AM"},
    {"id":4,"location":"Civil Hospital Road","water":52,"department":"Disaster Management","status":"Officer Assigned","risk":"HIGH","description":"Heavy flooding reported. Emergency access required.","officer":"Priya Singh","reported":"11:25 AM"}
]

OFFICERS = [
    {"id":1,"name":"Amit Sharma","department":"Traffic","area":"MG Road","status":"Active"},
    {"id":2,"name":"Neha Verma","department":"Municipal","area":"Railway Zone","status":"Active"},
    {"id":3,"name":"Rohan Patel","department":"Road Department","area":"Bus Stand","status":"Available"},
    {"id":4,"name":"Priya Singh","department":"Disaster Management","area":"Civil Hospital","status":"Active"}
]

WARNINGS = [
    {"location":"MG Road Junction","risk":"HIGH","message":"Avoid MG Road Junction because of dangerous flooding.","status":"Published"},
    {"location":"Civil Hospital Road","risk":"HIGH","message":"Avoid unnecessary travel on Civil Hospital Road.","status":"Published"}
]

SETTINGS = {"high":35,"medium":15,"authority":"AquaShield Authority Control Room"}

def calculate_risk(water):
    if water >= SETTINGS["high"]: return "HIGH"
    if water >= SETTINGS["medium"]: return "MEDIUM"
    return "LOW"

def next_id():
    return max([i["id"] for i in INCIDENTS], default=0) + 1

def get_incident(iid):
    return next((i for i in INCIDENTS if i["id"] == iid), None)

# ----------------- CITIZEN COMPLAINT API ENDPOINT -----------------
@app.route("/api/health", methods=["GET"])
def api_health():
    return jsonify({"service": "AquaShield Authority", "status": "healthy"})

@app.route("/api/incidents", methods=["GET"])
def get_incidents():
    """Public read-only incident feed for the Citizen portal and GIS."""
    return jsonify({
        "success": True,
        "incidents": INCIDENTS,
        "count": len(INCIDENTS)
    }), 200


@app.route("/api/public-stats", methods=["GET"])
def public_stats():
    """Live aggregate statistics for the Citizen home page."""
    total = len(INCIDENTS)
    resolved = sum(
        str(i.get("status", "")).lower() in ("resolved", "closed")
        for i in INCIDENTS
    )
    active = total - resolved
    registered = sum(
        str(i.get("status", "")).lower() not in ("resolved", "closed")
        for i in INCIDENTS
    )
    high = sum(str(i.get("risk", "")).upper() in ("HIGH", "CRITICAL") for i in INCIDENTS)
    medium = sum(str(i.get("risk", "")).upper() in ("MEDIUM", "MODERATE") for i in INCIDENTS)
    low = sum(str(i.get("risk", "")).upper() in ("LOW", "SAFE") for i in INCIDENTS)

    return jsonify({
        "success": True,
        "total": total,
        "registered": registered,
        "active": active,
        "solved": resolved,
        "high": high,
        "medium": medium,
        "low": low,
        "updated_at": datetime.now().isoformat()
    }), 200


@app.route("/api/incidents", methods=["POST"])
def receive_incident():
    data = request.get_json(silent=True) or request.form.to_dict() or {}

    location = data.get("location") or data.get("area") or "Unknown Location"
    depth = data.get("depth", "medium")
    
    raw_water = data.get("water", data.get("water_cm"))

    try:
        if raw_water not in (None, ""):
            water = int(float(raw_water))
        else:
            raise ValueError
    except (TypeError, ValueError):
        depth_map = {"low": 12, "medium": 28, "high": 55, "extreme": 85}
        water = depth_map.get(str(depth).lower(), 25)

    department = data.get("type") or data.get("department") or "Citizen Flood Complaint"
    status = "Under Review"
    description = data.get("description") or data.get("details") or "Reported by Citizen via AquaShield Complaint Portal"
    timestamp = data.get("timestamp") or data.get("reported") or datetime.now().strftime("%I:%M %p")

    incident = {
        "id": next_id(),
        "location": location,
        "water": water,
        "department": department,
        "status": status,
        "risk": calculate_risk(water),
        "description": description,
        "category": data.get("category", "Flood / Waterlogging"),
        "priority": data.get("priority", "Medium"),
        "severity": data.get("severity", "Medium"),
        "source": data.get("source", "Citizen + AquaShield AI"),
        "officer": "Unassigned",
        "reported": timestamp,
        "timestamp": datetime.now().isoformat()
    }

    INCIDENTS.insert(0, incident)

    return jsonify({
        "success": True,
        "message": "Complaint registered successfully in AquaShield System",
        "incident": incident
    }), 201

# ----------------- AUTHORITY DASHBOARD STYLES & LAYOUT -----------------
CSS = r"""
*{box-sizing:border-box}
body{margin:0;font-family:system-ui,-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,sans-serif;background:#f8fafc;color:#0f172a;font-size:15px}
a,a:hover,a:visited,a:active{text-decoration:none!important}
.sidebar{position:fixed;left:0;top:0;bottom:0;width:260px;background:#0f172a;color:#f8fafc;padding:24px 16px;overflow-y:auto;border-right:1px solid #1e293b}
.logo{display:flex;align-items:center;gap:12px;margin-bottom:32px;padding:4px;color:white}
.logo-icon{width:44px;height:44px;border-radius:12px;background:linear-gradient(135deg,#2563eb,#06b6d4);display:flex;align-items:center;justify-content:center;font-size:22px;box-shadow:0 4px 12px rgba(37,99,235,0.3)}
.logo b{font-size:18px;font-weight:700;letter-spacing:-0.5px}.logo small{display:block;font-size:11px;color:#94a3b8;margin-top:2px}
.nav-title{color:#64748b;font-size:10px;font-weight:700;margin:24px 10px 8px;letter-spacing:1px}
.nav{display:flex;align-items:center;gap:10px;padding:12px 14px;margin:4px 0;border-radius:10px;color:#94a3b8;font-size:14px;font-weight:600;transition:.2s}
.nav:hover,.nav.active{background:#2563eb;color:white}
.main{margin-left:260px}
.topbar{height:65px;background:#1e293b;color:#f8fafc;display:flex;align-items:center;justify-content:space-between;padding:0 30px;font-size:13px;border-bottom:1px solid #334155}
.online{color:#86efac;font-weight:500}.green-dot{display:inline-block;width:8px;height:8px;background:#22c55e;border-radius:50%;margin-right:8px}
.content{padding:30px;max-width:1500px;margin:auto}
.flash{background:#dcfce7;border:1px solid #bbf7d0;color:#166534;padding:14px 18px;border-radius:12px;margin-bottom:20px;font-size:14px;font-weight:500}
.heading{display:flex;justify-content:space-between;align-items:center;gap:15px;margin-bottom:24px}
.heading h1{margin:0;font-size:28px;font-weight:800;color:#0f172a;letter-spacing:-0.5px}.heading p{margin:4px 0 0;color:#64748b;font-size:14px}
.btn{display:inline-flex;align-items:center;gap:6px;border:0;border-radius:10px;padding:10px 18px;background:linear-gradient(135deg,#2563eb,#0284c7);color:white!important;font-weight:600;font-size:13px;cursor:pointer;transition:.2s;box-shadow:0 2px 8px rgba(37,99,235,0.2)}
.btn:hover{opacity:.95;transform:translateY(-1px)}.btn.red{background:#ef4444;box-shadow:none}.btn.green{background:#10b981;box-shadow:none}.btn.gray{background:#e2e8f0;color:#334155!important;box-shadow:none}
.stats{display:grid;grid-template-columns:repeat(4,1fr);gap:18px}
.card{background:white;border:1px solid #e2e8f0;border-radius:16px;padding:22px;box-shadow:0 1px 3px rgba(0,0,0,0.05)}
.card-title{color:#64748b;font-size:11px;font-weight:700;letter-spacing:0.5px}.number{font-size:32px;font-weight:800;margin:8px 0;color:#0f172a}.card-small{color:#94a3b8;font-size:12px}
.brief{margin:22px 0;padding:22px;border-radius:16px;background:linear-gradient(135deg,#0f172a,#1e293b);color:white;box-shadow:0 4px 14px rgba(15,23,42,0.15)}
.brief h3{margin:0;font-size:17px;font-weight:700}.brief p{font-size:13.5px;color:#cbd5e1;line-height:1.6;margin-top:6px}
.panel{background:white;border-radius:16px;border:1px solid #e2e8f0;overflow:hidden;margin-top:22px;box-shadow:0 1px 3px rgba(0,0,0,0.05)}
.panel-head{padding:18px 22px;border-bottom:1px solid #f1f5f9;display:flex;justify-content:space-between;align-items:center;gap:15px}
table{width:100%;border-collapse:collapse}th{background:#f8fafc;color:#64748b;text-align:left;padding:14px 18px;font-size:11px;font-weight:700;letter-spacing:0.5px}
td{padding:16px 18px;border-top:1px solid #f1f5f9;font-size:13.5px}td b{font-size:14px;color:#0f172a}
.badge{display:inline-block;padding:5px 12px;border-radius:20px;font-size:11px;font-weight:700}.high{background:#fee2e2;color:#dc2626}.medium{background:#fef3c7;color:#d97706}.low{background:#dcfce7;color:#15803d}
.action{display:flex;gap:8px;flex-wrap:wrap}
.form{padding:24px;display:grid;grid-template-columns:1fr 1fr;gap:20px}.field label{display:block;font-size:12px;font-weight:700;margin-bottom:8px;color:#475569}
input,select,textarea{width:100%;border:1px solid #cbd5e1;border-radius:10px;padding:12px 14px;font-family:inherit;font-size:14px;outline:none;background:#fff}
input:focus,select:focus,textarea:focus{border-color:#2563eb;box-shadow:0 0 0 3px rgba(37,99,235,0.15)}textarea{min-height:110px}.full{grid-column:1/-1}
.warning{background:#fff1f2;border-left:4px solid #f43f5e;padding:18px;border-radius:12px;margin:14px 0;font-size:13.5px;line-height:1.6;color:#881337}
.tiles{display:grid;grid-template-columns:repeat(3,1fr);gap:18px}.tile{background:white;padding:24px;border-radius:16px;border:1px solid #e2e8f0}.tile h3{font-size:17px;margin-top:0}.tile p{color:#64748b;font-size:13.5px;line-height:1.7}
.footer{margin-top:22px;display:grid;grid-template-columns:repeat(4,1fr);gap:14px}.footer-box{background:#1e293b;color:white;padding:18px;border-radius:12px;font-size:11px;color:#94a3b8}.footer-box b{font-size:16px;color:white}

/* ============================================================
   MOBILE RESPONSIVE FIX
   ============================================================ */
@media (max-width: 768px){
  .sidebar{position:static;width:100%;height:auto;max-height:none;padding:14px 12px;overflow:visible;border-right:0;border-bottom:1px solid #1e293b}
  .logo{margin-bottom:14px;padding:2px 4px}
  .logo-icon{width:40px;height:40px;font-size:20px}
  .logo b{font-size:16px}
  .nav-title{margin:14px 6px 6px}
  .nav{display:inline-flex;width:calc(50% - 5px);margin:3px 2px;padding:10px 9px;font-size:12px;vertical-align:top}
  .main{margin-left:0;width:100%}
  .topbar{height:auto;min-height:58px;padding:12px 15px;gap:8px;flex-wrap:wrap}
  .content{padding:16px 12px;max-width:100%;overflow:hidden}
  .heading{align-items:flex-start;flex-direction:column;margin-bottom:18px}
  .heading h1{font-size:22px;line-height:1.25}
  .heading p{font-size:12px}
  .heading .btn{width:100%;justify-content:center}
  .stats{grid-template-columns:1fr;gap:12px}
  .card{padding:16px}
  .number{font-size:28px}
  .panel{overflow:hidden}
  .panel-head{padding:14px;align-items:flex-start;flex-direction:column}
  .panel-head form{width:100%}
  .panel table{display:block;width:100%;overflow-x:auto;white-space:nowrap;-webkit-overflow-scrolling:touch}
  th{padding:11px 12px;font-size:10px}
  td{padding:12px;font-size:12px}
  .action{gap:6px}
  .action .btn{padding:8px 10px;font-size:11px}
  .form{grid-template-columns:1fr;padding:16px;gap:14px}
  .full{grid-column:auto}
  input,select,textarea{font-size:13px}
  .tiles{grid-template-columns:1fr;gap:12px}
  .tile{padding:18px}
  .footer{grid-template-columns:1fr;gap:10px}
  .footer-box{padding:14px}
  .brief{padding:16px;margin:16px 0}
}
"""

PAGE = """<!doctype html><html><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{{title}} - AquaShield AI Portal</title><style>""" + CSS + """</style></head><body>
<aside class="sidebar">
<a class="logo" href="{{url_for('dashboard')}}"><div class="logo-icon">🛡️</div><div><b>AquaShield AI</b><small>Authority Portal</small></div></a>
<a class="nav {% if page=='dashboard' %}active{% endif %}" href="{{url_for('dashboard')}}">🏠 Dashboard</a>
<div class="nav-title">OPERATIONS</div>
<a class="nav {% if page=='incidents' %}active{% endif %}" href="{{url_for('incidents')}}">🌊 Flood Incidents</a>
<a class="nav {% if page=='officers' %}active{% endif %}" href="{{url_for('officers')}}">👮 Officers</a>
<a class="nav {% if page=='warnings' %}active{% endif %}" href="{{url_for('warnings')}}">🚨 Public Warnings</a>
<a class="nav {% if page=='analytics' %}active{% endif %}" href="{{url_for('analytics')}}">📊 Analytics & Reports</a>
<div class="nav-title">SYSTEM</div>
<a class="nav {% if page=='settings' %}active{% endif %}" href="{{url_for('settings')}}">⚙️ Settings</a>
<a class="nav {% if page=='help' %}active{% endif %}" href="{{url_for('help_page')}}">❓ Help & Support</a>
</aside>
<div class="main">
<div class="topbar">
    <span>🌧️ Monsoon Response • Live Flood Intelligence System</span>
    <div style="display: flex; align-items: center; gap: 18px;">
        <span class="online"><span class="green-dot"></span>Authority Control Room Active</span>
        <span id="live-clock" style="font-weight:600;color:#cbd5e1;"></span>
        <a href="{{ url_for('logout') }}" class="btn red" style="padding: 6px 14px; font-size: 12px; text-decoration: none;">🚪 Logout</a>
    </div>
</div>
<div class="content">
{% with messages=get_flashed_messages() %}{% for message in messages %}<div class="flash">✅ {{message}}</div>{% endfor %}{% endwith %}
{{body|safe}}</div></div>
<script>
(function () {
  function updateLiveClock() {
    const el = document.getElementById("live-clock");
    if (!el) return;
    const now = new Date();
    el.textContent = "🕒 " + now.toLocaleTimeString("en-IN", {
      hour: "2-digit",
      minute: "2-digit",
      second: "2-digit"
    });
  }

  updateLiveClock();
  setInterval(updateLiveClock, 1000);
})();
</script>
</body></html>"""

# ----------------- DIRECT DASHBOARD ROUTES -----------------
@app.route("/")
@app.route("/dashboard")
def dashboard():
    total=len(INCIDENTS); high=sum(i["risk"]=="HIGH" for i in INCIDENTS); active=sum(i["status"]!="Resolved" for i in INCIDENTS); resolved=sum(i["status"]=="Resolved" for i in INCIDENTS)
    body=render_template_string("""<div class="heading"><div><h1>Flood Response, at a glance 🌊</h1><p>Real-time monitoring of dangerous roads and response teams.</p></div><a class="btn" href="{{url_for('add_incident')}}">➕ Add Incident</a></div>
<div class="stats"><div class="card"><div class="card-title">TOTAL INCIDENTS</div><div class="number">{{total}}</div><div class="card-small">🌊 All reported locations</div></div><div class="card"><div class="card-title">🔴 HIGH RISK</div><div class="number" style="color:#ef4444">{{high}}</div><div class="card-small">Needs authority attention</div></div><div class="card"><div class="card-title">🟡 ACTIVE RESPONSE</div><div class="number" style="color:#f59e0b">{{active}}</div><div class="card-small">Teams currently engaged</div></div><div class="card"><div class="card-title">🟢 RESOLVED TODAY</div><div class="number" style="color:#10b981">{{resolved}}</div><div class="card-small">Successfully cleared</div></div></div>
<div class="brief"><h3>🚨 Authority Control Room</h3><p>High-risk incidents require immediate attention. Coordinate with field officers and issue public warnings to prevent exposure to flooded areas.</p></div>
<div class="panel"><div class="panel-head"><b>🌊 Flood Incidents & Live Hazards</b><a class="btn gray" href="{{url_for('incidents')}}">View All</a></div><table><tr><th>LOCATION</th><th>RISK</th><th>WATER LEVEL</th><th>DEPARTMENT</th><th>STATUS</th><th>ACTION</th></tr>{% for i in incidents %}<tr><td>📍 <b>{{i.location}}</b><br><span style="color:#64748b">{{i.description}}</span></td><td><span class="badge {{i.risk.lower()}}">{{i.risk}}</span></td><td>💧 {{i.water}} cm</td><td>{{i.department}}</td><td>{{i.status}}</td><td><div class="action"><a class="btn gray" href="{{url_for('view_incident',iid=i.id)}}">View</a>{% if i.status!="Resolved" %}<a class="btn green" href="{{url_for('resolve_incident',iid=i.id)}}">✓</a>{% endif %}</div></td></tr>{% endfor %}</table></div>
<div class="footer"><div class="footer-box">🕒 Last Updated<br><b>{{time}}</b></div><div class="footer-box">📍 Monitored Zones<br><b>18 Areas</b></div><div class="footer-box">👮 Active Officers<br><b>{{officer_count}}</b></div><div class="footer-box">🚨 Quick Alert<br><b>{{high}} High Risk</b></div></div>""",incidents=INCIDENTS,total=total,high=high,active=active,resolved=resolved,time=datetime.now().strftime("%I:%M %p"),officer_count=len(OFFICERS))
    return render_template_string(PAGE,title="Dashboard",page="dashboard",body=body)

@app.route("/logout")
def logout():
    session.clear()
    return redirect(
        "https://aquashield-citizen.onrender.com/login.html?role=authority"
    )

@app.route("/incidents")
def incidents():
    search=request.args.get("search","").lower()
    filtered=[i for i in INCIDENTS if search in i["location"].lower() or search in i["risk"].lower() or search in i["department"].lower()]
    body=render_template_string("""<div class="heading"><div><h1>Flood Incidents 🌊</h1><p>Monitor all reported flooded roads and locations.</p></div><a class="btn" href="{{url_for('add_incident')}}">➕ Add Incident</a></div><div class="panel"><div class="panel-head"><b>All Flood Alerts</b><form><input name="search" value="{{search}}" placeholder="🔎 Search location..."></form></div><table><tr><th>LOCATION</th><th>RISK</th><th>WATER</th><th>DEPARTMENT</th><th>OFFICER</th><th>STATUS</th><th>ACTION</th></tr>{% for i in incidents %}<tr><td>📍 <b>{{i.location}}</b></td><td><span class="badge {{i.risk.lower()}}">{{i.risk}}</span></td><td>💧 {{i.water}} cm</td><td>{{i.department}}</td><td>👮 {{i.officer}}</td><td>{{i.status}}</td><td><a class="btn gray" href="{{url_for('view_incident',iid=i.id)}}">View</a></td></tr>{% else %}<tr><td colspan="7" style="text-align:center;padding:25px">No incidents found.</td></tr>{% endfor %}</table></div>""",incidents=filtered,search=search)
    return render_template_string(PAGE,title="Flood Incidents",page="incidents",body=body)

@app.route("/add",methods=["GET","POST"])
def add_incident():
    if request.method=="POST":
        try: water=int(request.form.get("water",0))
        except ValueError: water=0
        INCIDENTS.insert(0,{"id":next_id(),"location":request.form.get("location","Unknown Location"),"water":water,"department":request.form.get("department","Municipal Department"),"status":"Under Review","risk":calculate_risk(water),"description":request.form.get("description","Flooding reported."),"officer":"Unassigned","reported":datetime.now().strftime("%I:%M %p")})
        flash(f"Incident added successfully. AI risk classification: {INCIDENTS[0]['risk']}.")
        return redirect(url_for("incidents"))
    body="""<div class="heading"><div><h1>Add Flood Incident ➕</h1><p>Enter a newly reported flooded road or location.</p></div></div><div class="panel"><form method="POST"><div class="form"><div class="field"><label>LOCATION</label><input name="location" placeholder="e.g. MG Road Junction" required></div><div class="field"><label>WATER LEVEL (CM)</label><input type="number" name="water" min="0" placeholder="e.g. 42" required></div><div class="field"><label>DEPARTMENT</label><select name="department"><option>Traffic Department</option><option>Municipal Department</option><option>Road Department</option><option>Disaster Management</option></select></div><div class="field"><label>REPORT TYPE</label><select><option>Flood / Waterlogging</option><option>Road Blockage</option><option>Emergency Access Issue</option></select></div><div class="field full"><label>DESCRIPTION</label><textarea name="description" placeholder="Describe the situation..." required></textarea></div><div class="field full"><button class="btn" type="submit">🌊 Add & Analyze Incident</button></div></div></form></div>"""
    return render_template_string(PAGE,title="Add Incident",page="incidents",body=body)

@app.route("/incident/<int:iid>")
def view_incident(iid):
    i=get_incident(iid)
    if not i: return redirect(url_for("incidents"))
    body=render_template_string("""<div class="heading"><div><h1>{{i.location}} 📍</h1><p>Incident details and response controls.</p></div><a class="btn gray" href="{{url_for('incidents')}}">← Back</a></div><div class="stats"><div class="card"><div class="card-title">RISK LEVEL</div><div class="number"><span class="badge {{i.risk.lower()}}">{{i.risk}}</span></div></div><div class="card"><div class="card-title">WATER LEVEL</div><div class="number">💧 {{i.water}} cm</div></div><div class="card"><div class="card-title">OFFICER</div><div class="number" style="font-size:20px">👮 {{i.officer}}</div></div><div class="card"><div class="card-title">STATUS</div><div class="number" style="font-size:20px">{{i.status}}</div></div></div><div class="panel"><div class="panel-head"><b>🚨 Situation Details</b></div><div style="padding:22px;font-size:14px;line-height:2.1"><b>Location:</b> {{i.location}}<br><b>Water Level:</b> {{i.water}} cm<br><b>Department:</b> {{i.department}}<br><b>Reported:</b> {{i.reported}}<br><b>Description:</b> {{i.description}}</div></div><div class="panel"><div class="panel-head"><b>⚡ Response Actions</b></div><div style="padding:18px" class="action"><a class="btn green" href="{{url_for('resolve_incident',iid=i.id)}}">✓ Mark Resolved</a><a class="btn" href="{{url_for('assign_officer',iid=i.id)}}">👮 Assign Officer</a><a class="btn red" href="{{url_for('publish_warning',iid=i.id)}}">📢 Public Warning</a></div></div>""",i=i)
    return render_template_string(PAGE,title="Incident",page="incidents",body=body)

@app.route("/resolve/<int:iid>")
def resolve_incident(iid):
    i=get_incident(iid)
    if i: i["status"]="Resolved"; flash(f"{i['location']} has been marked as resolved.")
    return redirect(request.referrer or url_for("dashboard"))

@app.route("/assign/<int:iid>",methods=["GET","POST"])
def assign_officer(iid):
    i=get_incident(iid)
    if not i: return redirect(url_for("incidents"))
    if request.method=="POST":
        i["officer"]=request.form.get("officer"); i["status"]="Officer Assigned"; flash(f"{i['officer']} assigned to {i['location']}.")
        return redirect(url_for("view_incident",iid=iid))
    body=render_template_string("""<div class="heading"><div><h1>Assign Officer 👮</h1><p>{{i.location}}</p></div></div><div class="panel"><form method="POST"><div class="form"><div class="field"><label>SELECT OFFICER</label><select name="officer">{% for o in officers %}<option value="{{o.name}}">{{o.name}} — {{o.department}}</option>{% endfor %}</select></div><div class="field"><label>INCIDENT</label><input value="{{i.location}}" disabled></div><div class="field full"><button class="btn" type="submit">👮 Assign Officer</button></div></div></form></div>""",i=i,officers=OFFICERS)
    return render_template_string(PAGE,title="Assign Officer",page="officers",body=body)

@app.route("/officers")
def officers():
    active=sum(o["status"]=="Active" for o in OFFICERS); available=sum(o["status"]=="Available" for o in OFFICERS)
    body=render_template_string("""<div class="heading"><div><h1>Field Officers 👮</h1><p>Manage emergency response personnel.</p></div></div><div class="stats"><div class="card"><div class="card-title">TOTAL OFFICERS</div><div class="number">{{total}}</div></div><div class="card"><div class="card-title">ACTIVE</div><div class="number">{{active}}</div></div><div class="card"><div class="card-title">AVAILABLE</div><div class="number">{{available}}</div></div><div class="card"><div class="card-title">RESPONSE TEAM</div><div class="number">🚨</div></div></div><div class="panel"><table><tr><th>OFFICER</th><th>DEPARTMENT</th><th>AREA</th><th>STATUS</th><th>ACTION</th></tr>{% for o in officers %}<tr><td>👤 <b>{{o.name}}</b></td><td>{{o.department}}</td><td>{{o.area}}</td><td><span class="badge {% if o.status=='Available' %}low{% else %}medium{% endif %}">{{o.status}}</span></td><td><a class="btn gray" href="{{url_for('toggle_officer',oid=o.id)}}">Toggle Status</a></td></tr>{% endfor %}</table></div>""",officers=OFFICERS,total=len(OFFICERS),active=active,available=available)
    return render_template_string(PAGE,title="Officers",page="officers",body=body)

@app.route("/toggle-officer/<int:oid>")
def toggle_officer(oid):
    o=next((x for x in OFFICERS if x["id"]==oid),None)
    if o: o["status"]="Available" if o["status"]=="Active" else "Active"; flash(f"{o['name']} status updated.")
    return redirect(url_for("officers"))

@app.route("/warnings")
def warnings():
    body=render_template_string("""<div class="heading"><div><h1>Public Warnings 🚨</h1><p>Prepare safety warnings for people near dangerous roads.</p></div></div>{% for w in warnings %}<div class="warning"><b>⚠️ {{w.location}} — {{w.risk}} RISK</b><br><br>{{w.message}}<br><br><span class="badge {{w.risk.lower()}}">{{w.status}}</span></div>{% endfor %}<div class="panel"><div class="panel-head"><b>Generate Warning</b></div><table><tr><th>LOCATION</th><th>RISK</th><th>ACTION</th></tr>{% for i in incidents %}{% if i.risk=="HIGH" %}<tr><td>📍 {{i.location}}</td><td><span class="badge high">HIGH</span></td><td><a class="btn red" href="{{url_for('publish_warning',iid=i.id)}}">📢 Publish Warning</a></td></tr>{% endif %}{% endfor %}</table></div>""",warnings=WARNINGS,incidents=INCIDENTS)
    return render_template_string(PAGE,title="Public Warnings",page="warnings",body=body)

@app.route("/publish/<int:iid>")
def publish_warning(iid):
    i=get_incident(iid)
    if i:
        if not any(w["location"]==i["location"] for w in WARNINGS):
            WARNINGS.append({"location":i["location"],"risk":i["risk"],"message":f"⚠️ Public safety alert: Avoid {i['location']} due to reported flooding. Follow local authority instructions.","status":"Published"})
            flash(f"Public warning prepared for {i['location']}.")
        else: flash("A warning already exists for this location.")
    return redirect(url_for("warnings"))

@app.route("/analytics")
def analytics():
    total=len(INCIDENTS); high=sum(i["risk"]=="HIGH" for i in INCIDENTS); medium=sum(i["risk"]=="MEDIUM" for i in INCIDENTS); low=sum(i["risk"]=="LOW" for i in INCIDENTS)
    body=render_template_string("""<div class="heading"><div><h1>Analytics & Reports 📊</h1><p>Overview of current flood incidents.</p></div><button class="btn" onclick="window.print()">🖨️ Print Report</button></div><div class="stats"><div class="card"><div class="card-title">TOTAL</div><div class="number">{{total}}</div></div><div class="card"><div class="card-title">🔴 HIGH</div><div class="number">{{high}}</div></div><div class="card"><div class="card-title">🟡 MEDIUM</div><div class="number">{{medium}}</div></div><div class="card"><div class="card-title">🟢 LOW</div><div class="number">{{low}}</div></div></div><div class="panel"><div class="panel-head"><b>Risk Distribution</b></div><div style="padding:25px;line-height:2">🔴 HIGH — {{high}}<div style="height:18px;background:#fee2e2;border-radius:10px"><div style="height:18px;width:{{(high/total*100) if total else 0}}%;background:#ef4444;border-radius:10px"></div></div><br>🟡 MEDIUM — {{medium}}<div style="height:18px;background:#fef3c7;border-radius:10px"><div style="height:18px;width:{{(medium/total*100) if total else 0}}%;background:#f59e0b;border-radius:10px"></div></div><br>🟢 LOW — {{low}}<div style="height:18px;background:#dcfce7;border-radius:10px"><div style="height:18px;width:{{(low/total*100) if total else 0}}%;background:#10b981;border-radius:10px"></div></div></div></div>""",total=total,high=high,medium=medium,low=low)
    return render_template_string(PAGE,title="Analytics",page="analytics",body=body)

@app.route("/settings",methods=["GET","POST"])
def settings():
    if request.method=="POST":
        SETTINGS["authority"]=request.form.get("authority",SETTINGS["authority"])
        try:
            SETTINGS["high"]=int(request.form.get("high",35)); SETTINGS["medium"]=int(request.form.get("medium",15))
            flash("Settings saved successfully.")
        except ValueError: flash("Please enter valid numbers.")
    body=render_template_string("""<div class="heading"><div><h1>Settings ⚙️</h1><p>Configure AquaShield AI risk thresholds.</p></div></div><div class="panel"><form method="POST"><div class="form"><div class="field full"><label>AUTHORITY NAME</label><input name="authority" value="{{s.authority}}"></div><div class="field"><label>HIGH RISK WATER LEVEL (CM)</label><input type="number" name="high" value="{{s.high}}"></div><div class="field"><label>MEDIUM RISK WATER LEVEL (CM)</label><input type="number" name="medium" value="{{s.medium}}"></div><div class="field full"><button class="btn" type="submit">💾 Save Settings</button></div></div></form></div>""",s=SETTINGS)
    return render_template_string(PAGE,title="Settings",page="settings",body=body)

@app.route("/help")
def help_page():
    body="""<div class="heading"><div><h1>Help & Support ❓</h1><p>Understand the AquaShield AI workflow.</p></div></div><div class="tiles"><div class="tile"><h3>🧠 Risk Calculation</h3><p>Water level is used as a simple rule-based indicator. High water level produces HIGH risk, medium level produces MEDIUM risk, and lower level produces LOW risk.</p></div><div class="tile"><h3>🚨 High Risk Response</h3><p>Authorities can review the incident, assign officers and prepare a public safety warning.</p></div><div class="tile"><h3>🌊 Project Flow</h3><p>Flood Report → Risk Analysis → Authority Alert → Officer Assignment → Public Warning → Resolution.</p></div></div>"""
    return render_template_string(PAGE,title="Help",page="help",body=body)

@app.route("/index")
def index_page():
    return render_template_string("index.html")  # Aapki main landing page ki HTML file

if __name__ == "__main__":
    print("AquaShield AI starting...")
    print("Open http://127.0.0.1:5000")
    app.run(host="0.0.0.0", port=5000, debug=True)