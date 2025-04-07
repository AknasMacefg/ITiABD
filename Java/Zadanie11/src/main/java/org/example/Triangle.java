// Triangle.java
package org.example;

public class Triangle {
    protected double sideA;
    protected double sideB;
    protected double sideC;

    public Triangle(double a, double b, double c) {
        this.sideA = a;
        this.sideB = b;
        this.sideC = c;
    }

    public double calculatePerimeter() {
        return sideA + sideB + sideC;
    }

    public double calculateArea() {
        double p = calculatePerimeter() / 2;
        return Math.sqrt(p * (p - sideA) * (p - sideB) * (p - sideC));
    }

    public boolean isValid() {
        return (sideA + sideB > sideC) && (sideA + sideC > sideB) && (sideB + sideC > sideA);
    }
}