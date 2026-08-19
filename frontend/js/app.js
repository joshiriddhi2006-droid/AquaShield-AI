// ============================================================
// AQUASHIELD - CLIENT SIDE AUTH + COMPLAINT MANAGEMENT
// ============================================================

(function () {

  const authLink =
    document.getElementById("auth-link");


  // ============================================================
  // CURRENT USER
  // ============================================================

  function currentUser() {

    try {

      return JSON.parse(
        localStorage.getItem("user") || "null"
      );

    } catch (error) {

      console.error(
        "User storage error:",
        error
      );

      return null;

    }

  }


  // ============================================================
  // GET ALL COMPLAINTS
  // ============================================================

  function getComplaints() {

    try {

      const complaints =
        JSON.parse(
          localStorage.getItem("complaints") || "[]"
        );

      return Array.isArray(complaints)
        ? complaints
        : [];

    } catch (error) {

      console.error(
        "Complaint storage error:",
        error
      );

      return [];

    }

  }


  // ============================================================
  // UPDATE LOGIN / LOGOUT LINK
  // ============================================================

  function updateAuthLinks() {

    if (!authLink) return;

    const user =
      currentUser();


    if (user) {

      authLink.textContent =
        "Logout";

      authLink.href =
        "#";

    } else {

      authLink.textContent =
        "Login";

      authLink.href =
        "login.html";

    }

  }


  // ============================================================
  // ESCAPE HTML
  // Prevents complaint text from breaking the page
  // ============================================================

  function escapeHTML(value) {

    if (
      value === null ||
      value === undefined
    ) {

      return "";

    }


    return String(value)

      .replace(/&/g, "&amp;")

      .replace(/</g, "&lt;")

      .replace(/>/g, "&gt;")

      .replace(/"/g, "&quot;")

      .replace(/'/g, "&#039;");

  }


  // ============================================================
  // PRIORITY BADGE
  // ============================================================

  function priorityBadge(priority) {

    const value =
      String(
        priority || "Medium"
      ).toLowerCase();


    if (value === "high") {

      return `
        <span
          style="
            display:inline-block;
            padding:5px 10px;
            border-radius:999px;
            background:#fee2e2;
            color:#dc2626;
            font-size:12px;
            font-weight:700;
          "
        >
          HIGH
        </span>
      `;

    }


    if (value === "low") {

      return `
        <span
          style="
            display:inline-block;
            padding:5px 10px;
            border-radius:999px;
            background:#dcfce7;
            color:#16a34a;
            font-size:12px;
            font-weight:700;
          "
        >
          LOW
        </span>
      `;

    }


    return `
      <span
        style="
          display:inline-block;
          padding:5px 10px;
          border-radius:999px;
          background:#fef3c7;
          color:#d97706;
          font-size:12px;
          font-weight:700;
        "
      >
        MEDIUM
      </span>
    `;

  }


  // ============================================================
  // STATUS BADGE
  // ============================================================

  function statusBadge(status) {

    const value =
      String(
        status || "Submitted"
      );


    const lower =
      value.toLowerCase();


    let background =
      "#dbeafe";

    let color =
      "#2563eb";


    if (
      lower.includes("resolved") ||
      lower.includes("closed")
    ) {

      background =
        "#dcfce7";

      color =
        "#16a34a";

    }

    else if (
      lower.includes("review") ||
      lower.includes("progress")
    ) {

      background =
        "#fef3c7";

      color =
        "#d97706";

    }


    return `
      <span
        style="
          display:inline-block;
          padding:5px 10px;
          border-radius:999px;
          background:${background};
          color:${color};
          font-size:12px;
          font-weight:700;
        "
      >
        ${escapeHTML(value)}
      </span>
    `;

  }


  // ============================================================
  // RENDER SINGLE COMPLAINT
  // ============================================================

  function complaintCard(complaint) {

    const analysis =
      complaint.aiAnalysis || {};


    const category =
      analysis.category ||
      complaint.category ||
      "Water / Flood Complaint";


    const department =
      analysis.department ||
      complaint.department ||
      "Municipal Administration";


    const priority =
      analysis.priority ||
      complaint.priority ||
      "Medium";


    const severity =
      analysis.severity ||
      complaint.severity ||
      "Medium";


    const status =
      complaint.status ||
      "Submitted";


    const location =
      complaint.location ||
      "Location not provided";


    const description =
      complaint.description ||
      complaint.title ||
      "Complaint details not available";


    let dateText =
      "";


    if (complaint.submittedAt) {

      try {

        dateText =
          new Date(
            complaint.submittedAt
          ).toLocaleString(
            "en-IN",
            {
              dateStyle: "medium",
              timeStyle: "short"
            }
          );

      } catch (error) {

        dateText =
          "";

      }

    }


    return `

      <article
        class="complaint-card"
        style="
          background:#ffffff;
          border:1px solid #dbe3ee;
          border-radius:16px;
          padding:20px;
          box-shadow:0 4px 14px rgba(15,23,42,0.06);
          margin-bottom:16px;
        "
      >

        <!-- TOP -->

        <div
          style="
            display:flex;
            justify-content:space-between;
            align-items:flex-start;
            gap:15px;
            flex-wrap:wrap;
          "
        >

          <div>

            <div
              style="
                color:#0284c7;
                font-size:11px;
                font-weight:800;
                letter-spacing:.5px;
                margin-bottom:6px;
              "
            >
              AQUASHIELD COMPLAINT
            </div>


            <h3
              style="
                margin:0;
                color:#0f172a;
                font-size:18px;
                font-weight:800;
              "
            >
              ${escapeHTML(category)}
            </h3>

          </div>


          <div>

            ${statusBadge(status)}

          </div>

        </div>


        <!-- ID -->

        <div
          style="
            margin-top:12px;
            padding:10px 12px;
            background:#f8fafc;
            border-radius:9px;
            color:#475569;
            font-size:12px;
          "
        >

          <strong>Complaint ID:</strong>

          ${escapeHTML(
            complaint.id || "Not available"
          )}

        </div>


        <!-- DETAILS -->

        <div
          style="
            display:grid;
            grid-template-columns:repeat(auto-fit,minmax(180px,1fr));
            gap:12px;
            margin-top:14px;
          "
        >

          <div
            style="
              padding:12px;
              background:#f0f9ff;
              border-radius:10px;
            "
          >

            <div
              style="
                font-size:11px;
                color:#64748b;
                font-weight:700;
              "
            >
              LOCATION
            </div>

            <div
              style="
                margin-top:4px;
                color:#0f172a;
                font-size:13px;
                font-weight:700;
              "
            >
              📍 ${escapeHTML(location)}
            </div>

          </div>


          <div
            style="
              padding:12px;
              background:#f0fdf4;
              border-radius:10px;
            "
          >

            <div
              style="
                font-size:11px;
                color:#64748b;
                font-weight:700;
              "
            >
              DEPARTMENT
            </div>

            <div
              style="
                margin-top:4px;
                color:#0f172a;
                font-size:13px;
                font-weight:700;
              "
            >
              ${escapeHTML(department)}
            </div>

          </div>


          <div
            style="
              padding:12px;
              background:#fffbeb;
              border-radius:10px;
            "
          >

            <div
              style="
                font-size:11px;
                color:#64748b;
                font-weight:700;
              "
            >
              PRIORITY
            </div>

            <div
              style="
                margin-top:6px;
              "
            >
              ${priorityBadge(priority)}
            </div>

          </div>


          <div
            style="
              padding:12px;
              background:#fef2f2;
              border-radius:10px;
            "
          >

            <div
              style="
                font-size:11px;
                color:#64748b;
                font-weight:700;
              "
            >
              SEVERITY
            </div>

            <div
              style="
                margin-top:4px;
                color:#0f172a;
                font-size:13px;
                font-weight:700;
              "
            >
              ${escapeHTML(severity)}
            </div>

          </div>

        </div>


        <!-- DESCRIPTION -->

        <div
          style="
            margin-top:15px;
            padding-top:14px;
            border-top:1px solid #e2e8f0;
          "
        >

          <div
            style="
              font-size:11px;
              color:#64748b;
              font-weight:700;
              margin-bottom:5px;
            "
          >
            COMPLAINT
          </div>


          <div
            style="
              color:#334155;
              font-size:13px;
              line-height:1.6;
            "
          >
            ${escapeHTML(description)}
          </div>

        </div>


        <!-- DATE -->

        ${
          dateText
            ? `
              <div
                style="
                  margin-top:14px;
                  color:#94a3b8;
                  font-size:11px;
                "
              >
                <i class="fa-regular fa-clock"></i>
                Submitted: ${escapeHTML(dateText)}
              </div>
            `
            : ""
        }

      </article>

    `;

  }


  // ============================================================
  // RENDER PROFILE
  // ============================================================

  function renderProfile() {

    const user =
      currentUser();


    const name =
      document.getElementById(
        "user-name"
      );


    const email =
      document.getElementById(
        "user-email"
      );


    const list =
      document.getElementById(
        "user-complaints"
      );


    if (!list) return;


    const all =
      getComplaints();


    /*
     * IMPORTANT FIX
     *
     * Normally we show complaints belonging
     * to the logged-in citizen.
     *
     * If the browser has switched between
     * localhost and 127.0.0.1 and the user
     * session is unavailable, we still show
     * the locally saved complaints so the
     * hackathon demo does not look broken.
     */

    let mine = [];


    if (
      user &&
      user.email
    ) {

      if (name) {

        name.textContent =
          user.name ||
          "Citizen";

      }


      if (email) {

        email.textContent =
          user.email;

      }


      mine =
        all.filter(
          complaint =>
            String(
              complaint.userEmail || ""
            ).toLowerCase() ===
            String(
              user.email
            ).toLowerCase()
        );

    }


    /*
     * Fallback for local demo.
     */

    if (
      mine.length === 0 &&
      all.length > 0
    ) {

      mine =
        all;

      if (name) {

        name.textContent =
          user?.name ||
          "AquaShield Citizen";

      }


      if (email) {

        email.textContent =
          user?.email ||
          "Local complaint history";

      }

    }


    // ----------------------------------------------------------
    // EMPTY STATE
    // ----------------------------------------------------------

    if (
      mine.length === 0
    ) {

      list.innerHTML = `

        <div
          style="
            background:#ffffff;
            border:1px solid #dbe3ee;
            border-radius:16px;
            padding:40px 20px;
            text-align:center;
          "
        >

          <div
            style="
              width:58px;
              height:58px;
              margin:0 auto 14px;
              border-radius:50%;
              background:#e0f2fe;
              color:#0284c7;
              display:flex;
              align-items:center;
              justify-content:center;
              font-size:22px;
            "
          >

            <i
              class="fa-solid fa-file-circle-question"
            ></i>

          </div>


          <h3
            style="
              margin:0;
              font-size:17px;
              font-weight:800;
              color:#0f172a;
            "
          >
            No complaints found
          </h3>


          <p
            style="
              margin:6px 0 0;
              color:#64748b;
              font-size:13px;
            "
          >
            Register a complaint through AquaShield AI
            to see it here.
          </p>

        </div>

      `;

      return;

    }


    // ----------------------------------------------------------
    // RENDER COMPLAINTS
    // ----------------------------------------------------------

    list.innerHTML =
      mine
        .map(
          complaintCard
        )
        .join("");

  }


  // ============================================================
  // INDEX COMPLAINTS
  // ============================================================

  function renderIndexComplaints() {

    const element =
      document.getElementById(
        "complaint-list"
      );


    if (!element) return;


    const user =
      currentUser();


    const all =
      getComplaints();


    if (!user) {

      element.innerHTML =
        "Please log in to see complaints.";

      return;

    }


    const mine =
      all.filter(
        complaint =>
          complaint.userEmail ===
          user.email
      );


    if (
      mine.length === 0
    ) {

      element.innerHTML =
        '<div class="muted">No complaints yet.</div>';

      return;

    }


    element.innerHTML =
      mine
        .map(
          complaint =>
            `
              <div class="card">

                <strong>
                  ${escapeHTML(
                    complaint.title ||
                    complaint.aiAnalysis?.category ||
                    "Complaint"
                  )}
                </strong>

                <div class="muted">

                  ID:
                  ${escapeHTML(
                    complaint.id
                  )}

                  • Status:

                  ${escapeHTML(
                    complaint.status ||
                    "Submitted"
                  )}

                </div>

              </div>
            `
        )
        .join("");

  }


  // ============================================================
  // SIGNUP
  // ============================================================

  const signup =
    document.getElementById(
      "signup-form"
    );


  if (signup) {

    signup.addEventListener(
      "submit",
      function (event) {

        event.preventDefault();


        const formData =
          new FormData(
            signup
          );


        const user = {

          name:
            formData.get(
              "name"
            ),

          email:
            formData.get(
              "email"
            ),

          password:
            formData.get(
              "password"
            )

        };


        localStorage.setItem(
          "user",
          JSON.stringify(
            user
          )
        );


        alert(
          "Account created and signed in."
        );


        updateAuthLinks();


        location.href =
          "profile.html";

      }
    );

  }


  // ============================================================
  // LOGIN
  // ============================================================

  const login =
    document.getElementById(
      "login-form"
    );


  if (login) {

    login.addEventListener(
      "submit",
      function (event) {

        event.preventDefault();


        const formData =
          new FormData(
            login
          );


        const stored =
          currentUser();


        if (
          stored &&
          stored.email ===
            formData.get("email") &&
          stored.password ===
            formData.get("password")
        ) {

          localStorage.setItem(
            "user",
            JSON.stringify(
              stored
            )
          );


          alert(
            "Signed in successfully."
          );


          updateAuthLinks();


          location.href =
            "profile.html";

        }

        else {

          alert(
            "Invalid credentials or user does not exist. Please sign up first."
          );

        }

      }
    );

  }


  // ============================================================
  // LOGOUT
  // ============================================================

  if (authLink) {

    authLink.addEventListener(
      "click",
      function (event) {

        const user =
          currentUser();


        if (!user) return;


        event.preventDefault();


        localStorage.removeItem(
          "user"
        );


        updateAuthLinks();


        location.href =
          "index.html";

      }
    );

  }


  // ============================================================
  // INITIALIZE
  // ============================================================

  updateAuthLinks();

  renderIndexComplaints();

  renderProfile();


})();