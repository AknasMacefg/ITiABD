(() => {
    const board = document.getElementById('game-board');
    const target = document.getElementById('target');
    const startOverlay = document.getElementById('start-overlay');
    const startButton = document.getElementById('start-button');
    const timeLeft = document.getElementById('time-left');
    const scoreValue = document.getElementById('score-value');
    const scoreInput = document.getElementById('score-input');
    const scoreForm = document.getElementById('score-form');

    if (!board || !target || !startButton || !timeLeft || !scoreValue || !scoreInput || !scoreForm) {
        return;
    }

    const duration = Number(timeLeft.textContent || 60);
    let remaining = duration;
    let score = 0;
    let started = false;
    let timerHandle = null;
    let spawnHandle = null;
    let hideHandle = null;
    let targetVisible = false;

    const clearHandles = () => {
        window.clearInterval(timerHandle);
        window.clearTimeout(spawnHandle);
        window.clearTimeout(hideHandle);
    };

    const updateScore = () => {
        scoreValue.textContent = String(score);
        scoreInput.value = String(score);
    };

    const updateTimer = () => {
        timeLeft.textContent = String(Math.max(remaining, 0));
    };

    const getDifficulty = () => 1 - remaining / duration;

    const positionTarget = () => {
        const boardRect = board.getBoundingClientRect();
        const circleSize = Math.max(68 - getDifficulty() * 18, 42);
        const maxX = Math.max(boardRect.width - circleSize - 24, 0);
        const maxY = Math.max(boardRect.height - circleSize - 24, 0);
        const left = Math.random() * maxX + 12;
        const top = Math.random() * maxY + 12;

        target.style.width = `${circleSize}px`;
        target.style.height = `${circleSize}px`;
        target.style.left = `${left}px`;
        target.style.top = `${top}px`;
    };

    const hideTarget = () => {
        targetVisible = false;
        target.classList.remove('visible');
    };

    const showTarget = () => {
        if (!started || remaining <= 0) {
            return;
        }

        positionTarget();
        targetVisible = true;
        target.classList.add('visible');

        const lifeTime = Math.max(1200 - getDifficulty() * 900, 320);
        window.clearTimeout(hideHandle);
        hideHandle = window.setTimeout(() => {
            hideTarget();
            scheduleNextSpawn();
        }, lifeTime);
    };

    const scheduleNextSpawn = () => {
        if (!started || remaining <= 0) {
            return;
        }

        const spawnDelay = Math.max(720 - getDifficulty() * 520, 180);
        window.clearTimeout(spawnHandle);
        spawnHandle = window.setTimeout(showTarget, spawnDelay);
    };

    const finishGame = () => {
        if (!started) {
            return;
        }

        started = false;
        clearHandles();
        hideTarget();
        startOverlay.classList.add('visible');
        startOverlay.querySelector('h1').textContent = 'Время вышло';
        startOverlay.querySelector('p').textContent = `Финальный счёт: ${score}`;
        scoreForm.submit();
    };

    const startGame = () => {
        if (started) {
            return;
        }

        started = true;
        remaining = duration;
        score = 0;
        updateScore();
        updateTimer();
        startOverlay.classList.remove('visible');
        showTarget();

        timerHandle = window.setInterval(() => {
            remaining -= 1;
            updateTimer();
            if (remaining <= 0) {
                finishGame();
            }
        }, 1000);
    };

    target.addEventListener('click', () => {
        if (!started || !targetVisible) {
            return;
        }

        score += 1;
        updateScore();
        hideTarget();
        window.clearTimeout(hideHandle);
        scheduleNextSpawn();
    });

    startButton.addEventListener('click', startGame);
    updateScore();
    updateTimer();
})();