import random
from collections import deque
import matplotlib.pyplot as plt
import statistics

class SupplyNode():
    def __init__(self, name, inventory, incomingOrder, outgoingOrder, incomingShipment, outgoingShipment, inventoryCost, backlogCost, shiptime, ordertime, mode, target_inventory):
        self.name = name
        self.inventory = inventory
        self.backlog = 0
        self.incomingOrder = incomingOrder
        self.outgoingOrder = outgoingOrder
        self.incomingShipment = incomingShipment
        self.outgoingShipment = outgoingShipment
        self.inventoryCost = inventoryCost
        self.backlogCost = backlogCost
        self.cost = 0
        self.cumulative_cost = 0          # накопленные затраты
        self.shipque = deque()
        self.orderque = deque()
        for i in range(shiptime):
            self.shipque.append(incomingShipment)
        # Корректировка для завода (уменьшаем задержку заказа на 1, если ordertime >=2)
        if (name == "Завод" and ordertime >= 2):
            ordertime -= 1
        for i in range(ordertime):
            self.orderque.appendleft(incomingOrder)
        self.history = [
            {"week": 0,
             "incomingShipment": self.incomingShipment,
             "outgoingShipment": self.outgoingShipment,
             "backlog": self.backlog,
             "inventory": self.inventory,
             "outgoingOrder": self.outgoingOrder,
             "cost": self.cost}]
        self.mode = mode
        self.target_inventory = target_inventory

    def incomingShipmentUpdate(self):
        self.incomingShipment = self.shipque.popleft()
        self.inventory += self.incomingShipment

    def outgoingOrderUpdate(self):
        match self.mode:
            case "random":
                target = getattr(self, 'target_inventory', 40)
                self.outgoingOrder = target + random.randint(-20, 20)
            case "safe":
                target = getattr(self, 'target_inventory', 20)
                desired = self.incomingOrder + self.backlog * 0.5 + max(0, target - self.inventory)
                self.outgoingOrder = round(max(0, desired))
            case "medium":
                target = getattr(self, 'target_inventory', 20)
                desired = self.incomingOrder + self.backlog + max(0, target - self.inventory)
                self.outgoingOrder = round(max(0, desired))
            case "aggressive":
                target = getattr(self, 'target_inventory', 30)
                desired = (self.incomingOrder + self.backlog) * 1.5 + max(0, target - self.inventory)
                self.outgoingOrder = round(max(0, int(desired)))
            case _:
                self.outgoingOrder = self.incomingOrder + self.backlog
        self.orderque.appendleft(self.outgoingOrder)

    def update(self, incomingOrder):
        self.incomingOrder = incomingOrder
        needToShip = self.incomingOrder + self.backlog
        self.outgoingShipment = min(self.inventory, needToShip)
        self.backlog = needToShip - self.outgoingShipment
        self.inventory -= self.outgoingShipment
        self.cost = self.inventory * self.inventoryCost + self.backlog * self.backlogCost
        self.cumulative_cost += self.cost
        self.history.append({
            "week": len(self.history),
            "incomingShipment": self.incomingShipment,
            "outgoingShipment": self.outgoingShipment,
            "backlog": self.backlog,
            "inventory": self.inventory,
            "outgoingOrder": self.outgoingOrder,
            "cost": self.cost})
        return self.outgoingShipment

def plot_results(supplychain, timelimit):
    """Построение четырёх графиков: расходы, заказы, запасы, дефицит."""
    weeks = list(range(timelimit + 1))
    fig, axs = plt.subplots(2, 2, figsize=(12, 10))

    # 1. Расходы
    for node in supplychain:
        costs = [entry["cost"] for entry in node.history]
        axs[0, 0].plot(weeks, costs, label=node.name)
    axs[0, 0].set_title("Динамика расходов по узлам")
    axs[0, 0].set_xlabel("Неделя")
    axs[0, 0].set_ylabel("Расходы (у.е.)")
    axs[0, 0].legend()
    axs[0, 0].grid(True)

    # 2. Исходящие заказы
    for node in supplychain:
        orders = [entry["outgoingOrder"] for entry in node.history]
        axs[0, 1].plot(weeks, orders, label=node.name)
    axs[0, 1].set_title("Динамика исходящих заказов")
    axs[0, 1].set_xlabel("Неделя")
    axs[0, 1].set_ylabel("Объём заказа")
    axs[0, 1].legend()
    axs[0, 1].grid(True)

    # 3. Товары на складе (Inventory)
    for node in supplychain:
        inventory = [entry["inventory"] for entry in node.history]
        axs[1, 0].plot(weeks, inventory, label=node.name)
    axs[1, 0].set_title("Динамика запасов на складе")
    axs[1, 0].set_xlabel("Неделя")
    axs[1, 0].set_ylabel("Запас (ед.)")
    axs[1, 0].legend()
    axs[1, 0].grid(True)

    # 4. Дефицит (Backlog)
    for node in supplychain:
        backlog = [entry["backlog"] for entry in node.history]
        axs[1, 1].plot(weeks, backlog, label=node.name)
    axs[1, 1].set_title("Динамика дефицита")
    axs[1, 1].set_xlabel("Неделя")
    axs[1, 1].set_ylabel("Дефицит (ед.)")
    axs[1, 1].legend()
    axs[1, 1].grid(True)

    plt.tight_layout()
    plt.show()

