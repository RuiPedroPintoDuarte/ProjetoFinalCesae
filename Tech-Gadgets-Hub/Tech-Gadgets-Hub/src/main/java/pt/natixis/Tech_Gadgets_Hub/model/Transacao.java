package pt.natixis.Tech_Gadgets_Hub.model;

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
}