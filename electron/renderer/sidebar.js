const explorerButton = document.getElementById("explorer-button")
const arduinoButton =  document.getElementById("arduino-button")

const explorer = document.getElementById("project-tree")
const arduino = document.getElementById("arduino-panel")
arduino.hidden = true

export let current = "exp";

explorerButton.addEventListener("click", function (ev){
    if (explorerButton.classList.contains("selected")){
        return;
    }
    else {
        arduinoButton.classList.remove("selected")
        explorerButton.classList.add("selected")
        arduino.hidden = true
        explorer.hidden = false
        let current = "exp";
    }
})

arduinoButton.addEventListener("click", function (ev){
    if (arduinoButton.classList.contains("selected")){
        return;
    }
    else {
        explorerButton.classList.remove("selected")
        arduinoButton.classList.add("selected")
        arduino.hidden=false
        explorer.hidden=true
        let current = "ard";
    }
})