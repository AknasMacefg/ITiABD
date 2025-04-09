package org.example;

import java.sql.SQLException;
import java.util.Scanner;
import java.util.Locale;

public class Main {
    private static final Scanner sc = new Scanner(System.in);
    public static void Selector() {

        boolean exit = false;
        boolean checker;
        new SQLManager();
        while (!exit) {
            System.out.println("\n-------------------------------------\n");
            System.out.println("1. Вывести все таблицы PostgresSQL");
            System.out.println("2. Создать таблицу PostgresSQL");
            System.out.println("3. Решение базового варианта, сохранение результатов в MySQL");
            System.out.println("4. Вывод данных по ID строки. ");
            System.out.println("5. Экспорт данных из PostgresSQL в Excel");
            System.out.println("0. Выход из программы");
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
                            "(ID serial, Triangle_sizes varchar(100), Perimeter Real, Square Real, Number Integer, Factorial Float, Odd_even varchar(20))");
                    break;


                case 3:
                    TriangleMenu triangle = new TriangleMenu();
                    double[] triresult = triangle.processTriangle();
                    int number;
                    while (true) {
                        System.out.print("Введите число для нахождения факториала: ");
                        try {
                            number = sc.nextInt();
                            break;
                        } catch (Exception e) {
                            System.out.println("Неверный формат числа. Попробуйте снова.");
                        }
                    }
                    sc.nextLine();

                    double result = Factorial.FactorialCalculator(number);
                    String odd_even = (number % 2 == 0) ? "Четное" : "Нечетное";
                    System.out.println("Четность числа: " + odd_even);

                    checker = SQLManager.SQLQuerySelectTable();
                    if (!checker) continue;

                    System.out.print("Выберите таблицу для записи введя её имя: ");
                    String tableName = sc.nextLine();

                    String query = String.format(Locale.US,"INSERT INTO %s.%s (Triangle_sizes, Perimeter, Square, Number, Factorial, Odd_even) " +
                                    "VALUES ('a:%.2f b:%.2f c:%.2f', %.2f, %.2f, %d, %.0f, '%s')",
                            SQLManager.schemaname,
                            tableName,
                            triresult[0], // A
                            triresult[1], // B
                            triresult[2], // C
                            triresult[3], // perimeter
                            triresult[4], // area
                            number,
                            result,
                            odd_even
                    );

                    SQLManager.SQLQueryCreate(query);
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