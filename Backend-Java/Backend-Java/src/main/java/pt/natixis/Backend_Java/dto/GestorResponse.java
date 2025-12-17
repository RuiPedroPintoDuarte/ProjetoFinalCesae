package pt.natixis.Backend_Java.dto;
public class GestorResponse {
    private Integer gestorId;
    private UtilizadorResponse utilizador;

    public GestorResponse(Integer gestorId, UtilizadorResponse utilizador) {
        this.gestorId = gestorId;
        this.utilizador = utilizador;
    }

    public Integer getGestorId() {
        return gestorId;
    }

    public void setGestorId(Integer gestorId) {
        this.gestorId = gestorId;
    }

    public UtilizadorResponse getUtilizador() {
        return utilizador;
    }

    public void setUtilizador(UtilizadorResponse utilizador) {
        this.utilizador = utilizador;
    }
}