// RightTriangle.java
package org.example;

public class RightTriangle extends Triangle {
    public RightTriangle(double a, double b, double c) {
        super(a, b, c);
    }

    @Override
    public double calculateArea() {
        // Находим гипотенузу (она должна быть наибольшей стороной)
        double hypotenuse = Math.max(sideA, Math.max(sideB, sideC));
        if (hypotenuse == sideA) {
            return sideB * sideC / 2;
        } else if (hypotenuse == sideB) {
            return sideA * sideC / 2;
        } else {
            return sideA * sideB / 2;
        }
    }

    public boolean isRight() {
        double a2 = sideA * sideA;
        double b2 = sideB * sideB;
        double c2 = sideC * sideC;

        return Math.abs(a2 + b2 - c2) < 0.0001 ||
                Math.abs(a2 + c2 - b2) < 0.0001 ||
                Math.abs(b2 + c2 - a2) < 0.0001;
    }
}