package pt.natixis.Backend_Java.model;

import jakarta.persistence.*;

@Entity
@Table(
    name = "FactGestorCliente",
    uniqueConstraints = {
            @UniqueConstraint(columnNames = {"GestorId", "ClienteId"})
    }
)
public class GestorCliente {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    @Column(name = "GestorClienteId")
    private Integer id;

    @ManyToOne(optional = false)
    @JoinColumn(name = "GestorId")
    private Gestor gestor;

    @ManyToOne(optional = false)
    @JoinColumn(name = "ClienteId")
    private Cliente cliente;

    public GestorCliente() {}

    public GestorCliente(Gestor gestor, Cliente cliente) {
        this.gestor = gestor;
        this.cliente = cliente;
    }

    public Integer getId() {
        return id;
    }

    public Gestor getGestor() {
        return gestor;
    }

    public void setGestor(Gestor gestor) {
        this.gestor = gestor;
    }

    public Cliente getCliente() {
        return cliente;
    }

    public void setCliente(Cliente cliente) {
        this.cliente = cliente;
    }
}