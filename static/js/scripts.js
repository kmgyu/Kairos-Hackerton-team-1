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
    

    if (branch > 4) {
        window.location.href = '/game_ending'
    }
    else{
        // branch 값을 1 증가시킴
          branch += 1;

         // URL에 새로운 branch 값을 설정
        url.searchParams.set('branch', branch);

        // 새로운 URL로 리디렉션
        window.location.href = url.toString();
    }
   
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

function confirmCharacter() {
    const name = document.getElementById('name').value;
    const job = document.getElementById('job').value;

    // 스탯 값을 가져오는 코드 (예시: HTML에 해당 값을 넣은 요소가 있다고 가정)
    const strength = parseInt(document.getElementById('strength').textContent, 10);
    const dexterity = parseInt(document.getElementById('dexterity').textContent, 10);
    const defense = parseInt(document.getElementById('defense').textContent, 10);

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

    // 데이터 전송
    fetch('/confirm_character', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            name: name,
            job: job,
            Strength: strength,
            Dexterity: dexterity,
            Defense: defense
        }),
    })
    .then(response => response.json())  // 서버에서 받은 응답을 JSON으로 처리
    .then(data => {
        if (data.status === 'Character confirmed') {
            // 서버 응답에 따라 페이지 이동 없이 캐릭터 정보 처리
            window.location.href = '/ingame_ui';  // 페이지 이동
        } else {
            alert('Failed to confirm character.');
        }
    })
    .catch(error => {
        console.error('Error:', error);
    });
}

// 선택지1 선택 시 호출되는 함수
function chooseOption(option) {
    let resultContent = '';

    if (option === 1) {
        resultContent = '선택지 1을 선택하셨습니다.';
    } else if (option === 2) {
        resultContent = '선택지 2를 선택하셨습니다.';
    }

    // 결과를 result-box에 표시
    document.getElementById('result-content').textContent = resultContent;
    document.getElementById('result-box').style.display = 'block';

    // "다음으로" 버튼을 보이게 함
    document.getElementById('next-button-container').style.display = 'block';

    // 선택지와 주사위 버튼 숨기기
    document.getElementById('choices-container').style.display = 'none';
    const sendButton = document.getElementById('send-button');
    sendButton.disabled = true; // 전송 버튼 비활성화

    
}

// 주사위 사용 시 호출되는 함수
function useDice() {
    let diceRoll = Math.floor(Math.random() * 6) + 1;
    let resultContent = `주사위 결과: ${diceRoll}`;

    // 결과를 result-box에 표시
    document.getElementById('result-content').textContent = resultContent;
    document.getElementById('result-box').style.display = 'block';

    // "다음으로" 버튼을 보이게 함
    document.getElementById('next-button-container').style.display = 'block';

    // 선택지와 주사위 버튼 숨기기
    document.getElementById('choices-container').style.display = 'none';

    const sendButton = document.getElementById('send-button');
    sendButton.disabled = true; // 전송 버튼 비활성화
}

// branch 값에 따라 페이지를 변경하는 함수
function changeBranch() {
    // 현재 URL에서 'branch' 파라미터 값을 가져옴
    const url = new URL(window.location.href);
    let branch = parseInt(url.searchParams.get('branch') || 0);  // 기본값 0 설정

    // branch 값을 1 증가시킴
    if (branch > 8){
        window.location.href = '/game_ending';
    }
    else{
        branch += 1;

        // URL에 새로운 branch 값을 설정
        url.searchParams.set('branch', branch);

        // 새로운 URL로 리디렉션
        window.location.href = url.toString();
    }
}

function printf() {
    const userInput = document.getElementById('user-input').value;

    // fetch 요청 보내기
    fetch('/printf', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ user_input: userInput })  // 서버로 보내는 데이터
    })
    .then(response => response.json())
    .then(data => {
        // 서버 응답을 HTML에 출력
        document.getElementById('output').textContent = `입력: ${data.input_received}`;
        document.getElementById('output').style.display = 'block';
        // 입력 필드 초기화
        document.getElementById('user-input').value = '';
        const sendButton = document.getElementById('send-button');
        sendButton.disabled = true;
    })
    .catch(error => {
        console.error('Error:', error);
    });
}