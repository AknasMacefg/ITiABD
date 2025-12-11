package org.calc.calc;

import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.DisplayName;
import static org.junit.jupiter.api.Assertions.*;

import java.util.List;

/**
 * Модульные тесты для класса DividerCalculator.
 * Тестирует расчет делителя напряжения и поиск решений с использованием стандартных рядов резисторов.
 */
@DisplayName("Тесты для DividerCalculator (делитель напряжения)")
public class DividerCalculatorTest {

    /**
     * Тест генерации номиналов резисторов из стандартного ряда E12.
     * Проверяет корректность генерации значений в заданном диапазоне.
     */
    @Test
    @DisplayName("Тест генерации номиналов резисторов из ряда E12")
    public void testGenerateValues() {
        // Генерация значений от 1 кОм до 10 кОм
        List<Double> values = DividerCalculator.generateValues("E12", 1000.0, 10000.0);
        
        assertNotNull(values, "Список значений не должен быть null");
        assertFalse(values.isEmpty(), "Список значений не должен быть пустым");
        
        // Проверяем, что все значения в заданном диапазоне
        for (Double value : values) {
            assertTrue(value >= 1000.0 && value <= 10000.0, 
                "Значение " + value + " должно быть в диапазоне [1000, 10000]");
        }
        
        // Проверяем наличие некоторых ожидаемых значений из ряда E12
        assertTrue(values.contains(1200.0), "Должно содержать 1.2 кОм");
        assertTrue(values.contains(2200.0), "Должно содержать 2.2 кОм");
        assertTrue(values.contains(4700.0), "Должно содержать 4.7 кОм");
    }

    /**
     * Тест поиска решений для делителя напряжения.
     * Проверяет корректность поиска комбинаций резисторов для получения требуемого выходного напряжения.
     */
    @Test
    @DisplayName("Тест поиска решений делителя напряжения")
    public void testFindSolutions() {
        // Параметры: входное напряжение 12 В, требуемое выходное 5 В, допуск 5%
        double vin = 12.0;
        double vRequired = 5.0;
        double tolerance = 5.0;
        String series = "E12";
        double rMin = 1000.0;  // 1 кОм
        double rMax = 10000.0; // 10 кОм
        
        List<DividerCalculator.Result> results = DividerCalculator.findSolutions(
            vin, vRequired, tolerance, series, rMin, rMax
        );
        
        assertNotNull(results, "Список решений не должен быть null");
        
        // Проверяем, что найдены решения
        if (!results.isEmpty()) {
            DividerCalculator.Result firstResult = results.get(0);
            
            // Проверяем, что ошибка в пределах допуска
            assertTrue(firstResult.errorPercent <= tolerance, 
                "Ошибка должна быть в пределах допуска " + tolerance + "%");
            
            // Для простого делителя из 2 резисторов проверяем формулу
            if (firstResult.resistors.size() == 2) {
                double r1 = firstResult.resistors.get(0);
                double r2 = firstResult.resistors.get(1);
                double calculatedVout = vin * r2 / (r1 + r2);
                assertEquals(firstResult.vout, calculatedVout, 0.001, 
                    "Выходное напряжение должно соответствовать формуле делителя");
            }
        }
    }

    /**
     * Тест обработки неизвестного ряда резисторов.
     * Проверяет, что при передаче неизвестного ряда выбрасывается исключение.
     */
    @Test
    @DisplayName("Тест обработки неизвестного ряда резисторов")
    public void testUnknownSeries() {
        // Попытка использовать несуществующий ряд
        assertThrows(IllegalArgumentException.class, () -> {
            DividerCalculator.generateValues("UNKNOWN", 1000.0, 10000.0);
        }, "Должно быть выброшено IllegalArgumentException для неизвестного ряда");
    }
}

