package mas.curs.infsys.controllers;

import mas.curs.infsys.models.User;
import mas.curs.infsys.services.UserService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.*;

/**
 * Веб-контроллер для обработки регистрации и входа пользователей.
 * <p>
 * Обеспечивает отображение форм регистрации и авторизации,
 * а также обработку данных, введённых пользователями через веб-интерфейс.
 * </p>
 */
@Controller
public class AuthController {

    /** Сервис для выполнения операций с пользователями. */
    @Autowired
    private UserService userService;

    /**
     * Отображает форму регистрации нового пользователя.
     *
     * @param model объект {@link Model}, используемый для передачи данных в представление
     * @return имя шаблона страницы регистрации
     */
    @GetMapping("/register")
    public String showRegistrationForm(Model model) {
        model.addAttribute("user", new User());
        return "register";
    }

    /**
     * Обрабатывает отправку формы регистрации.
     *
     * @param user объект {@link User}, связанный с данными из формы
     * @param model объект {@link Model} для передачи ошибок при неудачной регистрации
     * @return перенаправление на страницу входа при успешной регистрации
     *         или возврат на форму с сообщением об ошибке, если пользователь уже существует
     */
    @PostMapping("/register")
    public String registerUser(@ModelAttribute("user") User user, Model model) {
        boolean success = userService.register(user);
        if (success) {
            return "redirect:/login";
        } else {
            model.addAttribute("error", "Пользователь с таким адресом уже существует");
            return "redirect:/register?error";
        }
    }

    /**
     * Отображает страницу входа пользователя.
     *
     * @return имя шаблона страницы входа (login)
     */
    @GetMapping("/login")
    public String showLoginForm() {
        return "login";
    }
}
