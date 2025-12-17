package pt.natixis.Backend_Java.model;

import jakarta.persistence.*;

@Entity
@Table(name = "DimGestor")
public class Gestor {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    @Column(name = "GestorId")
    private Integer id;

    @OneToOne
    @JoinColumn(name = "UtilizadorId", nullable = false)
    private Utilizador utilizador;

    public Gestor() {}

    public Gestor(Utilizador utilizador) {
        this.utilizador = utilizador;
    }

    public Gestor(Integer id, Utilizador utilizador) {
        this.id = id;
        this.utilizador = utilizador;
    }

    public Integer getId() {
        return id;
    }

    public void setId(Integer id) {
        this.id = id;
    }

    public Utilizador getUtilizador() {
        return utilizador;
    }

    public void setUtilizador(Utilizador utilizador) {
        this.utilizador = utilizador;
    }
}