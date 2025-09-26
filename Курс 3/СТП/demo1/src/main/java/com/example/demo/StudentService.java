package com.example.demo;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.util.*;

@Service
public class StudentService {
    @Autowired
    private StudentRepository studentRepository;
    List<Student> getAllStudents()
    {
        return studentRepository.findAll();
    }
    boolean isEmpty(){
        return studentRepository.count() == 0;
    }

    public void addStudent(Student student) {
        studentRepository.save(student);
    }
}
