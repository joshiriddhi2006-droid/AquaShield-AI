 🛡️ AquaShield AI

## AI-Powered Water & Flood Hazard Complaint Management System

AquaShield AI is an intelligent civic emergency and flood-management platform designed to help citizens report waterlogging and flood-related hazards while enabling authorities to analyse, prioritize, monitor and respond to incidents efficiently.

The system combines **AI-powered complaint analysis, citizen reporting, GIS-based safe-route navigation, emergency assistance, and an authority management dashboard** into a unified platform.

---

## 🚀 Live Project

### 👤 Citizen Portal
🔗 https://aquashield-citizen.onrender.com/

The Citizen Portal allows users to:

- Register waterlogging and flood-related complaints
- Automatically capture their current GPS location
- Describe complaints using natural language
- Get AI-based complaint analysis
- View complaint status and history
- Access GIS-based safe route navigation
- Use AquaBot for flood and emergency safety guidance
- Access emergency assistance

---

## 🎯 Problem Statement

Urban waterlogging and flooding can create serious risks for citizens, traffic and emergency services.

Traditional complaint systems often require citizens to manually determine the appropriate department and provide detailed information before a complaint can be processed.

AquaShield AI addresses this problem by providing an intelligent platform that can:

- Capture citizen complaints quickly
- Automatically analyse complaint descriptions
- Identify the appropriate department
- Determine complaint priority and severity
- Capture geographical information
- Support authority-side monitoring
- Provide safer route guidance during flooding
- Improve emergency response coordination

---

## 💡 Key Features

### 👤 Citizen Portal

- Citizen registration and login
- Waterlogging and flood hazard reporting
- GPS-based complaint location
- Complaint history
- Complaint status tracking
- AI-assisted complaint registration
- Emergency service access

### 🤖 AI Complaint Intelligence

AquaShield AI analyses the citizen's complaint and helps determine:

- Complaint category
- Responsible department
- Priority
- Severity
- Nature of the reported hazard

This reduces the need for citizens to manually determine where their complaint should be routed.

### 🗺️ GIS Safe Route Navigation

The GIS module provides:

- Interactive map visualization
- Current GPS location
- Destination search
- Route calculation
- Vehicle-specific route selection
- Flood-risk awareness
- Standard and satellite map views
- Google Maps navigation support

Vehicle options include:

- 🛵 2-Wheeler
- 🚗 Sedan / Hatchback
- 🛻 SUV
- 🚒 Emergency / Rescue Vehicle

### 🏛️ Authority Dashboard

The authority-side system provides officials with centralized access to reported incidents.

It supports:

- Complaint monitoring
- Complaint categorization
- Priority and severity information
- Department routing
- Incident management
- GIS-based monitoring
- Response coordination
- Complaint statistics and analytics

### 🤖 AquaBot

AquaBot is AquaShield's safety assistant that provides guidance related to:

- Flood safety
- Water levels
- Safe routes
- Alternate routes
- Vehicle safety
- Emergency vehicle access

### 🚑 Emergency Assistance

The platform provides direct access to emergency assistance information, including:

- Ambulance services
- Flood control support
- Municipal emergency contacts

---

## 🔄 System Workflow

```text
                    Citizen
                       │
                       ▼
              Complaint Registration
                       │
                       ▼
                GPS Location
                       │
                       ▼
             AquaShield AI Analysis
                       │
          ┌────────────┼────────────┐
          ▼            ▼            ▼
      Category     Department    Priority /
                                  Severity
          │            │            │
          └────────────┼────────────┘
                       ▼
              Citizen Confirmation
                       │
                       ▼
              Authority Dashboard
                       │
              ┌────────┴────────┐
              ▼                 ▼
          GIS Monitoring    Incident Management
              │                 │
              └────────┬────────┘
                       ▼
                Response & Resolution
````

---

## 🧠 AI Processing Pipeline

```text
Citizen Complaint
        │
        ▼
Natural Language Input
        │
        ▼
Complaint Classification
        │
        ├── Category
        │
        ├── Department
        │
        ├── Priority
        │
        └── Severity
        │
        ▼
Structured Complaint
        │
        ▼
Authority Dashboard
```

---

## 🏗️ System Architecture

```text
┌─────────────────────────────┐
│       Citizen Portal        │
│                             │
│  Complaint │ Profile │ GIS  │
│        AquaBot │ Emergency  │
└──────────────┬──────────────┘
               │
               ▼
