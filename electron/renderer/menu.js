import { onClickOfNewFile, onClickOfOpenFolder } from "./menu-actions"

const openFolder = document.getElementById("open-folder")
const newFile = document.getElementById("new-file")

openFolder.addEventListener("click", onClickOfOpenFolder)
newFile.addEventListener("click", onClickOfNewFile)