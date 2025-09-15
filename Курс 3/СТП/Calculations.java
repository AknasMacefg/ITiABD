package org.project.maslov_an_tasks;

public class Calculations {
    float I;
    float U;
    float R;

    public double ICalc(float U, float R){
        return U/R;
    }

    public double RCalc(float U, float I){
        return U/I;
    }

    public double UCalc(float I, float R){
        return I*R;
    }
}
