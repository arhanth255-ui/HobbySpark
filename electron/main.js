const fs = require("fs");
const { app, BrowserWindow, dialog, ipcMain } = require("electron");
const path = require("path");


function createWindow() {
    const win = new BrowserWindow({
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


app.whenReady().then(() => {
    createWindow();

    app.on("activate", () => {
        if (BrowserWindow.getAllWindows().length === 0) {
            createWindow();
        }
    });
});

app.on("window-all-closed", () => {
    if (process.platform !== "darwin") {
        app.quit();
    }
});
