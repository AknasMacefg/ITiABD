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
            System.out.println("3. Изменить порядок символов строки на обратный");
            System.out.println("4. Добавить одну строку в другую");
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
            String[] result;
            switch (choice) {
                case 1:
                    SQLManager.SQLQueries("", "select");
                    break;
                case 2:
                    System.out.print("Введите название таблицы: ");
                    String tablename = sc.nextLine();
                    SQLManager.SQLQueries("CREATE TABLE IF NOT EXISTS "+ SQLManager.schemaname + "." + tablename +
                            "(ID serial, Operation varchar(100), First_sentence text, Second_sentence text, Result text)", "create");
                    break;
                case 3:
                    result = MainTask.ReverseSentence(sc);
                    checker = SQLManager.SQLQueries("", "select");
                    if (!checker) continue;
                    System.out.print("Выберите таблицу для записи введя её имя: ");
                    SQLManager.SQLQueries("INSERT INTO "+ SQLManager.schemaname +"." + sc.nextLine() +
                            " (Operation, First_sentence, Result) VALUES('Отзеркалить','" + result[0] + "','" + result[1] + "');", "create");
                    break;
                case 4:
                    result = MainTask.InsertSentence(sc);
                    SQLManager.SQLQueries("", "select");
                    if (!checker) continue;
                    System.out.print("Выберите таблицу для записи введя её имя: ");
                    SQLManager.SQLQueries("INSERT INTO "+ SQLManager.schemaname +"." + sc.nextLine() +
                            " (Operation, First_sentence, Second_sentence, Result) VALUES('Вставить в " + result[2]+" позицию','" + result[0] + "','" + result[1] + "','" + result[3] + "');", "create");
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