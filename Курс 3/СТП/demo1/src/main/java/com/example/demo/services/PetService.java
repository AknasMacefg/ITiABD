package com.example.demo.services;

import com.example.demo.models.Pet;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import com.example.demo.repositories.PetRepository;

import java.util.*;

@Service
public class PetService {
    private static final Logger log = LoggerFactory.getLogger(PetService.class);
    @Autowired
    private PetRepository petRepository;
    public List<Pet> getAllPets()
    {

        return petRepository.findAll();
    }

    public Pet getPetById(long id) {
        return petRepository.findById(id).get();
    }
    public boolean isEmpty(){
        return petRepository.count() == 0;
    }


    public void deletePet(Long petId) {
        petRepository.delete(petRepository.findById(petId).get());
    }

    public void addPet(Pet pet) {
        System.out.println(pet.getId() + " " + pet.getOwner_name());
        petRepository.save(pet);
    }
}
