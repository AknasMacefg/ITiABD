package org.calc.calc;

import javafx.scene.canvas.Canvas;
import javafx.scene.canvas.GraphicsContext;
import javafx.scene.paint.Color;

import java.util.List;

public class DividerDrawer {

    public static void draw(Canvas canvas, DividerCalculator.Result result) {
        GraphicsContext gc = canvas.getGraphicsContext2D();
        gc.clearRect(0, 0, canvas.getWidth(), canvas.getHeight());

        gc.setStroke(Color.BLACK);
        gc.setFill(Color.BLACK);
        gc.setLineWidth(2);

        double w = canvas.getWidth();
        double h = canvas.getHeight();


        double marginX = 60;
        double marginY = 40;
        // Координаты основных узлов
        double vinX = marginX;
        double voutX = w - marginX;
        double centerX = w / 2;

        double yTop = marginY;
        double yBottom = h - marginY;
        double yMid = (yTop + yBottom) / 2;

        // Подписи узлов
        gc.fillText("Vin", vinX - 30, yTop + 5);
        gc.fillText("GND", vinX - 30, yBottom + 5);
        gc.fillText("Vout", voutX + 10, yMid + 5);

        // Входной проводник: Vin -> центр верхнего узла
        gc.strokeLine(vinX, yTop, centerX, yTop);
        gc.fillOval(vinX - 3, yTop - 3, 6, 6);

        // Земля: центр нижнего узла -> GND (через горизонтальный провод)
        gc.strokeLine(centerX, yBottom, vinX, yBottom);
        gc.fillOval(vinX - 3, yBottom - 3, 6, 6);

        // Соединение Vout: от средней точки вправо
        // (нарисуем после построения плеч, чтобы знать точку Vout)

        String scheme = result.scheme != null ? result.scheme.toLowerCase() : "";
        List<Double> r = result.resistors;

        // Определяем типы верхнего/нижнего плеча
        boolean is2r = scheme.startsWith("2r");
        boolean is3r = scheme.startsWith("3r");
        boolean is4r = scheme.startsWith("4r");

        boolean parallelTop = scheme.contains("parallel top+bottom") || scheme.contains("parallel top");
        boolean parallelBottom = scheme.contains("parallel top+bottom") || scheme.contains("parallel bottom");
        // Для 3R/4R: если явно не параллель — считаем серию (по умолчанию)
        // (для 2R это не используется)

        // Отрисовка по типам
        if (is2r) {
            // r[0] = R1 (верх), r[1] = R2 (ниж)
            drawSeriesBetween(gc, centerX, yTop, yMid, List.of(r.get(0)), List.of("R1=" + formatR(r.get(0))));
            drawSeriesBetween(gc, centerX, yMid, yBottom, List.of(r.get(1)), List.of("R2=" + formatR(r.get(1))));
            // Vout от yMid
            gc.strokeLine(centerX, yMid, voutX, yMid);
            gc.fillOval(centerX - 3, yMid - 3, 6, 6);
        }
        else if (is3r) {
            // Возможные схемы, ожидаемые из DividerCalculator:
            // "3R series top", "3R series bottom", "3R parallel top", "3R parallel bottom"
            if (scheme.contains("series top")) {
                // top = r0 + r1, bottom = r2
                drawSeriesBetween(gc, centerX, yTop, yMid, List.of(r.get(0), r.get(1)),
                        List.of("R1=" + formatR(r.get(0)), "R2=" + formatR(r.get(1))));
                drawSeriesBetween(gc, centerX, yMid, yBottom, List.of(r.get(2)), List.of("R3=" + formatR(r.get(2))));
            } else if (scheme.contains("series bottom")) {
                // top = r0, bottom = r1 + r2
                drawSeriesBetween(gc, centerX, yTop, yMid, List.of(r.get(0)), List.of("R1=" + formatR(r.get(0))));
                drawSeriesBetween(gc, centerX, yMid, yBottom, List.of(r.get(1), r.get(2)),
                        List.of("R2=" + formatR(r.get(1)), "R3=" + formatR(r.get(2))));
            } else if (scheme.contains("parallel top")) {
                // top = r0 || r1, bottom = r2
                drawParallelBetween(gc, centerX, yTop, yMid, r.get(0), r.get(1),
                        "R1=" + formatR(r.get(0)), "R2=" + formatR(r.get(1)));
                drawSeriesBetween(gc, centerX, yMid, yBottom, List.of(r.get(2)), List.of("R3=" + formatR(r.get(2))));
            } else if (scheme.contains("parallel bottom")) {
                // top = r0, bottom = r1 || r2
                drawSeriesBetween(gc, centerX, yTop, yMid, List.of(r.get(0)), List.of("R1=" + formatR(r.get(0))));
                drawParallelBetween(gc, centerX, yMid, yBottom, r.get(1), r.get(2),
                        "R2=" + formatR(r.get(1)), "R3=" + formatR(r.get(2)));
            } else {
                // На всякий случай, попробуем отрисовать общий случай:
                drawSeriesBetween(gc, centerX, yTop, yMid, List.of(r.get(0)), List.of("R1=" + formatR(r.get(0))));
                drawSeriesBetween(gc, centerX, yMid, yBottom, List.of(r.get(1), r.get(2)),
                        List.of("R2=" + formatR(r.get(1)), "R3=" + formatR(r.get(2))));
            }
            gc.strokeLine(centerX, yMid, voutX, yMid);
            gc.fillOval(centerX - 3, yMid - 3, 6, 6);
        }
        else if (is4r) {
            // Поддерживаем четыре варианта, которые генерировал калькулятор:
            // "4R series top+bottom"
            // "4R parallel top, series bottom"
            // "4R series top, parallel bottom"
            // "4R parallel top+bottom"
            if (scheme.contains("series top+bottom")) {
                // top: r0 + r1, bottom: r2 + r3
                drawSeriesBetween(gc, centerX, yTop, yMid, List.of(r.get(0), r.get(1)),
                        List.of("R1=" + formatR(r.get(0)), "R2=" + formatR(r.get(1))));
                drawSeriesBetween(gc, centerX, yMid, yBottom, List.of(r.get(2), r.get(3)),
                        List.of("R3=" + formatR(r.get(2)), "R4=" + formatR(r.get(3))));
            } else if (scheme.contains("parallel top, series bottom")) {
                // top: r0||r1, bottom: r2 + r3
                drawParallelBetween(gc, centerX, yTop, yMid, r.get(0), r.get(1),
                        "R1=" + formatR(r.get(0)), "R2=" + formatR(r.get(1)));
                drawSeriesBetween(gc, centerX, yMid, yBottom, List.of(r.get(2), r.get(3)),
                        List.of("R3=" + formatR(r.get(2)), "R4=" + formatR(r.get(3))));
            } else if (scheme.contains("series top, parallel bottom")) {
                // top: r0 + r1, bottom: r2||r3
                drawSeriesBetween(gc, centerX, yTop, yMid, List.of(r.get(0), r.get(1)),
                        List.of("R1=" + formatR(r.get(0)), "R2=" + formatR(r.get(1))));
                drawParallelBetween(gc, centerX, yMid, yBottom, r.get(2), r.get(3),
                        "R3=" + formatR(r.get(2)), "R4=" + formatR(r.get(3)));
            } else if (scheme.contains("parallel top+bottom")) {
                // top: r0||r1, bottom: r2||r3
                drawParallelBetween(gc, centerX, yTop, yMid, r.get(0), r.get(1),
                        "R1=" + formatR(r.get(0)), "R2=" + formatR(r.get(1)));
                drawParallelBetween(gc, centerX, yMid, yBottom, r.get(2), r.get(3),
                        "R3=" + formatR(r.get(2)), "R4=" + formatR(r.get(3)));
            } else {
                // fallback: разместим 4 в две серии
                drawSeriesBetween(gc, centerX, yTop, yMid, List.of(r.get(0), r.get(1)),
                        List.of("R1=" + formatR(r.get(0)), "R2=" + formatR(r.get(1))));
                drawSeriesBetween(gc, centerX, yMid, yBottom, List.of(r.get(2), r.get(3)),
                        List.of("R3=" + formatR(r.get(2)), "R4=" + formatR(r.get(3))));
            }
            gc.strokeLine(centerX, yMid, voutX, yMid);
            gc.fillOval(centerX - 3, yMid - 3, 6, 6);
        } else {
            gc.fillText("Неизвестная схема: " + result.scheme, 10, h / 2);
            return;
        }

    }

