let pageSize = 100;
let resultsPage = 1;

const booleanProps = [
    'fancy', 'pretied', 'newborns', 'legstraighteners', 'leaners', 'pregnancy',
    'bigkids', 'feeding', 'quickups', 'rings', 'pass_sling', 
    'pass_ruck', 'pass_kangaroo', 'pass_cross', 'pass_reinforcing_cross', 
    'pass_reinforcing_horizontal', 'pass_horizontal', 'pass_poppins', 
    'other_chestpass', 'other_bunchedpasses', 'other_shoulderflip', 
    'other_twistedpass', 'other_waistband', 'other_legpasses', 
    'other_s2s', 'other_eyelet', 'other_sternum', 'other_poppins',
    'no_pass_sling',
    'no_pass_ruck', 'no_pass_kangaroo', 'no_pass_cross',
    'no_pass_reinforcing_cross', 'no_pass_reinforcing_horizontal',
    'no_pass_horizontal', 'no_pass_poppins',
    'no_other_chestpass', 'no_other_bunchedpasses', 'no_other_shoulderflip', 
    'no_other_twistedpass', 'no_other_waistband', 'no_other_legpasses', 
    'no_other_s2s', 'no_other_eyelet', 'no_other_sternum', 'no_other_poppins'
];

async function fetchFileUrl(fileName, position) {
    try {
        const response = await fetch(`/file-url/${fileName}/?position=${position}`);
        const data = await response.json();
        return data.url;
    } catch (error) {
        return null;
    }
}

async function fetchFilteredCarries(page = 1, pageSize = 18, size, position) {
    let sizes = [size];
    const difficulties = ["Any"];
    const filters = {"position": position};
    
    // Build the query string from the filters object
    const queryString = Object.entries(filters)
        .map(([property, value]) => `property[]=${encodeURIComponent(property)}&value[]=${encodeURIComponent(value)}`)
        .concat(sizes.map(val => `size[]=${encodeURIComponent(val)}`))  // Add size separately
        .concat(`difficulty[]=Any`)  // Add difficulty separately
        .join('&');

    // Add pagination parameters to the query string
    const paginationParams = `page=${encodeURIComponent(page)}&page_size=${encodeURIComponent(pageSize)}`;

    // Combine filters and pagination parameters
    const fullQueryString = `${queryString}&${paginationParams}`;

    // Filter carries by using filter values
    const response = await fetch(`/api/filter-carries/?${fullQueryString}`);

    if (!response.ok) {
        throw new Error('Network response was not ok');
    }

    const data = await response.json();
    return data.carries;
}


function handleMouseEnter(event, carry, hoverLabel) {
    const rect = event.currentTarget.getBoundingClientRect();
    hoverLabel.style.left = `${rect.left + window.scrollX}px`;
    hoverLabel.style.top = `${rect.top + window.scrollY - 40}px`;
    hoverLabel.style.display = 'block'; // Show the label
    hoverLabel.textContent = carry.carry__title;
}

function handleMouseLeave(hoverLabel) {
    hoverLabel.style.display = 'none'; // Hide the label
}


function isLargeScreenDevice() {
    return window.innerWidth > 1024; // Example threshold for laptops/desktops
}


function handleGridItemClick(gridItem, carry, baseUrlPattern) {
    const hasBeenClicked = isLargeScreenDevice() ? true : gridItem.dataset.clicked === 'true';

    if (!hasBeenClicked) {
        // Show the hover label
        const hoverLabel = document.querySelector('.hover-label');
        const rect = gridItem.getBoundingClientRect();
        hoverLabel.style.left = `${rect.left + window.scrollX}px`;
        hoverLabel.style.top = `${rect.top + window.scrollY - 40}px`;
        hoverLabel.style.display = 'block'; // Show the label
        hoverLabel.textContent = carry.carry__title;

        // Mark the gridItem as clicked
        gridItem.dataset.clicked = 'true';
    } else {
        // Redirect to the constructed URL
        const url = `${baseUrlPattern}${carry.carry__name}`;

        // Deselect tabs
        document.querySelector('.nav-link[data-page="carries-page"]').classList.remove('active');
        document.querySelector('.nav-link[data-page="faq-page"]').classList.remove('active');

        // Redirect to the constructed URL
        window.location.href = url;
    }
}

