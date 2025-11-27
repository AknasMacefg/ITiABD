package mas.curs.infsys.models;

import jakarta.persistence.*;
@Entity
@Table (name = "authors")
public class Author {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private int id;

    @Column(nullable = false)
    private String firstname;

    @Column
    private String middlename;

    @Column
    private String lastname;

    @Column
    private String biography;

    @Column
    private String photo_url;

    public Author() {}

    public Author(String firstname, String middlename, String lastname, String biography, String photo_url) {
        this.firstname = firstname;
        this.middlename = middlename;
        this.lastname = lastname;
        this.biography = biography;
        this.photo_url = photo_url;
    }

    public int getId() {
        return id;
    }

    public void setId(int id) {
        this.id = id;
    }

    public String getFirstname() {
        return firstname;
    }

    public void setFirstname(String firstname) {
        this.firstname = firstname;
    }

    public String getMiddlename() {
        return middlename;
    }

    public void setMiddlename(String middlename) {
        this.middlename = middlename;
    }

    public String getLastname() {
        return lastname;
    }

    public void setLastname(String lastname) {
        this.lastname = lastname;
    }

    public String getBiography() {
        return biography;
    }

    public void setBiography(String biography) {
        this.biography = biography;
    }

    public String getPhoto_url() {
        return photo_url;
    }

    public void setPhoto_url(String photo_url) {
        this.photo_url = photo_url;
    }
}
