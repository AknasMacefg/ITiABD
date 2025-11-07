package com.example.demo.config;

import jakarta.annotation.PostConstruct;
import com.example.demo.models.Pet;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.security.crypto.password.PasswordEncoder;
import org.springframework.stereotype.Component;
import com.example.demo.services.PetService;
import com.example.demo.services.UserService;


@Component
public class AppInitializer {
    @Autowired
    private PetService petService;


    /** Репозиторий пользователей. */
    @Autowired
    private UserRepository userRepository;

    /** Кодировщик паролей, используемый для безопасного хранения паролей. */
    @Autowired
    private PasswordEncoder passwordEncoder;

    /**
     * Метод, автоматически вызываемый после создания компонента Spring.
     * <p>
     * Проверяет наличие базовых пользователей и студентов, добавляя их при необходимости.
     * </p>
     */
    @PostConstruct
    public void init() {
        createUserIfNotExists("superadmin@example.com", "password", Role.SUPER_ADMIN);
        createUserIfNotExists("admin@example.com", "password", Role.ADMIN);
        createUserIfNotExists("user@example.com", "password", Role.USER);
        createStudentsIfEmpty();
    }

    /**
     * Создаёт пользователя с указанным email, паролем и ролью, если пользователь с таким email ещё не существует.
     * <p>
     * Пароль шифруется с использованием {@link PasswordEncoder}.
     * </p>
     *
     * @param email       адрес электронной почты пользователя
     * @param rawPassword исходный (нешифрованный) пароль
     * @param role        роль пользователя (например, {@link Role#ADMIN})
     */
    private void createUserIfNotExists(String email, String rawPassword, Role role) {
        if (!userRepository.existsByEmail(email)) {
            User user = new User();
            user.setEmail(email);
            user.setPassword(passwordEncoder.encode(rawPassword));
            user.setRole(role);
            userRepository.save(user);
            System.out.println("Создан пользователь " + role + ": " + email);
        }
    }

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
