package org.example;

import java.sql.SQLException;
import java.util.*;

public class Main {
    private static final Scanner sc = new Scanner(System.in);
    public static void Selector() {

        boolean exit = false;
        boolean checker;
        new SQLManager();
        while (!exit) {
            System.out.println("\n-------------------------------------\n");
            System.out.println("1. Вывести все таблицы PostgresSQL;");
            System.out.println("2. Создать таблицу PostgresSQL;");
            System.out.println("3. Экспортировать все данные из файла в Excel в PostgresSQL;");
            System.out.println("4. Экспортировать по столбцам из файла в Excel в PostgresSQL;");
            System.out.println("5. Реализовать вывод из PostgresSQL всех данных по коду гидрологического поста;");
            System.out.println("6. Реализовать вывод из PostgresSQL данных по коду гидропоста и дате;");
            System.out.println("7. Восстановить все пропущенные данные в PostgresSQL методом k-ближайших соседей;");
            System.out.println("0. Завершить работу.");
            System.out.print("Выберите действие: ");
            int choice;
            try {
                choice = sc.nextInt();
            }
            catch (Exception e) {
                System.out.println("Введено неверное значение! Попробуйте снова. " + e);
                sc.nextLine();
                continue;
            }
            sc.nextLine();
            System.out.println("\n-------------------------------------\n");

            String tablename;
            switch (choice) {
                case 1:
                    SQLManager.SQLQuerySelectTable();
                    break;
                case 2:
                    System.out.print("Введите название таблицы: ");
                    tablename = sc.nextLine();
                    SQLManager.SQLQueryCreate("CREATE TABLE IF NOT EXISTS "+ SQLManager.schemaname + "." + tablename +
                            "(ID serial, 'Object ID' int, 'Код поста' int, 'Код параметра' int, 'Дата-время' datetime, 'Уровень воды' int, 'Описание' text, 'Температура воздуха' int, 'Атмосферное давление' int, 'Скорость ветра' int, 'Толщина снежного покрова' int, 'Количество осадков' int)");
                    break;
                case 3:

                    break;
                case 4:
                    break;
                case 5:
                    break;
                case 6:
                    break;
                case 7:
                    break;
                case 0:
                    exit = true;
                    sc.close();
                    try {
                        SQLManager.conn.close();
                    } catch (SQLException e) {
                        throw new RuntimeException(e);
                    }
                    break;
                default:
                    System.out.println("Введено неверное значение! Попробуйте снова.");
                    break;

            }


        }

    }
    public static void main(String[] args) {

        Selector();
    }

}