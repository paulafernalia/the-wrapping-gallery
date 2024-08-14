let counter = 0
let isFetching = false
let filteredResults = 0;

function getButtonByValueAndProperty(property, value) {
    // Get button that matches the data-property and data-value args given
    return document.querySelector(`button[data-value="${value}"][data-property="${property}"]`);
}

function getDropdownByValueAndProperty(property, value) {
    // Get button that matches the data-property and data-value args given
    return document.querySelector(`option[value="${value}"][data-property="${property}"]`);
}

function getSwitchByProperty(property) {
    return document.querySelector(`input[data-property="${property}"]`);
}

async function clickFilterButton(button) {
    // Set this button as active
    setActiveButton(button);

    // Filter carries by the property selected in the button
    await updateButtonBox();
}

async function handleSelectChange(dropdown) {
    const selectedOption = dropdown.options[dropdown.selectedIndex];

    // Store selected value in local storage
    localStorage.setItem(selectedOption.dataset.property, selectedOption.value);

    // Filter carries by the properties selected
    await updateButtonBox();
}


async function handleSwitchChange(switch_) {
    let checked = 0;
    if (switch_.checked) {
        checked = 1;
    }

    // Store selected value in local storage
    localStorage.setItem(switch_.dataset.property, checked);

    // Filter carries by the properties selected
    await updateButtonBox();
}


async function handleInputChange() {
    const searchInput = document.getElementById('search-input');
    localStorage.setItem('partialname', searchInput.value);

    // Filter carries by the properties selected
    await updateButtonBox();

    // Filter carries by the property selected in the button
    emptyCarryGallery();
    await showResults();
}

function initialiseSwitchData(property) {
    let init = 0;

    if (!localStorage.getItem(property)) {
        localStorage.setItem(property, 0);
    } else {
        init = localStorage.getItem(property);
    }

    // Get switch with this property and value
    const switch_ = getSwitchByProperty(property);
    if (switch_) {
        if (init === '1') {
            switch_.checked = true;
            return true;
        } else {
            switch_.checked = false;
            return false;
        }
    }
}


function hideAllFilters() {
    const buttonBox = document.getElementById('buttonBox');
    buttonBox.style.display = 'none';

    const filtertitle = document.getElementById('filter-title');
    filtertitle.style.display = 'none';

    const filtersContainer = document.getElementById('filters-container');
    filtersContainer.style.display = 'none';

}


function showAllFilters() {
    const filtersContainer = document.getElementById('filters-container');
    filtersContainer.style.display = 'block';

    const filtertitle = document.getElementById('filter-title');
    filtertitle.style.display = 'block';

    const buttonBox = document.getElementById('buttonBox');
    buttonBox.style.display = 'block';
}

async function resetFilters() {
    localStorage.setItem("size", "Any");
    localStorage.setItem("position", "Any");
    localStorage.setItem("mmposition", "Any");
    localStorage.setItem("layers", "Any");
    localStorage.setItem("shoulders", "Any");
    localStorage.setItem("difficulty", "Any");
    localStorage.setItem("finish", "Any");
    localStorage.setItem("fancy", "0");
    localStorage.setItem("pretied", "0");
    localStorage.setItem("newborns", "0");
    localStorage.setItem("legstraighteners", "0");
    localStorage.setItem("leaners", "0");
    localStorage.setItem("bigkids", "0");
    localStorage.setItem("feeding", "0");
    localStorage.setItem("quickups", "0");

    // Set initial values of filters
    initialiseFilters();

    // Update button box
    updateButtonBox();

    // Disable reset button
    const resetFiltersBtn = document.getElementById('resetFiltersBtn');
    resetFiltersBtn.classList.add('disabled');
}

function initialiseButtonData(property) {
    let init = 'Any';
    if (!localStorage.getItem(property)) {
        // If not, set the counter to 0 in local storage
        localStorage.setItem(property, 'Any');
    } else {
        init = localStorage.getItem(property);
    }

    // Get button with this property and value
    const button = getButtonByValueAndProperty(property, init);
    const btnGroup = button.parentElement;
    const buttons = btnGroup.getElementsByClassName('btn-custom');

    // Set all other buttons as inactive
    for (let btn of buttons) {
        btn.classList.remove('active');
    }

    if (button) {
        button.classList.add('active');
    }

    if (init !== "Any") {
        return true;
    }

    return false;
}

