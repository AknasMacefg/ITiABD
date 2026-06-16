import random
import statistics
import matplotlib.pyplot as plt

# ============================================================
#   Системно-динамическая модель «Пивной игры»
#   Задержки реализованы через явные «конвейеры» (pipeline).
#   Узлы: Магазин, Оптовик, Дистрибьютор, Завод.
# ============================================================

def shift_pipeline(pipeline, new_value):
    """
    Сдвиг конвейера на одну позицию влево:
    - элемент [0] покидает конвейер (возвращается),
    - все элементы сдвигаются,
    - в конец помещается new_value.
    """
    out = pipeline[0]
    for i in range(len(pipeline) - 1):
        pipeline[i] = pipeline[i + 1]
    pipeline[-1] = new_value
    return out


class Node:
    """Одно звено цепи поставок (кроме Завода – см. ниже)."""

    def __init__(self, name, init_inventory, target, inv_cost, back_cost,
                 shiptime, ordertime, mode):
        self.name = name
        self.inventory = init_inventory
        self.backlog = 0
        self.target = target
        self.inv_cost = inv_cost
        self.back_cost = back_cost
        self.mode = mode

        # Конвейер входящих поставок (товары в пути от поставщика)
        self.supply_line = [0] * shiptime
        # Конвейер исходящих заказов (заказы, отправленные вверх по цепи)
        self.order_line = [0] * ordertime

        # История для графиков и статистики
        self.history = []

    def receive_shipment(self):
        """Получить поставку, прибывшую на этой неделе. Возвращает её объём."""
        incoming = shift_pipeline(self.supply_line, 0)
        self.inventory += incoming
        return incoming

    def process_order(self, incoming_order, incoming_shipment):
        """
        Выполнить заказ от покупателя:
        - отгрузить максимально возможное,
        - обновить дефицит и запасы,
        - вычислить затраты,
        - записать состояние в историю.
        Возвращает фактическую отгрузку.
        """
        needed = incoming_order + self.backlog
        ship = min(self.inventory, needed)
        self.backlog = needed - ship
        self.inventory -= ship
        cost = self.inventory * self.inv_cost + self.backlog * self.back_cost

        # Исходящий заказ, помещённый на предыдущей неделе (пока ещё в очереди)
        outgoing_order = self.order_line[-1]

        self.history.append({
            'inventory': self.inventory,
            'backlog': self.backlog,
            'incoming_shipment': incoming_shipment,
            'outgoing_shipment': ship,
            'outgoing_order': outgoing_order,
            'cost': cost
        })
        return ship

    def decide_order(self, incoming_order):
        """Принять решение об исходящем заказе (вверх по цепи)."""
        if self.mode == 'random':
            return self.target + random.randint(-20, 20)
        elif self.mode == 'safe':
            desired = incoming_order + self.backlog * 0.5 + max(0, self.target - self.inventory)
        elif self.mode == 'medium':
            desired = incoming_order + self.backlog + max(0, self.target - self.inventory)
        elif self.mode == 'aggressive':
            desired = (incoming_order + self.backlog) * 1.5 + max(0, self.target - self.inventory)
        else:  # basic
            desired = incoming_order + self.backlog
        return max(0, round(desired))


