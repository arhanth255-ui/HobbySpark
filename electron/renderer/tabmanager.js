import { openFile, clearEditor, saveFile } from "./editor.js";
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
        this.active;
        this.historyOfActive = [];
        this.closed = [];
    }

    async add(name, path) {
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
        close.addEventListener("click", async function (event) {
            event.stopPropagation();
            await this.close(event);
        }.bind(this));

        tab.append(title, close);
        this.element.appendChild(tab);
        await openFile(path)
        this.active = name;
        const previous = this.historyOfActive.indexOf(name);
        if (previous !== -1) {
            this.historyOfActive.splice(previous, 1);
        }

        this.historyOfActive.push(name);
        
        return tab;
    }

    async onClick(event=null) {
        if (!event.target|| !event.target.isConnected) {
            return;
        }
        
        const tab = event.target.closest(".editor-tab");
        if (!tab) return;
        
        const name = tab.querySelector(".tab-name").textContent;
        this.active = name;
        const previous = this.historyOfActive.indexOf(name);

        if (previous !== -1) {
            this.historyOfActive.splice(previous, 1);
        }

        this.historyOfActive.push(name);
        
        console.log("Clicked on ", tab)

        
        console.log("Got name ", name)
        const path = this.openFilesAndPaths[name];
        await openFile(path)
        
    }

    async close(event){
        const tab = event.target.parentElement;
        const name = tab.querySelector(".tab-name")
        const index = this.openFiles.indexOf(name.textContent);

        if (index !== -1) {
            this.openFiles.splice(index, 1);
            console.log("Removed", name.textContent)
        }
        this.closed.push(name.textContent)
        delete this.openFilesAndPaths[name.textContent];
        this.historyOfActive = this.historyOfActive.filter(
            function (fileName) {
                return fileName !== name.textContent;
            }
        );

        if (this.active===name.textContent){
            let toOpen;
            let before = this.historyOfActive.indexOf(name.textContent);

            while (before > 0) {
                before--;
                const candidate = this.historyOfActive[before];

                if (
                    !this.closed.includes(candidate) &&
                    this.openFiles.includes(candidate)
                ) {
                    toOpen = candidate;
                    break;
                }
            }

            if (toOpen) {
                await openFile(this.openFilesAndPaths[toOpen]);
            } else {
                await clearEditor();
            }
        }
        tab.remove()
        

    }
    async saveCurrentFile(){
        await saveFile(this.openFilesAndPaths[this.active]);
        return this.openFilesAndPaths[this.active]
    }
}
