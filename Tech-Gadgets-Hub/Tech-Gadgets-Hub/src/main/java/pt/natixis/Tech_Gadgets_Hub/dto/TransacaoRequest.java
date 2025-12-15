package pt.natixis.Tech_Gadgets_Hub.dto;

import jakarta.persistence.JoinColumn;
import jakarta.persistence.ManyToOne;
import pt.natixis.Tech_Gadgets_Hub.model.Cliente;

import java.time.LocalDate;

public class TransacaoRequest {
    private String descricao;
    private Integer quantidade;
    private String dataTransacao;
    private String categoria;

    public String getDescricao() {
        return descricao;
    }

    public Integer getQuantidade() {
        return quantidade;
    }

    public String getDataTransacao() {
        return dataTransacao;
    }

    public String getCategoria() {
        return categoria;
    }

    public void setCategoria(String categoria) {
        this.categoria = categoria;
    }

    public void setDataTransacao(String dataTransacao) {
        this.dataTransacao = dataTransacao;
    }

    public void setQuantidade(Integer quantidade) {
        this.quantidade = quantidade;
    }

    public void setDescricao(String descricao) {
        this.descricao = descricao;
    }
}
