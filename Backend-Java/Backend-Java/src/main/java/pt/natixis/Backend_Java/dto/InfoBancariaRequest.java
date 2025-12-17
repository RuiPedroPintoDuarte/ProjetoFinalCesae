package pt.natixis.Backend_Java.dto;

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
