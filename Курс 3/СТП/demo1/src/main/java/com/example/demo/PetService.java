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

    public void deletePet(Long petId) {
        petRepository.delete(petRepository.findById(petId).get());
    }

    public void addPet(Pet pet) {
        petRepository.save(pet);
    }

    public void updatePet(long petId, String owner_name, String petname, String species) {
        Pet pet = petRepository.findById(petId).get();
        pet.setOwner_name(owner_name);
        pet.setPetname(petname);
        pet.setSpecies(species);
        petRepository.save(pet);
    }
}
