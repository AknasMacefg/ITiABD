package org.calc.calc;

import com.fasterxml.jackson.databind.JsonSerializer;
import javafx.collections.FXCollections;
import javafx.collections.ObservableList;
import javafx.fxml.FXML;
import javafx.scene.control.ChoiceBox;
import javafx.scene.control.PasswordField;
import javafx.scene.control.TextField;
import javafx.scene.layout.AnchorPane;
import javafx.stage.Stage;
import javafx.stage.Window;
import java.io.IOException;
import javafx.scene.control.Button;
import org.springframework.security.crypto.bcrypt.BCryptPasswordEncoder;
import javafx.beans.value.ChangeListener;
import javafx.beans.value.ObservableValue;

import java.util.Dictionary;
import java.util.HashMap;
import java.util.Locale;
import java.util.Map;

public class MainController {
   static public String userLogin;


    @FXML
    private Button ExitButton;

    @FXML
    private Button OmaCalcButton;

    @FXML
    private Button ResistorsCalcButton;

    @FXML
    private Button OperationsHistoryButton;

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