function initialiseDropdownData(property) {
    let init = 'Any';
    if (!localStorage.getItem(property)) {
        // If not, set the counter to 0 in local storage
        localStorage.setItem(property, 'Any');
    } else {
        init = localStorage.getItem(property);
    }

    // If it's not a button, it may be a dropdown
    const optionToSelect = getDropdownByValueAndProperty(property, init);
    if (optionToSelect) {
        optionToSelect.selected = true;
    }

    if (init !== "Any") {
        return true;
    }

    return false;
}


function initialiseSearchBar() {
    // Set content to localstorage if available
    if (localStorage.getItem('partialname')) {
        const searchInput = document.getElementById('search-input');
        searchInput.value = localStorage.getItem('partialname');
    }
}

async function initialiseFilters() {
    const fil1 = initialiseButtonData('size');
    const fil2 = initialiseButtonData('position');
    const fil3 = initialiseButtonData('shoulders');
    const fil4 = initialiseButtonData('layers');
    const fil5 = initialiseDropdownData('difficulty');
    const fil6 = initialiseDropdownData('finish');
    const fil7 = initialiseSwitchData('fancy');
    const fil8 = initialiseSwitchData('pretied');
    const fil9 = initialiseSwitchData('newborns');
    const fil10 = initialiseSwitchData('legstraighteners');
    const fil11 = initialiseSwitchData('leaners');
    const fil12 = initialiseSwitchData('bigkids');
    const fil13 = initialiseSwitchData('feeding');
    const fil14 = initialiseSwitchData('quickups');
    const fil15 = initialiseDropdownData('mmposition');
    initialiseSearchBar();

    if (fil1 || fil2 || fil3 || fil4 || fil5 || fil6 || fil7 || fil8 ||
        fil9 || fil10 || fil11 || fil12 || fil13 || fil14 || fil15) {
        return true;
    } else {
        return false;
    }
}

function isAnyFilterActive() {
    const choiceProperties = [
        "size", "position", "difficulty", "finish",
        "layers", "shoulders", "mmposition"
    ];

    for (let i = 0; i < choiceProperties.length; i++) {
        if (localStorage.getItem(choiceProperties[i]) != "Any") {
            return true;
        }
    }

    const boolProperties = [
        "fancy", "pretied", "newborns", "legstraighteners",
        "leaners", "bigkids", "feeding", "quickups"
    ];

    for (let i = 0; i < boolProperties.length; i++) {
        if (localStorage.getItem(boolProperties[i]) == "1") {
            return true;
        }
    }

    return false;
}



async function fetchFilteredCarries(includeAll = false) {
    let start = counter;
    let end = counter + 17;

    if (includeAll) {
        start = 0;
        end = 1000;
    } else {
        counter = end + 1;
    }

    // Read the property of the button group and the button value
    const filters = {
        size: localStorage.getItem("size"),
        position: localStorage.getItem("position"),
        shoulders: localStorage.getItem("shoulders"),
        layers: localStorage.getItem("layers"),
        difficulty: localStorage.getItem("difficulty"),
        mmposition: localStorage.getItem("mmposition"),
        partialname: localStorage.getItem("partialname"),
        pretied: localStorage.getItem("pretied"),
        fancy: localStorage.getItem("fancy"),
        finish: localStorage.getItem("finish"),
        newborns: localStorage.getItem("newborns"),
        legstraighteners: localStorage.getItem("legstraighteners"),
        leaners: localStorage.getItem("leaners"),
        bigkids: localStorage.getItem("bigkids"),
        feeding: localStorage.getItem("feeding"),
        quickups: localStorage.getItem("quickups"),
    };
    
    // Build the query string from the filters object
    const queryString = Object.entries(filters)
        .map(([property, value]) => `property[]=${encodeURIComponent(property)}&value[]=${encodeURIComponent(value)}`)
        .concat([`start=${start}`, `end=${end}`])  // Add start and end parameters
        .join('&');

    // Filter carries by using filter values
    const response = await fetch(`/api/filter-carries/?${queryString}`);

    if (!response.ok) {
        throw new Error('Network response was not ok');
    }

    const data = await response.json();
    return data.carries;
}

async function showResults() {
    // Hide all filters
    hideAllFilters();

    // Populate gallery
    const carries = await fetchFilteredCarries();

    await updateCarryGallery(carries);

    updateFooterPosition();
}


