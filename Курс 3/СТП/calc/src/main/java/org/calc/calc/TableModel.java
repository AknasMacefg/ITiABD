package org.calc.calc;

import javafx.beans.property.SimpleStringProperty;
import javafx.beans.property.StringProperty;

/**
 * Модель строки таблицы истории операций.
 *
 * <p>Содержит данные о пользователе, типе операции, входных и выходных данных,
 * а также времени выполнения операции. Используется в {@link javafx.scene.control.TableView}
 * для привязки к столбцам и отображения истории.</p>
 */
public class TableModel {
    /** Логин пользователя, выполнившего операцию. */
    private final StringProperty login;
    /** Тип операции (закон Ома, делитель напряжения и т.п.). */
    private final StringProperty operation;
    /** Входные данные операции в текстовом виде. */
    private final StringProperty input;
    /** Результат операции. */
    private final StringProperty output;
    /** Дата и время выполнения операции. */
    private final StringProperty datetime;

    /**
     * Создаёт модель строки истории операций.
     *
     * @param login    логин пользователя
     * @param operation тип операции
     * @param input    входные данные
     * @param output   результат операции
     * @param datetime дата и время выполнения
     */
    public TableModel(String login, String operation, String input, String output, String datetime) {
        this.login= new SimpleStringProperty(login);
        this.operation = new SimpleStringProperty(operation);
        this.input = new SimpleStringProperty(input);
        this.output = new SimpleStringProperty(output);
        this.datetime = new SimpleStringProperty(datetime);
    }

    /**
     * Возвращает логин пользователя.
     *
     * @return логин
     */
    public String getLogin() { return login.get(); }

    /**
     * Свойство логина для привязки к столбцу таблицы.
     *
     * @return свойство логина
     */
    public StringProperty loginProperty() { return login; }

    /**
     * Возвращает тип операции.
     *
     * @return тип операции
     */
    public String getOperation() { return operation.get(); }

    /**
     * Свойство типа операции для привязки к столбцу таблицы.
     *
     * @return свойство операции
     */
    public StringProperty operationProperty() { return operation; }

    /**
     * Возвращает входные данные операции.
     *
     * @return входные данные
     */
    public String getInput() { return input.get(); }

    /**
     * Свойство входных данных для привязки к столбцу таблицы.
     *
     * @return свойство входных данных
     */
    public StringProperty inputProperty() { return input; }

    /**
     * Возвращает результат операции.
     *
     * @return результат
     */
    public String getOutput() { return output.get(); }

    /**
     * Свойство результата для привязки к столбцу таблицы.
     *
     * @return свойство результата
     */
    public StringProperty outputProperty() { return output; }

    /**
     * Возвращает дату и время выполнения операции.
     *
     * @return дата и время
     */
    public String getDatetime() { return datetime.get(); }

    /**
     * Свойство даты и времени для привязки к столбцу таблицы.
     *
     * @return свойство даты и времени
     */
    public StringProperty datetimeProperty() { return datetime; }
}