def plot_results(nodes, weeks):
    """Построение четырёх графиков: расходы, заказы, запасы, дефицит."""
    fig, axs = plt.subplots(2, 2, figsize=(12, 10))
    x = list(range(weeks))

    # 1. Расходы
    for node in nodes:
        costs = [entry['cost'] for entry in node.history]
        axs[0, 0].plot(x, costs, label=node.name)
    axs[0, 0].set_title("Динамика расходов по узлам")
    axs[0, 0].set_xlabel("Неделя")
    axs[0, 0].set_ylabel("Расходы")
    axs[0, 0].legend()
    axs[0, 0].grid(True)

    # 2. Исходящие заказы
    for node in nodes:
        orders = [entry['outgoing_order'] for entry in node.history]
        axs[0, 1].plot(x, orders, label=node.name)
    axs[0, 1].set_title("Динамика исходящих заказов")
    axs[0, 1].set_xlabel("Неделя")
    axs[0, 1].set_ylabel("Объём заказа")
    axs[0, 1].legend()
    axs[0, 1].grid(True)

    # 3. Запасы на складе
    for node in nodes:
        inv = [entry['inventory'] for entry in node.history]
        axs[1, 0].plot(x, inv, label=node.name)
    axs[1, 0].set_title("Динамика запасов на складе")
    axs[1, 0].set_xlabel("Неделя")
    axs[1, 0].set_ylabel("Запас (ед.)")
    axs[1, 0].legend()
    axs[1, 0].grid(True)

    # 4. Дефицит
    for node in nodes:
        back = [entry['backlog'] for entry in node.history]
        axs[1, 1].plot(x, back, label=node.name)
    axs[1, 1].set_title("Динамика дефицита")
    axs[1, 1].set_xlabel("Неделя")
    axs[1, 1].set_ylabel("Дефицит (ед.)")
    axs[1, 1].legend()
    axs[1, 1].grid(True)

    plt.tight_layout()
    plt.show()


