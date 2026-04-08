const {BehaviorSubject} = window.rxjs;

/** Поток, содержащий значения громкости */
export const value$ = new BehaviorSubject(50);