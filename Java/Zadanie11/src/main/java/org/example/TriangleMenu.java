package org.example;

import java.util.Scanner;
import java.util.InputMismatchException;

public class TriangleMenu {
    private Scanner scanner;

    public TriangleMenu() {
        this.scanner = new Scanner(System.in);
    }

    public double[] processTriangle() {

        System.out.println("\nВыберите тип треугольника:");
        System.out.println("1. Произвольный треугольник (не прямоугольный)");
        System.out.println("2. Прямоугольный треугольник");
        System.out.print("Ваш выбор: ");

        int choice;
        while (true) {
            try {
                choice = scanner.nextInt();
            } catch (InputMismatchException e) {
                System.out.println("Ошибка ввода! Введите число 1 или 2.");
                scanner.nextLine();
                continue;
            }

            scanner.nextLine();
            try {
                System.out.println("Введите длины сторон треугольника:");
                System.out.print("Сторона A: ");
                double a = scanner.nextDouble();
                System.out.print("Сторона B: ");
                double b = scanner.nextDouble();
                System.out.print("Сторона C: ");
                double c = scanner.nextDouble();
                scanner.nextLine();

                // Создаем временный объект для проверки
                RightTriangle tempTriangle = new RightTriangle(a, b, c);

                if (choice == 1) {
                    if (tempTriangle.isRight()) {
                        System.out.println("Введенный треугольник является прямоугольным. " +
                                "Выберите другой тип треугольника или измените стороны.");
                        continue;
                    }
                    return processRegularTriangle(a, b, c);
                } else if (choice == 2) {
                    return processRightTriangle(a, b, c);
                } else {
                    System.out.println("Неверный выбор типа треугольника.");
                }
            } catch (InputMismatchException e) {
                System.out.println("Ошибка ввода: Введите числовые значения для сторон.");
                scanner.nextLine();
            }
        }
    }

    private double[] processRegularTriangle(double a, double b, double c) {
        Triangle triangle = new Triangle(a, b, c);
        if (!triangle.isValid()) {
            System.out.println("Треугольник с такими сторонами не существует");
            return new double[]{a,b,c,0,0};
        }

        double perimeter = triangle.calculatePerimeter();
        double area = triangle.calculateArea();

        printResults(perimeter, area);
        return new double[]{a,b,c,area,perimeter};
    }

    private double[] processRightTriangle(double a, double b, double c) {
        RightTriangle rightTriangle = new RightTriangle(a, b, c);
        if (!rightTriangle.isValid()) {
            System.out.println("Треугольник с такими сторонами не существует");
            return new double[]{a,b,c,0,0};
        }

        if (!rightTriangle.isRight()) {
            System.out.println("Введенный треугольник не является прямоугольным");
            return new double[]{a,b,c,0,0};
        }

        double perimeter = rightTriangle.calculatePerimeter();
        double area = rightTriangle.calculateArea();

        printResults(perimeter, area);
        return new double[]{a,b,c,area,perimeter};
    }

    private void printResults(double perimeter, double area) {
        System.out.println("\nРезультаты расчетов:");
        System.out.printf("Периметр: %.2f\n", perimeter);
        System.out.printf("Площадь: %.2f\n", area);
    }
}