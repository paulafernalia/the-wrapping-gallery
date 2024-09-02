let isFetching = false
let filteredResults = 0;
let resultsPage = 1;
let pageSize = 36;

const booleanProps = [
    'fancy', 'pretied', 'newborns', 'legstraighteners', 'leaners', 
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

function getButtonByValueAndProperty(property, value) {
    // Get button that matches the data-property and data-value args given
    return document.querySelector(`button[data-value="${value}"][data-property="${property}"]`);
}

function getMultiButtonByValueAndProperty(property, value) {
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

async function clickFilterMultiButton(button) {
    // Set this button as active
    setActiveMultiButton(button);

    // Filter carries by the property selected in the button
    await updateButtonBox();
}

async function handleSelectChange(dropdown) {
    const selectedOption = dropdown.options[dropdown.selectedIndex];

    // Store selected value in local storage
    sessionStorage.setItem(selectedOption.dataset.property, selectedOption.value);

    // Filter carries by the properties selected
    await updateButtonBox();
}


async function handleSwitchChange(switch_) {
    let checked = 0;
    if (switch_.checked) {
        checked = 1;
    }

    // Store selected value in local storage
    sessionStorage.setItem(switch_.dataset.property, checked);

    // Filter carries by the properties selected
    await updateButtonBox();
}


async function handleInputChange() {
    const searchInput = document.getElementById('search-input');
    sessionStorage.setItem('partialname', searchInput.value);

    // Filter carries by the properties selected
    await updateButtonBox();

    // Filter carries by the property selected in the button
    emptyCarryGallery();
    await showResults();
}

function initialiseSwitchData(property) {
    let init = 0;

    if (!sessionStorage.getItem(property)) {
        sessionStorage.setItem(property, 0);
    } else {
        init = sessionStorage.getItem(property);
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

    const footer = document.querySelector('footer');
    footer.style.display = 'block';
}


function showAllFilters() {
    const filtersContainer = document.getElementById('filters-container');
    filtersContainer.style.display = 'block';

    const filtertitle = document.getElementById('filter-title');
    filtertitle.style.display = 'block';

    const buttonBox = document.getElementById('buttonBox');
    buttonBox.style.display = 'block';

    const footer = document.querySelector('footer');
    footer.style.display = 'none';
}

async function resetFilters() {
    const filterDefaults = {
        size: JSON.stringify(['Any']),
        position: "Any",
        mmposition: "Any",
        layers: "Any",
        shoulders: "Any",
        difficulty: "Any",
        finish: "Any"
    };

    Object.entries(filterDefaults).forEach(([key, value]) => {
        sessionStorage.setItem(key, value);
    });

    booleanProps.forEach(key => {
        sessionStorage.setItem(key, "0");
    });    

    // Set initial values of filters
    initialiseFilters();

    // Update button box
    updateButtonBox();

    // Disable reset button
    const resetFiltersBtn = document.getElementById('resetFiltersBtn');
    resetFiltersBtn.classList.add('disabled');
    resetFiltersBtn.disabled = true;

    // Display gallery
    emptyCarryGallery();
    showResults();
}

function initialiseButtonData(property) {
    let init = 'Any';
    if (!sessionStorage.getItem(property)) {
        // If not, set the counter to 0 in local storage
        sessionStorage.setItem(property, 'Any');
    } else {
        init = sessionStorage.getItem(property);
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


function initialiseMultiButtonData(property) {
    let init = ['Any'];
    if (!sessionStorage.getItem(property)) {
        // If not, set the counter to 0 in local storage
        sessionStorage.setItem(property, JSON.stringify(['Any']));
    } else {
        initString = sessionStorage.getItem(property);
        init = JSON.parse(initString);
    }

    // Get button with this property and value
    const button = getButtonByValueAndProperty(property, init[0]);
    const btnGroup = button.parentElement;
    const buttons = btnGroup.getElementsByClassName('btn-custom');

    // Set all other buttons as inactive
    for (let btn of buttons) {
        btn.classList.remove('active');
    }

    for (let size of init) {
        // Get button with this size
        const button = getButtonByValueAndProperty(property, size);
        button.classList.add('active');
    }

    if (init.length !== 1 || init[0] !== "Any") {
        return true;
    }

    return false;
}

function initialiseDropdownData(property) {
    let init = 'Any';
    if (!sessionStorage.getItem(property)) {
        // If not, set the counter to 0 in local storage
        sessionStorage.setItem(property, 'Any');
    } else {
        init = sessionStorage.getItem(property);
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
    // Set content to sessionStorage if available
    if (sessionStorage.getItem('partialname')) {
        const searchInput = document.getElementById('search-input');
        searchInput.value = sessionStorage.getItem('partialname');
    }
}

async function initialiseFilters() {
    const multiButtonProps = ['size'];
    const buttonProps = ['position', 'shoulders', 'layers'];
    const dropdownProps = ['difficulty', 'finish', 'mmposition'];

    const filters = [
        ...multiButtonProps.map(prop => initialiseMultiButtonData(prop)),
        ...buttonProps.map(prop => initialiseButtonData(prop)),
        ...dropdownProps.map(prop => initialiseDropdownData(prop)),
        ...booleanProps.map(prop => initialiseSwitchData(prop))
    ];

    initialiseSearchBar();

    return filters.some(filter => filter);
}


function isAnyFilterActive() {
    const choiceProperties = [
        "position", "difficulty", "finish",
        "layers", "shoulders", "mmposition"
    ];

    for (let i = 0; i < choiceProperties.length; i++) {
        if (sessionStorage.getItem(choiceProperties[i]) != "Any") {
            return true;
        }
    }

    let sizeString = sessionStorage.getItem("size");
    let sizes = JSON.parse(sizeString);
    if (sizes.length > 1 || sizes[0] != "Any") {
        return true;
    }

    for (let i = 0; i < booleanProps.length; i++) {
        if (sessionStorage.getItem(booleanProps[i]) == "1") {
            return true;
        }
    }

    return false;
}



async function fetchFilteredCarries(page = 1, pageSize = 36) {
    // Read the property of the button group and the button value
    const nonBooleanProps = [
        "position", "shoulders", "layers", "difficulty", "mmposition", 
        "partialname", "finish"
    ];

    const filterKeys = nonBooleanProps.concat(booleanProps);

    const filters = Object.fromEntries(
        filterKeys.map(key => [key, sessionStorage.getItem(key)])
    );

    // size: sessionStorage.getItem("size"),
    const sizeString = sessionStorage.getItem("size"); // Extract the size values
    const sizes = JSON.parse(sizeString);
    
    // Build the query string from the filters object
    const queryString = Object.entries(filters)
        .map(([property, value]) => `property[]=${encodeURIComponent(property)}&value[]=${encodeURIComponent(value)}`)
        .concat(sizes.map(val => `size[]=${encodeURIComponent(val)}`))  // Add size values separately
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


function showAppliedFilters() {
    // Clear previous filters
    const filtersApplied = document.getElementById('filters-applied');
    filtersApplied.innerHTML = '';  // Clear any existing content

    // Function to create and style a filter span
    function createFilterSpan(text) {
        const span = document.createElement('span');
        span.className = 'filter-tag';  // Add a class for styling
        span.textContent = text;
        return span;
    }

    let anyApplied = false;

    sizes = JSON.parse(sessionStorage["size"]);
    let sizeStr = "";
    for (let size of sizes) {
        if (size !== "Any") {
            const sizeInt = parseInt(size);
            if (sizeInt === 0) {
                sizeStr += " Base";
            } else if (sizeInt > 0) {
                sizeStr += " Base +" + size;
            } else {
                sizeStr += " Base " + size;
            }
        }
    }

    const filterConditions = [
        { key: "size", value: sizeStr, format: val => `size: ${val}`, condition: val => val !== "" },
        { key: "difficulty", value: sessionStorage["difficulty"], format: val => `difficulty: ${val}`, condition: val => val !== "Any" },
        { key: "position", value: sessionStorage["position"], format: val => `${val} carries`, condition: val => val !== "Any" },
        { key: "finish", value: sessionStorage["finish"], format: val => `finish: ${val}`, condition: val => val !== "Any" },
        { key: "mmposition", value: sessionStorage["mmposition"], format: val => `MM position: ${val}`, condition: val => val !== "Any" },
        { key: "layers", value: sessionStorage["layers"], format: val => `${val} layers`, condition: val => val !== "Any" },
        { key: "shoulders", value: sessionStorage["shoulders"], format: val => `${val} shoulders`, condition: val => val !== "Any" },
    ];

    const booleanFilters = [
        { key: "bigkids", label: "good for big kids" },
        { key: "fancy", label: "fancy" },
        { key: "pretied", label: "can be pre-tied" },
        { key: "rings", label: "ring(s)" },
        { key: "leaners", label: "good for leaners" },
        { key: "quickups", label: "good for quickups" },
        { key: "legstraighteners", label: "good for leg straighteners" },
        { key: "feeding", label: "good for feeding" },
        { key: "newborns", label: "good for newborns" },
        { key: "pass_sling", label: "sling pass" },
        { key: "pass_ruck", label: "ruck pass" },
        { key: "pass_kangaroo", label: "kangaroo pass" },
        { key: "pass_cross", label: "cross pass" },
        { key: "pass_reinforcing_cross", label: "reinforcing cross pass" },
        { key: "pass_reinforcing_horizontal", label: "reinforcing horizontal pass" },
        { key: "pass_horizontal", label: "horizontal pass" },
        { key: "pass_poppins", label: "poppins pass" },
        { key: "no_pass_sling", label: "no sling pass" },
        { key: "no_pass_ruck", label: "no ruck pass" },
        { key: "no_pass_kangaroo", label: "no kangaroo pass" },
        { key: "no_pass_cross", label: "no cross pass" },
        { key: "no_pass_reinforcing_cross", label: "no reinforcing cross pass" },
        { key: "no_pass_reinforcing_horizontal", label: "no reinforcing horizontal pass" },
        { key: "no_pass_horizontal", label: "no horizontal pass" },
        { key: "no_pass_poppins", label: "no poppins pass" },
        { key: "other_chestpass", label: "chest pass" },
        { key: "other_bunchedpasses", label: "bunched pass(es)" },
        { key: "other_shoulderflip", label: "shoulder flip" },
        { key: "other_twistedpass", label: "twisted pass" },
        { key: "other_s2s", label: "S2S" },
        { key: "other_waistband", label: "waist band" },
        { key: "other_legpasses", label: "leg pass(es)" },
        { key: "other_eyelet", label: "eyelet" },
        { key: "other_poppins", label: "poppins (not as a pass)" },
        { key: "other_sternum", label: "pond" },
        { key: "no_other_chestpass", label: "no chest pass" },
        { key: "no_other_bunchedpasses", label: "no bunched pass(es)" },
        { key: "no_other_shoulderflip", label: "no shoulder flip" },
        { key: "no_other_twistedpass", label: "no twisted pass" },
        { key: "no_other_s2s", label: "no S2S" },
        { key: "no_other_waistband", label: "no waist band" },
        { key: "no_other_legpasses", label: "no leg pass(es)" },
        { key: "no_other_eyelet", label: "no eyelet" },
        { key: "no_other_poppins", label: "no poppins (not as a pass)" },
        { key: "no_other_sternum", label: "no pond" },
    ];

    // Process the filter conditions
    filterConditions.forEach(({ key, value, format, condition }) => {
        if (condition(value)) {
            filtersApplied.appendChild(createFilterSpan(format(value)));
            anyApplied = true;
        }
    });

    // Process the boolean filters
    booleanFilters.forEach(({ key, label }) => {
        if (sessionStorage[key] === "1") {
            filtersApplied.appendChild(createFilterSpan(label));
            anyApplied = true;
        }
    });

    // If any filters were added, add the reset "x" button
    if (anyApplied) {
        const resetButton = document.createElement('span');
        resetButton.className = 'reset-button';
        resetButton.innerHTML = '&times;';  // Use &times; HTML entity for ×
        resetButton.title = 'Reset Filters';
        resetButton.onclick = function() {
            // Clear filters in sessionStorage
            resetFilters();
        };
        filtersApplied.appendChild(resetButton);
    }
}



async function showResults() {
    // Hide all filters
    hideAllFilters();

    // Show applied filters
    showAppliedFilters();

    // Populate gallery
    resultsPage = 1;
    const carries = await fetchFilteredCarries(resultsPage, pageSize);

    await updateCarryGallery(carries);

    updateFooterPosition();

    let button = document.getElementById("loadMore");
    if (resultsPage * pageSize < filteredResults) {
        // there is nothing else to load, so hide load button
        button.style.display = 'inline-block';
    } else {
        button.style.display = 'none';
    }
}


async function loadMore(button) {
    console.log("trying to show page", resultsPage);

    resultsPage += 1;
    const carries = await fetchFilteredCarries(resultsPage, pageSize);
    await updateCarryGallery(carries);

    // Check if even more could be loaded
    if (resultsPage * pageSize >= filteredResults) {
        // there is nothing else to load, so hide load button
        button.style.display = 'none';
    }
}


async function updateButtonBox() {
    const showResultsBtn = document.getElementById('showResultsBtn');
    const countText = document.getElementById('count-text');

    let num_carries = 0;
    try {
        const carries = await fetchFilteredCarries(1, 300);
        filteredResults = carries.length;
        
        if (carries.length === 0) {
            showResultsBtn.classList.remove('active');
            showResultsBtn.classList.add('disabled');
            showResultsBtn.disabled = true;
            showResultsBtn.textContent = "No results";
            countText.textContent = "No carries found";
        } else {
            showResultsBtn.classList.remove('disabled');
            showResultsBtn.disabled = false;
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
        resetFiltersBtn.disabled = false;
    } else {
        resetFiltersBtn.classList.add('disabled');
        resetFiltersBtn.disabled = true;
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
    sessionStorage.setItem(button.dataset.property, button.dataset.value);
}

function setActiveMultiButton(button) {
    // Make the selected filter button active when clicking on it
    const btnGroup = button.parentElement;
    const buttons = btnGroup.getElementsByClassName('btn-custom');
    const property = button.dataset.property;
    const selected = button.dataset.value;

    // Make all buttons inactive
    for (let btn of buttons) {
        btn.classList.remove('active');
        btn.blur();
        btn.classList.remove('hover');
    }

    let values;
    // If button is any, disable all other buttons
    if (selected === "Any") {
        // Create jsonified array with single value Any
        values = ["Any"];
    } else {
        // Get current list
        let valueString = sessionStorage.getItem(property); // Extract the values
        values = JSON.parse(valueString);

        // Ensure "Any" is not in the array
        values = values.filter(val => val !== "Any");

        // Append clicked on val to list
        if (!values.includes(selected)) {
            // If the value is not in the array, add it
            values.push(selected);
        } else {
            // If it is in the array, remove it
            values = values.filter(val => val !== selected);

            // If we removed the last value, change to "Any"
            if (values.length === 0) {
                values = ["Any"];
            }
        }
    }

    // Make all selected buttons active
    for (let val of values) {
        const button = getButtonByValueAndProperty(property, val);
        button.classList.add('active');
    }

    // Stringify new array
    valueString = JSON.stringify(values);
    
    // Store selected value in local storage
    sessionStorage.setItem(button.dataset.property, valueString);
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

        const footer = document.querySelector('footer');
        footer.style.display = 'none';

        // Empty gallery
        emptyCarryGallery();

        const loadMoreBtn = document.getElementById('loadMore');
        loadMoreBtn.style.display = 'none';

    } else {
        hideAllFilters();

        // Show applied filters
        showAppliedFilters();

        resultsPage = 1;
        const carries = await fetchFilteredCarries(resultsPage, pageSize);
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

    const filtersApplied = document.getElementById('filters-applied');
    filtersApplied.style.display = 'none';

    const gridContainer = document.getElementById('imageGrid');
    gridContainer.innerHTML = '';
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

    const filtersApplied = document.getElementById('filters-applied');
    filtersApplied.style.display = 'block';

    // Disable filters until all images have rendered
    const filterBtn = document.getElementById('button-filter');
    filterBtn.classList.add('disabled');
    filterBtn.setAttribute('disabled', true);
    document.getElementById("search-input").disabled = true;

    const loadingSpinner = document.getElementById('loadingSpinner');
    loadingSpinner.style.display = 'block';

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

            const faqTab = document.querySelector('.nav-link[data-page="faq-page"]');
            faqTab.classList.remove('active');

            // Redirect to the constructed URL
            window.location.href = url;
        });

        // Append grid item to fragment
        gridContainer.appendChild(gridItem);
    };

    // Reactivate the filter button
    filterBtn.classList.remove('disabled');
    filterBtn.removeAttribute('disabled');
    document.getElementById("search-input").disabled = false;

    loadingSpinner.style.display = 'none';

    // Check if footer must be changed
    updateFooterPosition();
}


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


let lastScrollTop = 0;
const header = document.getElementById('header');
let isScrollingUp = false;
let isScrollingDown = false;



document.addEventListener('DOMContentLoaded', async function() { 
    // Reset gallery
    emptyCarryGallery();

    // Decide where footer should be
    updateFooterPosition();

    // Set initial active buttons in filters
    const anyapplied = await initialiseFilters();

    // Update button box
    updateButtonBox();

    // Update reset filters button
    resetFiltersBtn = document.getElementById('resetFiltersBtn');

    // Get all carries with session data and update gallery
    resetFiltersBtn.classList.add('disabled');
    resetFiltersBtn.disabled = true;

    // Filter carries by the property selected in the button
    emptyCarryGallery();
    showResults();
    // }

    const searchInput = document.getElementById('search-input');
    searchInput.addEventListener('keydown', function(event) {
        if (event.key === 'Enter') {
            event.preventDefault(); // Prevent the default action (if necessary)
            handleInputChange();
            this.blur();
        }
    });
});


function togglePasses(iconElement, group) {
    const passesGroup = document.getElementById(group);

    if (passesGroup.style.display === "none") {
        passesGroup.style.display = "block";
        iconElement.classList.remove("fa-caret-down");
        iconElement.classList.add("fa-caret-up");
    } else {
        passesGroup.style.display = "none";
        iconElement.classList.remove("fa-caret-up");
        iconElement.classList.add("fa-caret-down");
    }
}
