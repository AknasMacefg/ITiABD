package mas.curs.infsys.models;

import jakarta.persistence.*;
import java.io.Serializable;

@Entity
@Table (name = "book_series")
public class BookSeries {
    @EmbeddedId
    private BookSeriesId id;

    @ManyToOne
    @MapsId("seriesId")
    @JoinColumn(name = "series_id")
    private Series series;

    @ManyToOne
    @MapsId("bookId")
    @JoinColumn(name = "book_id")
    private Book book;

    public BookSeries() {}

    public BookSeries(Series series, Book book) {
        this.series = series;
        this.book = book;
    }

    public Series getSeries() {
        return series;
    }

    public void setSeries(Series series) {
        this.series = series;
    }

    public Book getBook() {
        return book;
    }

    public void setBook(Book book) {
        this.book = book;
    }
}

@Embeddable
class BookSeriesId implements Serializable {
    private Long seriesId;
    private Long bookId;

    public BookSeriesId() {}

    public BookSeriesId(Long seriesId, Long bookId) {
        this.seriesId = seriesId;
        this.bookId = bookId;
    }

    public Long getSeriesId() {
        return seriesId;
    }

    public void setSeriesId(Long seriesId) {
        this.seriesId = seriesId;
    }

    public Long getBookId() {
        return bookId;
    }

    public void setBookId(Long bookId) {
        this.bookId = bookId;
    }
}
