package pt.natixis.Tech_Gadgets_Hub.dto;

public class UtilizadorResponse {
    private Integer utilizadorId;
    private String username;
    private String email;
    private String role;
    private Boolean ativo;

    public UtilizadorResponse(Integer utilizadorId, String username, String email, String role, Boolean ativo) {
        this.utilizadorId = utilizadorId;
        this.username = username;
        this.email = email;
        this.role = role;
        this.ativo = ativo;
    }

    public Integer getUtilizadorId() {
        return utilizadorId;
    }

    public void setUtilizadorId(Integer utilizadorId) {
        this.utilizadorId = utilizadorId;
    }

    public String getUsername() {
        return username;
    }

    public void setUsername(String username) {
        this.username = username;
    }

    public String getEmail() {
        return email;
    }

    public void setEmail(String email) {
        this.email = email;
    }

    public String getRole() {
        return role;
    }

    public void setRole(String role) {
        this.role = role;
    }

    public Boolean getAtivo() {
        return ativo;
    }

    public void setAtivo(Boolean ativo) {
        this.ativo = ativo;
    }
}