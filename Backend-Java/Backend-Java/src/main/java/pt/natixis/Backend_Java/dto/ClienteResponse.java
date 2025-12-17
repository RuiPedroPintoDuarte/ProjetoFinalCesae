package pt.natixis.Backend_Java.dto;

public class ClienteResponse {

    private Integer clienteId;
    private Boolean ativo;
    private String nome;
    private Integer nif;
    private UtilizadorResponse utilizador;

    public Integer getClienteId() {
        return clienteId;
    }

    public Boolean getAtivo() {
        return ativo;
    }

    public String getNome() {
        return nome;
    }

    public Integer getNif() {
        return nif;
    }

    public UtilizadorResponse getUtilizador() {
        return utilizador;
    }

    public void setClienteId(Integer clienteId) {
        this.clienteId = clienteId;
    }

    public void setAtivo(Boolean ativo) {
        this.ativo = ativo;
    }

    public void setNome(String nome) {
        this.nome = nome;
    }

    public void setNif(Integer nif) {
        this.nif = nif;
    }

    public void setUtilizador(UtilizadorResponse utilizador) {
        this.utilizador = utilizador;
    }
}