import { editorTabs } from "./app.js";
import { notify, notifyError } from "./toasts.js";

// ── DOM elements ──────────────────────────────────────────────

const build = document.getElementById("build-button");
const upload = document.getElementById("upload-button");
const run = document.getElementById("run-button")

const boardSelector = document.getElementById("board-selector");
const portSelector = document.getElementById("port-selector");

// ── Icons ─────────────────────────────────────────────────────

const STOP_ICON = "./assets/icons/primitive-square.svg";

// ── Command state ─────────────────────────────────────────────

let activeButton = null;
let originalIcon = null;
let originalTooltip = null;
let commandRunning = false;
let command = null;

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

    button.classList.add("stop-button");

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

    activeButton.classList.remove("stop-button");

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
    resetButton();
}

export function onTranspileTest() {
    const file = editorTabs.active
    if (!file) {
        notifyError("Please open a tab before transpile-testing the file.");
        return;
    }
    window.hobbySpark.writeTerminal(
        `hobbyspark transpile-test "${file}" \n`
    );
    command = "transpile-testing"
    notify("Tranpile-test started");
}

export function onLex() {
    const file = editorTabs.active
    if (!file) {
        notifyError("Please open a tab before lexing the file.");
        return;
    }
    window.hobbySpark.writeTerminal(
        `hobbyspark lex "${file}" \n`
    );
    command = "lexing"
    notify("Lexing started");
}

export function onParse() {
    const file = editorTabs.active
    if (!file) {
        notifyError("Please open a tab before parsing the file.");
        return;
    }
    window.hobbySpark.writeTerminal(
        `hobbyspark parse "${file}" \n`
    );
    command = "Parsing"
    notify("Parsing started");
}

function onRun() {
    if (commandRunning) {
        if (activeButton === run) {
            onStop();
        }

        return;
    }

    const file = editorTabs.active;

    if (!file) {
        notifyError("Please open a tab before running the file.");
        return;
    }

    if (!setButtonRunning(run)) {
        return;
    }

    window.hobbySpark.writeTerminal(
        `hobbyspark run "${file}" \n`
    );
    command = "running"
    notify("Run started");
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

    command = "compiling"
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
    command = "upload"
    notify("Upload started");
}

// ── Event listeners ──────────────────────────────────────────

build.addEventListener("click", onBuild);
upload.addEventListener("click", onUpload);
run.addEventListener("click", onRun)

// ── Command completion ────────────────────────────────────────

// This callback must be implemented in your preload.js.
// It should fire when your renderer detects the CLI completion marker.
console.log("RENDERER: Registering completion listener");

window.hobbySpark.assignHobbySparkCommand(function (exitCode) {
    console.log("RENDERER: CALLBACK RECEIVED:", exitCode);

    if (command !== "transpile-testing") { resetButton(); }

    if (exitCode === 0) {
        notify(`Successfully finished ${command}!`);
    } else {
        notifyError(`Operation failed (exit code: ${exitCode}).`);
    }
});
