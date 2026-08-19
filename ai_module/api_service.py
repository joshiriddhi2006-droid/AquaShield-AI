from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
import re


# ============================================================
# AQUASHIELD AI SERVICE
# ============================================================

app = FastAPI(
    title="AquaShield AI Service",
    description="AI service for citizen complaint analysis",
    version="1.0"
)


# ============================================================
# CORS CONFIGURATION
# Allows AquaShield frontend to communicate with AI API
# ============================================================

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://127.0.0.1:5500",
        "http://localhost:5500"
    ],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ============================================================
# COMPLAINT CLASSIFICATION DATA
# ============================================================

complaints = [

    # Waterlogging
    "Water is accumulated on my road",
    "My street is completely waterlogged",
    "There is severe waterlogging in my area",
    "Rain water is not draining from the road",
    "The road is flooded after heavy rain",
    "My road is flooded",
    "There is waterlogging on the street",
    "Heavy rain has flooded the road",
    "Water has accumulated on the street",
    "The road is submerged in water",

    # Road Infrastructure
    "The road is damaged and needs repair",
    "There is a large damaged section of the road",
    "The road surface is broken and unsafe",
    "There are cracks on the road",
    "The road is full of potholes",
    "There is a large pothole on the road",

    # Traffic Safety
    "The flooded road is blocking traffic",
    "Vehicles cannot pass because of flooding",
    "This road is dangerous and traffic needs to be diverted",
    "An emergency vehicle cannot use this flooded road",
    "Ambulance cannot pass because of flooding",
    "Traffic is blocked due to waterlogging",
    "Cars cannot pass through the flooded road",

]


categories = [

    # Waterlogging
    "Waterlogging",
    "Waterlogging",
    "Waterlogging",
    "Waterlogging",
    "Waterlogging",
    "Waterlogging",
    "Waterlogging",
    "Waterlogging",
    "Waterlogging",
    "Waterlogging",

    # Road Infrastructure
    "Road Infrastructure",
    "Road Infrastructure",
    "Road Infrastructure",
    "Road Infrastructure",
    "Road Infrastructure",
    "Road Infrastructure",

    # Traffic Safety
    "Traffic Safety",
    "Traffic Safety",
    "Traffic Safety",
    "Traffic Safety",
    "Traffic Safety",
    "Traffic Safety",
    "Traffic Safety",
]


# ============================================================
# TRAIN CATEGORY MODEL
# ============================================================

vectorizer = TfidfVectorizer(
    lowercase=True,
    ngram_range=(1, 2)
)

X = vectorizer.fit_transform(complaints)

category_model = LogisticRegression(
    max_iter=1000
)

category_model.fit(
    X,
    categories
)


# ============================================================
# REQUEST FORMAT
# ============================================================

class ComplaintRequest(BaseModel):
    complaint: str


# ============================================================
# DEPARTMENT PREDICTION
# ============================================================

def get_department(category):

    department_map = {

        "Waterlogging":
            "Municipal / Water Management",

        "Road Infrastructure":
            "Road & Public Works",

        "Traffic Safety":
            "Traffic & Emergency Management"

    }

    return department_map.get(
        category,
        "Municipal Administration"
    )


# ============================================================
# WATER DEPTH DETECTION
# ============================================================

def get_water_depth(complaint):

    match = re.search(
        r"(\d+(?:\.\d+)?)\s*(cm|centimeter|centimeters|metre|meter|m)\b",
        complaint.lower()
    )

    if not match:
        return None

    value = float(match.group(1))

    unit = match.group(2)

    if unit in [
        "m",
        "meter",
        "metre"
    ]:
        value *= 100

    return value


# ============================================================
# PRIORITY DETECTION
# ============================================================

def get_priority(complaint):

    text = complaint.lower()

    # HIGH PRIORITY
    if any(keyword in text for keyword in [

        "emergency",
        "ambulance",
        "cannot pass",
        "can't pass",
        "emergency vehicle",
        "fire truck",
        "rescue vehicle",
        "trapped",
        "stranded",
        "completely blocked",
        "life threatening",
        "life-threatening",
        "critical",
        "extremely dangerous"

    ]):

        return "High"


    water_depth = get_water_depth(
        complaint
    )

    if water_depth is not None:

        if water_depth >= 35:
            return "High"

        if water_depth >= 15:
            return "Medium"


    # MEDIUM PRIORITY
    if any(keyword in text for keyword in [

        "severe",
        "severely",
        "heavy",
        "flooded",
        "flooding",
        "waterlogged",
        "traffic",
        "dangerous",
        "significant",
        "blocked"

    ]):

        return "Medium"


    return "Low"


# ============================================================
# SEVERITY DETECTION
# ============================================================

def get_severity(complaint):

    text = complaint.lower()


    # HIGH SEVERITY
    if any(keyword in text for keyword in [

        "ambulance cannot pass",
        "ambulance can't pass",
        "emergency vehicle cannot pass",
        "emergency vehicle can't pass",
        "cannot pass",
        "can't pass",
        "completely flooded",
        "fully submerged",
        "deep water",
        "deeply flooded",
        "completely blocked",
        "critical",
        "life threatening",
        "life-threatening",
        "extremely severe",
        "extremely dangerous"

    ]):

        return "High"


    water_depth = get_water_depth(
        complaint
    )

    if water_depth is not None:

        if water_depth >= 35:
            return "High"

        if water_depth >= 15:
            return "Medium"

        return "Low"


    # MEDIUM SEVERITY
    if any(keyword in text for keyword in [

        "severe",
        "severely",
        "heavy waterlogging",
        "heavy flooding",
        "large amount of water",
        "traffic affected",
        "dangerous",
        "significant",
        "blocked"

    ]):

        return "Medium"


    return "Low"


# ============================================================
# MAIN AI ENDPOINT
# ============================================================

@app.post("/predict")
def predict_complaint(
    request: ComplaintRequest
):

    complaint = request.complaint.strip()


    # Prevent empty complaints
    if not complaint:

        return {
            "success": False,
            "message": "Complaint cannot be empty"
        }


    # --------------------------------------------------------
    # CATEGORY PREDICTION
    # --------------------------------------------------------

    complaint_vector = vectorizer.transform(
        [complaint]
    )

    category = category_model.predict(
        complaint_vector
    )[0]


    # --------------------------------------------------------
    # DEPARTMENT
    # --------------------------------------------------------

    department = get_department(
        category
    )


    # --------------------------------------------------------
    # PRIORITY
    # --------------------------------------------------------

    priority = get_priority(
        complaint
    )


    # --------------------------------------------------------
    # SEVERITY
    # --------------------------------------------------------

    severity = get_severity(
        complaint
    )


    # --------------------------------------------------------
    # FINAL RESPONSE
    # --------------------------------------------------------

    return {

        "success": True,

        "complaint": complaint,

        "category": category,

        "department": department,

        "priority": priority,

        "severity": severity

    }


# ============================================================
# HEALTH CHECK
# ============================================================

@app.get("/")
def home():

    return {

        "service": "AquaShield AI",

        "status": "running"

    }


@app.get("/health")
def health():

    return {

        "service": "AquaShield AI",

        "status": "healthy"

    }


# ============================================================
# LOCAL RUN
# ============================================================

if __name__ == "__main__":

    import uvicorn

    uvicorn.run(
        "api_service:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )