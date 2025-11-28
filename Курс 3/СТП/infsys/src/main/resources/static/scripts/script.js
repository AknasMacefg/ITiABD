class Calendar {
    constructor() {
        this.calendar = document.getElementById('calendar');
        this.monthSelect = document.getElementById('month-select');
        this.yearSelect = document.getElementById('year-select');
        this.prevMonthBtn = document.getElementById('prev-month');
        this.nextMonthBtn = document.getElementById('next-month');
        this.prevYearBtn = document.getElementById('prev-year');
        this.nextYearBtn = document.getElementById('next-year');

        this.currentDate = new Date();
        this.events = {};

        this.init();
    }

    init() {
        this.initializeSelectors();
        this.renderCalendar();
        this.setupEventListeners();
        this.addTestEvents();
    }

    initializeSelectors() {
        // Месяцы
        const months = [
            'Январь', 'Февраль', 'Март', 'Апрель', 'Май', 'Июнь',
            'Июль', 'Август', 'Сентябрь', 'Октябрь', 'Ноябрь', 'Декабрь'
        ];

        this.monthSelect.innerHTML = '';
        months.forEach((month, index) => {
            const option = document.createElement('option');
            option.value = index;
            option.textContent = month;
            this.monthSelect.appendChild(option);
        });

        // Годы (от 2000 до 2030)
        this.yearSelect.innerHTML = '';
        for (let year = 2000; year <= 2030; year++) {
            const option = document.createElement('option');
            option.value = year;
            option.textContent = year;
            this.yearSelect.appendChild(option);
        }

        this.updateSelectors();
    }

    updateSelectors() {
        this.monthSelect.value = this.currentDate.getMonth();
        this.yearSelect.value = this.currentDate.getFullYear();

        // Блокировка кнопок при достижении границ
        this.prevYearBtn.disabled = this.currentDate.getFullYear() <= 2000;
        this.nextYearBtn.disabled = this.currentDate.getFullYear() >= 2030;
    }

    renderCalendar() {
        const year = this.currentDate.getFullYear();
        const month = this.currentDate.getMonth();

        // Удаляем старую сетку месяцев, если есть
        const oldGrid = document.querySelector('.month-grid');
        if (oldGrid) {
            oldGrid.remove();
        }

        const monthGrid = document.createElement('div');
        monthGrid.className = 'month-grid';

        // Заголовок месяца
        const monthHeader = document.createElement('div');
        monthHeader.className = 'current-month';
        monthHeader.textContent = `${this.currentDate.toLocaleString('ru', { month: 'long' })} ${year}`;
        monthHeader.style.gridColumn = '1 / -1';
        monthGrid.appendChild(monthHeader);

        // Первый день месяца
        const firstDay = new Date(year, month, 1);
        // Последний день месяца
        const lastDay = new Date(year, month + 1, 0);
        // День недели первого дня (0 - воскресенье, 1 - понедельник и т.д.)
        let firstDayWeekday = firstDay.getDay();
        if (firstDayWeekday === 0) firstDayWeekday = 7; // Воскресенье -> 7

        // Добавляем пустые ячейки для дней предыдущего месяца
        for (let i = 1; i < firstDayWeekday; i++) {
            const prevMonthDay = new Date(year, month, 1 - i);
            const emptyDay = this.createDayElement(prevMonthDay, true);
            monthGrid.appendChild(emptyDay);
        }

        // Ячейки текущего месяца
        for (let day = 1; day <= lastDay.getDate(); day++) {
            const dayDate = new Date(year, month, day);
            const dayElement = this.createDayElement(dayDate, false);
            monthGrid.appendChild(dayElement);
        }

        // Добавляем пустые ячейки для дней следующего месяца
        const totalCells = 42; // 6 строк по 7 дней
        const existingCells = monthGrid.children.length - 1; // минус заголовок
        const remainingCells = totalCells - existingCells;

        for (let i = 1; i <= remainingCells; i++) {
            const nextMonthDay = new Date(year, month + 1, i);
            const emptyDay = this.createDayElement(nextMonthDay, true);
            monthGrid.appendChild(emptyDay);
        }

        this.calendar.appendChild(monthGrid);
        this.updateSelectors();
    }

    createDayElement(date, isOtherMonth) {
        const dayElement = document.createElement('div');
        dayElement.className = 'day';

        if (isOtherMonth) {
            dayElement.classList.add('other-month');
        }

        // Проверка на выходные
        const dayOfWeek = date.getDay();
        if (dayOfWeek === 0 || dayOfWeek === 6) {
            dayElement.classList.add('weekend');
        }

        // Проверка на сегодняшний день
        const today = new Date();
        if (date.toDateString() === today.toDateString()) {
            dayElement.classList.add('today');
        }

        // Номер дня
        const dayNumber = document.createElement('div');
        dayNumber.className = 'day-number';
        dayNumber.textContent = date.getDate();
        dayElement.appendChild(dayNumber);

        // Область для событий
        const eventsContainer = document.createElement('div');
        eventsContainer.className = 'events';

        // Проверяем есть ли события для этой даты
        const dateKey = date.toISOString().split('T')[0];
        if (this.events[dateKey] && this.events[dateKey].length > 0) {
            this.events[dateKey].forEach(event => {
                const eventElement = document.createElement('div');
                eventElement.innerHTML = `<span class="event-marker"></span>${event}`;
                eventsContainer.appendChild(eventElement);
            });
        }

        dayElement.appendChild(eventsContainer);

        // Добавляем обработчик клика для создания событий
        dayElement.addEventListener('click', () => {
            if (!isOtherMonth) {
                this.handleDayClick(date);
            }
        });

        return dayElement;
    }

    handleDayClick(date) {
        const eventText = prompt('Добавить событие:');
        if (eventText) {
            this.addEvent(date, eventText);
            this.renderCalendar();
        }
    }

    addEvent(date, text) {
        const dateKey = date.toISOString().split('T')[0];
        if (!this.events[dateKey]) {
            this.events[dateKey] = [];
        }
        this.events[dateKey].push(text);
    }

    setupEventListeners() {
        this.prevMonthBtn.addEventListener('click', () => {
            this.currentDate.setMonth(this.currentDate.getMonth() - 1);
            this.renderCalendar();
        });

        this.nextMonthBtn.addEventListener('click', () => {
            this.currentDate.setMonth(this.currentDate.getMonth() + 1);
            this.renderCalendar();
        });

        this.prevYearBtn.addEventListener('click', () => {
            if (this.currentDate.getFullYear() > 2000) {
                this.currentDate.setFullYear(this.currentDate.getFullYear() - 1);
                this.renderCalendar();
            }
        });

        this.nextYearBtn.addEventListener('click', () => {
            if (this.currentDate.getFullYear() < 2030) {
                this.currentDate.setFullYear(this.currentDate.getFullYear() + 1);
                this.renderCalendar();
            }
        });

        this.monthSelect.addEventListener('change', () => {
            this.currentDate.setMonth(parseInt(this.monthSelect.value));
            this.renderCalendar();
        });

        this.yearSelect.addEventListener('change', () => {
            this.currentDate.setFullYear(parseInt(this.yearSelect.value));
            this.renderCalendar();
        });
    }

    addTestEvents() {
        const today = new Date();
        const tomorrow = new Date(today);
        tomorrow.setDate(today.getDate() + 1);

        this.addEvent(today, 'Пример события');
        this.addEvent(tomorrow, 'Встреча');
        this.addEvent(tomorrow, 'День рождения');
    }
}

// Инициализация календаря после загрузки DOM
document.addEventListener('DOMContentLoaded', () => {
    new Calendar();
});