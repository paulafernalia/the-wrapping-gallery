function getButtonByValueAndProperty(property, value) {
    // Get button that matches the data-property and data-value args given
    return document.querySelector(`button[data-value="${value}"][data-property="${property}"]`);
}

async function clickFilterButton(button) {
    // Set this button as active
    setActiveButton(button);

    // Filter carries by the property selected in the button
    filterCarries();
}



function showPage(tab) {
    // Clear active tab
    const carriesTab = document.querySelector('.nav-link[data-page="carries-page"]');
    carriesTab.classList.remove('active');

    const aboutTab = document.querySelector('.nav-link[data-page="about-page"]');
    aboutTab.classList.remove('active');

    // Hide all of the divs:
    const carriesPage = document.getElementById('carries-page');
    carriesPage.style.display = 'none';

    const aboutPage = document.getElementById('about-page');
    aboutPage.style.display = 'none';

    // Show the div provided in the argument
    const selectedPage = document.getElementById(tab.dataset.page);
    selectedPage.style.display = 'block';

    // Mark tab as active
    tab.classList.add('active');
}


function updateFilterData(button) {
    const property = button.parentElement.getAttribute('data-property');
    const value = button.getAttribute('data-value');

    // Update local storage
    localStorage.setItem(property, value);
}

function initialiseFilterData(property) {
    let init = 'Any';
    if (!localStorage.getItem(property)) {
        // If not, set the counter to 0 in local storage
        localStorage.setItem(property, 'Any');
    } else {
        init = localStorage.getItem(property);
    }

    // Get button with this property and value
    const button = getButtonByValueAndProperty(property, init);

    button.classList.add('active');
}

function initialiseFiltersData() {
    initialiseFilterData('size');
    initialiseFilterData('position');    
}

async function fetchFilteredCarries() {
    // Read the property of the button group and the button value
    const filters = {
        size: localStorage.getItem("size"),
        position: localStorage.getItem("position"),
    };
    
    // Build the query string from the filters object
    const queryString = Object.entries(filters)
        .map(([property, value]) => `property[]=${encodeURIComponent(property)}&value[]=${encodeURIComponent(value)}`)
        .join('&');

    // Filter carries by using filter values
    const response = await fetch(`/api/filter-carries/?${queryString}`);

    if (!response.ok) {
        throw new Error('Network response was not ok');
    }

    const data = await response.json();
    return data.carries;
}

async function filterCarries() {
    fetchFilteredCarries()
        .then(carries => {
            // Update gallery content
            updateCarryGallery(carries);
        })
        .catch(error => {
            console.error('There was a problem with the fetch operation:', error);
        });
}

function setActiveButton(button) {
    // Make the selected filter button active when clicking on it
    const btnGroup = button.parentElement;
    const buttons = btnGroup.getElementsByClassName('btn-custom');

    // Set all other buttons as inactive
    for (let btn of buttons) {
        btn.classList.remove('active');
    }
    button.classList.add('active');

    // Store selected value in local storage
    localStorage.setItem(button.dataset.property, button.dataset.value);
}

function toggleFilterBox() {
    console.log("triggered");
    const filterBox = document.getElementById('filterBox');
    if (filterBox.style.display === 'none' || filterBox.style.display === '') {
        filterBox.style.display = 'block';
    } else {
        filterBox.style.display = 'none';
    }
}


function updateCarryGallery(carries) {
    // Get imageGrid div
    const gridContainer = document.getElementById('imageGrid');
    gridContainer.innerHTML = '';

    carries.forEach(carry => {
        // Create grid item
        const gridItem = document.createElement('div');
        gridItem.className = 'grid-item';

        // Set image URL
        const imageUrl = '/media/' + carry.coverpicture;

        // Create image
        const img = document.createElement('img');
        img.src = imageUrl; // Combine the static URL with the file name
        img.alt = carry.coverpicture;

        // Create description container
        const descContainer = document.createElement('div');
        descContainer.className = 'desc-container';

        // Create carrydesc
        const carrydesc = document.createElement('div');
        carrydesc.className = 'carrydesc';
        carrydesc.textContent = carry.title;

        // Create sizedesc
        const sizedesc = document.createElement('div');
        sizedesc.className = 'sizedesc';
        if (carry.size == 0) {
            sizedesc.textContent = "Base";
        } else {
            sizedesc.textContent = "Base " + carry.size;
        }

        // Append descriptions to the description container
        descContainer.appendChild(carrydesc);
        descContainer.appendChild(sizedesc);

        // Append image and description container to grid item
        gridItem.appendChild(img);
        gridItem.appendChild(descContainer);

        // Append grid item to grid container
        gridContainer.appendChild(gridItem);
    })
}

document.addEventListener('DOMContentLoaded', function() {
    // Set initial active buttons in filters
    initialiseFiltersData();

    // Filter carries in gallery
    filterCarries();


});
