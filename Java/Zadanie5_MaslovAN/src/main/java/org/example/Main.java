package org.example;

import java.sql.SQLException;
import java.util.Scanner;

public class Main {
    private static Scanner sc = new Scanner(System.in);
    public static void Selector() {
        boolean exit = false;
        while (!exit) {
            System.out.println("\n-------------------------------------\n");
            System.out.println("1. Вывести все таблицы PostgresSQL");
            System.out.println("2. Создать таблицу PostgresSQL");
            System.out.println("3. Изменить порядок символов строки на обратный");
            System.out.println("4. Добавить одну строку в другую");
            System.out.println("5. Экспорт данных из PostgresSQL в Excel");
            System.out.println("0. Выход из программы");
            System.out.print("Выберите действие: ");
            int choice = -1;
            try {
                choice = sc.nextInt();
            }
            catch (Exception e) {
                System.out.println("Введено неверное значение! Попробуйте снова." + e);
            }


        }

    }
    public static void main(String[] args) {

    }


}