# AquaShield AI

## AI-Powered Water & Flood Hazard Complaint Management System

AquaShield AI is an intelligent civic grievance management platform designed to help citizens report waterlogging, flooding, road hazards, and related emergencies. The system uses AI to analyse complaints, identify the appropriate category, department, priority, and severity, and route the complaint to the authority dashboard for action.

## Problem Statement

During heavy rainfall and flooding, citizens often face difficulty reporting water-related hazards and reaching the correct authority. Complaints may be incomplete, incorrectly routed, or delayed, making emergency response difficult.

AquaShield AI provides a single intelligent platform for complaint registration, AI-based analysis, department routing, GIS monitoring, authority response, and complaint tracking.

## Key Features

- AI-powered complaint analysis
- Conversational complaint collection
- Intelligent detection of missing complaint information
- Complaint category classification
- Automatic department prediction
- Priority detection
- Severity detection
- Authority Dashboard for complaint management
- GIS-based incident monitoring
- Citizen complaint tracking
- Emergency and ambulance assistance
- Complaint ID generation
- Local complaint history
- Hindi/English-ready architecture for future multilingual expansion

## AI Workflow

Citizen Complaint
|
v
AquaShield AI Assistant
|
v
Information Extraction
|
+---- Problem / Category
+---- Location
+---- Severity
+---- Water Depth
|
v
AI Classification
|
+---- Department
+---- Priority
+---- Severity
|
v
Citizen Confirmation
|
v
Authority Dashboard
|
v
GIS Monitoring & Response

## AI Capabilities

### Complaint Classification

The AI classifies complaints into categories such as:

- Waterlogging
- Road Infrastructure
- Traffic Safety

### Department Routing

Complaints are automatically mapped to the appropriate department, including:

- Municipal / Water Management
- Road & Public Works
- Traffic & Emergency Management

### Priority & Severity

The system analyses complaint language and contextual indicators such as flooding intensity, emergency vehicles, blocked roads, dangerous conditions, and water depth to determine priority and severity.

### Intelligent Follow-up

If a citizen provides an incomplete complaint such as:

> "My road is flooded."

AquaShield AI asks only for the missing information, such as the affected road/location or severity.

If the citizen provides a complete complaint, the system proceeds directly to AI analysis without repeatedly asking for information already provided.

## Authority Dashboard

The Authority Dashboard provides officials with a centralized interface to:

- View incoming complaints
- Analyse complaint information
- View AI-generated category and priority
- Track complaint status
- Monitor incidents
- Access GIS-based information
- Support emergency response

## GIS Module

The GIS module provides geographical visualization of reported incidents and supports location-based monitoring of water and flood hazards.

## Emergency Services

AquaShield includes an emergency assistance section providing quick access to ambulance and emergency services.

## Technology Stack

### Frontend

- HTML
- CSS
- JavaScript
- Tailwind CSS

### AI Module

- Python
- FastAPI
- Scikit-learn
- TF-IDF Vectorization
- Logistic Regression

### Dashboard & Backend

- Python
- Flask
- REST APIs

### GIS

- Python
- GIS-based incident visualization

### Storage

- Browser LocalStorage for citizen-side prototype complaint history

## Project Structure

```text
AquaShield-main/
│
├── ai_module/
│   ├── run_workflow.py
│   └── ...
│
├── authority_dashboard/
│   ├── aquashield_ai.py
│   └── ...
│
├── frontend/
│   ├── css/
│   ├── js/
│   ├── index.html
│   ├── complaint.html
│   ├── login.html
│   ├── profile.html
│   └── signup.html
│
├── gis_module/
│   ├── app.py
│   └── ...
│
├── requirements.txt
├── start_aquashield.bat
├── stop_aquashield.bat
└── README.md
```
