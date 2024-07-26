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
    filterCarries();
}

async function handleSelectChange(dropdown) {
    const selectedOption = dropdown.options[dropdown.selectedIndex];

    // Store selected value in local storage
    localStorage.setItem(selectedOption.dataset.property, selectedOption.value);

    // Filter carries by the properties selected
    filterCarries();
}


async function handleSwitchChange(switch_) {
    let checked = 0;
    if (switch_.checked) {
        checked = 1;
    }

    // Store selected value in local storage
    localStorage.setItem(switch_.dataset.property, checked);

    // Filter carries by the properties selected
    filterCarries();
}


function handleInputChange() {
    const searchInput = document.getElementById('search-input');
    localStorage.setItem('partialname', searchInput.value);

    // Filter carries by the property selected in the button
    filterCarries();
}

function initialiseSwitchData(property) {
    let init = 0;

    if (!localStorage.getItem(property)) {
        localStorage.setItem(property, 0);
    } else {
        init = localStorage.getItem(property);

        // If any switches on, show filter box to alert user
        if (init === '1') {
            showAllFilters();
        }
    }

    // Get switch with this property and value
    const switch_ = getSwitchByProperty(property);
    if (switch_) {
        if (init === '1') {
            switch_.checked = true;
        } else {
            switch_.checked = false;
        }
    }
}


function hideAllFilters() {
    const filterBox = document.getElementById('filterBox');
    filterBox.style.display = 'none';

    const showMoreBtn = document.getElementById('showMoreBtn');
    showMoreBtn.style.display = 'none';

    const filterBoxExt = document.getElementById('filterBoxExt');
    filterBoxExt.style.display = 'none';

    const buttonBox = document.getElementById('buttonBox');
    buttonBox.style.display = 'none';
}


function showAllFilters() {
    const filterBox = document.getElementById('filterBox');
    filterBox.style.display = 'block';

    const showMoreBtn = document.getElementById('showMoreBtn');
    showMoreBtn.style.display = 'none';

    const filterBoxExt = document.getElementById('filterBoxExt');
    filterBoxExt.style.display = 'block';

    const buttonBox = document.getElementById('buttonBox');
    buttonBox.style.display = 'block';
}

async function resetFilters() {
    localStorage.setItem("size", "Any");
    localStorage.setItem("position", "Any");
    localStorage.setItem("difficulty", "Any");
    localStorage.setItem("finish", "Any");
    localStorage.setItem("fancy", "0");
    localStorage.setItem("pretied", "0");

    initialiseFiltersData();

    // Filter carries in gallery
    filterCarries();
}