def main():

    #Дискретно-событийное
    shiptime = 2
    ordertime = 2
    inventory = 12
    demand = 4
    clientmode = "hill"   # "fixed", "hill", "random"

    client_hillmode_max = 9
    client_hillmode_min = 5
    client_hillmode_timer = 22
    client_fixedmode_value = 9

    client_randmode_timer_flag = True

    #Агентное
    store_mode = "none"
    wholesaler_mode = "none"
    distributor_mode = "none"
    factroy_mode = "none"
    store_target = 10
    wholesaler_target = 10
    distributor_target = 10
    factory_target = 10

    incomingOrder = demand
    outgoingOrder = demand
    incomingShipment = demand
    outgoingShipment = demand

    inventoryCost = 1
    backlogCost = 2
    timelimit = 52
   

    store = SupplyNode("Магазин", inventory, incomingOrder, outgoingOrder,
                       incomingShipment, outgoingShipment, inventoryCost, backlogCost,
                       shiptime, ordertime, store_mode, store_target)
    wholesaler = SupplyNode("Оптовик", inventory, incomingOrder, outgoingOrder,
                            incomingShipment, outgoingShipment, inventoryCost, backlogCost,
                            shiptime, ordertime, wholesaler_mode, wholesaler_target)
    distributor = SupplyNode("Дистрибьютор", inventory, incomingOrder, outgoingOrder,
                             incomingShipment, outgoingShipment, inventoryCost, backlogCost,
                             shiptime, ordertime, distributor_mode, distributor_target)
    factory = SupplyNode("Завод", inventory, incomingOrder, outgoingOrder,
                         incomingShipment, outgoingShipment, inventoryCost, backlogCost,
                         shiptime, ordertime, factroy_mode, factory_target)
    clientinventory = 0

    supplychain = [store, wholesaler, distributor, factory]

    # Сохраняем историю спроса для расчёта BWE
    demand_history = []

    for t in range(timelimit):
        print(f"Неделя: {t}")
        demand_history.append(demand)   # запоминаем спрос этой недели до возможного изменения

        # Поступление поставок
        for node in supplychain:
            node.incomingShipmentUpdate()

        # Обновление звеньев (отгрузка, расчёт дефицита/запасов)
        clientinventory += store.update(incomingOrder=demand)
        store.shipque.append(wholesaler.update(incomingOrder=store.orderque.pop()))
        wholesaler.shipque.append(distributor.update(incomingOrder=wholesaler.orderque.pop()))
        distributor.shipque.append(factory.update(incomingOrder=distributor.orderque.pop()))
        factory.shipque.append(factory.orderque.pop())

        # Формирование новых заказов (отправка наверх)
        for node in supplychain:
            node.outgoingOrderUpdate()

        # Вывод отладочной информации (оставлено как в оригинале)
        for node in supplychain:
            print(f"""
            {node.name}: 
            Поставка: {node.incomingShipment},
            Входящий заказ: {node.incomingOrder}, 
            Отгрузка: {node.outgoingShipment}, 
            Дефицит: {node.backlog}, 
            Запас: {node.inventory}, 
            Заказ: {node.outgoingOrder}, 
            Траты: {node.cost}
            Текущая очередь заказов: {node.orderque}
            Текущая очередь материалов: {node.shipque}""")
        print("\n")

        # Генерация спроса на следующую неделю
        if clientmode == "fixed":
            demand = client_fixedmode_value
        elif clientmode == "hill":
            if (t > client_hillmode_timer  and t < 30):
                client_randmode_timer_flag = False
            else:
                client_randmode_timer_flag = True
            demand = client_hillmode_max if client_randmode_timer_flag else client_hillmode_min
        elif clientmode == "random":
            demand = random.randint(5, 9)

    # Построение графиков
    plot_results(supplychain, timelimit)

    # --- Вывод итоговых статистик ---
    print("\n" + "="*60)
    print("ИТОГОВЫЕ ПОКАЗАТЕЛИ ПО ЗВЕНЬЯМ")
    print("="*60)

    # Дисперсия спроса (нужна для BWE)
    demand_var = statistics.variance(demand_history) if len(demand_history) > 1 else 0.0
    print(f"\nДисперсия потребительского спроса: {demand_var:.2f}\n")

    for node in supplychain:
        # Извлекаем списки из истории
        inv_list = [entry["inventory"] for entry in node.history]
        back_list = [entry["backlog"] for entry in node.history]
        cost_list = [entry["cost"] for entry in node.history]
        order_list = [entry["outgoingOrder"] for entry in node.history]

        total_inventory = sum(inv_list)
        total_backlog = sum(back_list)
        total_cost = sum(cost_list)
        cumulative_cost = node.cumulative_cost  # совпадает с total_cost

        # BWE (bullwhip effect) = var(заказы) / var(спрос)
        if len(order_list) > 1 and demand_var != 0:
            order_var = statistics.variance(order_list)
            bwe = order_var / demand_var
        else:
            bwe = float('nan')

        print(f"--- {node.name} ---")
        print(f"  Суммарный запас (за все недели): {total_inventory:.1f}")
        print(f"  Суммарный дефицит (за все недели): {total_backlog:.1f}")
        print(f"  Суммарные расходы (за все недели): {total_cost:.1f}")
        print(f"  BWE: {bwe:.3f}")
        print()

if __name__ == "__main__":
    main()