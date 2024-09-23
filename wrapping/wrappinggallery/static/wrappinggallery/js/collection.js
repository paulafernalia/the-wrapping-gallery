let pageSize = 18;
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


async function loadMyCarries(size, position) {
    const gridContainer = document.querySelector(`.card-grid[data-size="${size}"][data-position="${position}"]`);
    gridContainer.innerHTML = '';

    const loadingSpinner = document.getElementById('loadingSpinner');
    loadingSpinner.style.display = 'block';

    resultsPage = 1;
    const carries = await fetchFilteredCarries(resultsPage, pageSize, size, position);

    // Create an array of promises to fetch all image URLs
    for (const carry of carries) {
        // Create grid item
        const gridItem = document.createElement('div');
        gridItem.className = 'card-grid-item clickable-grid-item';

        // Create image
        const img = document.createElement('img');
        let fileUrl = await fetchFileUrl(
            carry.carry__name, carry.carry__position);

        img.src = fileUrl;
        img.alt = carry.carry__title;
        img.loading = 'lazy'; // Enable lazy loading
        img.className = 'grid-item'; // Optional: Add class for styling

        // Create description container
        const descContainer = document.createElement('div');
        descContainer.className = 'card-desc-container';

        // Create carrydesc
        // const carrydesc = document.createElement('div');
        // carrydesc.className = 'carrydesc poppins-regular fssmall';
        // carrydesc.textContent = carry.carry__title;

        // Append descriptions to the description container
        // descContainer.appendChild(carrydesc);

        // Append image and description container to grid item
        gridItem.appendChild(img);
        gridItem.appendChild(descContainer);

        // Make the entire grid item clickable
        gridItem.addEventListener('click', () => {
            const url = `${baseUrlPattern}${carry.carry__name}`;

            const carriesTab = document.querySelector('.nav-link[data-page="carries-page"]');
            carriesTab.classList.remove('active');

            const faqTab = document.querySelector('.nav-link[data-page="faq-page"]');
            faqTab.classList.remove('active');

            // Redirect to the constructed URL
            window.location.href = url;
        });

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


async function initialiseSections() {
     const cats = document.querySelectorAll('p[data-size]');

    for (const element of cats) {
        const size = element.getAttribute('data-size');
        const position = element.getAttribute('data-position');

        const carries = await fetchFilteredCarries(resultsPage, pageSize, size, position);
        const carriesCount = Array.isArray(carries) ? carries.length : 0;
        
        // Create a new text node with conditional text
        const newText = document.createElement('span');
        newText.style.color = 'lightgrey'; // Set the font color to grey
        newText.textContent = `\u00A0 ( /${carriesCount})`;

        // Find the caret icon (<i> element)
        const caretIcon = element.querySelector('.toggle-icon');

        element.insertBefore(newText, caretIcon);

        if (carriesCount === 0) {
            element.style.display = "none";
        }

    };
}


function fetchDoneCarries() {
    fetch('/done-carries/')
        .then(response => response.json())
        .then(data => {
            if (data.carries) {
                console.log("Carries:", data.carries);  // This will log the array of carries
                // You can use data.carries as an array here
                // For example: 
                data.carries.forEach(carry => {
                    // Do something with each carry
                    console.log("Carry name:", carry);
                });
            } else {
                console.error(data.error);
            }
        })
        .catch(error => console.error('Error fetching carries:', error));
}


document.addEventListener('DOMContentLoaded', async function() {    
    updateFooterPosition();

    fetchDoneCarries();
    initialiseSections();
});
