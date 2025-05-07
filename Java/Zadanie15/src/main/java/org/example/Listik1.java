package org.example;

import java.util.HashSet;
import java.util.Set;

class Listik1 extends Listik {
    String NumbersString;
    Set<String> NumbersSet;
    public Listik1() {
        super.TakingNumbers();
        TakingNumbers();
    }
    @Override
    void TakingNumbers() {
        NumbersString = String.join(", ", NumbersList);
        NumbersSet = new HashSet<>(NumbersList);
        System.out.println("Строка: " + NumbersString);
        System.out.println("Множество: " + NumbersSet);
    }
}
