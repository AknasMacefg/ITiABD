package org.example.demo1fx;

import com.fasterxml.jackson.annotation.JsonProperty;

public class Pet {
    private Long id;

    @JsonProperty("owner_name")
    private String ownerName;

    @JsonProperty("petname")
    private String petName;

    private String species;

    public Pet() {}

    public Pet(String ownerName, String petName, String species) {
        this.ownerName = ownerName;
        this.petName = petName;
        this.species = species;
    }

    // Геттеры и сеттеры
    public Long getId() { return id; }
    public void setId(Long id) { this.id = id; }

    public String getOwnerName() { return ownerName; }
    public void setOwnerName(String ownerName) { this.ownerName = ownerName; }

    public String getPetName() { return petName; }
    public void setPetName(String petName) { this.petName = petName; }

    public String getSpecies() { return species; }
    public void setSpecies(String species) { this.species = species; }

    @Override
    public String toString() {
        return String.format("Pet{id=%d, ownerName='%s', petName='%s', species='%s'}",
                id, ownerName, petName, species);
    }
}