package com.example.demo.config;

import jakarta.servlet.http.HttpServletRequest;
import jakarta.servlet.http.HttpServletResponse;
import org.springframework.security.core.AuthenticationException;
import org.springframework.security.web.AuthenticationEntryPoint;
import org.springframework.stereotype.Component;

import java.io.IOException;

/**
 * Кастомная реализация интерфейса {@link AuthenticationEntryPoint} для обработки неавторизованных запросов.
 * <p>
 * Отвечает за реакцию системы на попытку доступа к защищённым ресурсам без аутентификации.
 * </p>
 * <ul>
 *     <li>Для REST API-запросов (URI начинается с {@code /api/}) возвращает JSON с ошибкой {@code 401 Unauthorized}.</li>
 *     <li>Для обычных веб-запросов перенаправляет пользователя на страницу входа {@code /login}.</li>
 * </ul>
 */
@Component
public class CustomAuthenticationEntryPoint implements AuthenticationEntryPoint {

    /**
     * Вызывается, когда неавторизованный пользователь пытается получить доступ
     * к защищённому ресурсу.
     * <p>
     * Определяет поведение для API и веб-запросов:
     * <ul>
     *     <li>Для API — возвращает JSON-ответ с ошибкой {@code Unauthorized}.</li>
     *     <li>Для веб-запросов — перенаправляет на страницу входа.</li>
     * </ul>
     * </p>
     *
     * @param request       текущий HTTP-запрос {@link HttpServletRequest}
     * @param response      HTTP-ответ {@link HttpServletResponse}
     * @param authException исключение, вызвавшее обработку (например, отсутствие токена)
     * @throws IOException в случае ошибок ввода-вывода при записи ответа
     */
    @Override
    public void commence(HttpServletRequest request,
                         HttpServletResponse response,
                         AuthenticationException authException)
            throws IOException {

        if (request.getRequestURI().startsWith("/api/")) {
            response.setStatus(HttpServletResponse.SC_UNAUTHORIZED);
            response.setContentType("application/json");
            response.getWriter().write("{\"error\": \"Unauthorized\"}");
        } else {
            response.sendRedirect("/login");
        }
    }
}