function initialiseButtonData(property) {
    let init = 'Any';
    if (!localStorage.getItem(property)) {
        // If not, set the counter to 0 in local storage
        localStorage.setItem(property, 'Any');
    } else {
        init = localStorage.getItem(property);

        if (init !== "Any") {
            // If any filters applied, show filter box to alert user
            const filterBox = document.getElementById('filterBox');
            filterBox.style.display = 'block';
        }
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
}

function initialiseDropdownData(property) {
    let init = 'Any';
    if (!localStorage.getItem(property)) {
        // If not, set the counter to 0 in local storage
        localStorage.setItem(property, 'Any');
    } else {
        init = localStorage.getItem(property);

        if (init !== "Any") {
            showAllFilters();
        }
    }

    // If it's not a button, it may be a dropdown
    const optionToSelect = getDropdownByValueAndProperty(property, init);
    if (optionToSelect) {
        optionToSelect.selected = true;
    }
}


function initialiseSearchBar() {
    // Set content to localstorage if available
    if (localStorage.getItem('partialname')) {
        const searchInput = document.getElementById('search-input');
        searchInput.value = localStorage.getItem('partialname');
    }
}

function initialiseFiltersData() {
    initialiseButtonData('size');
    initialiseButtonData('position');
    initialiseDropdownData('difficulty');
    initialiseDropdownData('finish');
    initialiseSwitchData('fancy');
    initialiseSwitchData('pretied');
    initialiseSearchBar();

}

async function fetchFilteredCarries() {
    // Read the property of the button group and the button value
    const filters = {
        size: localStorage.getItem("size"),
        position: localStorage.getItem("position"),
        difficulty: localStorage.getItem("difficulty"),
        partialname: localStorage.getItem("partialname"),
        pretied: localStorage.getItem("pretied"),
        fancy: localStorage.getItem("fancy"),
        finish: localStorage.getItem("finish"),
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

function showResults() {
    // Hide all filters
    hideAllFilters();

    // Scroll to gallery
    var targetElement = document.getElementById('imageGrid');
    targetElement.scrollIntoView({ behavior: 'smooth', block: 'start' });
}

async function filterCarries() {
    try {
        const carries = await fetchFilteredCarries();
        
        // Update gallery content
        await updateCarryGallery(carries);

        const showResultsBtn = document.getElementById('showResultsBtn');

        if (carries.length === 0) {
            showResultsBtn.classList.remove('active');
            showResultsBtn.classList.add('disabled');
            showResultsBtn.textContent = "No results";
        } else {
            showResultsBtn.classList.remove('disabled');
            showResultsBtn.classList.add('active');
            showResultsBtn.textContent = "Show " + carries.length + " results";
        }
    } catch (error) {
        console.error('There was a problem with the fetch operation:', error);
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

function toggleFilterBox() {
    const filterBox = document.getElementById('filterBox');
    if (filterBox.style.display === 'none') {
        filterBox.style.display = 'block';

        const buttonBox = document.getElementById('buttonBox');
        buttonBox.style.display = 'block';

        const showMoreBtn = document.getElementById('showMoreBtn');
        showMoreBtn.style.display = 'block';
    } else {
        hideAllFilters();
    }
}

function showFilterBoxExt() {
    const filterBoxExt = document.getElementById('filterBoxExt');
    filterBoxExt.style.display = 'block';

    const showMoreBtn = document.getElementById('showMoreBtn');
    showMoreBtn.style.display = 'none';
}

function hideFilterBoxExt() {
    const filterBoxExt = document.getElementById('filterBoxExt');
    filterBoxExt.style.display = 'none';

    const showMoreBtn = document.getElementById('showMoreBtn');
    showMoreBtn.style.display = 'block';
}


async function fetchFileUrl(fileName) {
    try {
        const response = await fetch(`/file-url/${fileName}/`);
        const data = await response.json();
        return data.url;
    } catch (error) {
        console.error('Error fetching file URL:', error);
    }
}


async function updateCarryGallery(carries) {
    // Get imageGrid div
    const gridContainer = document.getElementById('imageGrid');
    gridContainer.innerHTML = '';
    const baseUrlPattern = gridContainer.dataset.baseUrlPattern.replace('PLACEHOLDER', '');

    for (const carry of carries) {
        // Create grid item
        const gridItem = document.createElement('div');
        gridItem.className = 'grid-item';

        // Set image URL
        let imageFile = carry.carry__coverpicture;

        // Use placeholder if carry image not available
        if (carry.carry__coverpicture === "" ||
            carry.carry__coverpicture === null) {
            if (carry.carry__position === "back") {
                imageFile = "placeholder_back.png";
            } else {
                imageFile = "placeholder_front.png";
            }
        }

        const fileUrl = await fetchFileUrl(imageFile);

        // Create image
        const img = document.createElement('img');
        img.src = fileUrl; // Combine the static URL with the file name
        img.alt = carry.carry__name;
        
        // Create on click functionality
        img.addEventListener('click', function() {
            // Construct the full URL by appending the name to the base URL pattern
            const url = `${baseUrlPattern}${carry.carry__name}`;
            
            // Clear active tab
            const carriesTab = document.querySelector('.nav-link[data-page="carries-page"]');
            carriesTab.classList.remove('active');

            const aboutTab = document.querySelector('.nav-link[data-page="about-page"]');
            aboutTab.classList.remove('active');

            // Redirect to the constructed URL
            window.location.href = url;
        });

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
        if (carry.carry__size == 0) {
            sizedesc.textContent = "Base";
        } else {
            sizedesc.textContent = "Base " + carry.carry__size;
        }

        // Append descriptions to the description container
        descContainer.appendChild(carrydesc);
        descContainer.appendChild(sizedesc);

        // Append image and description container to grid item
        gridItem.appendChild(img);
        gridItem.appendChild(descContainer);

        // Append grid item to grid container
        gridContainer.appendChild(gridItem);
    }
}


document.addEventListener('DOMContentLoaded', function() { 
    // Set initial active buttons in filters
    initialiseFiltersData();

    // Filter carries in gallery
    filterCarries();

    const searchInput = document.getElementById('search-input');
    searchInput.addEventListener('keydown', function(event) {
        if (event.key === 'Enter') {
            handleInputChange();
        }
    });
});
