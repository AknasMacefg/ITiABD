package org.calc.calc;

/**
 * Класс для выполнения расчетов по закону Ома.
 * Закон Ома: U = I * R, где U - напряжение, I - ток, R - сопротивление.
 * 
 * <p>Класс предоставляет методы для расчета:
 * <ul>
 *   <li>Напряжения (V) по формуле: V = I * R</li>
 *   <li>Тока (I) по формуле: I = V / R</li>
 *   <li>Сопротивления (R) по формуле: R = V / I</li>
 * </ul>
 * 
 * <p>Поддерживаются единицы измерения:
 * <ul>
 *   <li>Напряжение: В (вольты), кВ (киловольты), мВ (милливольты)</li>
 *   <li>Ток: А (амперы), мА (миллиамперы)</li>
 *   <li>Сопротивление: Ом (омы), кОм (килоомы), МОм (мегаомы)</li>
 * </ul>
 * 
 * @author calc
 * @version 1.0
 */
public class CalcProcesses {

    /**
     * Вычисляет напряжение по закону Ома: V = I * R.
     * 
     * @param OM значение сопротивления в виде строки
     * @param A значение силы тока в виде строки
     * @param OMpar единица измерения сопротивления ("Ом", "кОм", "МОм")
     * @param Apar единица измерения тока ("А", "мА")
     * @param Vpar единица измерения напряжения для результата ("В", "кВ", "мВ")
     * @return строковое представление вычисленного напряжения в указанных единицах
     */
    static String VCalc(String OM, String A, String OMpar, String Apar, String Vpar) {
        double OMdouble = Double.parseDouble(OM);
        OMdouble = NumberConverter(OMdouble, OMpar);
        double Adouble = Double.parseDouble(A);
        Adouble = NumberConverter(Adouble, Apar);
        double Vdouble = OMdouble * Adouble;
        Vdouble = NumberConverterBack(Vdouble, Vpar);
        return Double.toString(Vdouble);
    }

    /**
     * Вычисляет силу тока по закону Ома: I = V / R.
     * 
     * @param V значение напряжения в виде строки
     * @param OM значение сопротивления в виде строки
     * @param OMpar единица измерения сопротивления ("Ом", "кОм", "МОм")
     * @param Apar единица измерения тока для результата ("А", "мА")
     * @param Vpar единица измерения напряжения ("В", "кВ", "мВ")
     * @return строковое представление вычисленной силы тока в указанных единицах
     */
    static String ACalc(String V, String OM, String OMpar, String Apar, String Vpar){
        double Vdouble = Double.parseDouble(V);
        Vdouble = NumberConverter(Vdouble, Vpar);
        double OMdouble = Double.parseDouble(OM);
        OMdouble = NumberConverter(OMdouble, OMpar);
        double Adouble = Vdouble / OMdouble;
        Adouble = NumberConverterBack(Adouble, Apar);
        return Double.toString(Adouble);
    }

    /**
     * Вычисляет сопротивление по закону Ома: R = V / I.
     * 
     * @param V значение напряжения в виде строки
     * @param A значение силы тока в виде строки
     * @param OMpar единица измерения сопротивления для результата ("Ом", "кОм", "МОм")
     * @param Apar единица измерения тока ("А", "мА")
     * @param Vpar единица измерения напряжения ("В", "кВ", "мВ")
     * @return строковое представление вычисленного сопротивления в указанных единицах
     */
    static String OMCalc(String V, String A, String OMpar, String Apar, String Vpar){
        double Vdouble = Double.parseDouble(V);
        Vdouble = NumberConverter(Vdouble, Vpar);
        double Adouble = Double.parseDouble(A);
        Adouble = NumberConverter(Adouble, Apar);
        double OMdouble = Vdouble / Adouble;
        OMdouble = NumberConverterBack(OMdouble, OMpar);
        return Double.toString(OMdouble);
    }

    /**
     * Преобразует число из указанных единиц измерения в базовые единицы СИ.
     * 
     * @param number числовое значение для преобразования
     * @param changer строка с единицей измерения (первый символ: 'м' - милли, 'к' - кило, 'М' - мега)
     * @return преобразованное значение в базовых единицах СИ
     */
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

    /**
     * Преобразует число из базовых единиц СИ в указанные единицы измерения.
     * 
     * @param number числовое значение в базовых единицах СИ
     * @param changer строка с единицей измерения (первый символ: 'м' - милли, 'к' - кило, 'М' - мега)
     * @return преобразованное значение в указанных единицах
     */
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
