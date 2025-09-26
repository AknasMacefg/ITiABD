package org.calc.calc;

import java.util.*;

public class DividerCalculator {

    // Ряды резисторов
    private static final Map<String, double[]> baseSeries = Map.of(
            "E6", new double[]{1.0, 1.5, 2.2, 3.3, 4.7, 6.8},
            "E12", new double[]{1.0, 1.2, 1.5, 1.8, 2.2, 2.7, 3.3, 3.9, 4.7, 5.6, 6.8, 8.2},
            "E24", new double[]{1.0, 1.1, 1.2, 1.3, 1.5, 1.6, 1.8, 2.0, 2.2, 2.4, 2.7, 3.0,
                    3.3, 3.6, 3.9, 4.3, 4.7, 5.1, 5.6, 6.2, 6.8, 7.5, 8.2, 9.1},
            "E96", new double[]{1.00, 1.02, 1.05, 1.07, 1.10, 1.13, 1.15, 1.18, 1.21, 1.24,
                    1.27, 1.30, 1.33, 1.37, 1.40, 1.43, 1.47, 1.50, 1.54, 1.58,
                    9.76, 9.88}
    );

    public static class Result {
        public String scheme;
        public List<Double> resistors;
        public double vout;
        public double errorPercent;
        public double power;

        @Override
        public String toString() {
            return String.format("%s: %s => Vout=%.3fV, err=%.3f%%, P=%.3fmW",
                    scheme, resistors, vout, errorPercent, power * 1000);
        }
    }

    // Генерация номиналов
    public static List<Double> generateValues(String series, double rMin, double rMax) {
        List<Double> values = new ArrayList<>();
        double[] base = baseSeries.get(series);
        if (base == null) throw new IllegalArgumentException("Unknown series: " + series);

        for (int exp = -1; exp <= 7; exp++) {
            double factor = Math.pow(10, exp);
            for (double b : base) {
                double r = b * factor;
                if (r >= rMin && r <= rMax) {
                    values.add(r);
                }
            }
        }
        return values;
    }

    // Основной поиск решений
    public static List<Result> findSolutions(double vin, double vRequired,
                                             double tolerancePercent,
                                             String series, double rMin, double rMax) {
        List<Double> values = generateValues(series, rMin, rMax);
        List<Result> results = new ArrayList<>();

        // --- 2 резистора ---
        for (double r1 : values) {
            for (double r2 : values) {
                checkAndAdd(results, "2R: R1,R2", List.of(r1, r2),
                        vin, r1, r2, vRequired, tolerancePercent);
            }
        }

        // --- 3 резистора ---
        for (double r1 : values) {
            for (double r2 : values) {
                for (double r3 : values) {
                    checkAndAdd(results, "3R series top", List.of(r1, r2, r3),
                            vin, r1 + r2, r3, vRequired, tolerancePercent);
                    checkAndAdd(results, "3R series bottom", List.of(r1, r2, r3),
                            vin, r1, r2 + r3, vRequired, tolerancePercent);

                    double rTopPar = 1.0 / (1.0 / r1 + 1.0 / r2);
                    double rBotPar = 1.0 / (1.0 / r2 + 1.0 / r3);

                    checkAndAdd(results, "3R parallel top", List.of(r1, r2, r3),
                            vin, rTopPar, r3, vRequired, tolerancePercent);
                    checkAndAdd(results, "3R parallel bottom", List.of(r1, r2, r3),
                            vin, r1, rBotPar, vRequired, tolerancePercent);
                }
            }
        }

        // --- 4 резистора ---
        for (double r1 : values) {
            for (double r2 : values) {
                for (double r3 : values) {
                    for (double r4 : values) {
                        checkAndAdd(results, "4R series top+bottom", List.of(r1, r2, r3, r4),
                                vin, r1 + r2, r3 + r4, vRequired, tolerancePercent);

                        double rTopPar = 1.0 / (1.0 / r1 + 1.0 / r2);
                        checkAndAdd(results, "4R parallel top, series bottom", List.of(r1, r2, r3, r4),
                                vin, rTopPar, r3 + r4, vRequired, tolerancePercent);

                        double rBotPar = 1.0 / (1.0 / r3 + 1.0 / r4);
                        checkAndAdd(results, "4R series top, parallel bottom", List.of(r1, r2, r3, r4),
                                vin, r1 + r2, rBotPar, vRequired, tolerancePercent);

                        checkAndAdd(results, "4R parallel top+bottom", List.of(r1, r2, r3, r4),
                                vin, rTopPar, rBotPar, vRequired, tolerancePercent);
                    }
                }
            }
        }

        // сортировка
        results.sort(Comparator
                .comparingDouble((Result r) -> r.errorPercent)
                .thenComparingInt(r -> r.resistors.size())
                .thenComparingDouble(r -> r.power));

        return results;
    }

    private static void checkAndAdd(List<Result> results, String scheme, List<Double> resistors,
                                    double vin, double rTop, double rBot,
                                    double vRequired, double tol) {
        double vout = vin * rBot / (rTop + rBot);
        double err = Math.abs(vout - vRequired) / vRequired * 100;
        if (err <= tol) {
            Result res = new Result();
            res.scheme = scheme;
            res.resistors = new ArrayList<>(resistors);
            res.vout = vout;
            res.errorPercent = err;
            res.power = vin * vin / (rTop + rBot);
            results.add(res);
        }
    }
}
