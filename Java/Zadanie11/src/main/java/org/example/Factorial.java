package org.example;
import java.util.Scanner;

public class Factorial {
    static int number;
    public Factorial() {
        Scanner sc = new Scanner(System.in);
        while (true) {
            System.out.print("Введите число для нахождения факториала: ");
            try {
                number = sc.nextInt();
                if (number < 0) {
                    System.out.println("Неверный формат числа. Попробуйте снова.");
                    continue;
                }
                break;
            } catch (Exception e) {
                System.out.println("Неверный формат числа. Попробуйте снова.");
                sc.nextLine();
            }
        }
    }
    public static double[] FactorialCalculator() {
        double result = number;
        int i = number;
        if (number == 0){
            System.out.println("Факториал числа "+number+" равняется: 1");
            return new double[]{number, 1};
        }
        while (i >= 1){
            if (i-2 <= 0) break;
            else i -= 2;
            result *= i;

        }
        System.out.println("Факториал числа "+number+" равняется: "+result);
        return new double[]{number, result};
    }

    public static String FactorialOddEven() {
        String odd_even = (number % 2 == 0) ? "Четное" : "Нечетное";
        System.out.println("Четность числа: " + odd_even);
        return odd_even;
    }
}
