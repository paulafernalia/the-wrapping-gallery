function addStarsToRatingGroup(groupId) {
    // Find the rating group by ID
    const ratingGroup = document.getElementById(groupId);
    if (!ratingGroup) return;

    // Get the number of checked stars from the data attribute
    const checkedStars = parseInt(ratingGroup.dataset.property, 10);
    if (isNaN(checkedStars)) return;

    // Create the stars
    for (let i = 0; i < 5; i++) {
        const star = document.createElement('span');
        star.classList.add('fa', 'fa-star');
        if (i < checkedStars) {
            star.classList.add('checked');
        } else {
            star.classList.add('notchecked');
        }
        // Append the star to the rating group
        ratingGroup.appendChild(star);
    }
}


function hidePictureTutorialContainer() {
    const tutorialContent = document.getElementById('tutorial-content');
    tutorialContent.style.display = 'none';
}


async function loadTutorialImages() {
    const gridContainer = document.getElementById('imageGrid');
    const carryName = gridContainer.dataset.name;
    const bucketName = "tutorials";

    const loadingSpinner = document.getElementById('loadingSpinner');
    loadingSpinner.style.display = 'block';


    const response = await fetch(`/step-urls/${carryName}/?bucket=${bucketName}`, {
        method: 'GET',
        headers: {
            'X-Requested-With': 'XMLHttpRequest',  // Custom header to identify AJAX request
        }
    });
    
    if (!response.ok) {
        return;
    }

    const data = await response.json();
    if (data["urls"].length == 0) {
        hidePictureTutorialContainer();
    }

    for (const stepurl of data["urls"]) {

        // Create grid item for image
        const gridItem = document.createElement('div');
        gridItem.className = 'grid-item';

        // Create image, set url and append to grid item
        const img = document.createElement('img');
        img.src = stepurl;
        gridItem.appendChild(img);

        // Append grid item to grid container
        gridContainer.appendChild(gridItem);
    }

    loadingSpinner.style.display = 'none';
}




document.addEventListener('DOMContentLoaded', async function() { 
    // Add stars to the rating groups based on their data attributes
    const ratingGroups = document.querySelectorAll('.rating-group');
    ratingGroups.forEach(group => {
        addStarsToRatingGroup(group.id);
    });

    // Load images
    await loadTutorialImages();

});
