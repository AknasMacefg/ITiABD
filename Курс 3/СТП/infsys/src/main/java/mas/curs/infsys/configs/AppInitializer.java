package mas.curs.infsys.configs;

import jakarta.annotation.PostConstruct;
import mas.curs.infsys.models.User;
import mas.curs.infsys.models.Role;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.security.crypto.password.PasswordEncoder;
import org.springframework.stereotype.Component;
import mas.curs.infsys.services.UserService;

import java.time.LocalDateTime;


@Component
public class AppInitializer {

    /** Репозиторий пользователей. */
    @Autowired
    private UserService userService;

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
        createUserIfNotExists("admin", "admin@example.com", true, "password", Role.ADMIN, LocalDateTime.now());
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
    private void createUserIfNotExists(String username, String email, boolean email_notification,
                                       String rawPassword, Role role, LocalDateTime created_at) {
        if (!userService.existsUserByEmail(email)) {
            User user = new User();
            user.setUsername(username);
            user.setEmail(email);
            user.setEmail_notification(email_notification);
            user.setPassword(passwordEncoder.encode(rawPassword));
            user.setRole(role);
            user.setCreated_at(created_at);
            userService.addUser(user);
            System.out.println("Создан пользователь " + role + ": " + email);
        }
    }

}
