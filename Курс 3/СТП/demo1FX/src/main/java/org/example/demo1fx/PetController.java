package org.example.demo1fx;

import org.example.demo1fx.Pet;
import org.example.demo1fx.PetService;
import javafx.beans.property.SimpleLongProperty;
import javafx.beans.property.SimpleStringProperty;
import javafx.collections.FXCollections;
import javafx.collections.ObservableList;
import javafx.fxml.FXML;
import javafx.fxml.Initializable;
import javafx.scene.control.*;

import java.net.URL;
import java.util.List;
import java.util.ResourceBundle;

public class PetController implements Initializable {

    @FXML private TextField ownerNameField;
    @FXML private TextField petNameField;
    @FXML private TextField speciesField;
    @FXML private TableView<Pet> petTable;
    @FXML private TableColumn<Pet, Long> idColumn;
    @FXML private TableColumn<Pet, String> ownerNameColumn;
    @FXML private TableColumn<Pet, String> petNameColumn;
    @FXML private TableColumn<Pet, String> speciesColumn;
    @FXML private Label statusLabel;

    private PetService petService;
    private ObservableList<Pet> petData;

    @Override
    public void initialize(URL location, ResourceBundle resources) {
        petService = new PetService();
        petData = FXCollections.observableArrayList();

        setupTableColumns();
        loadPets();

        petTable.getSelectionModel().selectedItemProperty().addListener(
                (observable, oldValue, newValue) -> showPetDetails(newValue));
    }

    private void setupTableColumns() {
        idColumn.setCellValueFactory(cellData ->
                new SimpleLongProperty(cellData.getValue().getId()).asObject());
        ownerNameColumn.setCellValueFactory(cellData ->
                new SimpleStringProperty(cellData.getValue().getOwnerName()));
        petNameColumn.setCellValueFactory(cellData ->
                new SimpleStringProperty(cellData.getValue().getPetName()));
        speciesColumn.setCellValueFactory(cellData ->
                new SimpleStringProperty(cellData.getValue().getSpecies()));

        petTable.setItems(petData);
    }

    private void loadPets() {
        try {
            petData.clear();
            List<Pet> pets = petService.getAllPets();
            if (pets != null) {
                petData.addAll(pets);
                statusLabel.setText("Загружено " + petData.size() + " питомцев");

                // Проверяем ID у загруженных питомцев
                for (Pet pet : pets) {
                    System.out.println("Loaded pet - ID: " + pet.getId() + ", Name: " + pet.getPetName());
                }
            }
        } catch (Exception e) {
            statusLabel.setText("Ошибка загрузки данных");
            e.printStackTrace();
        }
    }

    private void showPetDetails(Pet pet) {
        if (pet != null) {
            ownerNameField.setText(pet.getOwnerName());
            petNameField.setText(pet.getPetName());
            speciesField.setText(pet.getSpecies());
        } else {
            clearFields();
        }
    }

    private void clearFields() {
        ownerNameField.clear();
        petNameField.clear();
        speciesField.clear();
    }

    @FXML
    private void handleAddPet() {
        if (isInputValid()) {
            // Создаем нового питомца (без ID - он будет сгенерирован на сервере)
            Pet newPet = new Pet(
                    ownerNameField.getText().trim(),
                    petNameField.getText().trim(),
                    speciesField.getText().trim()
            );

            System.out.println("Adding new pet - Before API call - ID: " + newPet.getId());

            // Отправляем на сервер и получаем обратно объект с ID
            Pet createdPet = petService.createPet(newPet);

            if (createdPet != null && createdPet.getId() != null) {
                System.out.println("Added new pet - After API call - ID: " + createdPet.getId());
                petData.add(createdPet);
                statusLabel.setText("Питомец успешно добавлен (ID: " + createdPet.getId() + ")");
                clearFields();

                // Обновляем таблицу
                petTable.refresh();

                // Автоматически выбираем новую запись
                petTable.getSelectionModel().select(createdPet);
            } else {
                statusLabel.setText("Ошибка: питомец не был создан или ID не получен");
                System.err.println("Created pet is null or has null ID");
            }
        }
    }

    @FXML
    private void handleUpdatePet() {
        Pet selectedPet = petTable.getSelectionModel().getSelectedItem();
        if (selectedPet != null && isInputValid()) {
            // Обновляем данные выбранного питомца
            selectedPet.setOwnerName(ownerNameField.getText().trim());
            selectedPet.setPetName(petNameField.getText().trim());
            selectedPet.setSpecies(speciesField.getText().trim());

            if (petService.updatePet(selectedPet)) {
                petTable.refresh();
                statusLabel.setText("Питомец успешно обновлен (ID: " + selectedPet.getId() + ")");
                clearFields();
            } else {
                statusLabel.setText("Ошибка при обновлении питомца");
            }
        } else {
            showAlert("Не выбрано", "Пожалуйста, выберите питомца из таблицы.");
        }
    }

    @FXML
    private void handleDeletePet() {
        Pet selectedPet = petTable.getSelectionModel().getSelectedItem();
        if (selectedPet != null) {
            Alert confirmation = new Alert(Alert.AlertType.CONFIRMATION);
            confirmation.setTitle("Подтверждение удаления");
            confirmation.setHeaderText(null);
            confirmation.setContentText("Вы уверены, что хотите удалить питомца: " + selectedPet.getPetName() + "?");

            if (confirmation.showAndWait().get() == ButtonType.OK) {
                if (petService.deletePet(selectedPet.getId())) {
                    petData.remove(selectedPet);
                    statusLabel.setText("Питомец успешно удален");
                    clearFields();
                } else {
                    statusLabel.setText("Ошибка при удалении питомца");
                }
            }
        } else {
            showAlert("Не выбрано", "Пожалуйста, выберите питомца для удаления.");
        }
    }

    @FXML
    private void handleRefresh() {
        loadPets();
    }

    @FXML
    private void handleClear() {
        clearFields();
        petTable.getSelectionModel().clearSelection();
        statusLabel.setText("Готово");
    }

    private boolean isInputValid() {
        String errorMessage = "";

        if (ownerNameField.getText() == null || ownerNameField.getText().trim().isEmpty()) {
            errorMessage += "Имя владельца обязательно!\n";
        }
        if (petNameField.getText() == null || petNameField.getText().trim().isEmpty()) {
            errorMessage += "Имя питомца обязательно!\n";
        }
        if (speciesField.getText() == null || speciesField.getText().trim().isEmpty()) {
            errorMessage += "Вид питомца обязателен!\n";
        }

        if (errorMessage.isEmpty()) {
            return true;
        } else {
            showAlert("Неверные данные", errorMessage);
            return false;
        }
    }

    private void showAlert(String title, String message) {
        Alert alert = new Alert(Alert.AlertType.ERROR);
        alert.setTitle(title);
        alert.setHeaderText(null);
        alert.setContentText(message);
        alert.showAndWait();
    }
}