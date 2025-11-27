package mas.curs.infsys.models;

import jakarta.persistence.*;

import java.time.LocalDate;

@Entity
@Table (name = "user_wishlist")
public class UserWishlist {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @ManyToOne
    @JoinColumn(name = "user_id")
    private User user;

    @ManyToOne
    @JoinColumn(name = "book_id")
    private Book book;

    @Column
    private LocalDate added_at;

    public UserWishlist() {}

    public UserWishlist(User user, Book book, LocalDate added_at) {
        this.user = user;
        this.book = book;
        this.added_at = added_at;
    }

    public Long getId() {
        return id;
    }

    public void setId(Long id) {
        this.id = id;
    }

    public User getUser() {
        return user;
    }

    public void setUser(User user) {
        this.user = user;
    }

    public Book getBook() {
        return book;
    }

    public void setBook(Book book) {
        this.book = book;
    }

    public LocalDate getAdded_at() {
        return added_at;
    }

    public void setAdded_at(LocalDate added_at) {
        this.added_at = added_at;
    }
}
