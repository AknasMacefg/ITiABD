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
            System.out.println("1. Вывести все таблицы PostgresSQL");
            System.out.println("2. Создать таблицу PostgresSQL");
            System.out.println("3. Сохранить вводимый с клавиатуры список, а также строку и множество в PostgresSQL");
            System.out.println("4. Удалить элемент из списка, строки и множества в PostgresSQL по ID ");
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
                            "(ID serial, List text, String text, Set text)");
                    break;


                case 3:
                    checker = SQLManager.SQLQuerySelectTable();
                    if (!checker) continue;
                    Listik1 list = new Listik1();
                    System.out.print("Выберите таблицу для записи введя её имя: ");
                    String tableName = sc.nextLine();
                    String query = String.format(Locale.US,"INSERT INTO %s.%s (List, String, Set)" +
                                    "VALUES ('%s', '%s', '%s')",
                            SQLManager.schemaname,
                            tableName,
                            list.NumbersList.toString(),
                            list.NumbersString,
                            list.NumbersSet.toString()
                    );
                    SQLManager.SQLQueryCreate(query);
                    break;


                case 4:
                    checker = SQLManager.SQLQuerySelectTable();
                    if (!checker) continue;
                    System.out.print("Выберите таблицу для вывода введя её имя: ");
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
                    String[] row_result = SQLManager.SQLQuerySelect("SELECT * FROM "+ SQLManager.schemaname +"." + tablename +
                            " WHERE ID = " + id);
                    if (row_result == null || row_result.length == 0) break;
                    System.out.print("Введите элемент, который вы хотите удалить: ");
                    sc.nextLine();
                    String deleter = sc.nextLine();
                    ArrayList<String> row_temp;
                    System.out.println("Результат: ");
                    for (int i = 0; i < row_result.length; i++) {
                        if(i != 1){
                            row_temp = new ArrayList<>(Arrays.asList(row_result[i].substring(1, row_result[i].length() - 1).split(", ")));
                            row_temp.removeIf(tmp_text -> tmp_text.equals(deleter));
                            row_result[i] = row_temp.toString();
                        }
                        else {
                           row_result[i] = row_result[i].replace(deleter, "");
                        }

                        System.out.println(row_result[i]);
                    }
                    query = String.format(Locale.US,"UPDATE %s.%s SET List = '%s', String = '%s', Set = '%s'  WHERE ID = %d",
                            SQLManager.schemaname,
                            tablename,
                            row_result[0],
                            row_result[1],
                            row_result[2],
                            id
                    );
                    SQLManager.SQLQueryCreate(query);
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