module org.example.demo1fx {
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
    requires spring.web;
    requires com.fasterxml.jackson.databind;
    requires javafx.base;

    opens org.example.demo1fx to javafx.fxml;
    exports org.example.demo1fx;
}