import { runHobbySparkCommand } from "./app";
import { Terminal } from "@xterm/xterm";
import { FitAddon } from "@xterm/addon-fit";
import "@xterm/xterm/css/xterm.css";

var terminalElement = document.getElementById("console-output");

var terminal = new Terminal({
    cursorBlink: true,
    fontSize: 13,
    fontFamily: '"JetBrains Mono", "Fira Code", monospace',
    theme: {
        background: "#111216",
        foreground: "#d4d4d4",
        cursor: "#a6e3a1",
        selectionBackground: "#454955"
    },
    scrollback: 5000
});

var fitAddon = new FitAddon();
terminal.loadAddon(fitAddon);
terminal.open(terminalElement);

function fitTerminal() {
    fitAddon.fit();

    window.hobbySpark.resizeTerminal({
        cols: terminal.cols,
        rows: terminal.rows
    });
}

window.hobbySpark.onTerminalData(function (data) {
    terminal.write(data);
});

window.hobbySpark.onTerminalExit(function (code) {
    terminal.write("\r\n[Shell exited: " + code + "]\r\n");
});

var commandBuffer = "";

terminal.onData(function (data) {
    if (data === "\r") {
        var command = commandBuffer.trim();
        commandBuffer = "";

        if (command === "hobbyspark" ||
            command.startsWith("hobbyspark ")) {
            window.hobbySpark.writeTerminal("\r\n");

            runHobbySparkCommand(command);
            return;
        }

        window.hobbySpark.writeTerminal(data);
        return;
    }

    if (data === "\u007f" || data === "\b") {
        if (commandBuffer.length > 0) {
            commandBuffer = commandBuffer.slice(0, -1);
        }

        window.hobbySpark.writeTerminal(data);
        return;
    }

    if (!data.startsWith("\u001b") && data.length === 1) {
        commandBuffer += data;
    } else if (data.length > 1) {
        commandBuffer = "";
    }

    window.hobbySpark.writeTerminal(data);
});

window.addEventListener("resize", fitTerminal);

terminal.attachCustomKeyEventHandler(function (event) {
    if (
        event.type === "keydown" &&
        event.ctrlKey &&
        event.shiftKey &&
        event.code === "KeyC"
    ) {
        var selection = terminal.getSelection();

        if (selection) {
            navigator.clipboard.writeText(selection);
            return false;
        }
    }

    return true;
});

window.hobbySpark.startTerminal();

requestAnimationFrame(function () {
    fitTerminal();
    terminal.focus();
});
