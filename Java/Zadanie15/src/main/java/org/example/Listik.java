package org.example;
import java.util.ArrayList;
import java.util.Scanner;

public class Listik {
    ArrayList<String> NumbersList = new ArrayList<>();
    void TakingNumbers(){
        try{
            Scanner sc = new Scanner(System.in);
            while(true){
                System.out.print("Введите любое значение ("+ NumbersList.size()+ "/50): ");
                NumbersList.add(sc.next());
                if (NumbersList.size() == 10){
                    System.out.println("Список: " + NumbersList);
                    sc.nextLine();
                    return;
                }
            }
        } catch (Exception e){
            System.out.println("Ошибка ввода: " + e);
        }

    }
}

