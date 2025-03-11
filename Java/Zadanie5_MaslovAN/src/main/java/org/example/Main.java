package org.example;

import java.sql.SQLException;
import java.util.Scanner;

public class Main {
    private static Scanner sc = new Scanner(System.in);
    public static void Selector() {
        boolean exit = false;
        SQLManager sql = new SQLManager();

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
                System.out.println("Введено неверное значение! Попробуйте снова." + e);
            }
            sc.nextLine();
            String[] result;
            switch (choice) {
                case 1:
                    sql.SQLQueries("", "select");
                    break;
                case 2:
                    System.out.print("Введите название таблицы: ");
                    String tablename = sc.nextLine();
                    sql.SQLQueries("CREATE TABLE IF NOT EXISTS "+sql.schemaname + "." + tablename +
                            "(ID serial, Operation varchar(20), First_sentence text, Second_sentence text, Result text)", "create");
                    break;
                case 3:
                    result = MainTask.ReverseSentence(sc);
                    sql.SQLQueries("", "select");
                    System.out.print("Выберите таблицу для записи введя её имя: ");
                    sql.SQLQueries("INSERT INTO "+sql.schemaname+"." + sc.nextLine() +
                            " (Operation, First_sentence, Result) VALUES('Reverse','" + result[0] + "','" + result[1] + "');", "create");
                    break;
                case 4:
                    result = MainTask.InsertSentence(sc);
                    sql.SQLQueries("", "select");
                    System.out.print("Выберите таблицу для записи введя её имя: ");
                    sql.SQLQueries("INSERT INTO "+sql.schemaname+"." + sc.nextLine() +
                            " (Operation, First_sentence, Second_sentence, Result) VALUES('Insert to " + result[2]+" pos','" + result[0] + "','" + result[1] + "','" + result[3] + "');", "create");
                    break;
                case 5:
                    sql.ExcelWriter();
                    break;
                case 0:
                    exit = true;
                    sc.close();
                    try {
                        sql.conn.close();
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