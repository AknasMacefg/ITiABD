import com.opencsv.CSVWriter;
import java.io.FileWriter;
import java.io.IOException;
import java.sql.*;
import java.util.Scanner;

class SqlDatabase {
    static Scanner sc = new Scanner(System.in);
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
            throw new RuntimeException(e);
        }
    }

    public static void Selector() {
        while (true) {
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

            int choice = sc.nextInt();
            sc.nextLine();
            System.out.println("\n-------------------------------------\n");
            String[] split_answer;
            switch (choice) {
                case 3, 4, 5, 6, 7, 9:
                    while (true) {
                        System.out.print("Введите два числа через пробел: ");
                        String number = sc.nextLine();
                        split_answer = number.split(" ");
                        if (split_answer.length == 2) {
                            if ((choice == 6 || choice == 7) && Float.parseFloat(split_answer[1]) == 0f) {
                                System.out.println("На 0 делить нельзя!");
                                continue;
                            }
                            break;
                        }
                        else {
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
                        if (split_answer.length == 1) {
                            break;
                        }
                        else {
                            System.out.println("Введен неверный формат!");
                        }
                    }
                    OneNumber(split_answer);
                    break;
                case 0:
                    System.exit(0);
                    break;
                default:
                    System.out.println("Введено неверное значение! Попробуйте снова.");
                    break;
            }
        }

    }

   private static void TwoNumbers(int choice, String[] answer){
        float a = Float.parseFloat(answer[0]);
        float b = Float.parseFloat(answer[1]);
        float result = 0f;
       System.out.println("Текущие таблицы: ");
       Query("SELECT tablename FROM pg_tables\n" +
               "WHERE schemaname = 'seminar1'", "select");
        System.out.print("Выберите таблицу введя её имя: ");
        String table_choice = sc.nextLine();
        switch (choice){
            case 3:
                result = a + b;
                Query("INSERT INTO seminar1." + table_choice +
                        " (Operation, Result) VALUES('"+a+"+"+b+"',"+result+");", "insert");
                break;
            case 4:
                result = a - b;
                Query("INSERT INTO seminar1." + table_choice +
                        " (Operation, Result) VALUES('"+a+"-"+b+"',"+result+");", "insert");
                break;
            case 5:
                result = a * b;
                Query("INSERT INTO seminar1." + table_choice +
                        " (Operation, Result) VALUES('"+a+"*"+b+"',"+result+");", "insert");
                break;
            case 6:
                result = a / b;
                Query("INSERT INTO seminar1." + table_choice +
                        " (Operation, Result) VALUES('"+a+"/"+b+"',"+result+");", "insert");
                break;
            case 7:
                result = a % b;
                Query("INSERT INTO seminar1." + table_choice +
                        " (Operation, Result) VALUES('"+a+"%"+b+"',"+result+");", "insert");
                break;
            case 9:
                result = (float) Math.pow(a, b);
                Query("INSERT INTO seminar1." + table_choice +
                        " (Operation, Result) VALUES('"+a+"^"+b+"',"+result+");", "insert");
                break;

        }
       System.out.println("Ответ: " + result);
   }

   private static void OneNumber(String[] answer){
        float a = Float.parseFloat(answer[0]);
       System.out.println("Текущие таблицы: ");
       Query("SELECT tablename FROM pg_tables\n" +
               "WHERE schemaname = 'seminar1'", "select");
       System.out.print("Выберите таблицу введя её имя: ");
       String table_choice = sc.nextLine();
       float result = Math.abs(a);
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
                        "(ID serial, Operation varchar(100), Result float)", "create");
                break;

            case 10:
                Query("SELECT tablename FROM pg_tables\n" +
                        "WHERE schemaname = 'seminar1'", "CSV");
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
            }
            else if (type.equals("create")) {
                stmt.executeUpdate(sql);
            }
            else if (type.equals("CSV")) {
                ResultSet rs = stmt.executeQuery(sql);
                Statement stmt2 = conn.createStatement();
                while (rs.next()) {
                    String table = rs.getString(1);
                    CSVWriter writer = new CSVWriter(new FileWriter(table + ".csv"));
                    ResultSet rs2 = stmt2.executeQuery("SELECT * FROM seminar1." + table);
                    writer.writeAll(rs2, true);
                    writer.close();
                }
                System.out.println("Информация успешно экспортирована.");
            }
        } catch (SQLException | IOException e) {
            throw new RuntimeException(e);
        }
    }
}

public class Main {
    public static void main(String[] args) {
        SqlDatabase.Selector();
    }
}