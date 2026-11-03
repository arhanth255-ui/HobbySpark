import { debugPrint, readFile, recent, writeData } from "./run-before-all.js";
import { EditorTabs } from "./tabmanager.js";
import { notify } from "./toasts.js";
import { Tree } from "./tree.js";
export let folderPath;
export const editorTabs = new EditorTabs("#editor-tabs");
export let projectTree;



async function startApp() {
    folderPath = await window.hobbySpark.openProjectFolder();

    if (folderPath === null) {
        console.log("No project folder selected.");
        return;
    }

    console.log("Selected project:", folderPath);
}



export function getPathName(path) {
    if (typeof path !== "string" || path.length === 0) {
        return "";
    }

    return path.split("/").pop();
}

async function add(path, root = null) {
    console.log("Folder is ", path)
    var items = await window.hobbySpark.listFilesAndFolders(await path);
    items.sort(function (a, b) {
        if (a.isDirectory && !b.isDirectory) { return -1 }
        if (!a.isDirectory && b.isDirectory) { return 1 }
        return a.name.localeCompare(b.name)
    });

    for (var item of items) {
        if (!item.isDirectory) {
            projectTree.addFile(item.name, item.path, root);
        } else {
            projectTree.addFolder(item.name, root);
            await add(item.path, item.name);
        }
    }

}

export async function startup(ev, folder = null) {
    console.log("G")
    if (folder === null) { console.log("G"); await startApp(); }
    else {
        folderPath = folder;
        console.log("Folder is, ", folderPath);
    }
    projectTree = new Tree("#project-tree", editorTabs, getPathName(folderPath));
    console.log("Folder is from start, ", folderPath)
    if (folderPath !== null) { window.hobbySpark.writeTerminal("cd \"" + folderPath + "\"\n") }
    await add(folderPath, projectTree.root_name);
    projectTree.closeAllFolders()
    window.hobbySpark.onSessionRequest(async function () {
        debugPrint("Closing");

        let now = await readFile(recent);
        console.log("Now is ", now)


        now.folders.push(folderPath);

        writeData(recent, now);

        return { debug: true }
    });
}

document.addEventListener("DOMContentLoaded", startup);



console.log("Type of files", typeof filesAndFolders)
var portSelector = document.getElementById("port-selector");

async function loadPorts() {
    var result = await window.hobbySpark.getPorts();

    portSelector.innerHTML = "";

    for (const item of result.detected_ports ?? []) {
        var address = item.port.address;
        var option = document.createElement("option");

        option.value = address;
        option.textContent = address;

        portSelector.appendChild(option);
    }
}
loadPorts()

debugPrint("Started here")












