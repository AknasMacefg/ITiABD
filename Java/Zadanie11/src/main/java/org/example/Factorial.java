package org.example;

public class Factorial {

    public static double FactorialCalculator(int number) {
        double result = number;
        int i = number;
        if (number == 0){
            System.out.println("Факториал числа "+number+" равняется: 1");
            return 1;
        }
        while (i >= 1){
            if (i-2 <= 0) break;
            else i -= 2;
            result *= i;

        }
        System.out.println("Факториал числа "+number+" равняется: "+result);
        return result;
    }
}
