package org.calc.calc;

public class CalcProcesses {

    static String VCalc(String OM, String A){
        double OMdouble = Double.parseDouble(OM);
        double Adouble = Double.parseDouble(A);
        double Vdouble = OMdouble * Adouble;
        return Double.toString(Vdouble);
    }

    static String ACalc(String V, String OM){
        double Vdouble = Double.parseDouble(V);
        double OMdouble = Double.parseDouble(OM);
        double Adouble = Vdouble / OMdouble;
        return Double.toString(Adouble);
    }

    static String OMCalc(String V, String A){
        double Vdouble = Double.parseDouble(V);
        double Adouble = Double.parseDouble(A);
        double OMdouble = Vdouble / Adouble;
        return Double.toString(OMdouble);
    }

}
