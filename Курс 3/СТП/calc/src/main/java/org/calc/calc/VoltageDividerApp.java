package org.calc.calc;

import javafx.application.Application;
import javafx.scene.Scene;
import javafx.scene.canvas.Canvas;
import javafx.scene.control.*;
import javafx.scene.layout.*;
import javafx.stage.Stage;

import java.util.List;

public class VoltageDividerApp extends Application {

    @Override
    public void start(Stage stage) {
        // Вводные поля
        TextField vinField = new TextField("12");
        TextField voutField = new TextField("5");
        TextField tolField = new TextField("2");
        TextField rMinField = new TextField("100");
        TextField rMaxField = new TextField("100000");

        ComboBox<String> seriesBox = new ComboBox<>();
        seriesBox.getItems().addAll("E6", "E12", "E24", "E96");
        seriesBox.setValue("E12");

        Button calcBtn = new Button("Рассчитать");

        // Таблица результатов
        TableView<DividerCalculator.Result> table = new TableView<>();
        TableColumn<DividerCalculator.Result, String> schemeCol = new TableColumn<>("Схема");
        schemeCol.setCellValueFactory(c -> new javafx.beans.property.SimpleStringProperty(c.getValue().scheme));

        TableColumn<DividerCalculator.Result, String> resistorsCol = new TableColumn<>("Резисторы");
        resistorsCol.setCellValueFactory(c -> new javafx.beans.property.SimpleStringProperty(c.getValue().resistors.toString()));

        TableColumn<DividerCalculator.Result, String> voutCol = new TableColumn<>("Vout");
        voutCol.setCellValueFactory(c -> new javafx.beans.property.SimpleStringProperty(String.format("%.3f", c.getValue().vout)));

        TableColumn<DividerCalculator.Result, String> errCol = new TableColumn<>("Ошибка %");
        errCol.setCellValueFactory(c -> new javafx.beans.property.SimpleStringProperty(String.format("%.3f", c.getValue().errorPercent)));

        table.getColumns().addAll(schemeCol, resistorsCol, voutCol, errCol);
        table.setPrefWidth(500);

        // Холст для отрисовки схемы
        Canvas canvas = new Canvas(400, 300);

        // Кнопка рассчёта
        calcBtn.setOnAction(e -> {
            try {
                double vin = Double.parseDouble(vinField.getText());
                double vreq = Double.parseDouble(voutField.getText());
                double tol = Double.parseDouble(tolField.getText());
                double rmin = Double.parseDouble(rMinField.getText());
                double rmax = Double.parseDouble(rMaxField.getText());
                String series = seriesBox.getValue();

                List<DividerCalculator.Result> results = DividerCalculator.findSolutions(
                        vin, vreq, tol, series, rmin, rmax
                );
                table.getItems().setAll(results);

            } catch (Exception ex) {
                ex.printStackTrace();
                new Alert(Alert.AlertType.ERROR, "Ошибка ввода данных: " + ex.getMessage()).showAndWait();
            }
        });

        // Отображение схемы при выборе строки
        table.setOnMouseClicked(e -> {
            DividerCalculator.Result res = table.getSelectionModel().getSelectedItem();
            if (res != null) {
                DividerDrawer.draw(canvas, res);
            }
        });

        // Панель ввода
        VBox inputs = new VBox(5,
                new HBox(5, new Label("Vin:"), vinField),
                new HBox(5, new Label("Vout:"), voutField),
                new HBox(5, new Label("Допуск %:"), tolField),
                new HBox(5, new Label("Ряд:"), seriesBox),
                new HBox(5, new Label("R min:"), rMinField, new Label("R max:"), rMaxField),
                calcBtn
        );

        HBox root = new HBox(10, inputs, table, canvas);
        stage.setScene(new Scene(root, 1000, 400));
        stage.setTitle("Калькулятор делителя напряжения");
        stage.show();
    }

    public static void main(String[] args) {
        launch();
    }
}
