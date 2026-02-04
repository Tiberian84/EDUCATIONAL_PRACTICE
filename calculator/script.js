// Получаем элементы из DOM
const num1Input = document.getElementById('num1');
const num2Input = document.getElementById('num2');
const resultEl = document.getElementById('result');

const sumBtn = document.getElementById('sum');
const diffBtn = document.getElementById('difference');
const prodBtn = document.getElementById('product');
const divBtn = document.getElementById('division');

// Функция валидации ввода
function validateInput() {
    const num1 = num1Input.value.trim();
    const num2 = num2Input.value.trim();
    
    // Проверяем, что поля не пустые
    if (num1 === '' || num2 === '') {
        showError('Пожалуйста, заполните оба поля');
        return null;
    }
    
    // Преобразуем в числа
    const val1 = parseFloat(num1);
    const val2 = parseFloat(num2);
    
    // Проверяем, что введены числа
    if (isNaN(val1) || isNaN(val2)) {
        showError('Ошибка: введите корректные числа');
        return null;
    }
    
    return { val1, val2 };
}

// Функция показа ошибки
function showError(message) {
    resultEl.textContent = message;
    resultEl.className = 'result error';
}

// Функция показа результата
function showResult(value) {
    // Форматируем результат: если целое число - без десятичных знаков
    // Если дробное - оставляем до 6 знаков после запятой
    const formatted = Number.isInteger(value) ? value : parseFloat(value.toFixed(6));
    resultEl.textContent = formatted;
    resultEl.className = 'result';
}

// Математические функции
function sum(a, b) {
    return a + b;
}

function difference(a, b) {
    return a - b;
}

function product(a, b) {
    return a * b;
}

function division(a, b) {
    if (b === 0) {
        throw new Error('Ошибка: деление на ноль');
    }
    return a / b;
}

// Обработчики событий для кнопок
sumBtn.addEventListener('click', () => {
    const values = validateInput();
    if (!values) return;
    
    try {
        const result = sum(values.val1, values.val2);
        showResult(result);
    } catch (error) {
        showError(error.message);
    }
});

diffBtn.addEventListener('click', () => {
    const values = validateInput();
    if (!values) return;
    
    try {
        const result = difference(values.val1, values.val2);
        showResult(result);
    } catch (error) {
        showError(error.message);
    }
});

prodBtn.addEventListener('click', () => {
    const values = validateInput();
    if (!values) return;
    
    try {
        const result = product(values.val1, values.val2);
        showResult(result);
    } catch (error) {
        showError(error.message);
    }
});

divBtn.addEventListener('click', () => {
    const values = validateInput();
    if (!values) return;
    
    try {
        const result = division(values.val1, values.val2);
        showResult(result);
    } catch (error) {
        showError(error.message);
    }
});

// Дополнительный функционал: нажатие Enter для быстрого расчёта
num1Input.addEventListener('keypress', (e) => {
    if (e.key === 'Enter') {
        sumBtn.click();
    }
});

num2Input.addEventListener('keypress', (e) => {
    if (e.key === 'Enter') {
        sumBtn.click();
    }
});