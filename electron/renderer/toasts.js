export function notify(message, type = "info", duration = 3000) {
    const container = document.getElementById("toast-container");

    const toast = document.createElement("div");

    toast.className = `toast ${type}`;
    toast.textContent = message;

    container.appendChild(toast);

    requestAnimationFrame(function () {
        toast.classList.add("show");
    });

    setTimeout(function () {
        toast.classList.remove("show");

        setTimeout(function () {
            toast.remove();
        }, 200);
    }, duration);
}

export function notifyError(message, duration=3000){
    notify(message, "error", duration)
} 
export function notifySuccess(message, duration=3000){
    notify(message, "success", duration)
} 
export function notifyWarning(message, duration=3000){
    notify(message, "warning", duration)
} 
