package com.example.demo;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.GetMapping;

import java.time.LocalDateTime;

@Controller
public class PetController {
    @Autowired
    private PetService petService;

    @GetMapping("/")
    String index(Model model){
        model.addAttribute("today", LocalDateTime.now().getDayOfWeek());
        model.addAttribute("pets", petService.getAllPets());
        return "index";
    }
}
