var filesAndFolders;
var folderPath;
const editorTabs = new EditorTabs("#editor-tabs");
let projectTree;


async function startApp() {
    folderPath = await window.hobbySpark.openProjectFolder();

    if (folderPath === null) {
        console.log("No project folder selected.");
        return;
    }

    console.log("Selected project:", folderPath);
    
    filesAndFolders = await window.hobbySpark.listFilesAndFolders(folderPath);
    console.log("Received:", filesAndFolders);
    console.log("Type:", typeof filesAndFolders);
    console.log("Is array:", Array.isArray(filesAndFolders));
}
function getPathName(path) {
    return path.split(/[\\/]/).pop();
}

async function add(folderPath, root = null) {
    var items = await window.hobbySpark.listFilesAndFolders(folderPath);

    for (var item of items) {
        if (!item.isDirectory) {
            projectTree.addFile(item.name, root);
        } else {
            projectTree.addFolder(item.name, root);
            await add(item.path, item.name);
        }
    }
}

document.addEventListener("DOMContentLoaded", async function () {
    await startApp();
    projectTree = new Tree("#project-tree", getPathName(folderPath));
    await add(folderPath, projectTree.root_name);
});

console.log("Type of files", typeof filesAndFolders)


editorTabs.add("main.hsp");
editorTabs.add("boards.json");
editorTabs.add("README.md");