async function updateButtonBox() {
    const showResultsBtn = document.getElementById('showResultsBtn');
    const countText = document.getElementById('count-text');

    let num_carries = 0;
    try {
        const carries = await fetchFilteredCarries(true);
        filteredResults = carries.length;
        
        if (carries.length === 0) {
            showResultsBtn.classList.remove('active');
            showResultsBtn.classList.add('disabled');
            showResultsBtn.textContent = "No results";
            countText.textContent = "No carries found";
        } else {
            showResultsBtn.classList.remove('disabled');
            showResultsBtn.classList.add('active');
            showResultsBtn.textContent = "Show " + filteredResults + " results";
            countText.textContent = "Showing " + filteredResults + " carries.";
        }
    } catch (error) {
        console.error('There was a problem with the fetch operation:', error);
    }

    // Deactivate reset button if no filters have been applied
    const resetFiltersBtn = document.getElementById('resetFiltersBtn');

    if (isAnyFilterActive()) {
        resetFiltersBtn.classList.remove('disabled');
    } else {
        resetFiltersBtn.classList.add('disabled');
    }
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

async function toggleFilterBox(button) {
    button.blur();
    const filtersContainer = document.getElementById('filters-container');
    if (filtersContainer.style.display === 'none') {
        filtersContainer.style.display = 'block';

        const filtertitle = document.getElementById('filter-title');
        filtertitle.style.display = 'block';

        const buttonBox = document.getElementById('buttonBox');
        buttonBox.style.display = 'block';

        // Empty gallery
        emptyCarryGallery();

    } else {
        hideAllFilters();

        const carries = await fetchFilteredCarries();
        updateCarryGallery(carries);
    }

    updateFooterPosition();
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

function showFilterBoxExt() {
    const filterBoxExt = document.getElementById('filterBoxExt');
    filterBoxExt.style.display = 'block';

    const showMoreBtn = document.getElementById('showMoreBtn');
    showMoreBtn.style.display = 'none';

    var targetElement = document.getElementById('filterBoxExt');
    var elementPosition = targetElement.getBoundingClientRect().top;

    window.scrollTo({
        top: elementPosition,
        behavior: 'smooth'
    });

    // Check if footer position must be updated
    releaseFooter();
}

function hideFilterBoxExt() {
    const filterBoxExt = document.getElementById('filterBoxExt');
    filterBoxExt.style.display = 'none';

    const showMoreBtn = document.getElementById('showMoreBtn');
    showMoreBtn.style.display = 'block';

    var targetElement = document.getElementById('filterBox');
    var elementPosition = targetElement.getBoundingClientRect().top;

    window.scrollTo({
        top: elementPosition,
        behavior: 'smooth'
    });

    // Check if footer position must be updated
    releaseFooter();
}


async function fetchFileUrl(fileName, position) {
    try {
        const response = await fetch(`/file-url/${fileName}/?position=${position}`);
        const data = await response.json();
        return data.url;
    } catch (error) {
        return null;
    }
}

function emptyCarryGallery() {
    const countText = document.getElementById('count-text');
    countText.style.display = 'none';

    const gridContainer = document.getElementById('imageGrid');
    gridContainer.innerHTML = '';

    // Reset counter whenever we empty the gallery
    counter = 0;
}


// Function to check if the URL returns a 200 status
async function checkUrlStatus(url) {
    try {
        const response = await fetch(url, { method: 'HEAD' });
        if (response.status === 200) {
            // URL is valid
            console.log('URL is valid and returns a 200 status.');
            return true;
        }
        // No logging for non-200 status codes
        return false;
    } catch (error) {
        // Log only network errors or issues
        console.log('Error fetching URL:', error);
        return false;
    }
}



async function updateCarryGallery(carries) {
    // Check if footer must be changed
    updateFooterPosition();

    // // Show text counting results
    const countText = document.getElementById('count-text');
    countText.style.display = 'block';

    // Disable filters until all images have rendered
    const filterBtn = document.getElementById('button-filter');
    filterBtn.classList.add('disabled');
    filterBtn.setAttribute('disabled', true);

    // Get imageGrid div
    const gridContainer = document.getElementById('imageGrid');
    const baseUrlPattern = gridContainer.dataset.baseUrlPattern.replace('PLACEHOLDER', '');

    // Create an array of promises to fetch all image URLs
    for (const carry of carries) {
        // Create grid item
        const gridItem = document.createElement('div');
        gridItem.className = 'grid-item clickable-grid-item';

        // Create image
        const img = document.createElement('img');
        let fileUrl = await fetchFileUrl(
            carry.carry__name, carry.carry__position);

        img.src = fileUrl;
        img.alt = carry.carry__title;
        img.loading = 'lazy'; // Enable lazy loading
        img.className = 'grid-image'; // Optional: Add class for styling

        // Create description container
        const descContainer = document.createElement('div');
        descContainer.className = 'desc-container';

        // Create carrydesc
        const carrydesc = document.createElement('div');
        carrydesc.className = 'carrydesc poppins-regular fs16';
        carrydesc.textContent = carry.carry__title;

        // Create sizedesc
        const sizedesc = document.createElement('div');
        sizedesc.className = 'sizedesc dancing fs16';
        sizedesc.textContent = carry.carry__size === 0 ? 'Base' :
                               carry.carry__size > 0 ? `Base + ${carry.carry__size}` :
                               `Base ${carry.carry__size}`;

        // Append descriptions to the description container
        descContainer.appendChild(carrydesc);
        descContainer.appendChild(sizedesc);

        // Append image and description container to grid item
        gridItem.appendChild(img);
        gridItem.appendChild(descContainer);

        // Make the entire grid item clickable
        gridItem.addEventListener('click', () => {
            const url = `${baseUrlPattern}${carry.carry__name}`;

            const carriesTab = document.querySelector('.nav-link[data-page="carries-page"]');
            carriesTab.classList.remove('active');

            const aboutTab = document.querySelector('.nav-link[data-page="about-page"]');
            aboutTab.classList.remove('active');

            // Redirect to the constructed URL
            window.location.href = url;
        });

        // Append grid item to fragment
        gridContainer.appendChild(gridItem);
    };

    // Reactivate the filter button
    filterBtn.classList.remove('disabled');
    filterBtn.removeAttribute('disabled');

    // Check if footer must be changed
    updateFooterPosition();
}



document.addEventListener('DOMContentLoaded', function() { 
    // Reset gallery
    emptyCarryGallery();

    // Decide where footer should be
    updateFooterPosition();

    // Set initial active buttons in filters
    const anyapplied = initialiseFilters();

    // Update button box
    updateButtonBox();

    // Update reset filters button
    resetFiltersBtn = document.getElementById('resetFiltersBtn');

    // If any filters applied, show filter box to alert user
    if (anyapplied > 0) {
        showAllFilters();

        resetFiltersBtn.classList.remove('disabled');
    } else {
        // Get all carries with session data and update gallery
        resetFiltersBtn.classList.add('disabled');

        // Filter carries by the property selected in the button
        emptyCarryGallery();
        showResults();
    }

    const searchInput = document.getElementById('search-input');
    searchInput.addEventListener('keydown', function(event) {
        if (event.key === 'Enter') {
            event.preventDefault(); // Prevent the default action (if necessary)
            handleInputChange();
            this.blur();
        }
    });
});


// Define the async function to handle scrolling
async function handleScroll() {
    const gridContainer = document.getElementById('imageGrid');
    const loadingSpinner = document.getElementById('loadingSpinner');

    if (gridContainer.innerHTML === '') {
        return;
    }

    // Check if a request is already in progress
    if (isFetching) return;

    // Check if the user has scrolled to the bottom of the page
    if (window.innerHeight + window.scrollY >= document.body.offsetHeight) {
        isFetching = true;  // Set the flag to indicate a request is in progress
        loadingSpinner.style.display = 'block';  // Show the spinner

        try {
            const carries = await fetchFilteredCarries();
            updateCarryGallery(carries);
        } catch (error) {
            console.error('Error fetching carries:', error);
        } finally {
            isFetching = false;  // Reset the flag after the request completes
            loadingSpinner.style.display = 'none';  // Hide the spinner
        }
    }
}


// Attach the async scroll handler to the window's scroll event
window.onscroll = handleScroll;


function clearSearch() {
    document.getElementById('search-input').value = '';
    document.getElementById('search-input').focus();
    document.getElementById('clear-search').style.display = 'none';
    handleInputChange();
}

document.getElementById('search-input').addEventListener('input', function() {
    const clearBtn = document.getElementById('clear-search');
    clearBtn.style.display = this.value ? 'block' : 'none';
});
