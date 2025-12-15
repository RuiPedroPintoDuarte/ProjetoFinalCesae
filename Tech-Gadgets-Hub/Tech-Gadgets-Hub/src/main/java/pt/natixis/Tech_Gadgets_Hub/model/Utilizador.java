package pt.natixis.Tech_Gadgets_Hub.model;

import jakarta.persistence.*;
import jakarta.validation.constraints.*;

import java.time.LocalDateTime;

@Entity
@Table(name = "DimUtilizador")
public class Utilizador {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    @Column(name = "UtilizadorId")
    private Integer id;

    @Column(name = "Username", nullable = false, unique = true)
    private String username;

    @Column(name = "Email", nullable = false, unique = true)
    private String email;

    @Column(name = "PalavraPasse", nullable = false)
    private String palavraPasse;

    @Column(name = "Role", nullable = false)
    private String role;

    @Column(name = "Ativo")
    private Boolean ativo;

    public Utilizador() {}

    public Utilizador(String username, String email, String palavraPasse, String role, Boolean ativo) {
        this.username = username;
        this.email = email;
        this.palavraPasse = palavraPasse;
        this.role = role;
        this.ativo = ativo;
    }

    public Utilizador(Integer id, String username, String email, String palavraPasse, String role, Boolean ativo) {
        this.id = id;
        this.username = username;
        this.email = email;
        this.palavraPasse = palavraPasse;
        this.role = role;
        this.ativo = ativo;
    }

    public Integer getId() {
        return id;
    }

    public void setId(Integer id) {
        this.id = id;
    }

    public String getUsername() {
        return username;
    }

    public void setUsername(String username) {
        this.username = username;
    }

    public String getEmail() {
        return email;
    }

    public void setEmail(String email) {
        this.email = email;
    }

    public String getPalavraPasse() {
        return palavraPasse;
    }

    public void setPalavraPasse(String palavraPasse) {
        this.palavraPasse = palavraPasse;
    }

    public String getRole() {
        return role;
    }

    public void setRole(String role) {
        this.role = role;
    }

    public Boolean getAtivo() {
        return ativo;
    }

    public void setAtivo(Boolean ativo) {
        this.ativo = ativo;
    }
}