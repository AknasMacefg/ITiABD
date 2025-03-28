package org.example;
import org.apache.poi.ss.usermodel.*;
import org.apache.poi.xssf.usermodel.XSSFWorkbook;
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
            double a;
            double b;

            switch (choice) {
                case 3, 4, 5, 6, 7, 9:
                    while (true) {
                        System.out.print("Введите два числа через пробел: ");
                        String number = sc.nextLine();
                        split_answer = number.split(" ");

                        if (split_answer.length == 2) {
                            try {
                                a = Double.parseDouble(split_answer[0]);
                                b = Double.parseDouble(split_answer[1]);
                            } catch (Exception e){
                                System.out.println("Введен неверный формат! " + e);
                                continue;
                            }

                            if ((choice == 6 || choice == 7) && Double.parseDouble(split_answer[1]) == 0) {
                                System.out.println("На 0 делить нельзя!");
                                continue;
                            }
                            break;
                        } else {
                            System.out.println("Введен неверный формат!");
                        }
                    }
                    TwoNumbers(choice, a, b);
                    break;
                case 1, 2, 10:
                    SqlDatabase.SQLMethod(choice);
                    break;
                case 8:
                    while (true) {
                        System.out.print("Введите одно число: ");
                        String number = sc.nextLine();
                        split_answer = number.split(" ");

                        if (split_answer.length == 1) {
                            try {
                                a = Double.parseDouble(split_answer[0]);
                            } catch (Exception e) {
                                System.out.println("Введен неверный формат! " + e);
                                continue;
                            }
                            break;
                        }
                        else {
                            System.out.println("Введен неверный формат!");
                        }
                    }
                    OneNumber(a);
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

    private static void TwoNumbers(int choice, Double a, Double b) {
        double result = 0;
        String operation = "";
        System.out.println("Текущие таблицы: ");
        Query("SELECT tablename FROM pg_tables\n" +
                "WHERE schemaname = 'seminar1'", "select");
        System.out.print("Выберите таблицу введя её имя: ");
        String table_choice = sc.nextLine();
        switch (choice) {
            case 3:
                result = a + b;
                operation = "+";
                break;
            case 4:
                result = a - b;
                operation = "-";
                break;
            case 5:
                result = a * b;
                operation = "*";
               break;
            case 6:
                result = a / b;
                operation = "/";
               break;
            case 7:
                result = a % b;
                operation = "%";
                break;
            case 9:
                result = Math.pow(a, b);
                operation = "^";
                break;
        }
        if (Double.isInfinite(result))
        {
            System.out.println("Результат вышел за рамки значений! Невозможно занести значение в базу данных!");
        } else {
            Query("INSERT INTO seminar1." + table_choice +
                    " (Operation, Result) VALUES('" + a + operation + b + "'," + result + ");", "create");
        }
        System.out.println("Ответ: " + result);
    }

    private static void OneNumber(double a){
        System.out.println("Текущие таблицы: ");
        Query("SELECT tablename FROM pg_tables\n" +
                "WHERE schemaname = 'seminar1'", "select");
        System.out.print("Выберите таблицу введя её имя: ");
        String table_choice = sc.nextLine();
        double result = Math.abs(a);
        if (Double.isInfinite(result))
        {
            System.out.println("Результат вышел за рамки значений! Невозможно занести значение в базу данных!");
        } else {
            Query("INSERT INTO seminar1." + table_choice +
                    " (Operation, Result) VALUES('abs(" + a + ")'," + result + ");", "create");
        }
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
                    ResultSetMetaData rsmd = rs2.getMetaData();
                    int rowindex = 0;
                    while (rs2.next()) {
                        Row row = sheet.createRow(rowindex);
                        for (int x = 1; x <= rsmd.getColumnCount(); x++)
                        {
                            if (rowindex == 0) {
                                row.createCell(x-1).setCellValue(rsmd.getColumnName(x));
                                System.out.printf("%-22s", rsmd.getColumnName(x));
                                if (x == rsmd.getColumnCount())
                                {
                                    rowindex++;
                                    x=1;
                                    System.out.println();
                                    row = sheet.createRow(rowindex);
                                } else continue;
                            }
                            if (rsmd.getColumnClassName(x).equals("java.lang.Integer") || rsmd.getColumnClassName(x).equals("java.lang.Short")) {
                                row.createCell(x-1).setCellValue(rs2.getInt(x));
                                System.out.printf("%-22d", rs2.getInt(x));
                            } else if (rsmd.getColumnClassName(x).equals("java.lang.String")) {
                                row.createCell(x-1).setCellValue(rs2.getString(x));
                                System.out.printf("%-22s", rs2.getString(x));
                            } else if (rsmd.getColumnClassName(x).equals("java.lang.Double") || rsmd.getColumnClassName(x).equals("java.lang.Float")) {
                                row.createCell(x-1).setCellValue(rs2.getDouble(x));
                                System.out.printf("%-22f", rs2.getDouble(x));
                            }
                        }
                        System.out.println();
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
    public static void main(String[] args){
        SqlDatabase.Selector();
    }
}