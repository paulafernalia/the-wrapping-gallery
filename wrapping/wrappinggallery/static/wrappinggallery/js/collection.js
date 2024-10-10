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


function handleMouseEnter(event, carryTitle) {
    const hoverLabel = document.querySelector('.hover-label');
    const rect = event.currentTarget.getBoundingClientRect();

    hoverLabel.style.left = `${rect.left + window.scrollX}px`;
    hoverLabel.style.top = `${rect.top + window.scrollY - 40}px`;
    hoverLabel.style.display = 'block'; // Show the label
    hoverLabel.textContent = carryTitle;
}

function handleMouseLeave() {
    const hoverLabel = document.querySelector('.hover-label');
    hoverLabel.style.display = 'none'; // Hide the label
}


function isLargeScreenDevice() {
    return window.innerWidth > 1024; // Example threshold for laptops/desktops
}


function handleGridItemClick(gridItem, carryTitle, carryUrl) {
    const hasBeenClicked = isLargeScreenDevice() ? true : gridItem.dataset.clicked === 'true';

    if (!hasBeenClicked) {
        // Show the hover label
        const hoverLabel = document.querySelector('.hover-label');
        const rect = gridItem.getBoundingClientRect();
        hoverLabel.style.left = `${rect.left + window.scrollX}px`;
        hoverLabel.style.top = `${rect.top + window.scrollY - 40}px`;
        hoverLabel.style.display = 'block'; // Show the label
        hoverLabel.textContent = carryTitle;

        // Mark the gridItem as clicked
        gridItem.dataset.clicked = 'true';
    } else {
        // Deselect tabs
        document.querySelector('.nav-link[data-page="carries-page"]').classList.remove('active');
        document.querySelector('.nav-link[data-page="faq-page"]').classList.remove('active');

        // Redirect to the constructed URL
        window.location.href = carryUrl;
    }
}


async function removeCarryFromTodo(gridItem) {
    loadingSpinner.style.display = 'block';

    const carryName = gridItem.dataset.name;

    const formData = new FormData();
    const csrfToken = document.querySelector('input[name="csrfmiddlewaretoken"]').value;
    formData.append('csrfmiddlewaretoken', csrfToken);

    try {
        // Make an AJAX POST request to mark the carry as done
        fetch(`/remove-todo/${carryName}/`, {
            method: 'POST',
            body: formData,
            headers: {
                'X-CSRFToken': formData.get('csrfmiddlewaretoken'), // Pass CSRF token
            }
        })
        .catch(error => console.error('Error:', error));

        // Delete gridItem
        gridItem.remove();

        // Unhide element from dropdown
        const dropdownItem = document.querySelector(`.dropdown-item[data-name="${carryName}"]`);
        dropdownItem.style = "block";

    } catch (error) {
        console.error("Error marking carry as done:", error);
    }

    loadingSpinner.style.display = 'none';
}

// Function to handle "Mark as done" action
async function addCarryAsDone(carryName, addCircle) {
    loadingSpinner.style.display = 'block';
    
    const formData = new FormData();
    const csrfToken = document.querySelector('input[name="csrfmiddlewaretoken"]').value;
    formData.append('csrfmiddlewaretoken', csrfToken);

    const gridItem = addCircle.parentElement;

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
        gridItem.children[1].style.opacity = '1';
        gridItem.classList.add("shadow");
        gridItem.style.border = "1px solid lightgrey";
        gridItem.removeChild(gridItem.firstChild);
        gridItem.removeChild(addCircle); // Remove the "+" icon
    } catch (error) {
        console.error("Error marking carry as done:", error);
    }

    loadingSpinner.style.display = 'none';
}


function createCarryGridItem(carryTitle, carryName, pageUrl, imgUrl, disabled) {
    // Create grid item
    const gridItem = document.createElement('div');
    gridItem.className = 'card-grid-item clickable-grid-item';
    gridItem.dataset.name = carryName;
    gridItem.dataset.title = carryTitle;

    const img = document.createElement('img');
    img.src = imgUrl;
    img.alt = carryTitle;
    img.loading = 'lazy'; // Enable lazy loading
    img.className = 'grid-item'; // Optional: Add class for styling

    if (disabled) {
        img.style.opacity = '0.5'; // Set opacity of the image to 50%

        // Create overlay
        const overlay = document.createElement('div');
        overlay.classList.add('overlay'); // Add the overlay class to the div
        gridItem.appendChild(overlay);
        gridItem.style.border = "none";
    } else {
        gridItem.classList.add("shadow");
    }

    // Append image and description container to grid item
    gridItem.appendChild(img);

    // Event listeners for hover and click
    gridItem.addEventListener('mouseenter', (event) => {
        handleMouseEnter(event, carryTitle);
    });

    // Event listeners for hover and click
    gridItem.addEventListener('mouseleave', () => {
        handleMouseLeave();
    });
    gridItem.addEventListener('click', () => {
        // Redirect to the constructed URL
        handleGridItemClick(gridItem, carryTitle, pageUrl);
    });

    return gridItem;
}

