package com.example.demo.controllers;

import io.swagger.v3.oas.annotations.Operation;
import io.swagger.v3.oas.annotations.responses.ApiResponse;
import com.example.demo.models.Pet;
import com.example.demo.services.PetService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.security.access.prepost.PreAuthorize;
import org.springframework.web.bind.annotation.*;

import java.util.List;

/**
 * REST-контроллер для управления студентами через API.
 * <p>
 * Предоставляет конечные точки для получения, добавления, обновления и удаления студентов.
 * Доступ к методам контролируется на основе ролей (требуется роль {@code ADMIN}).
 * </p>
 */
@RestController
@RequestMapping("/api/pets")
public class PetRestController {

    /** Сервис для работы с объектами {@link Pet}. */
    @Autowired
    private PetService petService;

    /**
     * Возвращает список всех студентов.
     *
     * @return список студентов
     */
    @Operation(summary = "Получить всех студентов")
    @ApiResponse(responseCode = "200", description = "Список студентов успешно получен")
    @GetMapping
    //@PreAuthorize("hasRole('ADMIN')")
    public List<Pet> getAllPets() {
        return petService.getAllPets();
    }

    /**
     * Возвращает информацию о студенте по его идентификатору.
     *
     * @param id идентификатор студента
     * @return объект {@link Pet}, если найден, или статус 404, если не найден
     */
    @Operation(summary = "Получить студента по ID")
    @ApiResponse(responseCode = "200", description = "Студент найден")
    @ApiResponse(responseCode = "404", description = "Студент не найден")
    @GetMapping("/{id}")
    //@PreAuthorize("hasRole('ADMIN')")
    public ResponseEntity<Pet> getPetById(@PathVariable long id) {
        Pet student = petService.getPetById(id);
        return student != null
                ? ResponseEntity.ok(student)
                : ResponseEntity.notFound().build();
    }

    /**
     * Добавляет нового студента.
     *
     * @param pet объект {@link Pet}, переданный в теле запроса
     * @return созданный студент с присвоенным идентификатором
     */
    @Operation(summary = "Добавить нового студента")
    @ApiResponse(responseCode = "201", description = "Студент успешно создан")
    @PostMapping
    //@PreAuthorize("hasRole('ADMIN')")
    public ResponseEntity<Pet> addPet(@RequestBody Pet pet) {
        Pet saved = petService.addPet(pet);
        return ResponseEntity.status(HttpStatus.CREATED).body(saved);
    }

    /**
     * Обновляет данные существующего студента.
     *
     * @param id идентификатор студента
     * @param pet обновлённые данные студента
     * @return обновлённый объект {@link Pet} или статус 404, если студент не найден
     */
    @Operation(summary = "Обновить данные студента")
    @ApiResponse(responseCode = "200", description = "Студент успешно обновлён")
    @ApiResponse(responseCode = "404", description = "Студент не найден")
    @PutMapping("/{id}")
    //@PreAuthorize("hasRole('ADMIN')")
    public ResponseEntity<Pet> updatePet(@PathVariable long id, @RequestBody Pet pet) {
        Pet existing = petService.getPetById(id);
        if (existing == null) {
            return ResponseEntity.notFound().build();
        }
        pet.setId(id);
        return ResponseEntity.ok(petService.addPet(pet));
    }

    /**
     * Удаляет студента по идентификатору.
     *
     * @param id идентификатор студента
     * @return HTTP-ответ: 204 — если успешно удалён, 404 — если студент не найден
     */
    @Operation(summary = "Удалить студента")
    @ApiResponse(responseCode = "204", description = "Студент успешно удалён")
    @ApiResponse(responseCode = "404", description = "Студент не найден")
    @DeleteMapping("/{id}")
    //@PreAuthorize("hasRole('ADMIN')")
    public ResponseEntity<Void> deletePet(@PathVariable long id) {
        Pet existing = petService.getPetById(id);
        if (existing == null) {
            return ResponseEntity.notFound().build();
        }
        petService.deletePet(id);
        return ResponseEntity.noContent().build();
    }
}
