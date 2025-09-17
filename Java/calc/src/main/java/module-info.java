module org.calc.calc {
    requires javafx.controls;
    requires javafx.fxml;
    requires javafx.web;

    requires org.controlsfx.controls;
    requires com.dlsc.formsfx;
    requires net.synedra.validatorfx;
    requires org.kordamp.ikonli.javafx;
    requires org.kordamp.bootstrapfx.core;
    requires eu.hansolo.tilesfx;
    requires com.almasb.fxgl.all;
    requires org.apache.poi.ooxml;
    requires spring.security.crypto;
    requires com.fasterxml.jackson.databind;
    requires java.sql;

    opens org.calc.calc to javafx.fxml;
    exports org.calc.calc;
}