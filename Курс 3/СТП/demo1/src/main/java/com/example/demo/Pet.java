package com.example.demo;
import jakarta.persistence.*;

@Entity
@Table(name = "pets")
public class Pet {

    @Id
    @GeneratedValue(strategy = GenerationType.AUTO)
    @Column(name = "id")
    private long id;

    @Column(name = "owner_name")
    private String owner_name;

    @Column(name = "petname")
    private String surname;

    @Column(name = "species")
    private String species;

    public long getId() {
        return id;
    }

    public void setId(long id) {
        this.id = id;
    }

    public String getOwner_name() {
        return owner_name;
    }

    public void setOwner_name(String name) {
        this.owner_name = name;
    }

    public String getPetname() {
        return surname;
    }

    public void setPetname(String surname) {
        this.surname = surname;
    }

    public String getSpecies() {
        return species;
    }

    public void setSpecies(String species) {
        this.species = species;
    }


}
