import com.sun.jdi.connect.Connector;

import java.sql.*;
import java.util.Scanner;

/*class MathBody {

    private static Object Parser(String a) {
        try{
            return Byte.parseByte(a);
        }
        catch(Exception e){
            try {
                return Integer.parseInt(a);
            }
            catch(Exception e1){
                try {
                    return Double.parseDouble(a);
                }
                catch(Exception e2){
                    return null;
                }
            }

        }

    }

    private static void TwoNumbers(int choice, String number) {

        float a = Float.parseFloat(number.split(" ")[0]);
        float b = Float.parseFloat(number.split(" ")[1]);

        if (choice == 3) {
            System.out.println(a + b);
        }
        else if (choice == 4) {
            System.out.println(a - b);
        }
        else if (choice == 5) {
            System.out.println(a * b);
        }
        else if (choice == 6) {
            System.out.println(a / b);
        }
        else if (choice == 7) {
            System.out.println(a % b);
        }
        else if (choice == 9) {
            System.out.println(Math.pow(a, b));
        }

    }
    private static void OneNumber(String number) {
        int a = Integer.parseInt(number);
        System.out.println(Math.abs(a));
    }
    private static void SQLManagement(int choice) {
        System.out.println();
        if (choice == 1){
            try (Connection conn = DriverManager.getConnection("jdbc:postgresql://localhost:5432/postgres", "postgres", "postgres")) {
                Statement stmt = conn.createStatement();
                stmt.executeUpdate("CREATE SCHEMA IF NOT EXISTS Seminar1");
            } catch (SQLException e) {
                throw new RuntimeException(e);
            }
        }
        else if (choice == 2){

        }
        else if (choice == 10){

        }
    }

    public static void InfoOut(){
        Scanner sc = new Scanner(System.in);
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
        System.out.print("Выберите действие: ");
        int choice = sc.nextInt();
        sc.nextLine();
        switch (choice){
            case 3,4,5,6,7,9:
                System.out.print("Введите два числа через пробел: ");
                String number = sc.nextLine();
                TwoNumbers(choice, number);
                break;
            case 1, 2, 10:
                SQLManagement(choice);
                break;
            case 8:
                System.out.print("Введите одно число: ");
                OneNumber(sc.next());
                break;
            default:
                System.out.println("Введено неверное значение! Попробуйте снова.");
                InfoOut();
                break;


        }

    }
}
*/

class SqlDatabase {
    static Scanner sc = new Scanner(System.in);
    private static Connection conn;
    private static String url = "jdbc:postgresql://localhost:5432/postgres";
    private static String user = "postgres";
    private static String pass = "postgres";
    static {
        try {
            conn = DriverManager.getConnection(url, user, pass);
            Statement stmt = conn.createStatement();
            stmt.executeUpdate("CREATE SCHEMA IF NOT EXISTS Seminar1");
        } catch (SQLException e) {
            throw new RuntimeException(e);
        }
    }

    public static void Selector() {

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

        while (true) {
            int choice = sc.nextInt();
            sc.nextLine();
            switch (choice) {
                case 3, 4, 5, 6, 7, 9:
                    System.out.print("Введите два числа через пробел: ");
                    String number = sc.nextLine();
                    break;
                case 1, 2, 10:
                    break;
                case 8:
                    System.out.print("Введите одно число: ");
                    break;
                case 0:
                    System.exit(0);
                default:
                    System.out.println("Введено неверное значение! Попробуйте снова.");
                    break;
            }
        }

    }
}

public class Main {
    public static void main(String[] args) {
        SqlDatabase.Selector();
    }
}