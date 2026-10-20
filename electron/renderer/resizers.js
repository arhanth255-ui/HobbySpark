
var work = document.querySelector(".work");
var sidebar = document.getElementById("project-tree");
var editorPanel = document.querySelector(".editor-panel");
var terminal = document.getElementById("console-panel");

function makeResizer(element, onMove) {
    if (!element) {
        console.error("HobbySpark resizer: required element not found.");
        return;
    }

    var dragging = false;

    element.addEventListener("pointerdown", function (event) {
        dragging = true;
        element.classList.add("dragging");
        element.setPointerCapture(event.pointerId);
        document.body.style.userSelect = "none";
        event.preventDefault();
    });

    element.addEventListener("pointermove", function (event) {
        if (dragging) {
            onMove(event);
        }
    });

    function stopDragging() {
        dragging = false;
        element.classList.remove("dragging");
        document.body.style.userSelect = "";
    }

    element.addEventListener("pointerup", stopDragging);
    element.addEventListener("pointercancel", stopDragging);
}

if (!work || !sidebar || !editorPanel || !terminal) {
    console.error(
        "HobbySpark resizers: .work, #project-tree, .editor-panel, or #console-panel is missing."
    );
} else {
    // Create the tree divider without changing the existing tree contents.
    var treeResizer = document.createElement("div");
    treeResizer.id = "sidebar-resizer";
    treeResizer.className = "resizer";
    treeResizer.setAttribute("role", "separator");
    treeResizer.setAttribute("aria-orientation", "vertical");

    work.insertBefore(treeResizer, editorPanel);

    // Create the terminal divider without changing the editor or terminal.
    var terminalResizer = document.createElement("div");
    terminalResizer.id = "terminal-resizer";
    terminalResizer.className = "resizer horizontal";
    terminalResizer.setAttribute("role", "separator");
    terminalResizer.setAttribute("aria-orientation", "horizontal");

    terminal.parentNode.insertBefore(terminalResizer, terminal);

    // Resize the project tree horizontally.
    makeResizer(treeResizer, function (event) {
        var bounds = work.getBoundingClientRect();
        var width = event.clientX - bounds.left;

        width = Math.max(150, Math.min(500, width));

        sidebar.style.flex = "0 0 " + width + "px";
        sidebar.style.width = width + "px";
    });

    // Resize the terminal vertically.
    makeResizer(terminalResizer, function (event) {
        var availableHeight = terminal.parentElement.getBoundingClientRect().height;
        var bounds = terminal.parentElement.getBoundingClientRect();
        var height = bounds.bottom - event.clientY;

        height = Math.max(80, Math.min(availableHeight - 100, height));

        terminal.style.flex = "0 0 " + height + "px";

        // Notify xterm.js so its terminal grid can be resized.
        window.dispatchEvent(new Event("resize"));
    });
}
