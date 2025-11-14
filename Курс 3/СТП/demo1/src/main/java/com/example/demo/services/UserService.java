package com.example.demo.services;
import com.example.demo.models.User;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.security.crypto.bcrypt.BCryptPasswordEncoder;
import org.springframework.stereotype.Service;
import com.example.demo.repositories.UserRepository;
import org.springframework.security.crypto.password.PasswordEncoder;

import java.util.*;

@Service
public class UserService {
    private static final Logger log = LoggerFactory.getLogger(UserService.class);
    @Autowired
    private UserRepository userRepository;

    @Autowired
    private final PasswordEncoder passwordEncoder = new BCryptPasswordEncoder();

    public List<User> getAllUsers()
    {
        return userRepository.findAll();
    }

    public User getUserById(long id) {
        return userRepository.findById(id).get();
    }
    public boolean existsUserByEmail (String email) { return userRepository.existsByEmail(email); }
    public boolean isEmpty(){
        return userRepository.count() == 0;
    }
    public boolean register(User user) {
        if (user == null || user.getEmail() == null) {
            return false;
        }
        if (userRepository.existsByEmail(user.getEmail())) {
            return false;
        }
        // Шифруем сырой пароль перед сохранением
        if (user.getPassword() != null && !user.getPassword().isBlank()) {
            user.setPassword(passwordEncoder.encode(user.getPassword()));
        }
        userRepository.save(user);
        return true;
    }


    public void deleteUser(Long petId) {
        userRepository.delete(userRepository.findById(petId).get());
    }

    public void addUser(User user) {
        System.out.println(user.getId());
        userRepository.save(user);
    }
}
