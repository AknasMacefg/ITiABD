package com.example.demo.services;
import com.example.demo.models.User;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import com.example.demo.repositories.UserRepository;

import java.util.*;

@Service
public class UserService {
    private static final Logger log = LoggerFactory.getLogger(UserService.class);
    @Autowired
    private UserRepository userRepository;
    public List<User> getAllPets()
    {
        return userRepository.findAll();
    }

    public User getUserById(long id) {
        return userRepository.findById(id).get();
    }
    public boolean isEmpty(){
        return userRepository.count() == 0;
    }


    public void deletePet(Long petId) {
        userRepository.delete(userRepository.findById(petId).get());
    }

    public void addPet(User user) {
        System.out.println(user.getId());
        userRepository.save(user);
    }
}
