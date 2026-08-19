// ============================================================
// AQUASHIELD - COMPLAINT HANDLING
// ============================================================

(function () {

  const form = document.getElementById("complaint-form");
  const input = document.getElementById("evidence");
  const preview = document.getElementById("preview");


  // ============================================================
  // FILE TO BASE64
  // ============================================================

  function toBase64(file) {

    return new Promise((resolve, reject) => {

      const reader = new FileReader();

      reader.onload = () => resolve(reader.result);

      reader.onerror = reject;

      reader.readAsDataURL(file);

    });

  }


  // ============================================================
  // EVIDENCE PREVIEW
  // ============================================================

  if (input) {

    input.addEventListener("change", async function () {

      if (!preview) return;

      preview.innerHTML = "";

      for (const file of input.files) {

        try {

          const src = await toBase64(file);

          const img = document.createElement("img");

          img.src = src;

          img.style.maxWidth = "120px";
          img.style.maxHeight = "100px";
          img.style.objectFit = "cover";
          img.style.borderRadius = "8px";
          img.style.margin = "5px";

          preview.appendChild(img);

        } catch (error) {

          console.error(
            "Evidence preview error:",
            error
          );

        }

      }

    });

  }


  // ============================================================
  // SUBMIT COMPLAINT
  // ============================================================

  if (form) {

    form.addEventListener("submit", async function (event) {

      event.preventDefault();


      const formData =
        new FormData(form);


      // --------------------------------------------------------
      // CHECK USER
      // --------------------------------------------------------

      const user =
        JSON.parse(
          localStorage.getItem("user") || "null"
        );


      if (!user || !user.email) {

        alert(
          "Please login or signup before submitting a complaint."
        );

        return;

      }


      // --------------------------------------------------------
      // DESCRIPTION
      // --------------------------------------------------------

      const complaintText =
        String(
          formData.get("description") || ""
        ).trim();


      if (!complaintText) {

        alert(
          "Please enter your complaint description."
        );

        return;

      }


      // --------------------------------------------------------
      // LOCATION
      // --------------------------------------------------------

      const location =
        String(
          formData.get("location") || ""
        ).trim();


      // --------------------------------------------------------
      // AI ANALYSIS
      // --------------------------------------------------------

      let aiResult = null;


      try {

        const response =
          await fetch(
            "https://aquashield-ai-api.onrender.com/predict",
            {
              method: "POST",

              headers: {
                "Content-Type":
                  "application/json"
              },

              body: JSON.stringify({
                complaint:
                  complaintText
              })
            }
          );


        if (!response.ok) {

          throw new Error(
            "AI API request failed"
          );

        }


        aiResult =
          await response.json();


        console.log(
          "AquaShield AI Result:",
          aiResult
        );


      } catch (error) {

        console.error(
          "AI Error:",
          error
        );


        alert(
          "Complaint could not be analyzed by AquaShield AI.\n\n" +
          "Please make sure the AI service is running on port 8000."
        );

        return;

      }


      // --------------------------------------------------------
      // SAVE IMAGES
      // --------------------------------------------------------

      const images = [];


      if (input && input.files) {

        for (const file of input.files) {

          try {

            images.push(
              await toBase64(file)
            );

          } catch (error) {

            console.error(
              "Image error:",
              error
            );

          }

        }

      }


      // --------------------------------------------------------
      // GET EXISTING COMPLAINTS
      // --------------------------------------------------------

      let complaints = [];


      try {

        complaints =
          JSON.parse(
            localStorage.getItem(
              "complaints"
            ) || "[]"
          );

        if (!Array.isArray(complaints)) {

          complaints = [];

        }

      } catch (error) {

        complaints = [];

      }


      // --------------------------------------------------------
      // COMPLAINT ID
      // --------------------------------------------------------

      const complaintId =
        "AQ-" +
        Date.now()
          .toString(36)
          .toUpperCase()
          .slice(-7);


      // --------------------------------------------------------
      // TITLE
      // --------------------------------------------------------

      const title =
        String(
          formData.get("title") || ""
        ).trim() ||
        aiResult.category ||
        "Water / Flood Complaint";


      // --------------------------------------------------------
      // COMPLETE COMPLAINT OBJECT
      // --------------------------------------------------------

      const complaint = {

        id:
          complaintId,

        userEmail:
          user.email,

        userName:
          user.name ||
          "Citizen",

        title:
          title,

        description:
          complaintText,

        location:
          location ||
          "Location not provided",

        images:
          images,

        status:
          "Submitted",

        submittedAt:
          new Date().toISOString(),

        aiAnalysis: {

          category:
            aiResult.category ||
            "Waterlogging",

          department:
            aiResult.department ||
            "Municipal Administration",

          priority:
            aiResult.priority ||
            "Medium",

          severity:
            aiResult.severity ||
            "Medium"

        }

      };


      // --------------------------------------------------------
      // SAVE
      // --------------------------------------------------------

      complaints.unshift(
        complaint
      );


      localStorage.setItem(
        "complaints",
        JSON.stringify(
          complaints
        )
      );


      // VERY IMPORTANT:
      // Remember the last submitted complaint.
      localStorage.setItem(
        "lastComplaintId",
        complaintId
      );


      console.log(
        "AquaShield saved complaint:",
        complaint
      );


      // --------------------------------------------------------
      // SUCCESS MESSAGE
      // --------------------------------------------------------

      alert(
        "Complaint submitted successfully!\n\n" +

        "Complaint ID: " +
        complaintId +

        "\n\nCategory: " +
        complaint.aiAnalysis.category +

        "\nDepartment: " +
        complaint.aiAnalysis.department +

        "\nPriority: " +
        complaint.aiAnalysis.priority +

        "\nSeverity: " +
        complaint.aiAnalysis.severity +

        "\n\nStatus: Submitted"
      );


      // --------------------------------------------------------
      // OPEN GIS IN NEW TAB
      // --------------------------------------------------------

      const gisUrl =
        "http://localhost:8501/?" +

        "category=" +
        encodeURIComponent(
          complaint.aiAnalysis.category
        ) +

        "&title=" +
        encodeURIComponent(
          complaint.aiAnalysis.category
        );


      /*
       * IMPORTANT FIX:
       *
       * GIS opens in a NEW TAB.
       *
       * The current frontend tab stays on the
       * same origin, so localStorage remains
       * available to My Complaints.
       */

      window.open(
        gisUrl,
        "_blank"
      );


      // --------------------------------------------------------
      // OPEN MY COMPLAINTS IN CURRENT TAB
      // --------------------------------------------------------

      setTimeout(
        function () {

          window.location.href =
            "profile.html";

        },
        300
      );

    });

  }


  // ============================================================
  // TRACK RESULT
  // ============================================================

  const track =
    document.getElementById(
      "track-result"
    );


  if (track) {

    track.innerHTML =
      '<div class="muted">' +
      "Open My Complaints to view complaint IDs." +
      "</div>";

  }

})();