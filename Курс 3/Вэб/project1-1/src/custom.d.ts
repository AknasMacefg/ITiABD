export class BehaviorSubject<T> extends Subject<T> {
    constructor(_value: T);

    getValue(): T;

    next(value: T): void;
}

export interface Observer<T> {
    next: (value: T) => void;
    error: (err: any) => void;
    complete: () => void;
}

export interface Subscribable<T> {
    subscribe(observer: Partial<Observer<T>>): Unsubscribable;
}

export type TeardownLogic = Subscription | Unsubscribable | (() => void) | void;

export interface Operator<T, R> {
    call(subscriber: Subscriber<R>, source: any): TeardownLogic;
}

export interface UnaryFunction<T, R> {
    (source: T): R;
}

export interface OperatorFunction<T, R> extends UnaryFunction<Observable<T>, Observable<R>> {}

export class Observable<T> implements Subscribable<T> {
    constructor(subscribe: (this: Observable<T>, subscriber: Subscriber<T>) => TeardownLogic);

    "@@observable"(): any;

    forEach(next: (value: T) => void, promiseCtor: PromiseConstructorLike): Promise<void>;

    lift<R>(operator: Operator<T, R>): Observable<R>;

    pipe(): Observable<T>;
    pipe<A>(op1: OperatorFunction<T, A>): Observable<A>;
    pipe<A, B>(op1: OperatorFunction<T, A>, op2: OperatorFunction<A, B>): Observable<B>;
    pipe<A, B, C>(op1: OperatorFunction<T, A>, op2: OperatorFunction<A, B>, op3: OperatorFunction<B, C>): Observable<C>;
    pipe<A, B, C, D>(
        op1: OperatorFunction<T, A>,
        op2: OperatorFunction<A, B>,
        op3: OperatorFunction<B, C>,
        op4: OperatorFunction<C, D>
    ): Observable<D>;
    pipe<A, B, C, D, E>(
        op1: OperatorFunction<T, A>,
        op2: OperatorFunction<A, B>,
        op3: OperatorFunction<B, C>,
        op4: OperatorFunction<C, D>,
        op5: OperatorFunction<D, E>
    ): Observable<E>;
    pipe<A, B, C, D, E, F>(
        op1: OperatorFunction<T, A>,
        op2: OperatorFunction<A, B>,
        op3: OperatorFunction<B, C>,
        op4: OperatorFunction<C, D>,
        op5: OperatorFunction<D, E>,
        op6: OperatorFunction<E, F>
    ): Observable<F>;
    pipe<A, B, C, D, E, F, G>(
        op1: OperatorFunction<T, A>,
        op2: OperatorFunction<A, B>,
        op3: OperatorFunction<B, C>,
        op4: OperatorFunction<C, D>,
        op5: OperatorFunction<D, E>,
        op6: OperatorFunction<E, F>,
        op7: OperatorFunction<F, G>
    ): Observable<G>;
    pipe<A, B, C, D, E, F, G, H>(
        op1: OperatorFunction<T, A>,
        op2: OperatorFunction<A, B>,
        op3: OperatorFunction<B, C>,
        op4: OperatorFunction<C, D>,
        op5: OperatorFunction<D, E>,
        op6: OperatorFunction<E, F>,
        op7: OperatorFunction<F, G>,
        op8: OperatorFunction<G, H>
    ): Observable<H>;
    pipe<A, B, C, D, E, F, G, H, I>(
        op1: OperatorFunction<T, A>,
        op2: OperatorFunction<A, B>,
        op3: OperatorFunction<B, C>,
        op4: OperatorFunction<C, D>,
        op5: OperatorFunction<D, E>,
        op6: OperatorFunction<E, F>,
        op7: OperatorFunction<F, G>,
        op8: OperatorFunction<G, H>,
        op9: OperatorFunction<H, I>
    ): Observable<I>;
    pipe<A, B, C, D, E, F, G, H, I>(
        op1: OperatorFunction<T, A>,
        op2: OperatorFunction<A, B>,
        op3: OperatorFunction<B, C>,
        op4: OperatorFunction<C, D>,
        op5: OperatorFunction<D, E>,
        op6: OperatorFunction<E, F>,
        op7: OperatorFunction<F, G>,
        op8: OperatorFunction<G, H>,
        op9: OperatorFunction<H, I>,
        ...operations: OperatorFunction<any, any>[]
    ): Observable<unknown>;

    pipe(...operations: OperatorFunction<any, any>[]): Observable<any>;

