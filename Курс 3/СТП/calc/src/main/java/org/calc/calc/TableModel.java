package org.calc.calc;

import javafx.beans.property.SimpleStringProperty;
import javafx.beans.property.StringProperty;

public class TableModel {
    private final StringProperty login;
    private final StringProperty operation;
    private final StringProperty input;
    private final StringProperty output;
    private final StringProperty datetime;

    public TableModel(String login, String operation, String input, String output, String datetime) {
        this.login= new SimpleStringProperty(login);
        this.operation = new SimpleStringProperty(operation);
        this.input = new SimpleStringProperty(input);
        this.output = new SimpleStringProperty(output);
        this.datetime = new SimpleStringProperty(datetime);
    }


    public String getLogin() { return login.get(); }
    public StringProperty loginProperty() { return login; }

    public String getOperation() { return operation.get(); }
    public StringProperty operationProperty() { return operation; }

    public String getInput() { return input.get(); }
    public StringProperty inputProperty() { return input; }

    public String getOutput() { return output.get(); }
    public StringProperty outputProperty() { return output; }

    public String getDatetime() { return datetime.get(); }
    public StringProperty datetimeProperty() { return datetime; }
}
