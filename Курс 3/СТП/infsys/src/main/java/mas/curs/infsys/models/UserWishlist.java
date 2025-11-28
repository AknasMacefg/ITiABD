package mas.curs.infsys.models;

import jakarta.persistence.*;

import java.io.Serializable;
import java.time.LocalDate;

@Entity
@Table (name = "user_wishlist")
public class UserWishlist {
    @EmbeddedId
    private UserWishlistId id;

    @ManyToOne
    @MapsId("userId")
    @JoinColumn(name = "user_id")
    private User user;

    @ManyToOne
    @MapsId("bookId")
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

@Embeddable
class UserWishlistId implements Serializable {
    private Long userId;
    private Long bookId;

    public UserWishlistId() {}

    public UserWishlistId(Long userId, Long bookId) {
        this.userId = userId;
        this.bookId = bookId;
    }

    public Long getUserId() {
        return userId;
    }

    public void setUserId(Long userId) {
        this.userId = userId;
    }

    public Long getBookId() {
        return bookId;
    }

    public void setBookId(Long bookId) {
        this.bookId = bookId;
    }
}
