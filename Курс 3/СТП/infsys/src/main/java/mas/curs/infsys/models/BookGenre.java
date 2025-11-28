package mas.curs.infsys.models;

import jakarta.persistence.*;
import java.io.Serializable;

@Entity
@Table (name = "book_genre")
public class BookGenre {
    @EmbeddedId
    private BookGenreId id;

    @ManyToOne
    @MapsId("genreId")
    @JoinColumn(name = "genre_id")
    private Genre genre;

    @ManyToOne
    @MapsId("bookId")
    @JoinColumn(name = "book_id")
    private Book book;

    public BookGenre() {}

    public BookGenre(Genre genre, Book book) {
        this.genre = genre;
        this.book = book;
    }

    public Genre getGenre() {
        return genre;
    }

    public void setGenre(Genre genre) {
        this.genre = genre;
    }

    public Book getBook() {
        return book;
    }

    public void setBook(Book book) {
        this.book = book;
    }
}

@Embeddable
class BookGenreId implements Serializable {
    private Long genreId;
    private Long bookId;

    public BookGenreId() {}

    public BookGenreId(Long genreId, Long bookId) {
        this.genreId = genreId;
        this.bookId = bookId;
    }

    public Long getGenreId() {
        return genreId;
    }

    public void setGenreId(Long genreId) {
        this.genreId = genreId;
    }

    public Long getBookId() {
        return bookId;
    }

    public void setBookId(Long bookId) {
        this.bookId = bookId;
    }
}
