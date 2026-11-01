import { editorTabs } from "./app.js";
import { notify, notifyError } from "./toasts.js";

// ── DOM elements ──────────────────────────────────────────────

const build = document.getElementById("build-button");
const upload = document.getElementById("upload-button");

const boardSelector = document.getElementById("board-selector");
const portSelector = document.getElementById("port-selector");

// ── Icons ─────────────────────────────────────────────────────

const STOP_ICON = "./assets/icons/primitive-square.svg";

// ── Command state ─────────────────────────────────────────────

let activeButton = null;
let originalIcon = null;
let originalTooltip = null;
let commandRunning = false;

// ── Button management ─────────────────────────────────────────

function setButtonRunning(button) {
    if (commandRunning) {
        return false;
    }

    const img = button.querySelector("img");

    if (!img) {
        console.error("Toolbar button has no image:", button.id);
        return false;
    }

    activeButton = button;
    originalIcon = img.getAttribute("src");
    originalTooltip = button.dataset.tooltip;

    img.setAttribute("src", STOP_ICON);
    button.dataset.tooltip = "Stop";

    commandRunning = true;

    return true;
}

function resetButton() {
    if (!activeButton) {
        return;
    }

    const img = activeButton.querySelector("img");

    img.setAttribute("src", originalIcon);
    activeButton.dataset.tooltip = originalTooltip;

    activeButton = null;
    originalIcon = null;
    originalTooltip = null;

    commandRunning = false;
}

// ── Stop operation ────────────────────────────────────────────

function onStop() {
    if (!commandRunning) {
        return;
    }

    window.hobbySpark.writeTerminal("\x03");

    notify("Stopping operation...");
}

// ── Build ─────────────────────────────────────────────────────

function onBuild() {
    if (commandRunning) {
        if (activeButton === build) {
            onStop();
        }

        return;
    }

    const file = editorTabs.active;
    const board = boardSelector.value;

    if (!file) {
        notifyError("Please open a tab before building the file.");
        return;
    }

    if (!board) {
        notifyError("Please select a board.");
        return;
    }

    if (!setButtonRunning(build)) {
        return;
    }

    window.hobbySpark.writeTerminal(
        `hobbyspark build "${file}" "${board}"\n`
    );

    notify("Build started");
}

// ── Upload ────────────────────────────────────────────────────

function onUpload() {
    if (commandRunning) {
        if (activeButton === upload) {
            onStop();
        }

        return;
    }

    const file = editorTabs.active;
    const board = boardSelector.value;
    const port = portSelector.value;

    if (!file) {
        notifyError("Please open a tab before uploading.");
        return;
    }

    if (!board) {
        notifyError("Please select a board.");
        return;
    }

    if (!port) {
        notifyError("Please connect your microcontroller and select its port.");
        return;
    }

    if (!setButtonRunning(upload)) {
        return;
    }

    window.hobbySpark.writeTerminal(
        `hobbyspark upload "${file}" "${board}" "${port}"\n`
    );

    notify("Upload started");
}

// ── Event listeners ──────────────────────────────────────────

build.addEventListener("click", onBuild);
upload.addEventListener("click", onUpload);

// ── Command completion ────────────────────────────────────────

// This callback must be implemented in your preload.js.
// It should fire when your renderer detects the CLI completion marker.
console.log("RENDERER: Registering completion listener");

window.hobbySpark.assignHobbySparkCommand(function (exitCode) {
    console.log("RENDERER: CALLBACK RECEIVED:", exitCode);

    resetButton();

    if (exitCode === 0) {
        notify("Operation completed successfully!");
    } else {
        notifyError(`Operation failed (exit code: ${exitCode}).`);
    }
});
