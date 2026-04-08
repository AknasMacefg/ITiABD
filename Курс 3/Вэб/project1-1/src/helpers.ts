/** Корректирует значение в заданном диапазоне */
export const inRange = (min: number, max: number) =>
    (value: number) => Math.min(Math.max(min, value), max);

/** Превращает NaN в 0 */
export const notNaN = (value: number) => isNaN(value) ? 0 : value;

/** Преобразует строку в число */
export const toNumber = (value: string) => notNaN(parseInt(value));