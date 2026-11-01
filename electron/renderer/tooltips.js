function updateTooltipPosition(element) {
    const rect = element.getBoundingClientRect();

    const space = {
        top: rect.top,
        bottom: window.innerHeight - rect.bottom,
        left: rect.left,
        right: window.innerWidth - rect.right
    };

    const tooltipWidth = 120;
    const tooltipHeight = 30;
    const gap = 8;

    let position = "bottom";

    if (space.bottom >= tooltipHeight + gap) {
        position = "bottom";
    } else if (space.top >= tooltipHeight + gap) {
        position = "top";
    } else if (space.right >= tooltipWidth + gap) {
        position = "right";
    } else if (space.left >= tooltipWidth + gap) {
        position = "left";
    }

    element.dataset.tooltipPosition = position;
}

document.addEventListener("mouseover", function (event) {
    const element = event.target.closest("[data-tooltip]");

    if (element) {
        updateTooltipPosition(element);
    }
});