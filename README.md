 🌊 AquaShield AI

## AI-Powered Smart Waterlogging & Civic Complaint Management System

AquaShield is an AI-powered civic safety and complaint management platform designed to help citizens report waterlogging and related urban hazards while enabling authorities to receive structured, prioritized complaints for faster response.

The platform combines citizen reporting, AI-based complaint intelligence, GPS-based location services, complaint tracking, GIS-based safety services, AquaBot assistance, and authority-side complaint management.

---

## 🚀 Live Demo

### Citizen Portal
https://aquashield-citizen.onrender.com/

### Source Code
https://github.com/joshiriddhi2006-droid/AquaShield-AI

---

## 🎯 Problem Statement

Urban waterlogging and flooding can create serious transportation and public-safety problems.

Common challenges include:

- Waterlogged roads and inaccessible routes
- Vehicle breakdowns and traffic disruption
- Delays for emergency vehicles
- Manual complaint classification
- Complaints being routed to the wrong department
- Lack of automatic priority and severity assessment
- Limited visibility for citizens after submitting complaints
- Lack of centralized monitoring for authorities

AquaShield addresses these challenges through an AI-assisted civic complaint workflow.

---

## 💡 Proposed Solution

AquaShield provides a centralized platform connecting:

**Citizen → AI → Authority → GIS & Safety Services**

Citizens can submit flood and waterlogging complaints through the Citizen Portal. The AI module analyses the complaint and extracts structured information such as:

- Complaint category
- Responsible department
- Priority
- Severity

The structured complaint is then submitted to the authority system for monitoring and further action.

Citizens can also track their submitted complaints through the **My Complaints** section.

---

# ⭐ Key Features

## 1. 🧑‍💻 Citizen Complaint Portal

Citizens can report waterlogging and related civic hazards through a simple interface.

The complaint workflow supports:

- Complaint description
- GPS-based location detection
- Water-depth selection
- AI-assisted complaint analysis
- Complaint submission
- Automatic complaint ID generation
- Complaint tracking

---

## 2. 🤖 AI Complaint Intelligence

AquaShield AI analyses citizen complaint text and extracts meaningful information.

### AI capabilities include:

- Complaint classification
- Complaint categorization
- Department prediction
- Priority detection
- Severity detection
- Structured complaint generation

Example:

**Input:**

> "My road is severely flooded and vehicles cannot pass near Railway Station."

**AI Processing:**

- Category → Waterlogging
- Department → Relevant civic department
- Priority → High
- Severity → High

---

## 3. 📍 GPS-Based Location Detection

The Citizen Portal can capture the user's current location through browser-based GPS.

The detected location is attached to the complaint and can be used by the authority system and safety services.

---

## 4. 💧 Water Depth Assessment

Citizens can provide an approximate water depth through predefined levels.

The system uses water-depth information to support:

- Severity assessment
- Priority assessment
- Flood-risk interpretation
- Authority-side monitoring

---

## 5. 📸 Road Image Evidence

Citizens can optionally upload a road image while submitting a complaint.

The feature provides:

- Optional image upload
- Image preview
- Visual evidence associated with the complaint workflow
- Evidence that can support authority review

> **Note:** The current prototype treats the uploaded image as visual evidence. Fully automated computer-vision-based waterlogging detection is planned as a future enhancement.

---

## 6. 🗣️ Dhwani Mitra

Dhwani Mitra is the voice-based complaint interaction concept of AquaShield.

The intended pipeline is:

**Speech Input → Speech-to-Text → Complaint Processing → AI Classification → Department Routing**

This makes complaint reporting more accessible and provides a foundation for multilingual and regional-language interaction.

---

## 7. 📋 My Complaints

Citizens can view complaints submitted through the AquaShield Citizen Portal.

Each complaint can display information such as:

- Complaint ID
- Complaint title
- Description
- Location
- AI analysis
- Priority
- Severity
- Submission time
- Current status

---

## 8. 🗺️ GIS & Safe Route Services

AquaShield incorporates GIS-based services to support safer navigation during flooding and waterlogging.

The GIS module provides:

- Flood-risk visualization
- Monitored locations
- Water-depth information
- Route planning
- Safer route guidance
- Vehicle-aware safety considerations

The system is designed to help users avoid high-risk flooded locations.

---

## 9. 🤖 AquaBot

AquaBot is an AI-assisted safety chatbot that provides information related to:

- Flood safety
- Water levels
- Route safety
- Alternate routes
- Emergency vehicle considerations
- Waterlogging conditions

Example questions:

- "Is Railway Underpass safe for my bike?"
- "What is the water level at Main Junction?"
- "Is there a safer alternate route?"
- "Is this route safe for an ambulance?"

---

## 10. 🏢 Authority Dashboard

The authority-side system allows officials to monitor citizen-reported incidents.

It supports:

- Incoming complaint monitoring
- Complaint classification
- Department information
- Priority information
- Severity information
- Water-depth information
- Incident status
- Authority-side management

Citizen complaints can be forwarded to the authority system through the AquaShield API.

---

# 🔄 System Workflow

