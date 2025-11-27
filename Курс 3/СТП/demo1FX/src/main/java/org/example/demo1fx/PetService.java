package org.example.demo1fx;

import org.example.demo1fx.Pet;
import com.fasterxml.jackson.core.type.TypeReference;
import com.fasterxml.jackson.databind.ObjectMapper;
import org.springframework.http.*;
import org.springframework.web.client.RestTemplate;

import java.util.Arrays;
import java.util.Collections;
import java.util.List;

public class PetService {
    private static final String API_URL = "http://localhost:8080/api/pets";
    private final RestTemplate restTemplate;
    private final ObjectMapper objectMapper;

    public PetService() {
        this.restTemplate = new RestTemplate();
        this.objectMapper = new ObjectMapper();
    }

    public List<Pet> getAllPets() {
        try {
            ResponseEntity<Pet[]> response = restTemplate.getForEntity(API_URL, Pet[].class);
            if (response.getStatusCode() == HttpStatus.OK && response.getBody() != null) {
                List<Pet> pets = Arrays.asList(response.getBody());
                return pets;
            }
            return Collections.emptyList();

        } catch (Exception e) {
            System.err.println("Error fetching pets: " + e.getMessage());
            e.printStackTrace();
            return Collections.emptyList();
        }
    }

    public Pet createPet(Pet pet) {
        try {
            HttpHeaders headers = new HttpHeaders();
            headers.setContentType(MediaType.APPLICATION_JSON);
            HttpEntity<Pet> request = new HttpEntity<>(pet, headers);

            // Отправляем POST запрос и получаем ответ с созданным объектом (включая ID)
            ResponseEntity<Pet> response = restTemplate.postForEntity(API_URL, request, Pet.class);

            if (response.getStatusCode() == HttpStatus.CREATED || response.getStatusCode() == HttpStatus.OK) {
                Pet createdPet = response.getBody();
                return createdPet;
            } else {
                System.err.println("Unexpected response status: " + response.getStatusCode());
                return null;
            }

        } catch (Exception e) {
            System.err.println("Error creating pet: " + e.getMessage());
            e.printStackTrace();
            return null;
        }
    }

    public boolean updatePet(Pet pet) {
        try {
            HttpHeaders headers = new HttpHeaders();
            headers.setContentType(MediaType.APPLICATION_JSON);
            HttpEntity<Pet> request = new HttpEntity<>(pet, headers);

            restTemplate.put(API_URL + "/" + pet.getId(), request);
            return true;

        } catch (Exception e) {
            System.err.println("Error updating pet: " + e.getMessage());
            e.printStackTrace();
            return false;
        }
    }

    public boolean deletePet(Long id) {
        try {
            restTemplate.delete(API_URL + "/" + id);
            return true;
        } catch (Exception e) {
            System.err.println("Error deleting pet: " + e.getMessage());
            e.printStackTrace();
            return false;
        }
    }
}