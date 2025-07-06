document.getElementById("analyzeBtn").addEventListener("click", async () => {
  const url = document.getElementById("urlInput").value.trim();
  if (!url) {
    alert("Please enter a valid URL.");
    return;
  }

  document.getElementById("performanceMetrics").innerHTML = "";
  document.getElementById("securityMetrics").innerHTML = "";
  document.getElementById("resultContainer").classList.remove("hidden");

  document.getElementById("performanceMetrics").innerHTML = `<div class="loader">Analyzing...</div>`;
  document.getElementById("securityMetrics").innerHTML = `<div class="loader">Analyzing...</div>`;

  try {
    const response = await fetch("http://127.0.0.1:8000/analyze", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ url }),
    });

    const result = await response.json();
    document.getElementById("performanceMetrics").innerHTML = "";
    document.getElementById("securityMetrics").innerHTML = "";

    // PERFORMANCE METRICS
    if (result.performance) {
      for (const [key, value] of Object.entries(result.performance)) {
        const card = document.createElement("div");
        card.className = "card";
        card.innerHTML = `<h3>${key.replace(/_/g, " ")}</h3><p>${value} ms</p>`;
        document.getElementById("performanceMetrics").appendChild(card);
      }
    }

    // SECURITY METRICS
    if (result.security) {
      const sec = result.security;

      // CERTIFICATE VALIDITY
      if (sec.https_certificate_validity) {
        const cert = sec.https_certificate_validity;
        const certCard = document.createElement("div");
        certCard.className = "card";
        certCard.innerHTML = `
          <h3>Certificate Validity</h3>
          <p><strong>Valid From:</strong> ${cert.valid_from}</p>
          <p><strong>Valid To:</strong> ${cert.valid_to}</p>
        `;

        // If issuer exists
        if (cert.issuer) {
          cert.issuer.forEach((item) => {
            const group = item.map(
              (pair) =>
                `<p><strong>${pair[0]}</strong>: ${pair[1]}</p>`
            ).join("");
            certCard.innerHTML += group;
          });
        }

        document.getElementById("securityMetrics").appendChild(certCard);
      }

      // SECURE HEADERS
      if (sec.secure_headers_status) {
        for (const [key, value] of Object.entries(sec.secure_headers_status)) {
          const headerCard = document.createElement("div");
          headerCard.className = "card";

          // If value is object → stringify it prettily, else print directly
          const displayValue = typeof value === "object"
            ? `<pre>${JSON.stringify(value, null, 2)}</pre>`
            : `${value}`;

          headerCard.innerHTML = `<h3>${key}</h3><p>${displayValue}</p>`;
          document.getElementById("securityMetrics").appendChild(headerCard);
        }
      }
    }

  } catch (error) {
    console.error(error);
    alert("Error analyzing website: " + error);
  }
});
