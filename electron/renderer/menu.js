import { projectTree, startup } from "./app"
import { onClickOfNewFile, onClickOfOpenFolder } from "./menu-actions"
import { readFile, recent } from "./run-before-all"
import { onTranspileTest } from "./toolbar-buttons"

const openFolder = document.getElementById("open-folder")
const newFile = document.getElementById("new-file")
const openRecentFolder = document.getElementById("recent-folders")

const transpileTest = document.getElementById("transpile-test")

openFolder.addEventListener("click", onClickOfOpenFolder)
newFile.addEventListener("click", onClickOfNewFile)

transpileTest.addEventListener("click", onTranspileTest)



document.addEventListener("DOMContentLoaded", async function (ev) {
    const data = await readFile(recent);
    console.log("data is, ", data)

    for (const item of data.folders) {
        console.log("Got item!", item);
        const a = document.createElement("button")
        console.log("Added element, ", a)
        a.className = "dropdown-item"
        a.textContent = item
        openRecentFolder.appendChild(a)

        a.addEventListener("click", async function () {
            console.log("Item is in the function: ", item)
            projectTree.clear()
            await startup(null, item);
        })
    }
})