    subscribe(observerOrNext?: Partial<Observer<T>> | ((value: T) => void)): Subscription;
    subscribe(observerOrNext: Partial<Observer<T>> | ((value: T) => void) | null, error?: ((error: any) => void) | null, complete?: (() => void) | null): Subscription;
    subscribe(next?: ((value: T) => void) | null, error?: ((error: any) => void) | null, complete?: (() => void) | null): Subscription;

    toPromise(promiseCtor: any): any;

    static create(...args: any[]): any;

}

export interface Unsubscribable {
    unsubscribe(): void;
}

export interface SubscriptionLike extends Unsubscribable {
    unsubscribe(): void;
    readonly closed: boolean;
}

export class Subject<T> extends Observable<T> implements SubscriptionLike {
    closed;

    constructor();

    asObservable(): any;

    complete(): void;

    error(err: any): void;

    lift(operator: any): any;

    next(value: any): void;

    unsubscribe(): void;

    static create(destination: any, source: any): any;

}

export class Subscriber<T> {
    constructor(destination?: Subscriber<any> | Observer<any>);

    complete(): void;

    error(err?: any): void;

    next(value?: T): void;

    unsubscribe(): void;

    static create<T>(next?: (x?: T) => void, error?: (e?: any) => void, complete?: () => void): Subscriber<T>;

}

export class Subscription {
    constructor(initialTeardown: any);

    add(teardown: any): void;

    remove(teardown: any): void;

    unsubscribe(): void;

}


export function ArgumentOutOfRangeError(): void;

export function EmptyError(): void;

export function NotFoundError(message: any): void;

export function ObjectUnsubscribedError(): void;

export function SequenceError(message: any): void;

export function TimeoutError(info: any): void;

export function UnsubscriptionError(errors: any): void;

export function first(predicate: any, defaultValue: any, ...args: any[]): any;

export interface EventListenerObject<E> {
    handleEvent(evt: E): void;
}

export interface HasEventTargetAddRemove<E> {
    addEventListener(
        type: string,
        listener: ((evt: E) => void) | EventListenerObject<E> | null,
        options?: boolean | AddEventListenerOptions
    ): void;
    removeEventListener(
        type: string,
        listener: ((evt: E) => void) | EventListenerObject<E> | null,
        options?: EventListenerOptions | boolean
    ): void;
}

export function interval(period: any, scheduler: any): any;

export function last(predicate: any, defaultValue: any, ...args: any[]): any;



export interface InteropObservable<T> {
    [Symbol.observable]: () => Subscribable<T>;
}

export type ObservableInput<T> =
    | Observable<T>
    | InteropObservable<T>
    | PromiseLike<T>
    | ArrayLike<T>
    | Iterable<T>;


export type ObservableInputTuple<T> = {
    [K in keyof T]: ObservableInput<T[K]>;
};

export namespace EMPTY {
    function lift(operator: any): any;
    function pipe(...args: any[]): any;
    function subscribe(observerOrNext: any, error: any, complete: any): any;
}

export namespace NEVER {
    function lift(operator: any): any;
    function pipe(...args: any[]): any;
    function subscribe(observerOrNext: any, error: any, complete: any): any;
}

export namespace Subscriber {
    namespace EMPTY {
        const closed: boolean;

        const initialTeardown: any;

        function add(teardown: any): void;

        function remove(teardown: any): void;

        function unsubscribe(): void;
    }
}

export namespace Subscription {
    namespace EMPTY {
        const closed: boolean;

        const initialTeardown: any;

        function add(teardown: any): void;

        function remove(teardown: any): void;

        function unsubscribe(): void;
    }
}

interface BehaviorSubjectConstructor {
    new (a: number): BehaviorSubject<number>;
}

export declare global {
    interface Window {
        rxjs: {
            BehaviorSubject: BehaviorSubjectConstructor,
            fromEvent: <T>(target: HasEventTargetAddRemove<T> | ArrayLike<HasEventTargetAddRemove<T>>, eventName: string) => Observable<T>,
            withLatestFrom: <T, O extends unknown[]>(...inputs: [...ObservableInputTuple<O>]) => OperatorFunction<T, [T, ...O]>,
            map: <T, R>(project: (value: T, index?: number) => R, thisArg?: any) => OperatorFunction<T, R>,
            merge: <A extends readonly unknown[]>(...sources: [...ObservableInputTuple<A>]) => Observable<A[number]>,
            mergeWith: <T, A extends readonly unknown[]>(
                ...otherSources: [...ObservableInputTuple<A>]
            ) => OperatorFunction<T, T | A[number]>
        };
    }

    var window: Window;
}