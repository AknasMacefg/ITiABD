package com.example.demo.controllers;

import com.example.demo.models.Role;
import com.example.demo.models.User;
import com.example.demo.repositories.UserRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.security.access.prepost.PreAuthorize;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.servlet.mvc.support.RedirectAttributes;

import java.util.Optional;

/**
 * Веб-контроллер для управления пользователями (доступен только пользователям с ролью {@code SUPER_ADMIN}).
 * <p>
 * Обеспечивает отображение списка пользователей, изменение их ролей и удаление записей.
 * Используется в административной панели через Thymeleaf-шаблон {@code users.html}.
 * </p>
 */
@Controller
@RequestMapping("/users")
@PreAuthorize("hasRole('SUPER_ADMIN')")
public class UserController {


    /** Репозиторий пользователей, обеспечивающий доступ к данным. */
    private final UserRepository userRepository;

    /**
     * Конструктор контроллера пользователей.
     *
     * @param userRepository репозиторий пользователей
     */
    public UserController(UserRepository userRepository) {
        this.userRepository = userRepository;
    }

    /**
     * Отображает панель управления пользователями.
     *
     * @param model объект {@link Model} для передачи данных в шаблон (список пользователей и сообщения)
     * @param msg необязательное сообщение (используется для отображения статуса операции)
     * @return имя Thymeleaf-шаблона страницы пользователей ({@code users})
     */
    @GetMapping
    public String userPage(Model model, @RequestParam(required = false) String msg) {
        model.addAttribute("users", userRepository.findAll());
        model.addAttribute("message", msg);
        return "users";
    }

    /**
     * Обновляет роль выбранного пользователя.
     *
     * @param id идентификатор пользователя
     * @param role новая роль для назначения пользователю
     * @param redirectAttributes атрибуты для передачи flash-сообщений между запросами
     * @return редирект на страницу пользователей с сообщением об успешном обновлении или ошибке
     */
    @PostMapping("/update")
    public String updateRole(@RequestParam Long id,
                             @RequestParam Role role,
                             RedirectAttributes redirectAttributes) {
        Optional<User> optionalUser = userRepository.findById(id);
        if (optionalUser.isPresent()) {
            User user = optionalUser.get();
            user.setRole(role);
            userRepository.save(user);
            redirectAttributes.addAttribute("msg", "Роль успешно обновлена.");
        } else {
            redirectAttributes.addAttribute("msg", "Пользователь не найден.");
        }
        return "redirect:/users";
    }

    /**
     * Удаляет пользователя по его идентификатору.
     *
     * @param id идентификатор пользователя для удаления
     * @param redirectAttributes flash-атрибуты для передачи сообщений об операции
     * @return текстовое сообщение о результате операции
     */
    @DeleteMapping("/delete/{id}")
    @ResponseBody
    public String deleteUser(@PathVariable Long id,
                             RedirectAttributes redirectAttributes) {
        if (userRepository.existsById(id)) {
            userRepository.deleteById(id);
            return "Пользователь удалён.";
        } else {
            return "Пользователь не найден.";
        }
    }
}
