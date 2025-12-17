package pt.natixis.Backend_Java.model;

import jakarta.persistence.*;

import java.time.LocalDate;

@Entity
@Table(name = "FactTransacao")
public class Transacao {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    @Column(name = "TransacaoId")
    private Integer id;

    @ManyToOne
    @JoinColumn(name = "ClienteId")
    private Cliente cliente;

    private String descricao;
    private Integer quantidade;
    private LocalDate dataTransacao;
    private String categoria;

    public Transacao() {}

    public Transacao(Cliente cliente, String descricao, Integer quantidade, LocalDate dataTransacao, String categoria) {
        this.cliente = cliente;
        this.descricao = descricao;
        this.quantidade = quantidade;
        this.dataTransacao = dataTransacao;
        this.categoria = categoria;
    }

    public Transacao(Integer id, Cliente cliente, String descricao, Integer quantidade, LocalDate dataTransacao, String categoria) {
        this.id = id;
        this.cliente = cliente;
        this.descricao = descricao;
        this.quantidade = quantidade;
        this.dataTransacao = dataTransacao;
        this.categoria = categoria;
    }

    public Integer getId() {
        return id;
    }

    public Cliente getCliente() {
        return cliente;
    }

    public String getDescricao() {
        return descricao;
    }

    public Integer getQuantidade() {
        return quantidade;
    }

    public LocalDate getDataTransacao() {
        return dataTransacao;
    }

    public String getCategoria() {
        return categoria;
    }

    public void setId(Integer id) {
        this.id = id;
    }

    public void setCliente(Cliente cliente) {
        this.cliente = cliente;
    }

    public void setDescricao(String descricao) {
        this.descricao = descricao;
    }

    public void setQuantidade(Integer quantidade) {
        this.quantidade = quantidade;
    }

    public void setDataTransacao(LocalDate dataTransacao) {
        this.dataTransacao = dataTransacao;
    }

    public void setCategoria(String categoria) {
        this.categoria = categoria;
    }
}