package org.example;

public class Factorial {

    public static int FactorialCalculator(int number) {
        int result = number;
        int i = number;
        if (number == 0) return 1;
        while (i >= 1){
            System.out.println(i);
            if (i-2 <= 0) break;
            else i -= 2;
            result *= i;

        }
        return result;
    }
}
