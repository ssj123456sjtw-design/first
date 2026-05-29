document.addEventListener("DOMContentLoaded", () => {
    const fetchBtn = document.getElementById("fetch-btn");
    const consoleBox = document.getElementById("console-box");
    const jsonOutput = document.getElementById("json-output");
    const responseTime = document.getElementById("response-time");

    if (fetchBtn) {
        fetchBtn.addEventListener("click", async () => {
            const startTime = performance.now();
            fetchBtn.disabled = true;
            fetchBtn.innerText = "Querying API...";

            try {
                const response = await fetch("/api/health");
                const data = await response.json();
                const endTime = performance.now();
                const duration = (endTime - startTime).toFixed(1);

                // Show console
                consoleBox.classList.add("visible");
                
                // Set text
                jsonOutput.textContent = JSON.stringify(data, null, 2);
                responseTime.textContent = `Response time: ${duration}ms`;
            } catch (error) {
                consoleBox.classList.add("visible");
                jsonOutput.textContent = `Error fetching API: ${error.message}`;
                responseTime.textContent = "";
            } finally {
                fetchBtn.disabled = false;
                fetchBtn.innerText = "Test Health Check API";
            }
        });
    }

    // Feature 1: Image loading logic
    const picFetchBtn = document.getElementById("pic-fetch-btn");
    const picNameInput = document.getElementById("pic-name-input");
    const imagePreview = document.getElementById("image-preview");
    const picPlaceholder = document.getElementById("pic-placeholder");

    if (picFetchBtn) {
        picFetchBtn.addEventListener("click", () => {
            const picName = picNameInput.value.trim();
            if (!picName) {
                picPlaceholder.textContent = "Please enter a valid picture name.";
                picPlaceholder.style.display = "block";
                imagePreview.style.display = "none";
                return;
            }

            picPlaceholder.textContent = "Loading image...";
            picPlaceholder.style.display = "block";
            imagePreview.style.display = "none";

            // Load via feature1 route
            imagePreview.src = `/feature1/${encodeURIComponent(picName)}`;
            
            imagePreview.onload = () => {
                picPlaceholder.style.display = "none";
                imagePreview.style.display = "block";
            };

            imagePreview.onerror = () => {
                picPlaceholder.textContent = `Error loading image "${picName}". (File not found or access denied)`;
                picPlaceholder.style.display = "block";
                imagePreview.style.display = "none";
            };
        });
    }

    // Feature 2: Text file reading logic
    const txtFetchBtn = document.getElementById("txt-fetch-btn");
    const txtNameInput = document.getElementById("txt-name-input");
    const textPreviewOutput = document.getElementById("text-preview-output");

    if (txtFetchBtn) {
        txtFetchBtn.addEventListener("click", async () => {
            const fileName = txtNameInput.value.trim();
            if (!fileName) {
                textPreviewOutput.textContent = "Please enter a valid file name.";
                return;
            }

            textPreviewOutput.textContent = "Loading file content...";
            txtFetchBtn.disabled = true;

            try {
                const response = await fetch(`/feature2/${encodeURIComponent(fileName)}`);
                if (response.ok) {
                    const text = await response.text();
                    textPreviewOutput.textContent = text;
                } else {
                    const text = await response.text();
                    // Extract error description if available
                    textPreviewOutput.textContent = `Error ${response.status}: ${response.statusText}\n${text}`;
                }
            } catch (error) {
                textPreviewOutput.textContent = `Network Error: ${error.message}`;
            } finally {
                txtFetchBtn.disabled = false;
            }
        });
    }

    // Feature 4: CPU Stress Test Logic
    const cpuStressCard = document.getElementById("cpu-stress-card");
    const cpuStressBtn = document.getElementById("cpu-stress-btn");
    const cpuBtnText = document.getElementById("cpu-btn-text");
    const cpuCoresSelect = document.getElementById("cpu-cores-select");
    const cpuDurationSelect = document.getElementById("cpu-duration-select");
    const cpuProgressWrapper = document.getElementById("cpu-progress-wrapper");
    const cpuStatusText = document.getElementById("cpu-status-text");
    const cpuTimerText = document.getElementById("cpu-timer-text");
    const cpuProgressFill = document.getElementById("cpu-progress-fill");
    const cpuLogOutput = document.getElementById("cpu-log-output");

    if (cpuStressBtn) {
        let isStressing = false;
        let pollInterval = null;
        let countdownInterval = null;
        let startStressTime = null;
        let totalDuration = 10;

        function getTimestamp() {
            const now = new Date();
            return now.toTimeString().split(' ')[0];
        }

        function log(message) {
            const time = getTimestamp();
            const currentLogs = cpuLogOutput.textContent;
            if (currentLogs.startsWith("[System Idle]")) {
                cpuLogOutput.textContent = `[${time}] ${message}`;
            } else {
                cpuLogOutput.textContent = `${currentLogs}\n[${time}] ${message}`;
            }
            // Auto-scroll to bottom of log
            const logContainer = cpuLogOutput.closest('.cpu-log-container');
            if (logContainer) {
                logContainer.scrollTop = logContainer.scrollHeight;
            }
        }

        function setControlsDisabled(disabled) {
            cpuCoresSelect.disabled = disabled;
            cpuDurationSelect.disabled = disabled;
        }

        function resetUI() {
            isStressing = false;
            clearInterval(pollInterval);
            clearInterval(countdownInterval);
            pollInterval = null;
            countdownInterval = null;

            // Restore buttons and classes
            cpuStressBtn.className = "btn-stress-idle";
            cpuStressBtn.querySelector(".btn-icon").textContent = "⚡";
            cpuBtnText.textContent = "Start CPU Stress Test";
            cpuStressCard.classList.remove("stressing-active");
            cpuProgressWrapper.style.display = "none";
            cpuProgressFill.style.width = "0%";
            
            setControlsDisabled(false);
        }

        function enterStressingState(cores, duration, elapsed = 0) {
            isStressing = true;
            totalDuration = duration;
            setControlsDisabled(true);

            // Update UI components
            cpuStressBtn.className = "btn-stressing";
            cpuStressBtn.querySelector(".btn-icon").textContent = "⏹";
            cpuBtnText.textContent = "Stop CPU Stress Test";
            cpuStressCard.classList.add("stressing-active");
            cpuProgressWrapper.style.display = "block";

            // Initialize progress bar
            const remaining = Math.max(0, duration - elapsed);
            cpuTimerText.textContent = `${remaining.toFixed(1)}s`;
            cpuProgressFill.style.width = `${(elapsed / duration) * 100}%`;

            startStressTime = Date.now() - (elapsed * 1000);

            // Fast, high-fidelity local timer countdown (updates every 100ms for smooth bar movement)
            clearInterval(countdownInterval);
            countdownInterval = setInterval(() => {
                const now = Date.now();
                const msElapsed = now - startStressTime;
                const secElapsed = msElapsed / 1000;
                const secRemaining = Math.max(0, totalDuration - secElapsed);

                cpuTimerText.textContent = `${secRemaining.toFixed(1)}s`;
                
                const percentage = Math.min(100, (secElapsed / totalDuration) * 100);
                cpuProgressFill.style.width = `${percentage}%`;

                if (secRemaining <= 0) {
                    clearInterval(countdownInterval);
                }
            }, 100);

            // Server synchronizer polling (every 1.5 seconds)
            clearInterval(pollInterval);
            pollInterval = setInterval(syncStatus, 1500);
        }

        async function syncStatus() {
            try {
                const response = await fetch("/api/cpu/stress/status");
                if (response.ok) {
                    const data = await response.json();
                    if (data.status === "stressing") {
                        // Sync our timer if it deviates too far
                        const localElapsed = (Date.now() - startStressTime) / 1000;
                        const serverElapsed = data.duration - data.remaining_time;
                        if (Math.abs(localElapsed - serverElapsed) > 1.0) {
                            startStressTime = Date.now() - (serverElapsed * 1000);
                        }
                    } else if (data.status === "idle" && isStressing) {
                        log("Stress test duration completed.");
                        log("System returning to idle.");
                        resetUI();
                    }
                }
            } catch (error) {
                console.error("Error polling CPU stress status:", error);
            }
        }

        // Action when button is clicked
        cpuStressBtn.addEventListener("click", async () => {
            if (isStressing) {
                // STOP stress command
                log("Requested stop. Terminating stress processes...");
                cpuStressBtn.disabled = true;
                try {
                    const response = await fetch("/api/cpu/stress/stop", { method: "POST" });
                    if (response.ok) {
                        const data = await response.json();
                        log("Stress test aborted by user.");
                        log("All background workers terminated.");
                    } else {
                        log("Failed to stop stress test cleanly.");
                    }
                } catch (error) {
                    log(`Error stopping stress test: ${error.message}`);
                } finally {
                    cpuStressBtn.disabled = false;
                    resetUI();
                }
            } else {
                // START stress command
                const cores = parseInt(cpuCoresSelect.value);
                const duration = parseInt(cpuDurationSelect.value);

                log(`Requesting CPU stress test...`);
                log(`Configured cores: ${cores}, duration: ${duration}s`);
                cpuStressBtn.disabled = true;

                try {
                    const response = await fetch("/api/cpu/stress/start", {
                        method: "POST",
                        headers: { "Content-Type": "application/json" },
                        body: JSON.stringify({ cores, duration })
                    });

                    if (response.ok) {
                        const data = await response.json();
                        log(`Successfully spawned ${cores} backend stress workers.`);
                        log(`Warning: System CPU utilization will now rise!`);
                        enterStressingState(cores, duration);
                    } else {
                        const errText = await response.text();
                        log(`Error starting stress test: ${errText}`);
                    }
                } catch (error) {
                    log(`Network Error: ${error.message}`);
                } finally {
                    cpuStressBtn.disabled = false;
                }
            }
        });

        // Proactive initialization check on page load
        // This recovers UI state if a stress test is currently running on refresh!
        async function checkInitialState() {
            try {
                const response = await fetch("/api/cpu/stress/status");
                if (response.ok) {
                    const data = await response.json();
                    if (data.status === "stressing") {
                        const elapsed = data.duration - data.remaining_time;
                        log(`Reconnected to active stress session (${data.requested_cores} cores, ${data.remaining_time}s remaining).`);
                        enterStressingState(data.requested_cores, data.duration, elapsed);
                    }
                }
            } catch (e) {
                console.error("Initial CPU state check failed:", e);
            }
        }

        // Trigger state recovery check
        checkInitialState();
    }
});