    // Рисует последовательную цепочку из N резисторов между yStart и yEnd по координате x.
    private static void drawSeriesBetween(GraphicsContext gc, double x, double yStart, double yEnd,
                                          List<Double> values, List<String> labels) {
        int n = values.size();
        double seg = (yEnd - yStart) / n;
        double y0 = yStart;
        for (int i = 0; i < n; i++) {
            double y1 = y0;
            double y2 = y0 + seg;
            drawResistorVertical(gc, x, y1, y2, labels.get(i));
            y0 = y2;
            // соединительный провод между резисторами (если есть следующий) - уже рисуется линиями резистора
        }
    }

    // Рисует две параллельные ветви между yStart и yEnd (левый и правый от центра)
    private static void drawParallelBetween(GraphicsContext gc, double centerX, double yStart, double yEnd,
                                            double rLeft, double rRight, String labelLeft, String labelRight) {
        double dx = 36; // смещение ветвей от центра
        double leftX = centerX - dx;
        double rightX = centerX + dx;

        // верхняя шина (соединение ветвей сверху)
        gc.strokeLine(centerX - 12, yStart, centerX + 12, yStart);
        // нижняя шина
        gc.strokeLine(centerX - 12, yEnd, centerX + 12, yEnd);

        // Левая ветвь
        drawResistorVertical(gc, leftX, yStart, yEnd, labelLeft);
        // Правая ветвь
        drawResistorVertical(gc, rightX, yStart, yEnd, labelRight);

        // Соединительные линии от шин к ветвям
        gc.strokeLine(leftX, yStart, centerX - 12, yStart);
        gc.strokeLine(rightX, yStart, centerX + 12, yStart);
        gc.strokeLine(leftX, yEnd, centerX - 12, yEnd);
        gc.strokeLine(rightX, yEnd, centerX + 12, yEnd);
    }

    // Рисует "вертикальный" резистор между точками y1 и y2 по координате x.
    // Рисунок: провод — прямоугольник (как символ резистора) — провод
    private static void drawResistorVertical(GraphicsContext gc, double x, double y1, double y2, String label) {
        double segMid = (y1 + y2) / 2;
        // провод сверху
        gc.strokeLine(x, y1, x, segMid - 10);
        // резистор (прямоугольник)
        double w = 24, h = 20;
        gc.strokeRect(x - w / 2, segMid - h / 2, w, h);
        // провод снизу
        gc.strokeLine(x, segMid + 10, x, y2);
        // подпись справа от резистора
        gc.fillText(label, x + w / 2 + 6, segMid + 4);
    }

    private static String formatR(double r) {
        if (r >= 1_000_000) return String.format("%.2fMΩ", r / 1_000_000.0);
        if (r >= 1000) return String.format("%.2fkΩ", r / 1000.0);
        if (r >= 1) return String.format("%.0fΩ", r);
        return String.format("%.2fΩ", r);
    }
}
