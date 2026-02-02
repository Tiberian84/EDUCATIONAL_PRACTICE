// Получаем элементы из DOM
const minusBtn = document.getElementById('minus');
const plusBtn = document.getElementById('plus');
const resultEl = document.getElementById('result');
const messageEl = document.getElementById('message');

// Инициализируем счётчик
let count = 0;

// Функция обновления отображения
function updateDisplay() {
    // Обновляем текст в окошке
    resultEl.textContent = count;
    
    // Меняем фон в зависимости от значения
    resultEl.className = 'result'; // Сбрасываем все классы
    
    if (count > 0) {
        resultEl.classList.add('positive'); // Жёлтый фон
    } else if (count < 0) {
        resultEl.classList.add('negative'); // Зелёный фон
    } else {
        resultEl.classList.add('zero'); // Красный фон
    }
    
    // Блокируем/разблокируем кнопки при достижении экстремальных значений
    if (count >= 10) {
        plusBtn.disabled = true;
    } else {
        plusBtn.disabled = false;
    }
    
    if (count <= -10) {
        minusBtn.disabled = true;
    } else {
        minusBtn.disabled = false;
    }
    
    // Показываем/скрываем сообщение
    if (count === 10 || count === -10) {
        messageEl.textContent = '⚠️ Вы достигли экстремального значения';
        messageEl.classList.add('show');
    } else {
        messageEl.classList.remove('show');
    }
}

// Обработчик нажатия кнопки "минус"
minusBtn.addEventListener('click', () => {
    count--;
    updateDisplay();
});

// Обработчик нажатия кнопки "плюс"
plusBtn.addEventListener('click', () => {
    count++;
    updateDisplay();
});

// Инициализируем отображение при загрузке страницы
updateDisplay();