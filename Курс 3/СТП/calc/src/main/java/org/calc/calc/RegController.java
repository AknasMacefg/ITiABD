package org.calc.calc;

import javafx.fxml.FXML;
import javafx.scene.control.Label;
import javafx.scene.control.TextField;
import javafx.stage.Stage;
import javafx.stage.Window;
import java.io.IOException;
import javafx.scene.control.Button;
import org.springframework.security.crypto.bcrypt.BCryptPasswordEncoder;
import java.util.Locale;
import org.apache.commons.validator.routines.EmailValidator;

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
    private Label warningLabel;



    @FXML
    private void onRegButtonClick() throws IOException {

        if (!NameField.getText().isEmpty() && !LoginField.getText().isEmpty() && !EmailField.getText().isEmpty() && !PassField.getText().isEmpty() && !RPassField.getText().isEmpty()) {
            if (PassField.getText().equals(RPassField.getText())) {
                if (PassField.getText().length() > 6) {
                    if (SQLManager.SQLQuerySelectReturner(String.format("""
                            SELECT login
                            FROM %s.users
                            WHERE login = '%s' 
         
                            """, SQLManager.schemaname, LoginField.getText())).isEmpty())
                    {
                        if (SQLManager.SQLQuerySelectReturner(String.format("""
                            SELECT email
                            FROM %s.users
                            WHERE email = '%s' 
         
                            """, SQLManager.schemaname, EmailField.getText())).isEmpty()) {
                            if (EmailValidator.getInstance().isValid(EmailField.getText())) {
                                final BCryptPasswordEncoder passEncoder = new BCryptPasswordEncoder();
                                String PassHash = passEncoder.encode(PassField.getText());

                                String query = String.format(Locale.US, "INSERT INTO %s.%s (name, email, login, hash_password) " +
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
                                warningLabel.setVisible(false);
                            }
                            else {
                                warningLabel.setVisible(true);
                                warningLabel.setText("Неправильный формат электронной почты!");
                            }

                        }
                        else {
                            warningLabel.setVisible(true);
                            warningLabel.setText("Данная электронная почта уже зарегистрирована!");
                        }
                    }
                    else {
                        warningLabel.setVisible(true);
                        warningLabel.setText("Данный логин уже занят!");
                    }

                }
                else {
                    warningLabel.setVisible(true);
                    warningLabel.setText("Пароль должен быть длинее 6 символов!");
                }

            }
            else {
                warningLabel.setVisible(true);
                warningLabel.setText("Пароли не совпадают!");
            }
        }
        else {
            warningLabel.setVisible(true);
            warningLabel.setText("Не все поля заполнены!");
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