package org.example;

import org.apache.poi.ss.usermodel.*;
import org.apache.poi.xssf.usermodel.XSSFWorkbook;

import java.awt.dnd.DragSource;
import java.io.*;
import java.sql.*;
import java.util.Scanner;

class SqlDatabase {
    private static Scanner sc = new Scanner(System.in);
    private static Connection conn;
    static {
        try {
            String pass = "postgres";
            String user = "postgres";
            String url = "jdbc:postgresql://localhost:5432/postgres";
            conn = DriverManager.getConnection(url, user, pass);
            Statement stmt = conn.createStatement();
            stmt.executeUpdate("CREATE SCHEMA IF NOT EXISTS Seminar1");
        } catch (SQLException e) {
            System.out.println("Не удалось подключиться к базе данных! " + e);
            System.exit(0);
        }
    }

    public static void Selector() {
        boolean exit = false;
        while (!exit) {
            System.out.println("\n-------------------------------------\n");
            System.out.println("1. Вывести все таблицы PostgresSQL");
            System.out.println("2. Создать таблицу PostgresSQL");
            System.out.println("3. Сложение");
            System.out.println("4. Вычитание");
            System.out.println("5. Умножение");
            System.out.println("6. Деление");
            System.out.println("7. Деление по модулю");
            System.out.println("8. Модуль числа");
            System.out.println("9. Возведение в степень");
            System.out.println("10. Экспорт данных из PostgresSQL в Excel");
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
            System.out.println("\n-------------------------------------\n");
            String[] split_answer;

            switch (choice) {
                case 3, 4, 5, 6, 7, 9:
                    while (true) {
                        System.out.print("Введите два числа через пробел: ");
                        String number = sc.nextLine();
                        split_answer = number.split(" ");
                        if (split_answer.length == 2 && number.matches("[0-9. -]+")) {
                            if ((choice == 6 || choice == 7) && Double.parseDouble(split_answer[1]) == 0f) {
                                System.out.println("На 0 делить нельзя!");
                                continue;
                            }
                            break;
                        } else {
                            System.out.println("Введен неверный формат!");
                        }
                    }
                    TwoNumbers(choice, split_answer);
                    break;
                case 1, 2, 10:
                    SqlDatabase.SQLMethod(choice);
                    break;
                case 8:
                    while (true) {
                        System.out.print("Введите одно число: ");
                        String number = sc.nextLine();
                        split_answer = number.split(" ");
                        if (split_answer.length == 1 && number.matches("[0-9. -]+"))
                            break;
                        else {
                            System.out.println("Введен неверный формат!");
                        }
                    }
                    OneNumber(split_answer);
                    break;
                case 0:
                    exit = true;
                    sc.close();
                    try {
                        conn.close();
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

    private static void TwoNumbers(int choice, String[] answer){
        double  a = Double.parseDouble(answer[0]);
        double b = Double.parseDouble(answer[1]);
        double result = 0;
        System.out.println("Текущие таблицы: ");
        Query("SELECT tablename FROM pg_tables\n" +
                "WHERE schemaname = 'seminar1'", "select");
        System.out.print("Выберите таблицу введя её имя: ");
        String table_choice = sc.nextLine();
        switch (choice) {
            case 3:
                result = a + b;
                Query("INSERT INTO seminar1." + table_choice +
                        " (Operation, Result) VALUES('" + a + "+" + b + "'," + result + ");", "create");
                break;
            case 4:
                result = a - b;
                Query("INSERT INTO semi-nar1." + table_choice +
                        " (Operation, Result) VALUES('" + a + "-" + b + "'," + result + ");", "create");
                break;
            case 5:
                result = a * b;
                Query("INSERT INTO seminar1." + table_choice +
                        " (Operation, Result) VALUES('" + a + "*" + b + "'," + result + ");", "create");
                break;
            case 6:
                result = a / b;
                Query("INSERT INTO seminar1." + table_choice +
                        " (Operation, Result) VALUES('" + a + "/" + b + "'," + result + ");", "create");
                break;
            case 7:
                result = a % b;
                Query("INSERT INTO seminar1." + table_choice +
                        " (Operation, Result) VALUES('" + a + "%" + b + "'," + result + ");", "create");
                break;
            case 9:
                result = Math.pow(a, b);
                if (Double.isInfinite(result))
                {
                    System.out.println("Результат вышел за рамки значений!");
                    break;
                }
                Query("INSERT INTO seminar1." + table_choice +
                        " (Operation, Result) VALUES('" + a + "^" + b + "'," + result + ");", "create");
                break;
        }
        System.out.println("Ответ: " + result);
    }

    private static void OneNumber(String[] answer){
        double a = Double.parseDouble(answer[0]);
        System.out.println("Текущие таблицы: ");
        Query("SELECT tablename FROM pg_tables\n" +
                "WHERE schemaname = 'seminar1'", "select");
        System.out.print("Выберите таблицу введя её имя: ");
        String table_choice = sc.nextLine();
        double result = Math.abs(a);
        Query("INSERT INTO seminar1." + table_choice +
                " (Operation, Result) VALUES('abs("+a+")',"+result+");", "create");
        System.out.println("Ответ: " + result);
    }

    private static void SQLMethod(int choice) {
        switch (choice) {
            case 1:
                System.out.println("Текущие таблицы: ");
                Query("SELECT tablename FROM pg_tables\n" +
                        "WHERE schemaname = 'seminar1'", "select");
                break;
            case 2:
                System.out.print("Введите название таблицы: ");
                String tablename = sc.nextLine();
                Query("CREATE TABLE IF NOT EXISTS seminar1." + tablename +
                        "(ID serial, Operation varchar(100), Result double precision)", "create");
                break;
            case 10:
                Query("SELECT tablename FROM pg_tables\n" +
                        "WHERE schemaname = 'seminar1'", "excel");
                break;
        }

    }

    private static void Query(String sql, String type) {
        try {
            Statement stmt = conn.createStatement();
            if (type.equals("select")) {
                ResultSet rs = stmt.executeQuery(sql);
                while (rs.next()) {
                    System.out.println(rs.getString(1));
                }
            } else if (type.equals("create")) {
                stmt.executeUpdate(sql);
            } else if (type.equals("excel")) {
                ResultSet rs = stmt.executeQuery(sql);
                Statement stmt2 = conn.createStatement();
                while (rs.next()) {
                    Workbook workbook = new XSSFWorkbook();
                    String table = rs.getString(1);
                    Sheet sheet = workbook.createSheet(table);
                    ResultSet rs2 = stmt2.executeQuery("SELECT * FROM seminar1." + table);
                    int rowindex = 0;
                    while (rs2.next()) {
                        Row row = sheet.createRow(rowindex);
                        if (rowindex == 0) {
                            row.createCell(0).setCellValue("Id");
                            row.createCell(1).setCellValue("Operation");
                            row.createCell(2).setCellValue("Result");
                            System.out.println("Id \t Operation \t Result");
                        }
                        else {
                            row.createCell(0).setCellValue(rs2.getInt(1));
                            row.createCell(1).setCellValue(rs2.getString(2));
                            row.createCell(2).setCellValue(rs2.getDouble(3));
                            System.out.print(rs2.getInt(1)+" \t ");
                            System.out.print(rs2.getString(2)+" \t ");
                            System.out.println(rs2.getDouble(3));
                        }

                        rowindex++;
                    }
                    if (sheet.getRow(0) != null) {
                        int columnCount = sheet.getRow(0).getPhysicalNumberOfCells();
                        for (int i = 0; i < columnCount; i++) {
                            sheet.autoSizeColumn(i);
                        }
                    }
                    workbook.write(new FileOutputStream(table + ".xlsx"));
                    System.out.println("Данные успешно экспортированы в Excel-файл "+table+".xlsx");
                    workbook.close();
                }


            }
        } catch (SQLException e){
            System.out.println("Выбранной таблицы не существует ошибка синтаксиса. " + e);
        } catch (IOException e) {
            System.out.println("Информацию не удалось экспортировать. " + e);
        }
    }
}

public class Main {
    public static void main(String[] args) {
        SqlDatabase.Selector();

    }
}