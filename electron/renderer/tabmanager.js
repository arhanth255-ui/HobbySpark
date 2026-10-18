import { openFile } from "./editor.js";
export class EditorTabs {
    constructor(element) {
        this.element = typeof element === "string"
            ? document.querySelector(element)
            : element;

        if (!this.element) {
            throw new Error("Editor tabs element not found");
        }
        this.openFiles = [];
        this.openFilesAndPaths = {};
    }

    add(name, path) {
        if (this.openFiles.includes(name)){
            return;
        }
        const tab = document.createElement("button");
        tab.className = "editor-tab";
        tab.type = "button";
        tab.addEventListener("click", async (event)=>{await this.onClick(event)})

        const title = document.createElement("span");
        title.className = "tab-name"

        title.textContent = name;

        this.openFiles.push(name)
        this.openFilesAndPaths[name] = path;

        const close = document.createElement("span");
        close.className = "tab-close";
        close.textContent = "×";
        close.addEventListener("click", (event)=>this.close(event));

        tab.append(title, close);
        this.element.appendChild(tab);

        return tab;
    }

    async onClick(event) {
        const tab = event.target.closest(".editor-tab");
        console.log("Clicked on ", tab)

        if (!tab) return;
        
        const name = tab.querySelector(".tab-name").textContent;
        console.log("Got name ", name)
        const path = this.openFilesAndPaths[name];
        await openFile(path)
        
    }

    close(event){
        const tab = event.target.parentElement;
        const name = tab.querySelector(".tab-name")
        const index = this.openFiles.indexOf(name.textContent);

        if (index !== -1) {
            this.openFiles.splice(index, 1);
            console.log("Removed", name.textContent)
        }

        tab.remove()

    }
}
