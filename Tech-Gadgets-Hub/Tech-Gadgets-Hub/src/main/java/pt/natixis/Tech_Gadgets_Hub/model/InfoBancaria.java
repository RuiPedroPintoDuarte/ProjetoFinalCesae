package pt.natixis.Tech_Gadgets_Hub.model;

import jakarta.persistence.*;

import java.time.LocalDate;

@Entity
@Table(name = "FactInfoBancaria")
public class InfoBancaria {

    @Id
    @Column(name = "ClienteId")
    private Integer id;

    @OneToOne
    @MapsId
    @JoinColumn(name = "ClienteId")
    private Cliente cliente;

    private String emprego;
    private String estadoCivil;
    private String educacao;

    @Column(name = "DefaultCredit")
    private Boolean defaultCredit;

    private Integer saldo;

    private Boolean emprestimoCasa;
    private Boolean emprestimoPessoal;

    private LocalDate dataRegisto;

    public InfoBancaria() {}

    public InfoBancaria(Cliente cliente, String emprego, String estadoCivil, String educacao, Boolean defaultCredit, Integer saldo, Boolean emprestimoCasa, Boolean emprestimoPessoal, LocalDate dataRegisto) {
        this.cliente = cliente;
        this.emprego = emprego;
        this.estadoCivil = estadoCivil;
        this.educacao = educacao;
        this.defaultCredit = defaultCredit;
        this.saldo = saldo;
        this.emprestimoCasa = emprestimoCasa;
        this.emprestimoPessoal = emprestimoPessoal;
        this.dataRegisto = dataRegisto;
    }

    public InfoBancaria(Integer id, Cliente cliente, String emprego, String estadoCivil, String educacao, Boolean defaultCredit, Integer saldo, Boolean emprestimoCasa, Boolean emprestimoPessoal, LocalDate dataRegisto) {
        this.id = id;
        this.cliente = cliente;
        this.emprego = emprego;
        this.estadoCivil = estadoCivil;
        this.educacao = educacao;
        this.defaultCredit = defaultCredit;
        this.saldo = saldo;
        this.emprestimoCasa = emprestimoCasa;
        this.emprestimoPessoal = emprestimoPessoal;
        this.dataRegisto = dataRegisto;
    }

    public Integer getId() {
        return id;
    }

    public void setId(Integer id) {
        this.id = id;
    }

    public Cliente getCliente() {
        return cliente;
    }

    public void setCliente(Cliente cliente) {
        this.cliente = cliente;
    }

    public String getEmprego() {
        return emprego;
    }

    public void setEmprego(String emprego) {
        this.emprego = emprego;
    }

    public String getEstadoCivil() {
        return estadoCivil;
    }

    public void setEstadoCivil(String estadoCivil) {
        this.estadoCivil = estadoCivil;
    }

    public String getEducacao() {
        return educacao;
    }

    public void setEducacao(String educacao) {
        this.educacao = educacao;
    }

    public Boolean getDefaultCredit() {
        return defaultCredit;
    }

    public void setDefaultCredit(Boolean defaultCredit) {
        this.defaultCredit = defaultCredit;
    }

    public Integer getSaldo() {
        return saldo;
    }

    public void setSaldo(Integer saldo) {
        this.saldo = saldo;
    }

    public Boolean getEmprestimoCasa() {
        return emprestimoCasa;
    }

    public void setEmprestimoCasa(Boolean emprestimoCasa) {
        this.emprestimoCasa = emprestimoCasa;
    }

    public Boolean getEmprestimoPessoal() {
        return emprestimoPessoal;
    }

    public void setEmprestimoPessoal(Boolean emprestimoPessoal) {
        this.emprestimoPessoal = emprestimoPessoal;
    }

    public LocalDate getDataRegisto() {
        return dataRegisto;
    }

    public void setDataRegisto(LocalDate dataRegisto) {
        this.dataRegisto = dataRegisto;
    }
}