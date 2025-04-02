package org.example;

import java.sql.SQLException;
import java.util.Scanner;

public class Main {
    private static final Scanner sc = new Scanner(System.in);
    public static void Selector() {

        boolean exit = false;
        boolean checker = false;
        while (!exit) {
            System.out.println("\n-------------------------------------\n");
            System.out.println("1. Вывести все таблицы PostgresSQL");
            System.out.println("2. Создать таблицу PostgresSQL");
            System.out.println("3. Решение базового варианта, сохранение результатов в MySQL");
            System.out.println("4. Вывод данных по ID строки. ");
            System.out.println("5. Экспорт данных из PostgresSQL в Excel");
            System.out.println("0. Выход из программы");
            System.out.print("Выберите действие: ");
            int choice = -1;
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
            int result;
            String tablename;
            switch (choice) {
                case 1:
                    checker = SQLManager.SQLQuerySelectTable();
                    break;
                case 2:
                    System.out.print("Введите название таблицы: ");
                    tablename = sc.nextLine();
                    SQLManager.SQLQueryCreate("CREATE TABLE IF NOT EXISTS "+ SQLManager.schemaname + "." + tablename +
                            "(ID serial, Triangle_sizes varchar(100), Perimeter Double, Square Double, Number Integer, Factorial Bigint, Odd_even varchar(20))");
                    break;
                case 3:
                    int number = sc.nextInt();
                    result = Factorial.FactorialCalculator(number);
                    System.out.println(result);
                    checker = SQLManager.SQLQuerySelectTable();
                    if (!checker) continue;
                    System.out.print("Выберите таблицу для записи введя её имя: ");
                    SQLManager.SQLQueryCreate("INSERT INTO "+ SQLManager.schemaname +"." + sc.nextLine() +
                            " (Triangle_sizes, Perimeter, Square, Number, Factorial, Odd_even) VALUES('Отзеркалить','"  + "','" + "');");
                    break;
                case 4:
                    checker = SQLManager.SQLQuerySelectTable();
                    if (!checker) continue;
                    System.out.print("Выберите таблицу для записи введя её имя: ");
                    tablename = sc.nextLine();
                    int id;
                    while (true){
                        try {
                            System.out.print("Выберите строку по ID: ");
                            id = sc.nextInt();
                            break;
                        }
                        catch (Exception e) {
                            System.out.println("Введено неверное значение! Попробуйте снова. " + e);
                            sc.nextLine();
                        }
                    }
                    SQLManager.SQLQuerySelect("SELECT * FROM "+ SQLManager.schemaname +"." + tablename +
                            " WHERE ID = " + id);
                    break;
                case 5:
                    SQLManager.ExcelWriter();
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