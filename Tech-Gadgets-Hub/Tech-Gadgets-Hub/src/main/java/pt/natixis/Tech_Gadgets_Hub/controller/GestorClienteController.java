package pt.natixis.Tech_Gadgets_Hub.controller;

import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;
import pt.natixis.Tech_Gadgets_Hub.dto.AssociarClientesRequest;
import pt.natixis.Tech_Gadgets_Hub.model.Cliente;
import pt.natixis.Tech_Gadgets_Hub.model.GestorCliente;
import pt.natixis.Tech_Gadgets_Hub.service.GestorClienteService;

import java.util.List;

@RequestMapping("/gestor-clientes")
@RestController
public class GestorClienteController {

    private final GestorClienteService service;

    public GestorClienteController(GestorClienteService service) {
        this.service = service;
    }

    @GetMapping
    public List<GestorCliente> getAll() {
        return service.getAllGestorClientes();
    }

    @GetMapping("/{gestorId}")
    public ResponseEntity<List<Cliente>> getClientesByGestor(
            @PathVariable Integer gestorId
    ) {
        List<Cliente> clientes = service.getClientesByGestor(gestorId);
        return ResponseEntity.ok(clientes);
    }

    @PostMapping("/associar-clientes")
    public ResponseEntity<GestorCliente> assignClientes(
            @RequestBody AssociarClientesRequest request
    ) {
        service.associarClientes(
                request.getGestorId(),
                request.getClienteIds()
        );
        return ResponseEntity.ok().build();
    }
}