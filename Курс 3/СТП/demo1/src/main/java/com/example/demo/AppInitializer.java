package com.example.demo;

import jakarta.annotation.PostConstruct;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Component;

@Component
public class AppInitializer {
    @Autowired
    private StudentService studentService;

    @PostConstruct
    void init() {
        if (studentService.isEmpty())
        {
            Student student = new Student();
            student.setName("Alex");
            student.setSurname("Mas");
            studentService.addStudent(student);
        }
    }
}