┌─────────────────────────────┐
│       AI Processing         │
│                             │
│ Category │ Department       │
│ Priority │ Severity         │
└──────────────┬──────────────┘
               │
               ▼
┌─────────────────────────────┐
│     Authority Dashboard     │
│                             │
│ Incidents │ Analytics       │
│ GIS       │ Response        │
└─────────────────────────────┘
```

---

## 🧩 Main Modules

| Module              | Purpose                                           |
| ------------------- | ------------------------------------------------- |
| Citizen Portal      | Citizen complaint registration and tracking       |
| AI Module           | Complaint classification and intelligent analysis |
| GIS Module          | Flood-aware navigation and map visualization      |
| Authority Dashboard | Incident monitoring and management                |
| AquaBot             | Flood and emergency safety assistance             |
| Emergency Services  | Quick access to emergency support                 |

---

## 🛠️ Technology Stack

### Frontend

* HTML5
* CSS3
* JavaScript
* Tailwind CSS
* Font Awesome
* Leaflet.js

### AI / Backend

* Python
* AI/NLP processing
* REST APIs
* Uvicorn / API services

### GIS

* Leaflet
* OpenStreetMap
* Leaflet Routing Machine
* GPS / Geolocation API
* Satellite map layers
* Google Maps integration

### Data & Storage

* REST APIs
* Browser Local Storage
* Session Storage
* Authority-side incident storage

### Deployment

* Render
* GitHub

---

## 📁 Project Structure

```text
AquaShield-AI/
│
├── frontend/
│   ├── index.html
│   ├── complaint.html
│   ├── profile.html
│   ├── login.html
│   ├── aquabot.html
│   ├── gis-map.html
│   ├── app.js
│   ├── gis-style.css
│   └── js/
│
├── ai_module/
│   └── AI processing and API services
│
├── authority_dashboard/
│   └── Authority management system
│
├── gis_module/
│   └── GIS and route-related components
│
└── README.md
```

---

## 🔐 Citizen Complaint Privacy

AquaShield maintains complaint ownership using the citizen's account information.

Each citizen can access their own complaint history through the **My Complaints** section.

Complaints belonging to other citizens are not displayed in a user's personal complaint history.

---

## 🌊 Example Use Case

A citizen encounters severe waterlogging near a road.

```text
Citizen opens AquaShield
        ↓
Uses current GPS location
        ↓
Describes the waterlogging problem
        ↓
AquaShield AI analyses the complaint
        ↓
Category + Department + Priority + Severity
        ↓
Citizen confirms submission
        ↓
Complaint reaches Authority Dashboard
        ↓
Authority monitors the incident
        ↓
GIS helps identify affected areas
        ↓
Authorities can coordinate response
```

---

## 🎓 Project Objective

The objective of AquaShield AI is to provide a centralized and intelligent platform that connects citizens, AI-based complaint processing, GIS navigation and authorities for faster and more effective management of urban flood and waterlogging incidents.

---

## 👥 Project Team

AquaShield AI was developed as a collaborative project involving multiple team members working across:

* AI and NLP
* Frontend Development
* GIS and Navigation
* Authority Dashboard
* System Integration
* UI/UX Design
* Testing and Deployment

---

## 🔗 Project Links

### Citizen Portal

[https://aquashield-citizen.onrender.com/](https://aquashield-citizen.onrender.com/)

### GitHub Repository

[https://github.com/joshiriddhi2006-droid/AquaShield-AI](https://github.com/joshiriddhi2006-droid/AquaShield-AI)

---

## 🚀 Future Enhancements

Potential future improvements include:

* Multilingual citizen interface
* Voice-based complaint registration
* Real-time flood sensor integration
* IoT water-level monitoring
* Advanced predictive flood-risk modelling
* Mobile application
* Real-time authority notifications
* Advanced city-wide flood prediction
* Integration with additional emergency response systems

---

## 📌 Conclusion

AquaShield AI combines **Artificial Intelligence, GIS, citizen reporting and emergency response management** into a unified platform for urban flood and waterlogging management.

By automating complaint analysis and routing while providing GIS-based navigation and centralized authority monitoring, AquaShield aims to make emergency reporting and response more efficient, accessible and data-driven.

---

## 📄 License

This project was developed for academic and demonstration purposes.
