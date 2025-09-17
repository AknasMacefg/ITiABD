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

public class MainController {
   static public String userLogin;


    @FXML
    private Button ExitButton;


    @FXML
    private void onExitButtonClick() throws IOException {
        Window window = ExitButton.getScene().getWindow();
        if (window instanceof Stage) {
            CalcApplication.window_swap("login-view.fxml", (Stage) window, "Вход");
            userLogin = null;
        }
    }


}