package org.calc.calc;

import com.fasterxml.jackson.databind.JsonSerializer;
import javafx.fxml.FXML;
import javafx.scene.control.PasswordField;
import javafx.scene.control.TextField;
import javafx.stage.Stage;
import javafx.stage.Window;
import java.io.IOException;
import javafx.scene.control.Button;
import org.springframework.security.crypto.bcrypt.BCryptPasswordEncoder;
import javafx.beans.value.ChangeListener;
import javafx.beans.value.ObservableValue;
import java.util.Locale;

public class RegController {


    @FXML
    private TextField LoginField;

    @FXML
    private TextField NameField;

    @FXML
    private TextField EmailField;

    @FXML
    private javafx.scene.control.PasswordField PassField;

    @FXML
    private javafx.scene.control.PasswordField RPassField;

    @FXML
    private Button BackButton;



    @FXML
    private void onRegButtonClick() throws IOException {

        if (!NameField.getText().isEmpty() && !LoginField.getText().isEmpty() && !EmailField.getText().isEmpty() && !PassField.getText().isEmpty() && !RPassField.getText().isEmpty()) {
            if (PassField.getText().equals(RPassField.getText())) {
                final BCryptPasswordEncoder passEncoder = new BCryptPasswordEncoder();
                String PassHash = passEncoder.encode(PassField.getText());

                String query = String.format(Locale.US,"INSERT INTO %s.%s (name, email, login, hash_password) " +
                                "VALUES ('%s', '%s', '%s', '%s')",
                        SQLManager.schemaname,
                        "users",
                        NameField.getText(),
                        EmailField.getText(),
                        LoginField.getText(),
                        PassHash
                );

                SQLManager.SQLQueryCreate(query);
                onBackButtonClick();
            }
        }



    }

    @FXML
    private void onBackButtonClick() throws IOException {
        Window window = BackButton.getScene().getWindow();
        if (window instanceof Stage) {
            CalcApplication.window_swap("login-view.fxml", (Stage) window, "Вход");
        }
    }


}