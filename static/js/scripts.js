async function fetchData(url) {
    const response = await fetch(url);
    return response.json();
}

function moveSlide(sectionId, direction) {
    const slider = document.getElementById(sectionId);
    const content = slider.querySelector(".slider-content");
    const items = content.children;

    if (!items.length) return; // No items to slide

    const itemWidth = items[0].offsetWidth + 20; // Include margin or gap
    const maxScroll = content.scrollWidth - content.offsetWidth;
    let currentScroll = content.scrollLeft;

    // Calculate new scroll position
    let newScroll = currentScroll + direction * itemWidth;

    // Prevent scrolling beyond boundaries
    if (newScroll < 0) newScroll = 0;
    if (newScroll > maxScroll) newScroll = maxScroll;

    // Apply smooth scrolling
    content.scrollTo({
        left: newScroll,
        behavior: "smooth",
    });
}


function populateSlider(data, containerId) {
    const container = document.getElementById(containerId).querySelector('.slider-content');
    container.innerHTML = ''; // Clear existing content

    data.forEach(item => {
        const li = document.createElement('li');
        if (item.situation) {
            li.innerHTML = `
                <p><strong>Situation:</strong> ${item.situation}</p>
                <p><strong>Choices:</strong> ${item.choices}</p>
                <p><strong>Result:</strong> ${item.result}</p>
            `;
        } else if (item.title) {
            li.innerHTML = `
                <p><strong>${item.title}</strong></p>
                <p>${item.summary || ''}</p>
            `;
        }
        container.appendChild(li);
    });
}

async function loadRecentEvents() {
    const data = await fetchData('/api/recent-events');
    populateSlider(data, 'recent-events');
}

async function loadCompletedQuests() {
    const data = await fetchData('/api/completed-quests');
    populateSlider(data, 'completed-quests');
}

async function loadCurrentQuest() {
    const data = await fetchData('/api/current-quest');
    const container = document.getElementById('current-quest');
    container.innerHTML = `
        <p><strong>${data.title}</strong></p>
        <p>${data.description}</p>
        <p><strong>Progress:</strong> ${data.progress}%</p>
    `;
}

// Load data on page load
document.addEventListener('DOMContentLoaded', () => {
    loadRecentEvents();
    loadCompletedQuests();
    loadCurrentQuest();
});