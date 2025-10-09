package com.example.demo;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.ModelAttribute;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;

@Controller
public class PetController {
    @Autowired
    private PetService petService;

    @GetMapping("/")
    String index(Model model) {
        model.addAttribute("pets", petService.getAllPets());
        model.addAttribute("pet", new Pet());
        return "index";
    }

    @GetMapping("/delete/{id}")
    public String deletePet(@PathVariable long id) {
        petService.deletePet(id);
        return "redirect:/";
    }

    @GetMapping("/add")
    public String addPet(Model model) {
        Pet pet = new Pet();
        pet.setOwner_name("Alex");
        pet.setPetname("Murzik");
        pet.setSpecies("Cat");
        petService.addPet(pet);
        model.addAttribute("pets", petService.getAllPets());
        model.addAttribute("pet", petService.getPetById(pet.getId()));
        model.addAttribute("updatingId", pet.getId());
        return "index";
    }

    @GetMapping("/edit/{id}")
    public String editPet(@PathVariable long id, Model model) {
        model.addAttribute("pets", petService.getAllPets());
        model.addAttribute("pet", petService.getPetById(id));
        model.addAttribute("updatingId", id);
        return "index";
    }

    @PostMapping("/save")
    public String savePet(@ModelAttribute Pet pet) {
        petService.addPet(pet);
        return "redirect:/";
    }
}
