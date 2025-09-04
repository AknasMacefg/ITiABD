package org.example;

import java.util.Scanner;
import java.util.InputMismatchException;

public class TriangleMenu {
    private Scanner scanner;

    public TriangleMenu() {
        this.scanner = new Scanner(System.in);
    }

    public double[] processTriangle() {
        while (true) {
            try {
                System.out.println("\nВведите длины сторон треугольника:");
                System.out.print("Сторона A: ");
                double a = scanner.nextDouble();
                System.out.print("Сторона B: ");
                double b = scanner.nextDouble();
                System.out.print("Сторона C: ");
                double c = scanner.nextDouble();
                scanner.nextLine();

                Triangle triangle = new Triangle(a, b, c);
                RightTriangle rightTriangle = new RightTriangle(a, b, c);

                if (!triangle.isValid()) {
                    System.out.println("Треугольник с такими сторонами не существует!");
                    continue;
                }


                String triangleType;
                double area, perimeter;

                if (rightTriangle.isRight()) {
                    triangleType = "Прямоугольный";
                    perimeter = rightTriangle.calculatePerimeter();
                    area = rightTriangle.calculateArea();
                } else {
                    triangleType = "Произвольный";
                    perimeter = triangle.calculatePerimeter();
                    area = triangle.calculateArea();
                }

                System.out.println("\nОпределен тип треугольника: " + triangleType);
                System.out.printf("Периметр: %.2f\n", perimeter);
                System.out.printf("Площадь: %.2f\n", area);

                return new double[]{a, b, c, perimeter, area};

            } catch (InputMismatchException e) {
                System.out.println("Ошибка ввода! Введите числовые значения для сторон.");
                scanner.nextLine();
            }
        }
    }
}