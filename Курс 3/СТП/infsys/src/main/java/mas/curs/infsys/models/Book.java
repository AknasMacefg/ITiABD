package mas.curs.infsys.models;

import jakarta.persistence.*;

import java.time.LocalDate;

@Entity
@Table (name = "books")

public class Book {

    @Id
    @GeneratedValue (strategy = GenerationType.IDENTITY)
    private int id;

    @Column (nullable = false, unique = true)
    private String title;

    @Column
    private String description;

    @Column
    private LocalDate release_date;

    @Column (nullable = false, unique = true)
    private String isbn;

    @Column
    private double price;

    @Column (nullable = false)
    private String language;

    @Column
    private int pages;

    @Column (nullable = false)
    private String status;

    @Column
    private String image_url;

    @Column
    private boolean adult_check;

    public Book() {}

    public Book(
            String title, String description, LocalDate release_date, String isbn, double price, String language,
            int pages, String status, String image_url, boolean adult_check) {
        this.title = title;
        this.description = description;
        this.release_date = release_date;
        this.isbn = isbn;
        this.price = price;
        this.language = language;
        this.pages = pages;
        this.status = status;
        this.image_url = image_url;
        this.adult_check = adult_check;
    }

    public int getId() {
        return id;
    }

    public void setId(int id) {
        this.id = id;
    }

    public String getTitle() {
        return title;
    }

    public void setTitle(String title) {
        this.title = title;
    }

    public String getDescription() {
        return description;
    }

    public void setDescription(String description) {
        this.description = description;
    }

    public LocalDate getRelease_date() {
        return release_date;
    }

    public void setRelease_date(LocalDate release_date) {
        this.release_date = release_date;
    }

    public String getIsbn() {
        return isbn;
    }

    public void setIsbn(String isbn) {
        this.isbn = isbn;
    }

    public double getPrice() {
        return price;
    }

    public void setPrice(double price) {
        this.price = price;
    }

    public String getLanguage() {
        return language;
    }

    public void setLanguage(String language) {
        this.language = language;
    }

    public int getPages() {
        return pages;
    }

    public void setPages(int pages) {
        this.pages = pages;
    }

    public String getStatus() {
        return status;
    }

    public void setStatus(String status) {
        this.status = status;
    }

    public String getImage_url() {
        return image_url;
    }

    public void setImage_url(String image_url) {
        this.image_url = image_url;
    }

    public boolean isAdult_check() {
        return adult_check;
    }

    public void setAdult_check(boolean adult_check) {
        this.adult_check = adult_check;
    }
}
