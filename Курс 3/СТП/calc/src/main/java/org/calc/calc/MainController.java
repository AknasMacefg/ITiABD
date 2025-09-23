package org.calc.calc;

import javafx.collections.FXCollections;
import javafx.collections.ObservableList;
import javafx.collections.transformation.FilteredList;
import javafx.fxml.FXML;
import javafx.scene.control.*;
import javafx.scene.control.cell.PropertyValueFactory;
import javafx.scene.layout.AnchorPane;
import javafx.stage.Stage;
import javafx.stage.Window;
import java.io.IOException;

import java.sql.ResultSet;
import java.sql.SQLException;

public class MainController {
   static public String userLogin;


    @FXML
    private Button ExitButton;

    @FXML
     private AnchorPane OmaCalc;

    @FXML
    private ChoiceBox<String> VChoice;

    @FXML
    private TextField VField;

    @FXML
    private AnchorPane ResistorsCalc;

    @FXML
    private ChoiceBox<String> AChoice;

    @FXML
    private TextField AField;

    @FXML
    private AnchorPane OperationsHistory;

    @FXML
    private ChoiceBox<String> OMChoice;

    @FXML
    private TextField OMField;

    @FXML
    private TableView<TableModel> HistoryTable;

    @FXML
    private TextField searchField;

    ObservableList<TableModel> data;





    @FXML
    private void onExitButtonClick() throws IOException {
        Window window = ExitButton.getScene().getWindow();
        if (window instanceof Stage) {
            CalcApplication.window_swap("login-view.fxml", (Stage) window, "Вход");
            userLogin = null;
        }
    }

    @FXML
    private void onOmaCalcButtonClick() throws IOException {
        OmaCalc.setVisible(true);
        ResistorsCalc.setVisible(false);
        OperationsHistory.setVisible(false);
        ObservableList<String> items = VChoice.getItems();
        if (items.size() == 0) {
            items.add("В");
            items.add("мВ");
            VChoice.setItems(items);
            VChoice.setValue(items.getFirst());
        }
        items = AChoice.getItems();
        if (items.size() == 0) {
            items.add("А");
            items.add("мА");
            AChoice.setItems(items);
            AChoice.setValue(items.getFirst());
            items = OMChoice.getItems();
        }
        if (items.size() == 0) {
            items.add("Ом");
            items.add("кОм");
            items.add("МОм");
            OMChoice.setItems(items);
            OMChoice.setValue(items.getFirst());
        }

    }

    @FXML
    private void onResistorsCalcButtonClick() throws IOException {
        OmaCalc.setVisible(false);
        ResistorsCalc.setVisible(true);
        OperationsHistory.setVisible(false);


    }

    @FXML
    private void onOperationsHistoryButtonClick() throws IOException {
        OmaCalc.setVisible(false);
        ResistorsCalc.setVisible(false);
        OperationsHistory.setVisible(true);

        data = FXCollections.observableArrayList();

        data.clear();
        HistoryTable.getColumns().clear();

        // Создаем колонки
        TableColumn<TableModel, String> loginColumn = new TableColumn<>("Логин");
        loginColumn.setCellValueFactory(new PropertyValueFactory<>("login"));

        TableColumn<TableModel, String> operationColumn = new TableColumn<>("Операция");
        operationColumn.setCellValueFactory(new PropertyValueFactory<>("operation"));

        TableColumn<TableModel, String> inputColumn = new TableColumn<>("Входные данные");
        inputColumn.setCellValueFactory(new PropertyValueFactory<>("input"));

        TableColumn<TableModel, String> outputColumn = new TableColumn<>("Результат");
        outputColumn.setCellValueFactory(new PropertyValueFactory<>("output"));

        TableColumn<TableModel, String> datetimeColumn = new TableColumn<>("Время выполнения");
        datetimeColumn.setCellValueFactory(new PropertyValueFactory<>("datetime"));

        HistoryTable.getColumns().addAll(loginColumn, operationColumn, inputColumn, outputColumn, datetimeColumn);

        ResultSet rs;
        if (SQLManager.SQLQuerySelectReturner("SELECT role FROM " + SQLManager.schemaname +".users WHERE login = '"+userLogin+"'") == "admin"){
            rs = SQLManager.SQLQueryRowSelect(String.format("""
                SELECT
                    u.login as login,
                    o.operation_type,
                    o.input_data,
                    o.result,
                    o.created_at
                FROM %s.operations o
                INNER JOIN %s.users u ON o.user_id = u.id
                WHERE u.login = '%s';
                """, SQLManager.schemaname, SQLManager.schemaname, userLogin));
            if (rs == null) return;
        }
        else {
            rs = SQLManager.SQLQueryRowSelect(String.format("""
                SELECT
                    u.login as login,
                    o.operation_type,
                    o.input_data,
                    o.result,
                    o.created_at
                FROM %s.operations o
                INNER JOIN %s.users u ON o.user_id = u.id;
                """, SQLManager.schemaname, SQLManager.schemaname));
            if (rs == null) return;
        }


        try {
            do {
                String login = rs.getString("login");
                String operation = rs.getString("operation_type");
                String input = rs.getString("input_data");
                String output = rs.getString("result");
                String datetime = rs.getString("created_at");

                data.add(new TableModel(login, operation, input, output, datetime));
            } while (rs.next());

            HistoryTable.setItems(data);

        } catch (SQLException e) {
            e.printStackTrace();
        } finally {
            try {
                if (rs != null) {
                    rs.getStatement().close();
                }
            } catch (SQLException e) {
                e.printStackTrace();
            }
        }
    }

