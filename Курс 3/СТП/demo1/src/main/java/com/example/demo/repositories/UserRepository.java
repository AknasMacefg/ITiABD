package com.example.demo.repositories;
import com.example.demo.models.User;
import org.springframework.data.jpa.repository.JpaRepository;

import java.util.Optional;

/**
 * Репозиторий доступа к данным сущности {@link User}.
 * <p>
 * Наследуется от {@link JpaRepository}, предоставляя стандартные CRUD-операции,
 * а также содержит дополнительные методы поиска по email.
 * </p>
 */
public interface UserRepository extends JpaRepository<User, Long> {

    /**
     * Ищет пользователя по адресу электронной почты.
     *
     * @param email адрес электронной почты
     * @return обёртка {@link Optional} с {@link User}, если найден; иначе пустая обёртка
     */
    Optional<User> findByEmail(String email);

    /**
     * Проверяет, существует ли пользователь с указанным email.
     *
     * @param email адрес электронной почты
     * @return {@code true}, если пользователь существует; {@code false} — если нет
     */
    boolean existsByEmail(String email);
}
