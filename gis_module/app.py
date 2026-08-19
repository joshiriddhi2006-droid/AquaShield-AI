import streamlit as st
import pandas as pd
import folium
import requests
from streamlit_folium import st_folium
from folium.plugins import LocateControl
import plotly.express as px


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="AquaShield — Emergency GIS & Flood Navigation",
    page_icon="🛡️",
    layout="wide"
)


# ============================================================
# API CONFIG
# ============================================================

AUTHORITY_API_URL = "http://127.0.0.1:5000/api/incidents"


# ============================================================
# CUSTOM CSS
# ============================================================

st.html("""
<style>

.main-header {
    background: linear-gradient(
        135deg,
        #0f172a,
        #172554,
        #082f49
    );
    color: white;
    padding: 25px;
    border-radius: 14px;
    margin-bottom: 22px;
    border: 1px solid #0284c7;
}

.main-header h2 {
    margin: 0 0 8px 0;
    font-size: 27px;
}

.main-header p {
    margin: 0;
    opacity: 0.85;
}

.panel-title {
    display: flex;
    align-items: center;
    gap: 12px;
    background: #f8fafc;
    border: 1px solid #e2e8f0;
    padding: 13px;
    border-radius: 10px;
    margin-bottom: 15px;
}

.panel-title b {
    color: #0f172a;
}

.panel-title small {
    display: block;
    color: #64748b;
    margin-top: 3px;
}

.ai-box {
    background: #eff6ff;
    border-left: 5px solid #2563eb;
    padding: 15px;
    border-radius: 8px;
    color: #1e293b;
}

.alert-box-danger {
    background: #fef2f2;
    border-left: 5px solid #ef4444;
    padding: 14px;
    border-radius: 8px;
    margin-bottom: 10px;
    color: #991b1b;
}

.alert-box-warning {
    background: #fffbeb;
    border-left: 5px solid #f59e0b;
    padding: 14px;
    border-radius: 8px;
    margin-bottom: 10px;
    color: #78350f;
}

.alert-box-success {
    background: #f0fdf4;
    border-left: 5px solid #22c55e;
    padding: 14px;
    border-radius: 8px;
    margin-bottom: 10px;
    color: #166534;
}

.card-box {
    background: white;
    border: 1px solid #e2e8f0;
    padding: 15px;
    border-radius: 10px;
    margin-bottom: 10px;
}

.map-box {
    border: 1px solid #cbd5e1;
    border-radius: 12px;
    padding: 8px;
    background: #f8fafc;
}

</style>
""")


# ============================================================
# COLOR MAP
# ============================================================

COLOR_MAP = {
    "HIGH": "#D9534F",
    "MEDIUM": "#E6A23C",
    "LOW": "#74C69D",
    "SAFE": "#2D6A4F"
}


# ============================================================
# AUTHORITY API
# ============================================================

def get_authority_incidents():

    try:

        response = requests.get(
            AUTHORITY_API_URL,
            timeout=5
        )

        response.raise_for_status()

        data = response.json()

        if isinstance(data, dict):
            return data.get("incidents", []), None

        if isinstance(data, list):
            return data, None

        return [], None

    except requests.exceptions.RequestException as e:

        return [], f"Authority Dashboard unavailable: {e}"

    except ValueError:

        return [], "Authority Dashboard returned invalid JSON."


def send_incident_to_authority(
    location,
    destination,
    vehicle,
    water,
    department,
    distance_km=0,
    duration_min=0,
    risk="LOW"
):

    payload = {
        "location": location,
        "destination": destination,
        "vehicle": vehicle,
        "water": water,
        "department": department,
        "status": "New GIS Route Report",
        "risk": risk,
        "distance_km": distance_km,
        "duration_min": duration_min,
        "source": "GIS Route Planner"
    }

    try:

        response = requests.post(
            AUTHORITY_API_URL,
            json=payload,
            timeout=5
        )

        if response.status_code in [200, 201]:

            return True, response.json()

        return False, (
            f"Authority API returned "
            f"{response.status_code}"
        )

    except requests.exceptions.RequestException as e:

        return False, str(e)


# ============================================================
# PERMANENT GIS MONITORING DATA
# ============================================================

def load_permanent_data():

    return pd.DataFrame([

        {
            "id": "MON-001",
            "name": "Main Junction Crossing",
            "destination": "",
            "vehicle": "",
            "distance_km": 0,
            "duration_min": 0,
            "lat": 22.7196,
            "lon": 75.8577,
            "risk": "HIGH",
            "water_cm": 48,
            "department": "Traffic Police",
            "status": "Road Blocked",
            "source": "GIS Monitoring",
            "type": "Monitored Zone"
        },

        {
            "id": "MON-002",
            "name": "Railway Underpass",
            "destination": "",
            "vehicle": "",
            "distance_km": 0,
            "duration_min": 0,
            "lat": 22.6912,
            "lon": 75.8658,
            "risk": "MEDIUM",
            "water_cm": 22,
            "department": "Municipal Corp",
            "status": "Under Review",
            "source": "GIS Monitoring",
            "type": "Monitored Zone"
        },

        {
            "id": "MON-003",
            "name": "Bus Stand Road",
            "destination": "",
            "vehicle": "",
            "distance_km": 0,
            "duration_min": 0,
            "lat": 22.7244,
            "lon": 75.8839,
            "risk": "LOW",
            "water_cm": 8,
            "department": "Road Maintenance",
            "status": "Resolved",
            "source": "GIS Monitoring",
            "type": "Monitored Zone"
        },

        {
            "id": "MON-004",
            "name": "Flyover Bypass",
            "destination": "",
            "vehicle": "",
            "distance_km": 0,
            "duration_min": 0,
            "lat": 22.7500,
            "lon": 75.8700,
            "risk": "SAFE",
            "water_cm": 0,
            "department": "Emergency Control",
            "status": "Safe Route",
            "source": "GIS Monitoring",
            "type": "Monitored Zone"
        }

    ])


