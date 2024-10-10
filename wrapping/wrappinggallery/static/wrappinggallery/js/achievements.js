async function fetchAchievementFileUrl(achievementName) {
    try {
        const response = await fetch(`/achievement-file-url/${achievementName}`);
        const data = await response.json();
        return data.url;
    } catch (error) {
        return null;
    }
}


function showHoverLabel(item, hoverLabel, hoverTitle, hoverDescription) {
    // Set the title and description
    hoverTitle.textContent = item.getAttribute('data-title');
    hoverDescription.textContent = item.getAttribute('data-description'); // Assuming you have this data attribute
    
    // Move hover label near the achievement badge
    const rect = item.getBoundingClientRect();
    hoverLabel.style.left = `${rect.left + window.scrollX}px`;
    hoverLabel.style.top = `${rect.top + window.scrollY - 40}px`;
    hoverLabel.style.display = 'block'; // Show the label
}


// Function to hide the hover label
function hideHoverLabel(hoverLabel) {
    hoverLabel.style.display = 'none'; // Hide the label
}


async function updateGridItem(item) {
    const img = item.querySelector('img');
    if (item.dataset.done === "True") {
        try {
            // Get URL of the achievement illustration
            let fileUrl = await fetchAchievementFileUrl(item.dataset.name);

            // Update image
            img.src = fileUrl;
        } catch (error) {
            console.error('Error fetching file URL:', error);
        }
    } else {
        item.style.padding = "20px";
        img.style.opacity = "0.2";
    }
}

document.addEventListener('DOMContentLoaded', async function() {
    const gridItems = document.querySelectorAll('.achievement-grid-item');
    const hoverLabel = document.querySelector('.hover-label');
    const hoverTitle = hoverLabel.querySelector('.hover-title');
    const hoverDescription = hoverLabel.querySelector('.hover-description');

    for (const item of gridItems) {
        updateGridItem(item);
    }

    // Add event listeners for grid items
    gridItems.forEach(item => {
        item.addEventListener('mouseenter', function() {
            showHoverLabel(item, hoverLabel, hoverTitle, hoverDescription);
        });

        item.addEventListener('mouseleave', function() {
            hideHoverLabel(hoverLabel);
        });
        
        // Add click event to show the hover label
        item.addEventListener('click', function() {
            showHoverLabel(item, hoverLabel, hoverTitle, hoverDescription);
        });
    });
});