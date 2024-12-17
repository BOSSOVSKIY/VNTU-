document.getElementById('scan-form').addEventListener('submit', function(event) {
    event.preventDefault();

    const email = document.getElementById('email').value;
    const password = document.getElementById('password').value;
    if (!email || !password) {
        alert('Email и пароль обязательны!');
        return;
    }

    const progressBar = document.getElementById('progress-bar');
    const progressText = document.getElementById('progress-text');
    const progressContainer = document.getElementById('progress-container');
    const resultsContainer = document.getElementById('results-container');
    const resultsList = document.getElementById('results-list');
    
    progressContainer.style.display = 'block';
    resultsContainer.style.display = 'none';
    progressBar.value = 0;
    progressText.textContent = '0%';

    let progress = 0;
    const interval = setInterval(() => {
        progress += 1;
        progressBar.value = progress;
        progressText.textContent = `${progress}%`;

        if (progress >= 100) {
            clearInterval(interval);

            // Генерация случайного числа подозрительных писем (от 0 до 50)
            const suspiciousEmailsCount = Math.floor(Math.random() * 10);

            // Создание и добавление сообщения о подозрительных письмах
            const spamMessageDiv = document.createElement('div');
            spamMessageDiv.textContent = `На пошті ${email} знайдено ${suspiciousEmailsCount} підозрілих листів.`;
            resultsContainer.appendChild(spamMessageDiv);
            
            // Отображение результатов
            resultsContainer.style.display = 'block';
        }
    }, 50); // Настройка скорости интервала по необходимости
});
