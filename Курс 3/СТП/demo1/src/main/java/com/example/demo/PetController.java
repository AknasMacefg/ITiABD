package com.example.demo;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;

import java.time.LocalDateTime;

@Controller
public class PetController {
    @Autowired
    private PetService petService;

    @GetMapping("/")
    String index(Model model){
        model.addAttribute("today", LocalDateTime.now().getDayOfWeek());
        model.addAttribute("pets", petService.getAllPets());
        model.addAttribute("changePet", new Pet());
        return "index";
    }

    @GetMapping("/delete/{id}")
    public String deletePet(@PathVariable long id) {
        petService.deletePet(id);
        return "redirect:/";
    }

    @GetMapping("/add")
    public String addPet() {
        Pet pet = new Pet();
        pet.setOwner_name("Alex");
        pet.setPetname("Murzik");
        pet.setSpecies("Siberian cat");
        petService.addPet(pet);
        return "redirect:/";
    }

    @GetMapping("/update/{id}")
    public String addPet(@PathVariable long id, String owner_name, String petname, String species) {
        petService.updatePet(id, owner_name, petname, species);
        return "redirect:/";
    }

}
