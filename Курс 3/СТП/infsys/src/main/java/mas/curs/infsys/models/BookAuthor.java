package mas.curs.infsys.models;

import jakarta.persistence.*;
import java.io.Serializable;

@Entity
@Table (name = "user_author")
public class BookAuthor {
    @EmbeddedId
    private BookAuthorId id;

    @ManyToOne
    @MapsId("authorId")
    @JoinColumn(name = "author_id")
    private Author author;

    @ManyToOne
    @MapsId("bookId")
    @JoinColumn(name = "book_id")
    private Book book;

    @Column
    private boolean main_author;

    public BookAuthor() {}

    public BookAuthor(Author author, Book book, boolean main_author) {
        this.author = author;
        this.book = book;
        this.main_author = main_author;
    }

    public Author getAuthor() {
        return author;
    }

    public void setAuthor(Author author) {
        this.author = author;
    }

    public Book getBook() {
        return book;
    }

    public void setBook(Book book) {
        this.book = book;
    }

    public boolean getMain_author() {
        return main_author;
    }

    public void setMain_author(boolean main_author) {
        this.main_author = main_author;
    }
}

@Embeddable
class BookAuthorId implements Serializable {
    private Long authorId;
    private Long bookId;

    public BookAuthorId() {}

    public BookAuthorId(Long authorId, Long bookId) {
        this.authorId = authorId;
        this.bookId = bookId;
    }

    public Long getAuthorId() {
        return authorId;
    }

    public void setAuthorId(Long authorId) {
        this.authorId = authorId;
    }

    public Long getBookId() {
        return bookId;
    }

    public void setBookId(Long bookId) {
        this.bookId = bookId;
    }
}