```text
Citizen
   │
   ▼
Complaint Registration
   │
   ├── GPS Location
   ├── Water Depth
   └── Optional Road Image Evidence
   │
   ▼
AquaShield AI
   │
   ├── Complaint Classification
   ├── Department Prediction
   ├── Priority Detection
   └── Severity Detection
   │
   ▼
Structured Complaint
   │
   ▼
Authority Dashboard
   │
   ├── Incident Monitoring
   ├── Priority Management
   └── Status Management
   │
   ▼
GIS / Safety Services
   │
   ▼
Citizen Guidance & Response
````

---

# 🧠 AI Module

The AquaShield AI module converts unstructured citizen complaints into structured information for automated routing and prioritization.

### Complaint Classification

Identifies the relevant civic issue category.

### Department Prediction

Predicts the department responsible for handling the complaint.

### Priority Detection

Determines the urgency of the reported issue.

### Severity Detection

Evaluates the seriousness and potential impact of the complaint.

### Complaint Categorization

Converts the citizen's complaint into structured information that can be used by downstream systems.

---

# 🛠️ Technology Stack

| Layer            | Technology                   |
| ---------------- | ---------------------------- |
| Frontend         | HTML, CSS, JavaScript        |
| UI Framework     | Tailwind CSS                 |
| AI Module        | Python                       |
| AI API           | REST API                     |
| Backend Services | Python / Flask               |
| GIS              | Python, Streamlit, Folium    |
| Maps             | OpenStreetMap-based services |
| Deployment       | Render                       |
| Version Control  | Git & GitHub                 |
| Development      | Visual Studio Code           |

---

# 🏗️ Project Structure

```text
AquaShield-AI/
│
├── ai_module/
│   └── AI complaint analysis services
│
├── authority_dashboard/
│   └── Authority-side complaint management
│
├── frontend/
│   └── Citizen Portal
│
├── gis_module/
│   └── GIS, route planning and flood-risk services
│
├── requirements.txt
├── README.md
├── start_aquashield.bat
└── stop_aquashield.bat
```

---

# 👥 User Roles

## Citizen

* Submit complaints
* Provide complaint details
* Use GPS location
* Upload optional road evidence
* Interact with AquaShield AI
* Track submitted complaints
* Access GIS safety services
* Use AquaBot

## Authority

* Monitor incoming complaints
* View AI-generated complaint information
* Identify high-priority cases
* Monitor incident status
* Manage complaint responses
* Use location and flood-risk information

## AI System

* Analyse complaints
* Categorize complaints
* Predict responsible departments
* Determine priority
* Determine severity
* Support structured complaint routing

---

# 🌟 Innovation / USP

AquaShield combines AI-powered complaint intelligence with civic grievance management and location-aware safety services.

### Key differentiators:

* AI-based complaint classification
* Automatic department prediction
* Priority and severity detection
* GPS-enabled citizen reporting
* Citizen complaint tracking
* Optional road-image evidence
* GIS-based flood-risk and route services
* AquaBot safety assistance
* Authority-side complaint monitoring
* Voice-based Dhwani Mitra concept

Instead of functioning as a simple complaint form, AquaShield focuses on understanding citizen complaints and converting them into structured information that can support faster authority response.

---

# 📊 Expected Impact

AquaShield aims to:

* Reduce manual complaint classification
* Improve complaint routing
* Help authorities identify urgent cases
* Improve citizen reporting
* Improve complaint transparency
* Support faster response to critical waterlogging situations
* Provide structured civic data for future analytics
* Improve location-aware safety guidance

---

# 🔮 Future Scope

The project can be extended with:

* Multilingual and regional-language support
* Improved speech recognition for local accents and dialects
* Real-time water-level sensor integration
* Predictive waterlogging and flood-risk analysis
* Advanced GIS heatmaps
* Automated authority notifications
* Automated image-based waterlogging and damage detection
* Historical complaint analytics
* Predictive drainage maintenance
* Integration with municipal emergency-response systems

---

# 📸 Project Screenshots

Recommended screenshots for project demonstration:

1. Citizen Home Page
2. Complaint Registration
3. AI Analysis Result
4. Road Image Evidence Upload
5. Successful Complaint Submission
6. My Complaints
7. AquaBot
8. GIS Route Planner
9. Authority Dashboard

---

# 🚀 Deployment

The Citizen Portal is deployed using Render.

### Citizen Portal

[https://aquashield-citizen.onrender.com/](https://aquashield-citizen.onrender.com/)

### Source Repository

[https://github.com/joshiriddhi2006-droid/AquaShield-AI](https://github.com/joshiriddhi2006-droid/AquaShield-AI)

---

# 👨‍💻 Team Contributions

### Member 1 – Frontend / Citizen Portal

* Citizen-facing interface
* Complaint submission workflow
* UI / UX implementation
* Citizen complaint tracking

### Member 2 – Backend / Authority System

* Backend services
* Authority dashboard
* Complaint management
* API integration

### Member 3 – AI Module

* Complaint text classification
* Department prediction
* Priority detection
* Severity detection
* Complaint categorization
* Dhwani Mitra voice processing pipeline
* AI API development and integration

### Member 4 – GIS / Safety Services

* GIS-based flood-risk visualization
* Route planning
* Location-aware safety services
* AquaBot / safety assistance integration

---

# 📝 Academic Project

AquaShield was developed as an academic and demonstration project focused on applying artificial intelligence, GIS, and web technologies to smart-city civic safety and waterlogging management.

---

# 📄 License

This project was developed for academic and demonstration purposes.