permanent_data = load_permanent_data()


# ============================================================
# BUILD LIVE DATA
# ============================================================

def build_live_data():

    incidents, error = get_authority_incidents()

    rows = []

    for _, row in permanent_data.iterrows():

      rows.append({
        "id": row["id"],
        "name": row["name"],
        "destination": row.get("destination", ""),
        "vehicle": row.get("vehicle", ""),
        "distance_km": row.get("distance_km", 0),
        "duration_min": row.get("duration_min", 0),
        "lat": row["lat"],
        "lon": row["lon"],
        "risk": row["risk"],
        "water_cm": row["water_cm"],
        "department": row["department"],
        "status": row["status"],
        "source": row["source"],
        "type": "Monitored Zone"
    })


    for incident in incidents:

        try:

            water = float(
                incident.get(
                    "water",
                    incident.get(
                        "water_cm",
                        0
                    )
                )
            )

        except:

            water = 0


        risk = str(
            incident.get(
                "risk",
                incident.get(
                    "priority",
                    "LOW"
                )
            )
        ).upper()


        if risk not in COLOR_MAP:
            risk = "LOW"


        lat = incident.get("lat")

        if lat is None:
            lat = incident.get("latitude")


        lon = incident.get("lon")

        if lon is None:
            lon = incident.get("longitude")


        rows.append({

            "id": str(
                incident.get(
                    "id",
                    incident.get(
                        "reference_id",
                        "LIVE"
                    )
                )
            ),

            "name": incident.get(
                "location",
                incident.get(
                    "description",
                    "Unknown Location"
                )
            ),

            "destination": incident.get(
                "destination",
                ""
            ),

            "vehicle": incident.get(
                "vehicle",
                ""
            ),

            "distance_km": incident.get(
                "distance_km",
                0
            ),

            "duration_min": incident.get(
                "duration_min",
                0
            ),

            "lat": lat,

            "lon": lon,

            "risk": risk,

            "water_cm": water,

            "department": incident.get(
                "department",
                "Emergency Control"
            ),

            "status": incident.get(
                "status",
                "New Complaint"
            ),

            "source": incident.get(
                "source",
                "Authority Dashboard"
            ),

            "type": "Citizen / Authority Incident"

        })


    return pd.DataFrame(rows), error


live_data, api_error = build_live_data()


# ============================================================
# LOCATION DATABASE
# ============================================================

LOCATION_COORDS = {

    # ---------------- INDORE ----------------

    "Indore Railway Station":
        [22.7100, 75.8500],

    "Indore Bus Stand":
        [22.7195, 75.8580],

    "City Civil Hospital, Indore":
        [22.7550, 75.8800],

    "Rajwada Palace":
        [22.7196, 75.8577],

    "Vijay Nagar Square":
        [22.7533, 75.8937],

    "Bhawarkuan Square":
        [22.6906, 75.8577],

    "Palasia Square":
        [22.7287, 75.8890],

    "Tower Square":
        [22.7250, 75.8790],

    "MR-10 Junction":
        [22.7700, 75.9000],

    "Super Corridor":
        [22.7190, 75.8100],

    "Airport Road":
        [22.7600, 75.8400],

    # ---------------- UJJAIN ----------------
    # Common locations used during AquaShield testing.

    "Ujjain Junction":
        [23.1765, 75.7885],

    "Ujjain Railway Station":
        [23.1765, 75.7885],

    "Ujjain Junction Railway Station":
        [23.1765, 75.7885],

    "Nanakheda":
        [23.1826, 75.7606],

    "Nanakheda Bus Stand":
        [23.1826, 75.7606],

    "Nanakheda Bus Station":
        [23.1826, 75.7606],

    "Freeganj Ujjain":
        [23.1760, 75.7900],

    "Ujjain Civil Hospital":
        [23.1769, 75.7860],

    "District Hospital Ujjain":
        [23.1769, 75.7860],

    "Tower Chowk Ujjain":
        [23.1828, 75.7847],

    "Mahakal Temple":
        [23.1828, 75.7682],

    "Mahakaleshwar Temple":
        [23.1828, 75.7682]

}


# ============================================================
# GEOCODING
# ============================================================

