package pt.natixis.Tech_Gadgets_Hub.dto;

import jakarta.persistence.Column;
import pt.natixis.Tech_Gadgets_Hub.model.Cliente;

import java.time.LocalDate;

public class InfoBancariaRequest {

    private String emprego;
    private String estadoCivil;
    private String educacao;

    private Boolean defaultCredit;

    private Integer saldo;

    private Boolean emprestimoCasa;
    private Boolean emprestimoPessoal;

    public String getEmprego() {
        return emprego;
    }

    public String getEstadoCivil() {
        return estadoCivil;
    }

    public String getEducacao() {
        return educacao;
    }

    public Boolean getDefaultCredit() {
        return defaultCredit;
    }

    public Integer getSaldo() {
        return saldo;
    }

    public Boolean getEmprestimoCasa() {
        return emprestimoCasa;
    }

    public Boolean getEmprestimoPessoal() {
        return emprestimoPessoal;
    }

}
