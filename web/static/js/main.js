document.addEventListener("DOMContentLoaded", function () {
  const searchInput = document.getElementById("search-input");
  const searchButton = document.getElementById("search-button");
  const resultsList = document.getElementById("results-list");
  const resultsCount = document.getElementById("results-count");
  const searchTime = document.getElementById("search-time");
  const techniqueButtons = document.querySelectorAll(".technique-btn");
  const processButtons = document.querySelectorAll(".process-btn");
  const visualizationArea = document.getElementById("visualization-area");

  let currentMode = "combined";
  let currentProcessFilter = "all";

  techniqueButtons.forEach((button) => {
    button.addEventListener("click", function () {
      techniqueButtons.forEach((btn) => btn.classList.remove("active"));
      this.classList.add("active");

      currentMode = this.dataset.mode;

      if (searchInput.value.trim()) {
        performSearch();
      }
    });
  });

  processButtons.forEach((button) => {
    button.addEventListener("click", function () {
      processButtons.forEach((btn) => btn.classList.remove("active"));
      this.classList.add("active");

      currentProcessFilter = this.dataset.technique;

      updateVisualization();
    });
  });

  searchButton.addEventListener("click", function () {
    performSearch();
    visualizeProcess();
  });

  searchInput.addEventListener("keypress", function (e) {
    if (e.key === "Enter") {
      performSearch();
      visualizeProcess();
    }
  });

  function performSearch() {
    const query = searchInput.value.trim();

    if (!query) {
      return;
    }

    resultsList.innerHTML = `
            <div class="loading">
                <div class="loading-spinner"></div>
                <p>Searching...</p>
            </div>
        `;

    fetch("/search", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        query: query,
        mode: currentMode,
      }),
    })
      .then((response) => response.json())
      .then((data) => {
        displayResults(data);
      })
      .catch((error) => {
        console.error("Error:", error);
        resultsList.innerHTML = `
                <div class="no-results">
                    An error occurred while searching. Please try again.
                </div>
            `;
      });
  }

  function visualizeProcess() {
    const query = searchInput.value.trim();

    if (!query) {
      return;
    }

    visualizationArea.innerHTML = `
            <div class="loading">
                <div class="loading-spinner"></div>
                <p>Analyzing search process...</p>
            </div>
        `;

    fetch("/process", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        query: query,
      }),
    })
      .then((response) => response.json())
      .then((data) => {
        processData = data;
        updateVisualization();
      })
      .catch((error) => {
        console.error("Error:", error);
        visualizationArea.innerHTML = `
                <div class="visualization-placeholder">
                    An error occurred while visualizing the process. Please try again.
                </div>
            `;
      });
  }

  let processData = null;

  function updateVisualization() {
    if (
      !processData ||
      !processData.processes ||
      processData.processes.length === 0
    ) {
      visualizationArea.innerHTML = `
                <div class="visualization-placeholder">
                    Enter a search query to visualize the search process
                </div>
            `;
      return;
    }

    let html = "";

    const processes = processData.processes.filter(
      (p) =>
        currentProcessFilter === "all" || p.technique === currentProcessFilter
    );

    processes.forEach((process) => {
      html += `
                <div class="process-panel ${process.technique}">
                    <div class="process-header">
                        <h4>
                            <span class="process-icon"></span>
                            ${capitalizeFirstLetter(
                              process.technique
                            )} Search Process
                        </h4>
                    </div>
                    <div class="process-steps">
            `;

      process.steps.forEach((step, index) => {
        html += `
                    <div class="process-step" style="animation-delay: ${
                      index * 0.2
                    }s">
                        <div class="step-name">${index + 1}. ${step.name}</div>
                        <div class="step-description">${step.description}</div>
                    </div>
                `;
      });

      html += `
                    </div>
                </div>
            `;
    });

    visualizationArea.innerHTML = html;
  }

  // Display results function
  function displayResults(data) {
    const results = data.results;
    resultsCount.textContent = `(${results.length})`;
    searchTime.textContent = data.search_time;

    if (results.length === 0) {
      resultsList.innerHTML = `
                <div class="no-results">
                    No results found for "${data.query}".
                </div>
            `;
      return;
    }

    let resultsHTML = "";

    results.forEach((result) => {
      resultsHTML += `
                <div class="result-item">
                    <div class="result-content">
                        ${result.content}
                    </div>
                    <div class="result-meta">
                        <div>
                            <span class="result-technique technique-${result.technique}">${result.technique}</span>
                            <span>Doc #${result.doc_id}</span>
                        </div>
                        <div>Score: ${result.score}</div>
                    </div>
                </div>
            `;
    });

    resultsList.innerHTML = resultsHTML;
  }

  function capitalizeFirstLetter(string) {
    return string.charAt(0).toUpperCase() + string.slice(1);
  }

  document.querySelectorAll(".search-tips strong").forEach((tip) => {
    tip.parentElement.style.cursor = "pointer";
    tip.parentElement.addEventListener("click", function () {
      searchInput.value = this.querySelector("strong").textContent;
      performSearch();
      visualizeProcess();
    });
  });
});