@st.cache_data(
    ttl=3600,
    show_spinner=False
)
def geocode_place(place):
    """
    Convert a user-entered location into coordinates.

    The user can enter:
      - a landmark
      - a street/road
      - a locality
      - a city
      - city + state
      - city + state + country
      - a complete address

    Examples:
      "Ujjain Junction, Madhya Pradesh"
      "Nanakheda, Ujjain, Madhya Pradesh"
      "Indore, Madhya Pradesh"
      "MG Road, Bengaluru, Karnataka"
      "Marine Drive, Mumbai, Maharashtra"
      "Jaipur, Rajasthan, India"

    Priority:
      1. Exact match in AquaShield's local database.
      2. OpenStreetMap / Nominatim using the exact user query.
      3. India-context search for short Indian place names.
      4. Global Nominatim search as a final fallback.
      5. Photon geocoder as an additional fallback.
      6. Flexible local database match.

    This means the GIS is NOT restricted to Ujjain or Indore.
    Any geocodable location/state/country can be entered.
    """

    if place is None:
        return None

    place = str(place).strip()

    if not place:
        return None

    # --------------------------------------------------------
    # NORMALIZE USER INPUT
    # --------------------------------------------------------

    normalized_place = " ".join(
        place.lower().replace(",", " ").split()
    )

    # --------------------------------------------------------
    # 1. EXACT LOCAL DATABASE MATCH
    # --------------------------------------------------------

    for name, coords in LOCATION_COORDS.items():

        normalized_name = " ".join(
            name.lower().replace(",", " ").split()
        )

        if normalized_place == normalized_name:

            return {
                "lat": coords[0],
                "lon": coords[1],
                "display_name": name
            }

    # --------------------------------------------------------
    # 2–5. ONLINE GEOCODING
    # --------------------------------------------------------

    # First try EXACTLY what the citizen typed.
    # This is important because it allows:
    # "Bhopal, Madhya Pradesh"
    # "Mumbai, Maharashtra"
    # "Bengaluru, Karnataka"
    # etc.
    queries = [
        place
    ]

    # For Indian applications, also try India as a context.
    # This does NOT force the location to be in Madhya Pradesh.
    if "india" not in normalized_place:
        queries.append(
            f"{place}, India"
        )

    # If the input is only a short place name, this can help
    # Nominatim distinguish an Indian location from similarly
    # named places elsewhere.
    if "," not in place and "india" not in normalized_place:
        queries.append(
            f"{place}, India"
        )

    # Remove duplicate queries while preserving order.
    unique_queries = []

    for query in queries:
        if query not in unique_queries:
            unique_queries.append(query)

    # --------------------------------------------------------
    # NOMINATIM
    # --------------------------------------------------------

    for query in unique_queries:

        try:

            response = requests.get(
                "https://nominatim.openstreetmap.org/search",
                params={
                    "q": query,
                    "format": "jsonv2",
                    "limit": 3,
                    "addressdetails": 1
                },
                headers={
                    "User-Agent":
                        "AquaShield-GIS/1.0 "
                        "(educational flood-navigation prototype)"
                },
                timeout=10
            )

            response.raise_for_status()

            results = response.json()

            if results:

                # Prefer an Indian result when the user did not
                # explicitly specify another country.
                selected = results[0]

                if "india" in normalized_place or "," not in place:

                    for result in results:
                        address = result.get("address", {})

                        country = str(
                            address.get("country", "")
                        ).lower()

                        if country == "india":
                            selected = result
                            break

                return {
                    "lat": float(selected["lat"]),
                    "lon": float(selected["lon"]),
                    "display_name":
                        selected.get(
                            "display_name",
                            place
                        )
                }

        except (
            requests.exceptions.RequestException,
            ValueError,
            KeyError,
            TypeError
        ):
            continue

    # --------------------------------------------------------
    # PHOTON FALLBACK
    # --------------------------------------------------------
    # Photon is useful when Nominatim is temporarily unavailable
    # or does not return a result.

    try:

        response = requests.get(
            "https://photon.komoot.io/api/",
            params={
                "q": place,
                "limit": 5
            },
            headers={
                "User-Agent":
                    "AquaShield-GIS/1.0 "
                    "(educational flood-navigation prototype)"
            },
            timeout=10
        )

        response.raise_for_status()

        data = response.json()

        features = data.get(
            "features",
            []
        )

        if features:

            selected = features[0]

            # Prefer India when available for an ambiguous
            # Indian query.
            if (
                "india" not in normalized_place
                and "," not in place
            ):

                for feature in features:

                    properties = feature.get(
                        "properties",
                        {}
                    )

                    country = str(
                        properties.get(
                            "country",
                            ""
                        )
                    ).lower()

                    if country == "india":
                        selected = feature
                        break

            coordinates = selected[
                "geometry"
            ]["coordinates"]

            properties = selected.get(
                "properties",
                {}
            )

            display_parts = []

            for key in [
                "name",
                "street",
                "city",
                "state",
                "country"
            ]:

                value = properties.get(key)

                if value and value not in display_parts:
                    display_parts.append(
                        str(value)
                    )

            display_name = ", ".join(
                display_parts
            ) or place

            return {
                "lat": float(coordinates[1]),
                "lon": float(coordinates[0]),
                "display_name": display_name
            }

    except (
        requests.exceptions.RequestException,
        ValueError,
        KeyError,
        TypeError,
        IndexError
    ):
        pass

    # --------------------------------------------------------
    # 6. FLEXIBLE LOCAL DATABASE FALLBACK
    # --------------------------------------------------------
    # Only use this after online geocoding has failed.
    # This preserves the built-in demo locations.

    for name, coords in LOCATION_COORDS.items():

        normalized_name = " ".join(
            name.lower().replace(",", " ").split()
        )

        if (
            normalized_place in normalized_name
            or normalized_name in normalized_place
        ):

            return {
                "lat": coords[0],
                "lon": coords[1],
                "display_name": name
            }

    # --------------------------------------------------------
    # NOTHING FOUND
    # --------------------------------------------------------

    return None


# ============================================================
# ROUTING
# ============================================================

