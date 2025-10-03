package com.example.demo;

import jakarta.annotation.PostConstruct;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Component;

@Component
public class AppInitializer {
    @Autowired
    private PetService petService;

    @PostConstruct
    void init() {
        if (petService.isEmpty())
        {
            Pet pet = new Pet();
            pet.setOwner_name("Alex");
            pet.setPetname("Murzik");
            pet.setSpecies("Siberian cat");
            petService.addPet(pet);
        }
    }
}
