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
        // Insert star before the last span (text)
        ratingGroup.insertBefore(star, ratingGroup.lastElementChild);
    }
}

function updateFooterPosition() {
    releaseFooter();

    // print position of footer
    let element = document.querySelector('footer');
    elementPosition = 0;

    while(element) {
        elementPosition += element.offsetTop;
        element = element.offsetParent;
    }

    let viewportHeight = window.innerHeight;

    if (elementPosition < viewportHeight) {
        fixFooter();
    } else {
        releaseFooter();
    }
}

function releaseFooter() {
    const footer = document.querySelector('footer');
    footer.style.position = 'static'; // Reset to default position
    footer.style.bottom = 'auto'; // Reset to default value
    footer.style.width = 'auto'; // Reset to default width
}


function fixFooter() {
    const footer = document.querySelector('footer');
    footer.style.position = 'fixed'; 
    footer.style.bottom = '0';
    footer.style.width = '100%';
}


function hidePictureTutorialContainer() {
    const tutorialContent = document.getElementById('tutorial-content');
    tutorialContent.style.display = 'none';
}


async function loadTutorialImages() {
    const gridContainer = document.getElementById('imageGrid');
    const carryName = gridContainer.dataset.name;
    const bucketName = "tutorials";

    const response = await fetch(`/step-urls/${carryName}/?bucket=${bucketName}`);
    
    if (!response.ok) {
        return false;
    }

    const data = await response.json();

    let anyFound = false;
    for (const stepurl of data["urls"]) {
        anyFound = true;

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

    return anyFound;
}




document.addEventListener('DOMContentLoaded', async function() { 
    // Hide picture tutorial section if no tutorial available
    const found = await loadTutorialImages();
    if (!found) {
        hidePictureTutorialContainer();
    }


    // Add stars to the rating groups based on their data attributes
    const ratingGroups = document.querySelectorAll('.rating-group');
    ratingGroups.forEach(group => {
        addStarsToRatingGroup(group.id);
    });

    updateFooterPosition();
});