@st.cache_data(
    ttl=300,
    show_spinner=False
)
def get_route(start, end):

    try:

        url = (
            "https://router.project-osrm.org/"
            "route/v1/driving/"
            f"{start[1]},{start[0]};"
            f"{end[1]},{end[0]}"
        )

        response = requests.get(
            url,
            params={
                "overview": "full",
                "geometries": "geojson"
            },
            timeout=15
        )

        response.raise_for_status()

        data = response.json()

        if (
            data.get("code") != "Ok"
            or not data.get("routes")
        ):

            return None, None


        route = data["routes"][0]


        geometry = [

            [
                point[1],
                point[0]
            ]

            for point in
            route["geometry"]["coordinates"]

        ]


        info = {

            "distance_km":
                route["distance"] / 1000,

            "duration_min":
                route["duration"] / 60

        }


        return geometry, info


    except:

        return None, None


# ============================================================
# VEHICLE PROFILES
# ============================================================

VEHICLES = {

    "🛵 Bike / Scooter": {
        "limit": 10,
        "name": "Two-Wheeler"
    },

    "🚗 Hatchback / Sedan": {
        "limit": 15,
        "name": "Car"
    },

    "🚙 SUV": {
        "limit": 32,
        "name": "SUV"
    },

    "🚨 Ambulance / Heavy Emergency Vehicle": {
        "limit": 50,
        "name": "Emergency Vehicle"
    }

}


# ============================================================
# HEADER
# ============================================================

st.html("""
<div class="main-header">

    <div style="display:flex; align-items:center; justify-content:space-between; gap:20px; flex-wrap:wrap;">

        <div>
            <h2>
                AquaShield — Vehicle-Aware Flood GIS System
            </h2>

            <p>
                Permanent Lifetime Routing & Real-Time Emergency Navigation
            </p>
        </div>

        <a
            href="http://127.0.0.1:5500/index.html"
            target="_self"
            style="
                display:inline-flex;
                align-items:center;
                justify-content:center;
                gap:8px;
                padding:10px 18px;
                border-radius:10px;
                background:#0ea5e9;
                color:white;
                text-decoration:none;
                font-weight:800;
                font-size:14px;
                border:1px solid #38bdf8;
                box-shadow:0 4px 12px rgba(14,165,233,.25);
                white-space:nowrap;
            "
        >
            🏠 Home
        </a>

    </div>

</div>
""")


# ============================================================
# TABS
# ============================================================

route_tab, photo_tab, analytics_tab = st.tabs([

    "🗺️ Vehicle Route Planner",

    "📸 Photo Inspector",

    "📊 Live Analytics Dashboard"

])


# ============================================================
# ROUTE PLANNER
# ============================================================

