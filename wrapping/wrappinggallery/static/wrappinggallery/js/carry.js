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
        star.classList.add('fa', 'fa-star', 'small-star');
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

// Function to update the label on slider move
function updateVoteText(category, rating) {
    if (category === "difficulty") {
        switch (rating) {
            case 0:
                return '?';
            case 1:
                return ': Beginner';
            case 2:
                return ': Beginner +';
            case 3:
                return ': Intermediate';
            case 4:
                return ': Advanced';
            case 5:
                return ': Guru';
        }
    } else if (category === "fancy") {
        switch (rating) {
            case 0:
                return '?';
            case 1:
                return ': 1/5';
            case 2:
                return ': 2/5';
            case 3:
                return ': 3/5';
            case 4:
                return ': 4/5';
            case 5:
                return ': 5/5';
        }
    } else {
        switch (rating) {
            case 0:
                return '?';
            case 1:
                return 'Avoid with';
            case 2:
                return 'Not great for';
            case 3:
                return 'Okay for';
            case 4:
                return 'Good for';
            case 5:
                return 'Great for';
        }
    }
}


function handleStarClick(stars, rating, title, category, hiddenInput) {

    console.log("handle", rating, title, category, hiddenInput);
    // Update the classes of the stars based on the clicked star
    stars.forEach((s, index) => {
        if (index < rating) {
            s.classList.remove('notchecked');
            s.classList.add('checked');
        } else {
            s.classList.remove('checked');
            s.classList.add('notchecked');
        }
    });

    // Update the rating text
    const textLabel = updateVoteText(category, rating);
    title.querySelector('span').textContent = textLabel; // Update the rating in the <p>

    // Update the hidden input value
    hiddenInput.value = rating; // Set the hidden input to the selected rating
}

document.querySelectorAll('.vote-group').forEach(voteGroup => {
    const stars = voteGroup.querySelectorAll('.fa-star');
    const title = voteGroup.previousElementSibling; // The <p> element
    const hiddenInput = voteGroup.querySelector('input[type="hidden"]'); // Get the hidden input

    const category = voteGroup.parentElement.dataset.property;

    stars.forEach(star => {
        star.addEventListener('click', function() {
            const rating = parseInt(this.getAttribute('data-value'));
            handleStarClick(stars, rating, title, category, hiddenInput); // Call the separate function on click
        });
    });
});


const stars = document.querySelectorAll('.star');
const ratingValue = document.getElementById('ratingValue');

// Function to update the star ratings based on user click
stars.forEach(star => {
    star.addEventListener('click', function() {
        const rating = parseInt(this.getAttribute('data-value'));
        updateStars(rating);
    });
});


function updateStars(rating) {
    stars.forEach(star => {
        star.classList.remove('filled'); // Clear existing filled stars
        if (parseInt(star.getAttribute('data-value')) <= rating) {
            star.classList.add('filled'); // Fill stars up to the selected rating
        }
    });
    ratingValue.textContent = rating; // Update the displayed rating
}


document.addEventListener('DOMContentLoaded', async function() { 
    // Add stars to the rating groups based on their data attributes
    const ratingGroups = document.querySelectorAll('.rating-group');
    ratingGroups.forEach(group => {
        addStarsToRatingGroup(group.id);
    });

    // Load images
    await loadTutorialImages();


    document.querySelectorAll('.vote-group').forEach(voteGroup => {
        const stars = voteGroup.querySelectorAll('.fa-star');
        const hiddenInput = voteGroup.querySelector('input[type="hidden"]'); 
        const title = voteGroup.previousElementSibling; // The <p> element
        const category = voteGroup.parentElement.dataset.property;
        
        // Call the function to set initial values based on the hidden input when the DOM loads
        const initialRating = parseInt(hiddenInput.value);
        if (initialRating) {
            handleStarClick(stars, initialRating, title, category, hiddenInput); // Set initial star ratings
        } else {
            handleStarClick(stars, 0, title, category, hiddenInput); // Set initial star ratings
        }
    });
});
