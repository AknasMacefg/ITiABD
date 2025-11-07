package com.example.demo.models;

import jakarta.persistence.*;

/**
 * Сущность пользователя приложения.
 * <p>
 * Каждый пользователь имеет адрес электронной почты, пароль и связанную роль {@link Role}.
 * Используется для аутентификации и авторизации на основе ролей в системе.
 * </p>sa
 */
@Entity
@Table(name = "users")
public class User {

    /** Уникальный идентификатор пользователя (первичный ключ). */
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    /** Адрес электронной почты пользователя. Должен быть уникальным и не равен null. */
    @Column(nullable = false, unique = true)
    private String email;

    /** Пароль пользователя, сохраняемый в зашифрованном (хешированном) виде. */
    @Column(nullable = false)
    private String password;

    /** Назначенная пользователю роль: USER, ADMIN или SUPER_ADMIN. */
    @Enumerated(EnumType.STRING)
    @Column(nullable = false)
    private Role role = Role.USER;

    /**
     * Конструктор без аргументов.
     * <p>Используется JPA и Spring для создания экземпляров через рефлексию.</p>
     */
    public User() {}

    /**
     * Конструктор для создания пользователя с указанным email и паролем.
     * <p>Роль по умолчанию устанавливается как {@link Role#USER}.</p>
     *
     * @param email адрес электронной почты пользователя
     * @param password пароль пользователя
     */
    public User(String email, String password) {
        this.email = email;
        this.password = password;
        this.role = Role.USER;
    }

    /** @return уникальный идентификатор пользователя */
    public Long getId() { return id; }

    /** @return адрес электронной почты пользователя */
    public String getEmail() { return email; }

    /** @param email адрес электронной почты пользователя */
    public void setEmail(String email) { this.email = email; }

    /** @return пароль пользователя (в виде хеша) */
    public String getPassword() { return password; }

    /** @param password пароль пользователя (сырой или хешированный, в зависимости от контекста) */
    public void setPassword(String password) { this.password = password; }

    /** @return роль пользователя */
    public Role getRole() { return role; }

    /** @param role роль пользователя */
    public void setRole(Role role) { this.role = role; }

    /** @param id идентификатор пользователя */
    public void setId(long id) {
        this.id = id;
    }
}