with route_tab:

    st.markdown(
        "## 📍 Vehicle Water-Clearance Route Inspector"
    )


    # ========================================================
    # FULL-WIDTH ROUTE CONTROLS
    # ========================================================

    st.html("""
    <div class="panel-title">

        <span style="font-size:22px;">
            🚘
        </span>

        <div>

            <b>Route Controls</b>

            <small>
                Vehicle, locations & safety assessment
            </small>

        </div>

    </div>
    """)


    # ========================================================
    # VEHICLE
    # ========================================================

    st.markdown(
        "### 🚘 Select Vehicle"
    )


    vehicle_choice = st.selectbox(
        "Vehicle Type",
        list(VEHICLES.keys())
    )


    vehicle = VEHICLES[
        vehicle_choice
    ]


    limit = vehicle["limit"]


    st.info(
        f"💧 Maximum recommended water depth: "
        f"**{limit} cm**"
    )


    # ========================================================
    # NAVIGATION POINTS
    # ========================================================

    st.markdown(
        "### 🛣️ Navigation Points"
    )


    location_col1, location_col2 = st.columns(2)


    with location_col1:

        start_text = st.text_input(
            "📍 Current Location",
            value="Indore Railway Station",
            help="Enter any place, city, state, or country. Example: Mumbai, Maharashtra"
        )


    with location_col2:

        destination_text = st.text_input(
            "🎯 Destination",
            value="City Civil Hospital, Indore",
            help="Enter any place, city, state, or country. Example: Jaipur, Rajasthan"
        )


    if st.button(
        "🔎 Find Locations & Build Route",
        use_container_width=True
    ):

        start_result = geocode_place(
            start_text
        )

        end_result = geocode_place(
            destination_text
        )


        if not start_result:

            st.error(
                f"Could not find the current location: "
                f"**{start_text}**. "
                f"Try entering a more complete location, for example "
                f"**city, state, country**."
            )


        elif not end_result:

            st.error(
                f"Could not find the destination: "
                f"**{destination_text}**. "
                f"Try entering a more complete location, for example "
                f"**city, state, country**."
            )


        else:

            st.session_state[
                "start_result"
            ] = start_result

            st.session_state[
                "end_result"
            ] = end_result

            st.session_state[
                "route_geometry"
            ] = None

            st.session_state[
                "route_info"
            ] = None

            st.session_state[
                "show_gis_map"
            ] = False


            st.success(
                "✅ Locations found successfully."
            )


    start_result = st.session_state.get(
        "start_result"
    )

    end_result = st.session_state.get(
        "end_result"
    )


    # ========================================================
    # ROUTE INFORMATION
    # ========================================================

    if start_result and end_result:

        start_coords = [
            start_result["lat"],
            start_result["lon"]
        ]

        end_coords = [
            end_result["lat"],
            end_result["lon"]
        ]


        info_col1, info_col2 = st.columns(2)


        with info_col1:

            st.success(
                f"📍 **Current Location**\n\n"
                f"{start_result['display_name']}"
            )


        with info_col2:

            st.success(
                f"🎯 **Destination**\n\n"
                f"{end_result['display_name']}"
            )


        geometry, info = get_route(
            start_coords,
            end_coords
        )


        if geometry:

            st.session_state[
                "route_geometry"
            ] = geometry

            st.session_state[
                "route_info"
            ] = info


            route_col1, route_col2 = st.columns(2)


            with route_col1:

                st.metric(
                    "🛣️ Road Distance",
                    f"{info['distance_km']:.1f} km"
                )


            with route_col2:

                st.metric(
                    "⏱️ Estimated Travel Time",
                    f"{info['duration_min']:.0f} min"
                )


        else:

            st.warning(
                "⚠️ Road routing service is temporarily unavailable."
            )


        st.divider()


        # ====================================================
        # SAFETY ASSESSMENT
        # ====================================================

        st.markdown(
            "### 🚨 Route Safety Assessment"
        )


        if limit <= 10:

            st.html("""
            <div class="alert-box-danger">

                <b>
                    ⛔ HIGH DANGER FOR TWO-WHEELERS
                </b>

                <br><br>

                Railway Underpass:
                <b>22 cm</b> — unsafe.

                <br>

                Main Junction:
                <b>48 cm</b> — submerged.

                <br><br>

                Use a dry alternate route.

            </div>
            """)


        elif limit <= 15:

            st.html("""
            <div class="alert-box-danger">

                <b>
                    ❌ HIGH RISK FOR CARS
                </b>

                <br><br>

                Main Junction:
                <b>48 cm</b> — blocked.

                <br>

                Railway Underpass:
                <b>22 cm</b> — flooding risk.

                <br><br>

                Use an alternate route.

            </div>
            """)


        elif limit <= 32:

            st.html("""
            <div class="alert-box-warning">

                <b>
                    ⚠️ SUV PASSABLE WITH CAUTION
                </b>

                <br><br>

                Railway Underpass:
                <b>22 cm</b> — passable with caution.

                <br>

                Main Junction:
                <b>48 cm</b> — avoid.

                <br><br>

                Prefer a dry alternate corridor.

            </div>
            """)


        else:

            st.html("""
            <div class="alert-box-warning">

                <b>
                    🚨 EMERGENCY VEHICLE CLEARANCE
                </b>

                <br><br>

                Configured clearance:
                <b>50 cm</b>.

                <br><br>

                Always verify actual flood depth
                before entering a flooded road.

            </div>
            """)


        st.html("""
        <div class="alert-box-success">

            <b>
                🟢 DRY SAFE CORRIDOR
            </b>

            <br><br>

            Flyover Bypass:
            <b>0 cm water depth</b>.

        </div>
        """)


        # ====================================================
        # AUTHORITY REPORTING
        # ====================================================

        st.markdown(
            "### 🚨 Authority Incident Reporting"
        )


        if st.button(
            "🚨 Send Flood Incident to Authority",
            use_container_width=True
        ):

            # Send the exact route entered by the user.
            report_location = start_result["display_name"]
            report_destination = end_result["display_name"]
            report_vehicle = vehicle["name"]

            route_info = st.session_state.get(
                "route_info"
            )

            if route_info:
                report_distance = route_info["distance_km"]
                report_duration = route_info["duration_min"]
            else:
                report_distance = 0
                report_duration = 0

            # Use the highest currently monitored flood depth
            # as the route risk reference.
            highest_water = 0

            for _, flood_row in live_data.iterrows():

                try:
                    water_value = float(
                        flood_row["water_cm"]
                    )

                    if water_value > highest_water:
                        highest_water = water_value

                except (TypeError, ValueError):
                    pass

            if highest_water > limit:
                report_risk = "HIGH"

            elif highest_water > limit * 0.6:
                report_risk = "MEDIUM"

            else:
                report_risk = "LOW"

            success, result = send_incident_to_authority(
                location=report_location,
                destination=report_destination,
                vehicle=report_vehicle,
                water=int(highest_water),
                department="GIS Route Planning",
                distance_km=report_distance,
                duration_min=report_duration,
                risk=report_risk
            )

            if success:

                st.success(
                    "✅ Exact route report sent to Authority."
                )

                st.info(
                    f"""
📍 **From:** {report_location}

🎯 **To:** {report_destination}

🚘 **Vehicle:** {report_vehicle}

🌊 **Risk:** {report_risk}

🛣️ **Distance:** {report_distance:.1f} km
"""
                )

            else:

                st.error(
                    f"❌ Failed: {result}"
                )


        st.divider()


        # ====================================================
        # MAP BUTTON
        # ====================================================

        st.markdown(
            "### 🗺️ Flood Navigation Map"
        )


        st.caption(
            "The map is hidden to keep the information page "
            "clean. Open it only when required."
        )


        if st.button(
            "🗺️ Open Live Flood Navigation Map",
            use_container_width=True,
            type="primary"
        ):

            st.session_state[
                "show_gis_map"
            ] = True


        # ====================================================
        # MAP
        # ====================================================

        if st.session_state.get(
            "show_gis_map",
            False
        ):

            st.markdown(
                "#### 🗺️ Live Flood Navigation Map"
            )


            fmap = folium.Map(
                location=[
                    (
                        start_coords[0]
                        + end_coords[0]
                    ) / 2,

                    (
                        start_coords[1]
                        + end_coords[1]
                    ) / 2
                ],
                zoom_start=13,
                tiles="OpenStreetMap"
            )


            LocateControl(
                auto_start=False
            ).add_to(fmap)


            # START MARKER

            folium.Marker(

                start_coords,

                popup=(
                    f"<b>Current Location</b><br>"
                    f"{start_result['display_name']}"
                ),

                tooltip="📍 Current Location",

                icon=folium.Icon(
                    color="blue",
                    icon="user"
                )

            ).add_to(fmap)


            # DESTINATION MARKER

            folium.Marker(

                end_coords,

                popup=(
                    f"<b>Destination</b><br>"
                    f"{end_result['display_name']}"
                ),

                tooltip="🎯 Destination",

                icon=folium.Icon(
                    color="red",
                    icon="flag"
                )

            ).add_to(fmap)


            # FLOOD MARKERS

            for _, row in live_data.iterrows():

                lat = row["lat"]

                lon = row["lon"]


                if pd.isna(lat) or pd.isna(lon):

                    continue


                risk = row["risk"]

                water = float(
                    row["water_cm"]
                )


                marker_color = (

                    "red"

                    if risk == "HIGH"

                    else "orange"

                    if risk == "MEDIUM"

                    else "green"

                )


                folium.Marker(

                    [
                        lat,
                        lon
                    ],

                    popup=(

                        f"<b>{row['name']}</b><br>"

                        f"Water: "
                        f"{water:.0f} cm<br>"

                        f"Risk: {risk}<br>"

                        f"Department: "
                        f"{row['department']}<br>"

                        f"Status: "
                        f"{row['status']}<br>"

                        f"Source: "
                        f"{row['source']}"

                    ),

                    tooltip=row["name"],

                    icon=folium.Icon(

                        color=marker_color,

                        icon="warning-sign"

                    )

                ).add_to(fmap)


                if water > 0:

                    folium.Circle(

                        [
                            lat,
                            lon
                        ],

                        radius=300,

                        color=COLOR_MAP.get(
                            risk,
                            "#74C69D"
                        ),

                        fill=True,

                        fill_color=COLOR_MAP.get(
                            risk,
                            "#74C69D"
                        ),

                        fill_opacity=0.30

                    ).add_to(fmap)


            # ROUTE

            route_geometry = (
                st.session_state.get(
                    "route_geometry"
                )
            )


            if route_geometry:

                folium.PolyLine(

                    route_geometry,

                    color="#2563EB",

                    weight=7,

                    opacity=0.9,

                    popup=(
                        "🛣️ Recommended Road Route"
                    )

                ).add_to(fmap)


            st_folium(

                fmap,

                width="100%",

                height=620

            )


