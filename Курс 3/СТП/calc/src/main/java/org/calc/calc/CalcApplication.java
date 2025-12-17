package org.calc.calc;

import javafx.application.Application;
import javafx.fxml.FXMLLoader;
import javafx.scene.Scene;
import javafx.stage.Stage;

import java.io.IOException;

/**
 * Главный класс приложения для расчетов по закону Ома и делителю напряжения.
 * 
 * <p>Приложение предоставляет графический интерфейс для:
 * <ul>
 *   <li>Расчетов по закону Ома (напряжение, ток, сопротивление)</li>
 *   <li>Поиска оптимальных комбинаций резисторов для делителя напряжения</li>
 *   <li>Просмотра истории операций</li>
 * </ul>
 * 
 * <p>Приложение использует JavaFX для графического интерфейса и PostgreSQL
 * для хранения данных пользователей и истории операций.
 * 
 * @author calc
 * @version 1.0
 */
public class CalcApplication extends Application {

    /**
     * Инициализирует и отображает главное окно приложения.
     * Создает подключение к базе данных и загружает форму входа.
     * 
     * @param stage главное окно приложения
     * @throws IOException если не удалось загрузить FXML файл
     */
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

    /**
     * Переключает отображаемое окно приложения.
     * Загружает указанный FXML файл и отображает его в текущем окне.
     * 
     * @param name имя FXML файла для загрузки
     * @param stage окно для отображения новой сцены
     * @param titleName заголовок окна
     * @throws IOException если не удалось загрузить FXML файл
     */
    static void window_swap(String name, Stage stage, String titleName) throws IOException {
        FXMLLoader fxmlLoader = new FXMLLoader(CalcApplication.class.getResource(name));
        Scene scene = new Scene(fxmlLoader.load());
        stage.setScene(scene);
        stage.setTitle(titleName);
        stage.centerOnScreen();
        stage.show();
    }

    @Override
    public void stop() throws Exception {
        if (SQLManager.conn != null && !SQLManager.conn.isClosed()) {
            SQLManager.conn.close();
            System.out.println("Подключение закрыто.");
        }
        super.stop();
    }


    public static void main(String[] args) {
        launch();
    }
}