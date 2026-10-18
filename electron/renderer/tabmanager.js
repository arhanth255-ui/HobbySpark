
class EditorTabs {
    constructor(element) {
        this.element = typeof element === "string"
            ? document.querySelector(element)
            : element;

        if (!this.element) {
            throw new Error("Editor tabs element not found");
        }
        this.openFiles = [];
    }

    add(name) {
        if (this.openFiles.includes(name)){
            return;
        }
        const tab = document.createElement("button");
        tab.className = "editor-tab";
        tab.type = "button";

        const title = document.createElement("span");
        title.className = "tab-name"

        title.textContent = name;

        this.openFiles.push(name)

        const close = document.createElement("span");
        close.className = "tab-close";
        close.textContent = "×";
        close.addEventListener("click", (event)=>this.close(event));

        tab.append(title, close);
        this.element.appendChild(tab);

        return tab;
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