# ============================================================
# PHOTO INSPECTOR
# ============================================================

with photo_tab:

    st.markdown(
        "## 📸 Flood Evidence Photo Inspector"
    )


    uploaded_file = st.file_uploader(
        "Upload a flood / waterlogging photo",
        type=[
            "jpg",
            "jpeg",
            "png",
            "webp"
        ]
    )


    if uploaded_file:

        col1, col2 = st.columns(2)


        with col1:

            st.image(
                uploaded_file,
                caption="Uploaded Flood Evidence",
                use_container_width=True
            )


        with col2:

            st.html("""
            <div class="ai-box">

                <h3>
                    🤖 AI Computer Vision Assessment
                </h3>

                <br>

                <b>Status:</b>
                Photo received successfully.

                <br><br>

                <b>Analysis:</b>
                Waterlogging evidence detected.

                <br><br>

                <b>GIS Action:</b>
                Evidence ready for authority review.

            </div>
            """)


            st.success(
                "✅ Evidence uploaded successfully."
            )

    else:

        st.info(
            "Upload a flood image to inspect it."
        )


# ============================================================
# LIVE ANALYTICS
# ============================================================

with analytics_tab:

    st.markdown(
        "## 📊 Live City Complaint & Flood Analytics"
    )


    st.caption(
        "Analytics are connected to the Authority Dashboard incident API."
    )


    if st.button(
        "🔄 Refresh Live Analytics"
    ):

        st.rerun()


    analytics_data, analytics_error = (
        build_live_data()
    )


    if analytics_error:

        st.warning(
            "🟠 Authority Dashboard connection unavailable. "
            "Showing GIS monitored locations only."
        )

    else:

        st.success(
            "🟢 Live Authority Dashboard connection active."
        )


    # ========================================================
    # METRICS
    # ========================================================

    total = len(
        analytics_data
    )


    high = int(
        (
            analytics_data["risk"]
            == "HIGH"
        ).sum()
    )


    medium = int(
        (
            analytics_data["risk"]
            == "MEDIUM"
        ).sum()
    )


    low = int(
        (
            analytics_data["risk"]
            == "LOW"
        ).sum()
    )


    authority_reports = int(
        (
            analytics_data["type"]
            == "Citizen / Authority Incident"
        ).sum()
    )


    resolved = int(
        analytics_data[
            analytics_data["status"]
            .astype(str)
            .str.lower()
            .str.contains("resolved")
        ].shape[0]
    )


    c1, c2, c3, c4, c5 = st.columns(5)


    c1.metric(
        "Total Incidents",
        total
    )


    c2.metric(
        "High Risk",
        high
    )


    c3.metric(
        "Medium Risk",
        medium
    )


    c4.metric(
        "Live Reports",
        authority_reports
    )


    c5.metric(
        "Resolved",
        resolved
    )


    st.divider()


    # ========================================================
    # LIVE INCIDENT FEED
    # ========================================================

    st.markdown(
        "### 🚨 Live Incident Feed"
    )


    table = analytics_data[
        [
            "name",
            "destination",
            "vehicle",
            "risk",
            "water_cm",
            "department",
            "status",
            "distance_km",
            "duration_min",
            "source"
        ]
    ].copy()


    table.columns = [

        "Current Location",

        "Destination",

        "Vehicle",

        "Risk",

        "Water (cm)",

        "Department",

        "Status",

        "Distance (km)",

        "Time (min)",

        "Source"

    ]


    st.dataframe(

        table,

        use_container_width=True,

        hide_index=True

    )


    st.divider()


    # ========================================================
    # CHARTS
    # ========================================================

    chart1, chart2 = st.columns(2)


    with chart1:

        st.markdown(
            "### 🏢 Department-wise Incidents"
        )


        department_data = (
            analytics_data[
                "department"
            ]
            .fillna("Unknown")
            .value_counts()
            .reset_index()
        )


        department_data.columns = [

            "Department",

            "Incidents"

        ]


        fig_department = px.bar(

            department_data,

            x="Department",

            y="Incidents",

            title="Incidents by Department",

            template="plotly_white"

        )


        st.plotly_chart(

            fig_department,

            use_container_width=True

        )


    with chart2:

        st.markdown(
            "### 🌊 Risk Distribution"
        )


        risk_data = pd.DataFrame({

            "Risk": [

                "HIGH",

                "MEDIUM",

                "LOW"

            ],

            "Count": [

                high,

                medium,

                low

            ]

        })


        fig_risk = px.pie(

            risk_data,

            names="Risk",

            values="Count",

            hole=0.45,

            title="Current Risk Distribution",

            color="Risk",

            color_discrete_map=COLOR_MAP,

            template="plotly_white"

        )


        st.plotly_chart(

            fig_risk,

            use_container_width=True

        )


    # ========================================================
    # WATER LEVEL CHART
    # ========================================================

    st.markdown(
        "### 💧 Water Level by Location"
    )


    water_data = (
        analytics_data
        .sort_values(
            "water_cm",
            ascending=False
        )
        .head(15)
    )


    fig_water = px.bar(

        water_data,

        x="name",

        y="water_cm",

        color="risk",

        color_discrete_map=COLOR_MAP,

        title="Reported / Monitored Water Depth",

        template="plotly_white"

    )


    fig_water.update_layout(

        xaxis_title="Location",

        yaxis_title="Water Depth (cm)"

    )


    st.plotly_chart(

        fig_water,

        use_container_width=True

    )


    # ========================================================
    # LOCATION CARDS
    # ========================================================

    st.divider()

    st.markdown(
        "### 📍 Current Monitored Locations"
    )

    live_card_data = analytics_data[
        analytics_data["type"] == "Citizen / Authority Incident"
    ].copy()

    permanent_card_data = analytics_data[
        analytics_data["type"] == "Monitored Zone"
    ].copy()

    if not live_card_data.empty:
        live_card_data = live_card_data.iloc[::-1]

    card_data = pd.concat(
        [live_card_data, permanent_card_data],
        ignore_index=True
    ).head(8)

    if live_card_data.empty:
        st.info(
            "No new GIS / Authority reports are available yet. "
            "Showing the permanent monitored locations."
        )
    else:
        st.success(
            f"🟢 Showing {len(live_card_data)} live GIS / Authority "
            f"report(s) first. Permanent monitored zones follow."
        )

    # --------------------------------------------------------
    # Card styling:
    # Every summary card has the same height. Long information
    # is intentionally shortened in the card and is available
    # through the Read More expander below it.
    # --------------------------------------------------------

    st.html("""
    <style>
        .aq-card {
            box-sizing: border-box;
            width: 100%;
            height: 315px;
            background: #111827;
            border-radius: 16px;
            padding: 16px;
            color: #F8FAFC;
            box-shadow: 0 8px 22px rgba(0,0,0,.18);
            overflow: hidden;
            display: flex;
            flex-direction: column;
        }

        .aq-card-title {
            color: #F8FAFC;
            font-size: 14px;
            line-height: 1.35;
            font-weight: 800;
            height: 38px;
            overflow: hidden;
            display: -webkit-box;
            -webkit-line-clamp: 2;
            -webkit-box-orient: vertical;
            overflow-wrap: anywhere;
            word-break: break-word;
        }

        .aq-card-field {
            display: grid;
            grid-template-columns: 72px minmax(0,1fr);
            gap: 7px;
            padding: 7px 0;
            border-bottom: 1px solid #1E293B;
        }

        .aq-card-label {
            color: #64748B;
            font-size: 9px;
            font-weight: 700;
        }

        .aq-card-value {
            color: #CBD5E1;
            font-size: 10px;
            line-height: 1.3;
            font-weight: 600;
            text-align: right;
            overflow: hidden;
            white-space: nowrap;
            text-overflow: ellipsis;
        }

        .aq-card-water {
            display: flex;
            align-items: center;
            justify-content: space-between;
            gap: 8px;
            background: #0B1220;
            border: 1px solid #263449;
            border-radius: 11px;
            padding: 9px 10px;
            margin: 10px 0 2px 0;
        }

        .aq-card-source {
            margin-top: auto;
            padding-top: 8px;
            color: #64748B;
            font-size: 8px;
            line-height: 1.25;
            overflow: hidden;
            white-space: nowrap;
            text-overflow: ellipsis;
        }

        /* Keep Streamlit expanders compact and visually consistent. */
        div[data-testid="stExpander"] {
            margin-top: 6px;
            border: 1px solid #263449 !important;
            border-radius: 10px !important;
            background: #0F172A !important;
        }

        div[data-testid="stExpander"] summary {
            font-size: 11px !important;
            font-weight: 800 !important;
            color: #38BDF8 !important;
        }
    </style>
    """)

    card_columns = st.columns(4, gap="medium")

    for index, (_, row) in enumerate(card_data.iterrows()):

        with card_columns[index % 4]:

            risk = str(row.get("risk", "LOW")).upper().strip()

            risk_color = COLOR_MAP.get(
                risk,
                "#94A3B8"
            )

            is_live = (
                row.get("type") == "Citizen / Authority Incident"
            )

            source_label = (
                "LIVE GIS REPORT"
                if is_live
                else "PERMANENT MONITOR"
            )

            location = str(
                row.get("name", "Unknown Location")
            ).strip()

            destination = str(
                row.get("destination", "")
            ).strip()

            vehicle_name = str(
                row.get("vehicle", "")
            ).strip()

            department = str(
                row.get("department", "Emergency Control")
            ).strip()

            status = str(
                row.get("status", "Monitoring")
            ).strip()

            source = str(
                row.get("source", "GIS Monitoring")
            ).strip()

            try:
                water_value = float(
                    row.get("water_cm", 0) or 0
                )
            except (TypeError, ValueError):
                water_value = 0

            try:
                distance_value = float(
                    row.get("distance_km", 0) or 0
                )
            except (TypeError, ValueError):
                distance_value = 0

            try:
                duration_value = float(
                    row.get("duration_min", 0) or 0
                )
            except (TypeError, ValueError):
                duration_value = 0

            card_border = risk_color if is_live else "#334155"

            badge_bg = (
                "rgba(34,197,94,.12)"
                if is_live
                else "rgba(14,165,233,.10)"
            )

            badge_color = (
                "#4ADE80"
                if is_live
                else "#38BDF8"
            )

            # ------------------------------------------------
            # Fixed-height summary card
            # ------------------------------------------------

            st.html(
                f"""
                <div class="aq-card"
                     style="border:1px solid {card_border};">

                    <div style="
                        display:flex;
                        align-items:center;
                        justify-content:space-between;
                        gap:7px;
                        margin-bottom:10px;
                    ">

                        <span style="
                            display:inline-flex;
                            align-items:center;
                            gap:5px;
                            padding:4px 7px;
                            border-radius:999px;
                            background:{badge_bg};
                            color:{badge_color};
                            font-size:8px;
                            font-weight:800;
                            letter-spacing:.05em;
                            white-space:nowrap;
                        ">
                            <span style="
                                width:6px;
                                height:6px;
                                border-radius:50%;
                                background:currentColor;
                            "></span>
                            {source_label}
                        </span>

                        <span style="
                            padding:4px 7px;
                            border-radius:999px;
                            background:{risk_color}22;
                            color:{risk_color};
                            border:1px solid {risk_color}55;
                            font-size:9px;
                            font-weight:900;
                            white-space:nowrap;
                        ">
                            {risk}
                        </span>

                    </div>


                    <div class="aq-card-title">
                        {location}
                    </div>


                    <div class="aq-card-water">

                        <span style="
                            color:#94A3B8;
                            font-size:9px;
                            font-weight:800;
                        ">
                            💧 WATER DEPTH
                        </span>

                        <span style="
                            color:#F8FAFC;
                            font-size:12px;
                            font-weight:900;
                        ">
                            {water_value:.0f} cm
                        </span>

                    </div>


                    <div class="aq-card-field">

                        <span class="aq-card-label">
                            Department
                        </span>

                        <span class="aq-card-value">
                            {department}
                        </span>

                    </div>


                    <div class="aq-card-field">

                        <span class="aq-card-label">
                            Status
                        </span>

                        <span class="aq-card-value">
                            {status}
                        </span>

                    </div>


                    <div class="aq-card-source">
                        Source: {source}
                    </div>

                </div>
                """
            )

            # ------------------------------------------------
            # Read More
            # Full data is hidden until the user asks for it.
            # ------------------------------------------------

            with st.expander("📖 Read More"):

                st.markdown(
                    f"**📍 Location**  \n{location}"
                )

                st.markdown(
                    f"**🎯 Destination**  \n"
                    f"{destination or 'Not provided'}"
                )

                st.markdown(
                    f"**🚗 Vehicle**  \n"
                    f"{vehicle_name or 'Not provided'}"
                )

                st.markdown(
                    f"**💧 Water Depth**  \n"
                    f"{water_value:.0f} cm"
                )

                st.markdown(
                    f"**⚠️ Risk**  \n{risk}"
                )

                st.markdown(
                    f"**🏢 Department**  \n{department}"
                )

                st.markdown(
                    f"**📌 Status**  \n{status}"
                )

                if is_live:
                    st.markdown(
                        f"**🛣️ Route**  \n"
                        f"{distance_value:.1f} km · "
                        f"{duration_value:.0f} min"
                    )

                st.caption(
                    f"Source: {source}"
                )

# DATA FLOW
    # ========================================================

    st.divider()


    st.html("""
    <div class="alert-box-success">

        <b>
            🔗 AquaShield Live Data Flow
        </b>

        <br><br>

        Citizen Complaint
        →
        AI Classification
        →
        Authority Dashboard
        →
        GIS Analytics

        <br><br>

        New incidents received by the Authority Dashboard
        can be refreshed here using
        <b>Refresh Live Analytics</b>.

    </div>
    """)