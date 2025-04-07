package org.example;

public class Factorial {

    public static int FactorialCalculator(int number) {
        int result = number;
        int i = number;
        if (number == 0) return 1;
        while (i >= 1){
            if (i-2 <= 0) break;
            else i -= 2;
            result *= i;

        }
        System.out.println("Факториал числа "+number+" равняется: "+result);
        return result;
    }
}