def main():
    # --------------------------------------------------------
    # Параметры моделирования
    # --------------------------------------------------------
    shiptime = 4         # недель доставки товара
    ordertime = 4        # недель доставки заказа (для всех, кроме завода)

    # У завода задержка принятия решения о производстве на 1 неделю меньше
    factory_ordertime = max(1, ordertime - 1) if ordertime >= 2 else ordertime

    # Режимы работы звеньев
    store_mode = "safe"
    wholesaler_mode = "safe"
    distributor_mode = "safe"
    factory_mode = "safe"

    # Целевые запасы
    store_target = 10
    wholesaler_target = 10
    distributor_target = 10
    factory_target = 10

    # Начальные условия
    init_inventory = 12
    init_demand = 4
    inv_cost = 1
    back_cost = 2
    total_weeks = 52

    # Режим конечного потребителя
    client_mode = "hill"         # "fixed", "hill", "random"
    client_fixed_value = 9
    client_hill_max = 9
    client_hill_min = 5
    client_hill_timer = 22        # после этой недели переключаем в максимум
    client_rand_timer_flag = True

    # --------------------------------------------------------
    # Инициализация узлов
    # --------------------------------------------------------
    store = Node("Магазин", init_inventory, store_target, inv_cost, back_cost,
                 shiptime, ordertime, store_mode)
    wholesaler = Node("Оптовик", init_inventory, wholesaler_target, inv_cost, back_cost,
                      shiptime, ordertime, wholesaler_mode)
    distributor = Node("Дистрибьютор", init_inventory, distributor_target, inv_cost, back_cost,
                       shiptime, ordertime, distributor_mode)
    factory = Node("Завод", init_inventory, factory_target, inv_cost, back_cost,
                   shiptime, factory_ordertime, factory_mode)

    # У завода есть дополнительный конвейер производства (shiptime)
    factory_production_line = [0] * shiptime

    # Заполняем начальные значения конвейеров, чтобы избежать переходных процессов
    for node in (store, wholesaler, distributor, factory):
        for i in range(len(node.supply_line)):
            node.supply_line[i] = init_demand
        for i in range(len(node.order_line)):
            node.order_line[i] = init_demand
    for i in range(shiptime):
        factory_production_line[i] = init_demand

    # Спрос и прочие переменные
    demand = init_demand
    client_inventory = 0
    demand_history = []

    # --------------------------------------------------------
    # Главный цикл (недели)
    # --------------------------------------------------------
    for week in range(total_weeks):
        demand_history.append(demand)

        # --- 1. Получение поставок (прибытие товаров) ---
        store_incoming = store.receive_shipment()
        wholesaler_incoming = wholesaler.receive_shipment()
        distributor_incoming = distributor.receive_shipment()

        # Завод получает продукцию из своего производственного конвейера
        factory_incoming = shift_pipeline(factory_production_line, 0)
        factory.inventory += factory_incoming

        # --- 2. Обработка заказов (снизу вверх) ---
        # Магазин
        store_ship = store.process_order(demand, store_incoming)
        client_inventory += store_ship

        # Оптовик получает заказ из очереди магазина
        order_to_wholesaler = shift_pipeline(store.order_line, 0)
        whole_ship = wholesaler.process_order(order_to_wholesaler, wholesaler_incoming)

        # Дистрибьютор получает заказ из очереди оптовика
        order_to_distributor = shift_pipeline(wholesaler.order_line, 0)
        distr_ship = distributor.process_order(order_to_distributor, distributor_incoming)

        # Завод получает заказ из очереди дистрибьютора
        order_to_factory = shift_pipeline(distributor.order_line, 0)
        factory_ship = factory.process_order(order_to_factory, factory_incoming)

        # --- 3. Отправка отгруженных товаров в конвейеры поставок ---
        store.supply_line[-1] += whole_ship
        wholesaler.supply_line[-1] += distr_ship
        distributor.supply_line[-1] += factory_ship

        # --- 4. Завод: перенос созревшего производственного заказа в производственный конвейер ---
        production_order = shift_pipeline(factory.order_line, 0)
        factory_production_line[-1] += production_order

        # --- 5. Принятие решений о новых заказах (отправка вверх) ---
        store_order = store.decide_order(demand)
        whole_order = wholesaler.decide_order(order_to_wholesaler)
        distr_order = distributor.decide_order(order_to_distributor)
        fact_order = factory.decide_order(order_to_factory)

        store.order_line[-1] = store_order
        wholesaler.order_line[-1] = whole_order
        distributor.order_line[-1] = distr_order
        factory.order_line[-1] = fact_order

        # --- 6. Генерация спроса на следующую неделю ---
        if client_mode == "fixed":
            demand = client_fixed_value
        elif client_mode == "hill":
            if week > client_hill_timer and week < 30:
                client_rand_timer_flag = False
            else:
                client_rand_timer_flag = True
            demand = client_hill_max if client_rand_timer_flag else client_hill_min
        elif client_mode == "random":
            demand = random.randint(5, 9)

    # --------------------------------------------------------
    # Визуализация
    # --------------------------------------------------------
    plot_results([store, wholesaler, distributor, factory], total_weeks)

    # --------------------------------------------------------
    # Итоговая статистика
    # --------------------------------------------------------
    print("\n" + "=" * 60)
    print("ИТОГОВЫЕ ПОКАЗАТЕЛИ ПО ЗВЕНЬЯМ")
    print("=" * 60)

    demand_var = statistics.variance(demand_history) if len(demand_history) > 1 else 0.0
    print(f"\nДисперсия потребительского спроса: {demand_var:.2f}\n")

    for node in (store, wholesaler, distributor, factory):
        inv_sum = sum(e['inventory'] for e in node.history)
        back_sum = sum(e['backlog'] for e in node.history)
        cost_sum = sum(e['cost'] for e in node.history)
        orders = [e['outgoing_order'] for e in node.history]

        order_var = statistics.variance(orders) if len(orders) > 1 else 0.0
        bwe = order_var / demand_var if demand_var != 0 else float('nan')

        print(f"--- {node.name} ---")
        print(f"  Суммарный запас (за все недели): {inv_sum:.1f}")
        print(f"  Суммарный дефицит (за все недели): {back_sum:.1f}")
        print(f"  Суммарные расходы (за все недели): {cost_sum:.1f}")
        print(f"  BWE: {bwe:.3f}")
        print()


if __name__ == "__main__":
    main()