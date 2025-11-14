package com.example.demo.services;

import com.example.demo.models.Role;
import com.example.demo.models.User;
import com.example.demo.repositories.UserRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.security.core.GrantedAuthority;
import org.springframework.security.core.authority.SimpleGrantedAuthority;
import org.springframework.security.core.userdetails.UserDetails;
import org.springframework.security.core.userdetails.UserDetailsService;
import org.springframework.security.core.userdetails.UsernameNotFoundException;
import org.springframework.stereotype.Service;

import java.util.Collection;
import java.util.List;

/**
 * Сервис, реализующий интерфейс {@link UserDetailsService} для интеграции со Spring Security.
 * <p>
 * Отвечает за поиск пользователя в базе данных и преобразование его ролей
 * в полномочия (authorities), необходимые для механизма аутентификации Spring Security.
 * </p>
 */
@Service
public class CustomUserDetailsService implements UserDetailsService {

    /** Репозиторий пользователей, используемый для поиска по email. */
    @Autowired
    private UserRepository userRepository;

    /**
     * Загружает пользователя по имени пользователя (обычно email), переданному при аутентификации.
     * <p>
     * Метод выполняет поиск в базе данных и, если пользователь найден, возвращает объект
     * {@link UserDetails},
     * содержащий email, пароль и набор полномочий.
     * </p>
     *
     * @param username имя пользователя или адрес электронной почты
     * @return объект {@link UserDetails}, необходимый для аутентификации
     * @throws UsernameNotFoundException если пользователь с данным именем не найден
     */
    @Override
    public UserDetails loadUserByUsername(String username) throws UsernameNotFoundException {
        User u = userRepository.findByEmail(username)
                .orElseThrow(() -> new UsernameNotFoundException("User not found: " + username));

        return org.springframework.security.core.userdetails.User
                .withUsername(u.getEmail())
                .password(u.getPassword())
                .authorities(toAuthorities(u.getRole()))
                .accountLocked(false)
                .disabled(false)
                .build();
    }

    /**
     * Преобразует роль пользователя из доменной модели {@link Role}
     * в коллекцию полномочий (authorities) Spring Security.
     *
     * @param role роль пользователя
     * @return коллекция объектов {@link GrantedAuthority}, описывающих права пользователя
     */
    private Collection<? extends GrantedAuthority> toAuthorities(Role role) {
        return List.of(new SimpleGrantedAuthority("ROLE_" + role.name()));
    }
}
