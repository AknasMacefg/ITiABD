package com.example.demo;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.util.*;

@Service
public class PetService {
    @Autowired
    private PetRepository petRepository;
    List<Pet> getAllPets()
    {
        return petRepository.findAll();
    }
    boolean isEmpty(){
        return petRepository.count() == 0;
    }

    public void addPet(Pet student) {
        petRepository.save(student);
    }
}
