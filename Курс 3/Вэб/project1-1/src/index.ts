const { fromEvent, withLatestFrom, map, merge, mergeWith } = window.rxjs;

import { inRange, toNumber } from './helpers';
import { value$ } from './state';

const buttonMinus = document.querySelector<HTMLButtonElement>('.button_minus');
const buttonPlus = document.querySelector<HTMLButtonElement>('.button_plus');
const buttonMute = document.querySelector<HTMLButtonElement>('.button_mute');
const input = document.querySelector<HTMLInputElement>('.input');
const progress = document.querySelector<HTMLProgressElement>('.progress');

if (buttonMinus && buttonPlus && input && progress && buttonMute) {
    /* Подписываемся на изменение данных */
    value$.subscribe(value => {
        input.value = String(value);
        progress.value = value;
    });

    /* Создаём поток из нажатий на кнопку - */
    const decrements$ = fromEvent(buttonMinus, 'click')
        /* Превращаем каждый элемент потока в -1 */
        .pipe(map(() => -5));

    /* Создаём поток из нажатий на кнопку + */
    const increments$ = fromEvent(buttonPlus, 'click')
        /* Превращаем каждый элемент потока в 1 */
        .pipe(map(() => 5));

    const mute$ = fromEvent(buttonMute, 'click' )
        .pipe(map(() => -100));
    /* Создаём поток изменений поля ввода */
    const byInput$ = fromEvent(input, 'change')
        /* Превращаем каждый элемент потока в значение поле ввода */
        .pipe(map(() => toNumber(input.value)));

    /* Объединяем потоки инкремента и декремента */
    merge(decrements$, increments$, mute$).pipe(
        /* Присоединяем к каждому элементу последнее значение громкости */
        withLatestFrom(value$),
        /* Складываем предыдущее значение и инкремент */
        map(([increment, previous]) => previous + increment),
        /* Объедняем с потоком значений поля ввода */
        mergeWith(byInput$),
        /* Корректируем результат, чтобы он не выходил за пределы допустимого интервала */
        map(inRange(0, 100)),
    /* Помещаем каждое новое значение в поток значений уровня громкости */
    ).subscribe(result => value$.next(result));
}