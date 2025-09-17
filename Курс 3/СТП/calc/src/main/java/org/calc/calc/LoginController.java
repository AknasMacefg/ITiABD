package org.calc.calc;

import javafx.fxml.FXML;
import javafx.scene.control.Hyperlink;
import javafx.scene.control.TextField;
import javafx.stage.Stage;
import javafx.stage.Window;
import javafx.scene.control.Button;
import org.springframework.security.crypto.bcrypt.BCryptPasswordEncoder;

import java.io.IOException;

public class LoginController {
    @FXML
    private TextField LoginField;

    @FXML
    private TextField PassField;

    @FXML
    private Hyperlink RegLink;

    @FXML
    private Button LoginButton;

    @FXML
    protected void onLoginButtonClick() throws IOException {

        if (!LoginField.getText().isEmpty() && !PassField.getText().isEmpty()){
            String login = SQLManager.SQLQuerySelectReturner("SELECT login FROM "+ SQLManager.schemaname + ".users WHERE login = '" + LoginField.getText() + "'");
            String hashedPass = SQLManager.SQLQuerySelectReturner("SELECT hash_password FROM "+SQLManager.schemaname + ".users WHERE login = '" + LoginField.getText()+ "'");
            final BCryptPasswordEncoder passEncoder = new BCryptPasswordEncoder();
            if (!login.isEmpty() && passEncoder.matches(PassField.getText(), hashedPass)) {
                Window window = LoginButton.getScene().getWindow();
                if (window instanceof Stage) {
                    CalcApplication.window_swap("main-view.fxml", (Stage) window, "Калькулятор");
                    MainController.userLogin = login;
                }

            }
        }
    }
    @FXML
    protected void onRegLinkClick() throws IOException {

        Window window = RegLink.getScene().getWindow();
        if (window instanceof Stage) {
            CalcApplication.window_swap("reg-view.fxml", (Stage) window, "Регистрация");
        }
    }


}