    @FXML
    private void onUpdateButtonClick() throws IOException {
        onOperationsHistoryButtonClick();
        searchField.setText("");
    }

    @FXML
    private void onSearchButtonClick() throws IOException {
        FilteredList<TableModel> filteredData = new FilteredList<>(data, p -> true);
        filteredData.setPredicate(TableModel -> {
            if (searchField == null || searchField.getText().isEmpty()) {
                return true;
            }

            String lowerCaseFilter = searchField.getText().toLowerCase(); 

            if (TableModel.getLogin().toLowerCase().contains(lowerCaseFilter)) {
                return true;
            } else if (TableModel.getOperation().toLowerCase().contains(lowerCaseFilter)) {
                return true;
            } else if (TableModel.getInput().toLowerCase().contains(lowerCaseFilter)) {
                return true;
            } else if (TableModel.getOutput().toLowerCase().contains(lowerCaseFilter)) {
                return true;
            } else if (TableModel.getDatetime().toLowerCase().contains(lowerCaseFilter)) {
                return true;
            }

            return false; // No match
        });
        HistoryTable.setItems(filteredData); // Or tableView.setItems(sortedData);

    }


    @FXML
    private void onClearButtonClick() throws IOException {
        VField.clear();
        AField.clear();
        OMField.clear();
        VChoice.setValue(VChoice.getItems().getFirst());
        AChoice.setValue(AChoice.getItems().getFirst());
        OMChoice.setValue(OMChoice.getItems().getFirst());

    }



    @FXML
    private void onProcessButtonClick() throws IOException {
        String Vtext = VField.getText();
        String Atext = AField.getText();
        String OMtext = OMField.getText();

        if (Vtext.isEmpty() && !Atext.isEmpty() && !OMtext.isEmpty()) {
            Vtext = CalcProcesses.VCalc(OMtext, Atext);
            VField.setText(Vtext);
            SQLManager.SQLQueryCreate(String.format("""
                    INSERT INTO %s.operations (user_id, operation_type, input_data, result)
                    SELECT
                        u.id,
                        '%s',
                        '%s',
                        '%s'
                    FROM %s.users u
                    WHERE u.login = '%s';
                    """,
                    SQLManager.schemaname,
                    "Калькулятор по закону Ома",
                    "{R: " + OMtext +", I: " + Atext + "}",
                    "{U: " + Vtext + "}",
                    SQLManager.schemaname,
                    userLogin));

        } else if (!Vtext.isEmpty() && Atext.isEmpty() && !OMtext.isEmpty() && Double.parseDouble(OMtext) != 0) {
            Atext = CalcProcesses.ACalc(Vtext, OMtext);
            AField.setText(Atext);
            SQLManager.SQLQueryCreate(String.format("""
                    INSERT INTO %s.operations (user_id, operation_type, input_data, result)
                    SELECT
                        u.id,
                        '%s',
                        '%s',
                        '%s'
                    FROM %s.users u
                    WHERE u.login = '%s';
                    """,
                    SQLManager.schemaname,
                    "Калькулятор по закону Ома",
                    "{U: " + Vtext +", R: " + OMtext + "}",
                    "{I: " + Atext + "}",
                    SQLManager.schemaname,
                    userLogin));

        } else if (!Vtext.isEmpty() && !Atext.isEmpty() && OMtext.isEmpty() && Double.parseDouble(Atext) != 0) {
            OMtext = CalcProcesses.OMCalc(Vtext, Atext);
            OMField.setText(OMtext);
            SQLManager.SQLQueryCreate(String.format("""
                    INSERT INTO %s.operations (user_id, operation_type, input_data, result)
                    SELECT
                        u.id,
                        '%s',
                        '%s',
                        '%s'
                    FROM %s.users u
                    WHERE u.login = '%s';
                    """,
                    SQLManager.schemaname,
                    "Калькулятор по закону Ома",
                    "{U: " + Vtext +", I: " + Atext + "}",
                    "{R: " + OMtext + "}",
                    SQLManager.schemaname,
                    userLogin));
        }
        else {

        }

    }





}