// Function to handle "Mark as done" action
async function addCarryAsDone(carryName, gridItem, img, overlay, addCircle) {
    loadingSpinner.style.display = 'block';
    
    const formData = new FormData();
    const csrfToken = document.querySelector('input[name="csrfmiddlewaretoken"]').value;
    formData.append('csrfmiddlewaretoken', csrfToken);

    try {
        // Make an AJAX POST request to mark the carry as done
        fetch(`/mark-done/${carryName}/`, {
            method: 'POST',
            body: formData,
            headers: {
                'X-CSRFToken': formData.get('csrfmiddlewaretoken'), // Pass CSRF token
            }
        })
        .then(response => response.json())
        .then(data => {
            // Add achievements to congrats box
            if (data.unlocked_achievements.length > 0) {
                loadCongratsBox(data.unlocked_achievements);
                createConfetti();
            }
        })
        .catch(error => console.error('Error:', error));

        // Update the UI: Remove opacity, show shadow, and remove "+" icon
        img.style.opacity = '1';
        gridItem.classList.add("shadow");
        gridItem.style.border = "1px solid lightgrey";
        gridItem.removeChild(overlay);
        gridItem.removeChild(addCircle); // Remove the "+" icon
    } catch (error) {
        console.error("Error marking carry as done:", error);
    }

    loadingSpinner.style.display = 'none';
}

async function loadMyCarries(size, position) {
    const gridContainer = document.querySelector(`.card-grid[data-size="${size}"][data-position="${position}"]`);
    gridContainer.innerHTML = '';

    const baseUrlPattern = gridContainer.dataset.baseUrlPattern.replace('PLACEHOLDER', '');

    const loadingSpinner = document.getElementById('loadingSpinner');
    loadingSpinner.style.display = 'block';

    resultsPage = 1;
    const carries = await fetchFilteredCarries(resultsPage, pageSize, size, position);

    // Create a hover label element outside the loop
    const hoverLabel = document.createElement('div');
    hoverLabel.className = 'hover-label poppins-regular'; // Class for styling the label
    hoverLabel.style.display = 'none'; // Hide by default
    document.body.appendChild(hoverLabel); // Append hover label to body

    // Create an array of promises to fetch all image URLs
    for (const carry of carries) {
        // Create grid item
        const gridItem = document.createElement('div');
        gridItem.className = 'card-grid-item clickable-grid-item';

        // Check if carry is done
        const isDone = carriesInfo[position][size].includes(carry.carry__name);

        let fileUrl = await fetchFileUrl(carry.carry__name, carry.carry__position);

        const img = document.createElement('img');
        img.src = fileUrl;
        img.alt = carry.carry__title;
        img.loading = 'lazy'; // Enable lazy loading
        img.className = 'grid-item'; // Optional: Add class for styling

        if (!isDone) {
            img.style.opacity = '0.5'; // Set opacity of the image to 50%

            // Create overlay
            const overlay = document.createElement('div');
            overlay.classList.add('overlay'); // Add the overlay class to the div
            gridItem.appendChild(overlay);
            gridItem.style.border = "none";

            // Create the "+" circle button and append it to the grid item
            const addCircle = document.createElement('div');
            addCircle.className = 'add-circle'; // Style using the same CSS class as in the example
            addCircle.innerHTML = '<i class="fa fa-plus"></i>'; // Add the "+" icon

            // Separate the click handler
            addCircle.onclick = function(event) {
                event.stopPropagation(); // Prevent the click from bubbling up to the grid item
                addCarryAsDone(carry.carry__name, gridItem, img, overlay, addCircle);
            };

            gridItem.appendChild(addCircle); // Append the circle to the grid item
        } else {
            gridItem.classList.add("shadow");
        }

        // Append image and description container to grid item
        gridItem.appendChild(img);

        // Event listeners for hover and click
        gridItem.addEventListener('mouseenter', (event) => {
            handleMouseEnter(event, carry, hoverLabel);
        });

        // Event listeners for hover and click
        gridItem.addEventListener('mouseleave', () => {
            handleMouseLeave(hoverLabel);
        });
        gridItem.addEventListener('click', () => handleGridItemClick(gridItem, carry, baseUrlPattern));

        // Append grid item to fragment
        gridContainer.appendChild(gridItem);
    };

    
    loadingSpinner.style.display = 'none';
}


async function toggleGroup(iconElement) {
    const size = iconElement.getAttribute('data-size');
    const position = iconElement.getAttribute('data-position');

    const carriesGroup = document.querySelector(`.collapsable[data-size="${size}"][data-position="${position}"]`);
    const imageGrid = document.querySelector(`.card-grid[data-size="${size}"][data-position="${position}"]`);
    
    if (carriesGroup.style.display === "none") {
        carriesGroup.style.display = "block";
        iconElement.classList.remove("fa-caret-right");
        iconElement.classList.add("fa-caret-down");
    } else {
        carriesGroup.style.display = "none";
        iconElement.classList.remove("fa-caret-down");
        iconElement.classList.add("fa-caret-right");
    }

    // Load images
    await loadMyCarries(size, position);
    updateFooterPosition();
}



document.addEventListener('DOMContentLoaded', async function() {    
    updateFooterPosition();
});
