# AquaShield AI

Integrated smart flood intelligence, citizen complaint analysis, authority response, and vehicle-aware GIS navigation.

## Modules
- Citizen Portal: `frontend/`
- AI Service: `ai_module/`
- Authority Dashboard: `authority_dashboard/`
- Emergency GIS + AquaBot: `gis_module/`

## One-time setup (Windows)
```powershell
python -m pip install -r requirements.txt
```

## Start the complete project
Double-click `start_aquashield.bat`.

It starts:
- Citizen Portal: http://127.0.0.1:5500
- Authority Dashboard: http://127.0.0.1:5000
- AI API: http://127.0.0.1:8000
- GIS: http://127.0.0.1:8501

## System flow
Citizen complaint → AI classification → department/priority/severity → Authority incident → GIS flood-aware navigation.

The project no longer depends on the old Dhwani Mitra voice module or external Render endpoints for its local core workflow.

## Notes
The GIS uses OpenStreetMap/Nominatim and OSRM for geocoding and road routing, so internet access is required for live map/routing requests.
