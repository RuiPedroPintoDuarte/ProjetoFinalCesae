package pt.natixis.Backend_Java.model;

import jakarta.persistence.*;

import java.time.LocalDate;

@Entity
@Table(name = "DimCliente")
public class Cliente {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    @Column(name = "ClienteId")
    private Integer id;

    @OneToOne
    @JoinColumn(name = "UtilizadorId", nullable = false)
    private Utilizador utilizador;

    @Column(name = "Nome", nullable = false)
    private String nome;

    @Column(name = "DataNascimento")
    private LocalDate dataNascimento;

    @Column(name = "NIF", unique = true)
    private Integer nif;

    public Cliente() {}

    public Cliente(Utilizador utilizador, String nome, LocalDate dataNascimento, Integer nif) {
        this.utilizador = utilizador;
        this.nome = nome;
        this.dataNascimento = dataNascimento;
        this.nif = nif;
    }

    public Cliente(Integer id, Utilizador utilizador, String nome, LocalDate dataNascimento, Integer nif) {
        this.id = id;
        this.utilizador = utilizador;
        this.nome = nome;
        this.dataNascimento = dataNascimento;
        this.nif = nif;
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

    public String getNome() {
        return nome;
    }

    public void setNome(String nome) {
        this.nome = nome;
    }

    public LocalDate getDataNascimento() {
        return dataNascimento;
    }

    public void setDataNascimento(LocalDate dataNascimento) {
        this.dataNascimento = dataNascimento;
    }

    public Integer getNif() {
        return nif;
    }

    public void setNif(Integer nif) {
        this.nif = nif;
    }
}