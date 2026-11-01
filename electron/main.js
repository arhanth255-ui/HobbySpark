const { spawn } = require("node:child_process");
const fs = require("fs");
const { app, BrowserWindow, dialog, ipcMain } = require("electron");
const path = require("path");
const {
    startLanguageServer,
    stopLanguageServer
} = require("./lsp-connect.js");
const os = require("node:os");
const pty = require("node-pty");
const { execFile } = require("node:child_process");
const { promisify } = require("node:util");


let win;
function createWindow() {
    win = new BrowserWindow({
        width: 1136,
        height: 651,
        minWidth: 800,
        minHeight: 500,
        title: "HobbySpark",
        webPreferences: {
            preload: path.join(__dirname, "preload.js"),
            contextIsolation: true,
            nodeIntegration: false
        }
    });

    win.loadURL("http://127.0.0.1:5173");
}

ipcMain.handle("project:open-folder", async function () {
    var result = await dialog.showOpenDialog({
        title: "Open HobbySpark Project",
        properties: ["openDirectory"]
    });

    if (result.canceled) {
        return null;
    }

    return result.filePaths[0];
});

ipcMain.handle("project:read-folder", async function (event, folderPath) {
    var entries = await fs.promises.readdir(folderPath, {
        withFileTypes: true
    });

    var files = entries.map(function (entry) {
        return {
            name: entry.name,
            path: path.join(folderPath, entry.name),
            isDirectory: entry.isDirectory()
        };
    });

    return files;   
})


ipcMain.handle("file:read", async function (event, filePath) {
    return await fs.promises.readFile(filePath, "utf8");
});

ipcMain.handle("file:write", async function (event, filePath, contents) {
    await fs.promises.writeFile(filePath, contents, "utf8");
    return true;
});



const execFileAsync = promisify(execFile);

ipcMain.handle("project:get-com-ports", async function (event) {
    const result = await execFileAsync("arduino-cli", [
        "board", "list", "--format", "json"
    ]);

    return JSON.parse(result.stdout);
});





let terminalProcess = null;

function startTerminal() {
    if (terminalProcess) {
        return;
    }

    terminalProcess = pty.spawn("/bin/bash", ["-i"], {
        name: "xterm-256color",
        cols: 100,
        rows: 30,
        cwd: os.homedir(),
        env: {
            ...process.env,
            TERM: "xterm-256color",
            PS1: "\\[\\e[1;32m\\]\\u\\[\\e[0m\\]@\\[\\e[1;36m\\]\\h\\[\\e[0m\\]:\\[\\e[1;34m\\]\\w\\[\\e[0m\\]\\[\\e[1;33m\\]\\$\\[\\e[0m\\] "
        }
    });

    terminalProcess.onData(function (data) {
        if (win && !win.isDestroyed()) {
            win.webContents.send("terminal:data", data);
        }
    });

    terminalProcess.onExit(function (event) {
        terminalProcess = null;

        if (win && !win.isDestroyed()) {
            win.webContents.send("terminal:exit", event.exitCode);
        }
    });

    const runnerPath = path.resolve(
        __dirname,
        "../hobbyspark-cli-runner.py"
    );

    terminalProcess.write(
        `function hobbyspark() { python3 "${runnerPath}" "$@"; }\n`
    );
}



ipcMain.on("terminal:write", function (event, data, root = false) {
    if (root) {
        terminal.write(data)
    }
    console.log("Giving out data, ", data)
    terminalProcess.write(data);

});

ipcMain.on("terminal:resize", function (event, size) {
    if (
        terminalProcess &&
        Number.isInteger(size.cols) &&
        Number.isInteger(size.rows) &&
        size.cols > 0 &&
        size.rows > 0
    ) {
        terminalProcess.resize(size.cols, size.rows);
    }
});

ipcMain.on("terminal:start", function () {
    startTerminal();
});

function stopTerminal() {
    if (terminalProcess) {
        terminalProcess.kill();
        terminalProcess = null;
    }
}


app.whenReady().then(() => {
    startLanguageServer();
    startTerminal();
    createWindow();

    app.on("activate", () => {
        if (BrowserWindow.getAllWindows().length === 0) {
            createWindow();
        }
    });
});

app.on("window-all-closed", () => {
    stopLanguageServer();
    stopTerminal();
    if (process.platform !== "darwin") {
        app.quit();
    }
});
