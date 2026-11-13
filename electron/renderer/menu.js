import { projectTree, startup } from "./app"
import { onClickOfNewFile, onClickOfOpenFolder } from "./menu-actions"
import { readFile, recent } from "./run-before-all"
import { onLex, onTranspileTest, onParse, onTranspile } from "./toolbar-buttons"

const openFolder = document.getElementById("open-folder")
const newFile = document.getElementById("new-file")
const openRecentFolder = document.getElementById("recent-folders")

const undo = document.getElementById("undo")
const redo = document.getElementById("redo")
const cut = document.getElementById("cut")
const copy = document.getElementById("copy")
const paste = document.getElementById("paste")

const transpileTest = document.getElementById("transpile-test")
const lex = document.getElementById("lex")
const parse = document.getElementById("parse")
const transpile = document.getElementById("transpile")

const devToolsButton = document.getElementById("dev-tools")
const fullscreenButton = document.getElementById("full-screen")
const reloadButton = document.getElementById("reload-window")

openFolder.addEventListener("click", onClickOfOpenFolder)
newFile.addEventListener("click", onClickOfNewFile)

paste.addEventListener("click", function (ev) { window.hobbySpark.doFunc("paste") })
cut.addEventListener("click", function (ev) { window.hobbySpark.doFunc("cut") })
copy.addEventListener("click", function (ev) { window.hobbySpark.doFunc("copy") })
redo.addEventListener("click", function (ev) { window.hobbySpark.doFunc("redo") })
undo.addEventListener("click", function (ev) { window.hobbySpark.doFunc("undo") })

transpileTest.addEventListener("click", onTranspileTest)
lex.addEventListener("click", onLex)
parse.addEventListener("click", onParse)
transpile.addEventListener("click", onTranspile)

devToolsButton.addEventListener("click", () => {
    window.electronAPI.toggleDevTools()
})

fullscreenButton.addEventListener("click", () => {
    window.electronAPI.toggleFullscreen()
})

reloadButton.addEventListener("click", () => {
    window.electronAPI.reload()
})




document.addEventListener("DOMContentLoaded", async function (ev) {
    const data = await readFile(recent);
    console.log("data is, ", data)
    let alreadyAdded = [];
    if (data.folders.length === 0) {
        console.log("There's no data")

    }
    else {
        for (const item of data.folders) {
            if (alreadyAdded.includes(item)) {
                continue;
            }
            else {
                document.getElementById("none").remove()
                console.log("Got item!", item);
                alreadyAdded.push(item)
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
        }
    }
})