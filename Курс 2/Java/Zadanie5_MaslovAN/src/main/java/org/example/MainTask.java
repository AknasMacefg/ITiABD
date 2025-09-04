package org.example;

import java.util.Scanner;

public class MainTask {

    protected static String[] ReverseSentence(Scanner sc){
        StringBuffer s;
        while (true) {
            System.out.print("Введите предложение не менее 50 символов: ");
             s = new StringBuffer(sc.nextLine());
            if (s.length() >= 50){
                String temp_s = s.toString();
                System.out.println("Результат: " + s.reverse());
                return new String[]{temp_s, s.toString()};
            }
            System.out.println("Недостаточно длинное предложение. Попробуйте снова.");
        }


    }

    protected static String[] InsertSentence(Scanner sc){
        StringBuffer s1, s2;
        while (true) {
            System.out.print("Введите первое предложение не менее 50 символов: ");
            s1 = new StringBuffer(sc.nextLine());
            if (s1.length() >= 50){
                while (true){
                    System.out.print("Введите второе предложение не менее 50 символов: ");
                    s2 = new StringBuffer(sc.nextLine());
                    if (s2.length() >= 50){
                        break;
                    }
                    System.out.println("Недостаточно длинное предложение. Попробуйте снова.");
                }
                break;
            }
            System.out.println("Недостаточно длинное предложение.");
        }

        while (true){
            try {
                System.out.print("Введите позицию в первом предложении, куда нужно вставить второе предложение: ");
                int i = sc.nextInt();
                sc.nextLine();
                if (i >= 0 && i <= s1.length()){
                    String temp_s1 = s1.toString();
                    System.out.println("Результат: " + s1.insert(i, s2));
                    return new String[]{temp_s1, s2.toString(), String.valueOf(i), s1.toString()};
                }
                System.out.println("Введенный индекс выходит за рамки первого предложения.");
            } catch (Exception e) {
                System.out.println("Введенное значение не число. " + e);
                sc.nextLine();
            }

        }

    }
}