async function loadMyCarries(size, position) {
    const gridContainer = document.querySelector(`.card-grid[data-size="${size}"][data-position="${position}"]`);
    gridContainer.innerHTML = '';

    const baseUrlPattern = gridContainer.dataset.baseUrlPattern.replace('PLACEHOLDER', '');

    const loadingSpinner = document.getElementById('loadingSpinner');
    loadingSpinner.style.display = 'block';

    resultsPage = 1;
    const carries = await fetchFilteredCarries(resultsPage, pageSize, size, position);

    // Create an array of promises to fetch all image URLs
    for (const carry of carries) {
        // Create grid item for this carry
        const title = carry.carry__title;
        const name = carry.carry__name;
        const pageUrl = `${baseUrlPattern}${carry.carry__name}`;
        const imgUrl = await fetchFileUrl(carry.carry__name, carry.carry__position);
        const disabled = !(carriesInfo[position][size].includes(carry.carry__name));

        const gridItem = createCarryGridItem(title, name, pageUrl, imgUrl, disabled)

        if (disabled) {
            // Create the "+" circle button and append it to the grid item
            const addCircle = document.createElement('div');
            addCircle.className = 'add-circle'; // Style using the same CSS class as in the example
            addCircle.innerHTML = '<i class="fa fa-plus"></i>'; // Add the "+" icon

            // Separate the click handler
            // addCircle.onclick = function(event) {
            //     event.stopPropagation(); // Prevent the click from bubbling up to the grid item
            //     addCarryAsDone(name, gridItem, gridItem.img, overlay, addCircle);
            // };

            addCircle.onclick = (event) => {
                event.stopPropagation(); // Prevent the click from bubbling up to the grid item
                addCarryAsDone(name, addCircle);
            };

            gridItem.appendChild(addCircle);
        }

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

function showDropdown() {
    document.getElementById('carryDropdown').style.display = 'block';
}

function hideDropdown() {
    document.getElementById('carryDropdown').style.display = 'none';
}


function filterCarries() {
    const input = document.getElementById('carrySearch');
    const filter = input.value.toLowerCase();
    const dropdown = document.getElementById('carryDropdown');
    const items = dropdown.getElementsByClassName('dropdown-item');

    // Loop through the items and hide those that don't match the search query
    for (let i = 0; i < items.length; i++) {
        const item = items[i];
        const txtValue = item.innerText.toLowerCase();
        item.style.display = txtValue.includes(filter) ? 'block' : 'none';
    }
}

function clickOnRemoveIcon(event, div) {
    event.stopPropagation(); // Prevent the click from bubbling up to the grid item

    const gridItem = div.parentElement;
    removeCarryFromTodo(gridItem);
}

// Function to handle the selection of a carry
async function addCarryToTodo(div) {
    const name = div.dataset.name;
    const title = div.innerText;
    const pageUrl = div.dataset.url;
    const position = div.dataset.position;
    const imgUrl = await fetchFileUrl(name, position);

    div.style.display = 'none';
    document.getElementById('carryDropdown').style.display = 'none'; // Hide the dropdown

    loadingSpinner.style.display = 'block';
    
    const formData = new FormData();
    const csrfToken = document.querySelector('input[name="csrfmiddlewaretoken"]').value;
    formData.append('csrfmiddlewaretoken', csrfToken);

    try {
        // Make an AJAX POST request to mark the carry as done
        fetch(`/add-todo/${name}/`, {
            method: 'POST',
            body: formData,
            headers: {
                'X-CSRFToken': formData.get('csrfmiddlewaretoken'), // Pass CSRF token
            }
        })
        .catch(error => console.error('Error:', error));

        // add carry to todo grid
        const gridContainer = document.getElementById('todoGrid');
        const gridItem = createCarryGridItem(title, name, pageUrl, imgUrl, false);

        // Create the "+" circle button and append it to the grid item
        const removeIcon = document.createElement('div');
        removeIcon.className = 'add-circle'; // Style using the same CSS class as in the example
        removeIcon.innerHTML = '<i class="fa fa-minus"></i>'; // Add the "-" icon

        removeIcon.onclick = (event) => {
            clickOnRemoveIcon(event, removeIcon);
        };

        gridItem.appendChild(removeIcon);

        // Append grid item to fragment
        gridContainer.appendChild(gridItem);


    } catch (error) {
        console.error("Error marking carry as done:", error);
    }

    loadingSpinner.style.display = 'none';
}

document.addEventListener('DOMContentLoaded', function() {
    document.addEventListener('click', function(event) {
        const dropdown = document.getElementById('carryDropdown');
        const searchBox = document.getElementById('carrySearch');

        // Check if the click was outside the dropdown and the search box
        if (!dropdown.contains(event.target) && event.target !== searchBox) {
            hideDropdown();  // Hide the dropdown
        }
    });
});

