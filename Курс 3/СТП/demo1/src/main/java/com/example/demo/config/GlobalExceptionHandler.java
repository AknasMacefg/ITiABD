package com.example.demo.config;

import jakarta.servlet.http.HttpServletRequest;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.ControllerAdvice;
import org.springframework.web.bind.annotation.ExceptionHandler;
import org.springframework.web.servlet.NoHandlerFoundException;

import java.util.HashMap;
import java.util.Map;

/**
 * Глобальный обработчик исключений для всего приложения.
 * <p>
 * Отвечает за перехват и корректную обработку всех непредвиденных ошибок,
 * как для REST API, так и для обычных веб-запросов.
 * </p>
 * <ul>
 *     <li>Для API-запросов (URI начинается с {@code /api/}) возвращает JSON-ответ с кодом ошибки.</li>
 *     <li>Для веб-запросов отображает страницу с сообщением об ошибке через шаблон {@code error.html}.</li>
 * </ul>
 */
@ControllerAdvice
public class GlobalExceptionHandler {

    /**
     * Обрабатывает все необработанные исключения приложения.
     * <p>
     * Если запрос относится к REST API, возвращается JSON-ответ с кодом {@code 500 Internal Server Error}.
     * Если запрос веб-страничный — рендерится шаблон {@code error.html} с сообщением об ошибке.
     * </p>
     *
     * @param ex      возникшее исключение
     * @param request текущий HTTP-запрос
     * @param model   модель для передачи данных в шаблон (веб-запросы)
     * @return {@link ResponseEntity} с ошибкой для API или имя шаблона ошибки для веб
     */
    @ExceptionHandler(Exception.class)
    public Object handleException(Exception ex, HttpServletRequest request, Model model) {
        boolean isApi = request.getRequestURI().startsWith("/api/");

        if (isApi) {
            Map<String, String> error = new HashMap<>();
            error.put("error", ex.getMessage() != null ? ex.getMessage() : "Internal Server Error");
            return new ResponseEntity<>(error, HttpStatus.INTERNAL_SERVER_ERROR);
        } else {
            model.addAttribute("message", ex.getMessage());
            return "error"; // шаблон error.html
        }
    }

    /**
     * Обрабатывает ошибки 404 (ресурс не найден).
     * <p>
     * Если URI начинается с {@code /api/}, возвращается JSON с сообщением {@code Not Found}
     * и статусом {@code 404}.
     * В противном случае отображается страница с сообщением о ненайденной странице.
     * </p>
     *
     * @param ex      исключение {@link NoHandlerFoundException}, возникающее при отсутствии маршрута
     * @param request текущий HTTP-запрос
     * @param model   модель для передачи данных в шаблон
     * @return JSON-ответ для API или имя шаблона для веб-запроса
     */
    @ExceptionHandler(NoHandlerFoundException.class)
    public Object handleNotFound(NoHandlerFoundException ex, HttpServletRequest request, Model model) {
        boolean isApi = request.getRequestURI().startsWith("/api/");

        if (isApi) {
            Map<String, String> error = new HashMap<>();
            error.put("error", "Not Found");
            return new ResponseEntity<>(error, HttpStatus.NOT_FOUND);
        } else {
            model.addAttribute("message", "Страница не найдена: " + request.getRequestURI());
            return "error"; // тот же шаблон
        }
    }
}
