package org.calc.calc;

import javafx.application.Application;
import javafx.fxml.FXMLLoader;
import javafx.scene.Scene;
import javafx.stage.Stage;

import java.io.IOException;


public class CalcApplication extends Application {

    @Override
    public void start(Stage stage) throws IOException {
        new SQLManager();
        FXMLLoader fxmlLoader = new FXMLLoader(CalcApplication.class.getResource("login-view.fxml"));
        Scene scene = new Scene(fxmlLoader.load());
        stage.setResizable(false);
        stage.setTitle("Вход");
        stage.setScene(scene);
        stage.show();


    }

    static void window_swap(String name, Stage stage, String titleName) throws IOException {
        FXMLLoader fxmlLoader = new FXMLLoader(CalcApplication.class.getResource(name));
        Scene scene = new Scene(fxmlLoader.load());
        stage.setScene(scene);
        stage.setTitle(titleName);
        stage.centerOnScreen();
        stage.show();
    }

    public static void main(String[] args) {
        launch();
    }
}