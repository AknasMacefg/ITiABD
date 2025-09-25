package org.calc.calc;

public class CalcProcesses {

    static String VCalc(String OM, String A, String OMpar, String Apar, String Vpar) {
        double OMdouble = Double.parseDouble(OM);
        OMdouble = NumberConverter(OMdouble, OMpar);
        double Adouble = Double.parseDouble(A);
        Adouble = NumberConverter(Adouble, Apar);
        double Vdouble = OMdouble * Adouble;
        Vdouble = NumberConverterBack(Vdouble, Vpar);
        return Double.toString(Vdouble);
    }

    static String ACalc(String V, String OM, String OMpar, String Apar, String Vpar){
        double Vdouble = Double.parseDouble(V);
        Vdouble = NumberConverter(Vdouble, Vpar);
        double OMdouble = Double.parseDouble(OM);
        OMdouble = NumberConverter(OMdouble, OMpar);
        double Adouble = Vdouble / OMdouble;
        Adouble = NumberConverterBack(Adouble, Apar);
        return Double.toString(Adouble);
    }

    static String OMCalc(String V, String A, String OMpar, String Apar, String Vpar){
        double Vdouble = Double.parseDouble(V);
        Vdouble = NumberConverter(Vdouble, Vpar);
        double Adouble = Double.parseDouble(A);
        Adouble = NumberConverter(Adouble, Apar);
        double OMdouble = Vdouble / Adouble;
        OMdouble = NumberConverterBack(OMdouble, OMpar);
        return Double.toString(OMdouble);
    }

    private static double NumberConverter(double number, String changer) {
        switch (changer.charAt(0)) {
            case 'м':
                number = number * 0.001;
                break;
            case 'М':
                number = number * 10000000;
                break;
            case 'к':
                number = number * 1000;
                break;
        }
        return number;
    }

    private static double NumberConverterBack(double number, String changer) {
        switch (changer.charAt(0)) {
            case 'м':
                number = number * 1000;
                break;
            case 'М':
                number = number * 0.000001;
                break;
            case 'к':
                number = number * 0.001;
                break;
        }
        return number;
    }

}
