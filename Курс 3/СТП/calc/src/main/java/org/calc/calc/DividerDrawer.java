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

        // Входной проводник:
        gc.strokeLine(vinX, yTop, centerX, yTop);
        gc.fillOval(vinX - 3, yTop - 3, 6, 6);

        // Земля:
        gc.strokeLine(centerX, yBottom, vinX, yBottom);
        gc.fillOval(vinX - 3, yBottom - 3, 6, 6);


        String scheme = result.scheme != null ? result.scheme.toLowerCase() : "";
        List<Double> r = result.resistors;

        boolean is2r = scheme.startsWith("2r");
        boolean is3r = scheme.startsWith("3r");
        boolean is4r = scheme.startsWith("4r");

        boolean parallelTop = scheme.contains("parallel top+bottom") || scheme.contains("parallel top");
        boolean parallelBottom = scheme.contains("parallel top+bottom") || scheme.contains("parallel bottom");

        // Отрисовка по типам
        if (is2r) {
            drawSeriesBetween(gc, centerX, yTop, yMid, List.of(r.get(0)), List.of("R1=" + formatR(r.get(0))));
            drawSeriesBetween(gc, centerX, yMid, yBottom, List.of(r.get(1)), List.of("R2=" + formatR(r.get(1))));
            // Vout от yMid
            gc.strokeLine(centerX, yMid, voutX, yMid);
            gc.fillOval(centerX - 3, yMid - 3, 6, 6);
        }
        else if (is3r) {
            if (scheme.contains("series top")) {
                drawSeriesBetween(gc, centerX, yTop, yMid, List.of(r.get(0), r.get(1)),
                        List.of("R1=" + formatR(r.get(0)), "R2=" + formatR(r.get(1))));
                drawSeriesBetween(gc, centerX, yMid, yBottom, List.of(r.get(2)), List.of("R3=" + formatR(r.get(2))));
            } else if (scheme.contains("series bottom")) {
                drawSeriesBetween(gc, centerX, yTop, yMid, List.of(r.get(0)), List.of("R1=" + formatR(r.get(0))));
                drawSeriesBetween(gc, centerX, yMid, yBottom, List.of(r.get(1), r.get(2)),
                        List.of("R2=" + formatR(r.get(1)), "R3=" + formatR(r.get(2))));
            } else if (scheme.contains("parallel top")) {
                drawParallelBetween(gc, centerX, yTop, yMid, r.get(0), r.get(1),
                        "R1=" + formatR(r.get(0)), "R2=" + formatR(r.get(1)));
                drawSeriesBetween(gc, centerX, yMid, yBottom, List.of(r.get(2)), List.of("R3=" + formatR(r.get(2))));
            } else if (scheme.contains("parallel bottom")) {
                drawSeriesBetween(gc, centerX, yTop, yMid, List.of(r.get(0)), List.of("R1=" + formatR(r.get(0))));
                drawParallelBetween(gc, centerX, yMid, yBottom, r.get(1), r.get(2),
                        "R2=" + formatR(r.get(1)), "R3=" + formatR(r.get(2)));
            } else {
                drawSeriesBetween(gc, centerX, yTop, yMid, List.of(r.get(0)), List.of("R1=" + formatR(r.get(0))));
                drawSeriesBetween(gc, centerX, yMid, yBottom, List.of(r.get(1), r.get(2)),
                        List.of("R2=" + formatR(r.get(1)), "R3=" + formatR(r.get(2))));
            }
            gc.strokeLine(centerX, yMid, voutX, yMid);
            gc.fillOval(centerX - 3, yMid - 3, 6, 6);
        }
        else if (is4r) {
            if (scheme.contains("series top+bottom")) {
                drawSeriesBetween(gc, centerX, yTop, yMid, List.of(r.get(0), r.get(1)),
                        List.of("R1=" + formatR(r.get(0)), "R2=" + formatR(r.get(1))));
                drawSeriesBetween(gc, centerX, yMid, yBottom, List.of(r.get(2), r.get(3)),
                        List.of("R3=" + formatR(r.get(2)), "R4=" + formatR(r.get(3))));
            } else if (scheme.contains("parallel top, series bottom")) {
                drawParallelBetween(gc, centerX, yTop, yMid, r.get(0), r.get(1),
                        "R1=" + formatR(r.get(0)), "R2=" + formatR(r.get(1)));
                drawSeriesBetween(gc, centerX, yMid, yBottom, List.of(r.get(2), r.get(3)),
                        List.of("R3=" + formatR(r.get(2)), "R4=" + formatR(r.get(3))));
            } else if (scheme.contains("series top, parallel bottom")) {
                drawSeriesBetween(gc, centerX, yTop, yMid, List.of(r.get(0), r.get(1)),
                        List.of("R1=" + formatR(r.get(0)), "R2=" + formatR(r.get(1))));
                drawParallelBetween(gc, centerX, yMid, yBottom, r.get(2), r.get(3),
                        "R3=" + formatR(r.get(2)), "R4=" + formatR(r.get(3)));
            } else if (scheme.contains("parallel top+bottom")) {
                drawParallelBetween(gc, centerX, yTop, yMid, r.get(0), r.get(1),
                        "R1=" + formatR(r.get(0)), "R2=" + formatR(r.get(1)));
                drawParallelBetween(gc, centerX, yMid, yBottom, r.get(2), r.get(3),
                        "R3=" + formatR(r.get(2)), "R4=" + formatR(r.get(3)));
            } else {
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

        }
    }


    private static void drawParallelBetween(GraphicsContext gc, double centerX, double yStart, double yEnd,
                                            double rLeft, double rRight, String labelLeft, String labelRight) {
        double dx = 36;
        double leftX = centerX - dx;
        double rightX = centerX + dx;


        gc.strokeLine(centerX - 12, yStart, centerX + 12, yStart);

        gc.strokeLine(centerX - 12, yEnd, centerX + 12, yEnd);


        drawResistorVertical(gc, leftX, yStart, yEnd, labelLeft);

        drawResistorVertical(gc, rightX, yStart, yEnd, labelRight);

        // Соединительные линии от шин к ветвям
        gc.strokeLine(leftX, yStart, centerX - 12, yStart);
        gc.strokeLine(rightX, yStart, centerX + 12, yStart);
        gc.strokeLine(leftX, yEnd, centerX - 12, yEnd);
        gc.strokeLine(rightX, yEnd, centerX + 12, yEnd);
    }

    private static void drawResistorVertical(GraphicsContext gc, double x, double y1, double y2, String label) {
        double segMid = (y1 + y2) / 2;
        gc.strokeLine(x, y1, x, segMid - 10);
        double w = 24, h = 20;
        gc.strokeRect(x - w / 2, segMid - h / 2, w, h);
        gc.strokeLine(x, segMid + 10, x, y2);
        gc.fillText(label, x + w / 2 + 6, segMid + 4);
    }

    private static String formatR(double r) {
        if (r >= 1_000_000) return String.format("%.2fMΩ", r / 1_000_000.0);
        if (r >= 1000) return String.format("%.2fkΩ", r / 1000.0);
        if (r >= 1) return String.format("%.0fΩ", r);
        return String.format("%.2fΩ", r);
    }
}
