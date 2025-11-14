package com.example.demo.config;

import jakarta.servlet.http.HttpServletRequest;
import jakarta.servlet.http.HttpServletResponse;
import org.springframework.security.access.AccessDeniedException;
import org.springframework.security.web.access.AccessDeniedHandler;
import org.springframework.stereotype.Component;

import java.io.IOException;

/**
 * Кастомный обработчик исключений {@link AccessDeniedException},
 * возникающих при попытке доступа к ресурсам без достаточных прав.
 * <p>
 * Определяет различное поведение для REST API и веб-запросов:
 * </p>
 * <ul>
 *     <li>Для API-запросов (URI начинается с {@code /api/}) возвращает JSON-ответ с кодом {@code 403 Forbidden}.</li>
 *     <li>Для веб-запросов выполняет перенаправление на страницу {@code /access-denied}.</li>
 * </ul>
 */
@Component
public class CustomAccessDeniedHandler implements AccessDeniedHandler {

    /**
     * Обрабатывает исключение {@link AccessDeniedException} при отсутствии прав доступа.
     * <p>
     * Проверяет, начинается ли URI запроса с {@code /api/}.
     * </p>
     * <ul>
     *     <li>Если да — формирует JSON-ответ с кодом {@code 403 Forbidden}.</li>
     *     <li>Если нет — перенаправляет пользователя на страницу {@code /access-denied}.</li>
     * </ul>
     *
     * @param request               HTTP-запрос {@link HttpServletRequest}
     * @param response              HTTP-ответ {@link HttpServletResponse}
     * @param accessDeniedException выброшенное исключение при запрете доступа
     * @throws IOException в случае ошибки ввода-вывода при записи ответа
     */
    @Override
    public void handle(HttpServletRequest request,
                       HttpServletResponse response,
                       AccessDeniedException accessDeniedException)
            throws IOException {

        if (request.getRequestURI().startsWith("/api/")) {
            response.setStatus(HttpServletResponse.SC_FORBIDDEN);
            response.setContentType("application/json");
            response.getWriter().write("{\"error\": \"Forbidden\"}");
        } else {
            response.sendRedirect("/access-denied");
        }
    }
}
