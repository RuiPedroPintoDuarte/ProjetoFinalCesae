package pt.natixis.Backend_Java.dto;

import java.util.List;

public class AssociarClientesRequest {

    private Integer gestorId;
    private List<Integer> clienteIds;

    public Integer getGestorId() {
        return gestorId;
    }

    public void setGestorId(Integer gestorId) {
        this.gestorId = gestorId;
    }

    public List<Integer> getClienteIds() {
        return clienteIds;
    }

    public void setClienteIds(List<Integer> clienteIds) {
        this.clienteIds = clienteIds;
    }
}