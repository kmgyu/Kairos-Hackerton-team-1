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

function changeBranch() {
    // 현재 URL에서 'branch' 파라미터 값을 가져옴
    const url = new URL(window.location.href);
    let branch = parseInt(url.searchParams.get('branch') || 0);  // 기본값 0 설정

    // branch 값을 1 증가시킴
    branch += 1;

    // URL에 새로운 branch 값을 설정
    url.searchParams.set('branch', branch);

    // 새로운 URL로 리디렉션
    window.location.href = url.toString();
}

// 스탯 업데이트 함수
function updateStat(stat, amount) {
    fetch('/update_stats', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ stat: stat, amount: amount }),
    })
    .then(response => response.json())
    .then(data => {
        // UI 업데이트
        document.getElementById('strength').textContent = data.stats.Strength;
        document.getElementById('dexterity').textContent = data.stats.Dexterity;
        document.getElementById('defense').textContent = data.stats.Defense;
        document.getElementById('points').textContent = data.points;
    })
    .catch(error => {
        console.error('Error:', error);
    });
}

// 스탯 초기화 함수
function resetStats() {
    fetch('/reset_stats', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
    })
    .then(response => response.json())
    .then(data => {
        // UI 초기화
        document.getElementById('strength').textContent = data.stats.Strength;
        document.getElementById('dexterity').textContent = data.stats.Dexterity;
        document.getElementById('defense').textContent = data.stats.Defense;
        document.getElementById('points').textContent = data.points;

        // 이름과 직업 초기화
        document.getElementById('name').value = data.name;
        document.getElementById('job').value = data.job;
    })
    .catch(error => {
        console.error('Error:', error);
    });
}

// 캐릭터 확정 함수
function confirmCharacter() {
    const name = document.getElementById('name').value;
    const job = document.getElementById('job').value;

    if (!name) {
        alert('Please enter a name for your character.');
        return;
    }

    if (!job) {
        alert('Please choose a job for your character.');
        return;
    }

    if (points > 0) {
        alert('You must allocate all points before proceeding.');
        return;
    }

    fetch('/confirm_character', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ name: name, job: job }),
    })
    .catch(error => {
        print("error")
        console.error('Error:', error);
    });

}