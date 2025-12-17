package pt.natixis.Backend_Java.controller;

import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;
import pt.natixis.Backend_Java.dto.CriarClienteRequest;
import pt.natixis.Backend_Java.model.Cliente;
import pt.natixis.Backend_Java.service.ClienteService;

import java.util.List;

@RequestMapping("/clientes")
@RestController
public class ClienteController {
    private final ClienteService clienteService;

    public ClienteController(ClienteService clienteService){
        this.clienteService = clienteService;
    }

    @GetMapping()
    public List<Cliente> getClientes(){
        return clienteService.getAllClientes();
    }

    @GetMapping("/{id}")
    public ResponseEntity<Cliente> getClienteById(@PathVariable int id){
        Cliente cliente = clienteService.getClienteByClienteId(id);
        if (cliente == null){
            return ResponseEntity.notFound().build();
        }
        return ResponseEntity.ok(cliente);
    }

    @PostMapping("/criar-cliente")
    public ResponseEntity<Cliente> createCliente(@RequestBody CriarClienteRequest cliente){
        Cliente created = clienteService.createCliente(cliente);
        if(created == null){
            return ResponseEntity.badRequest().build();
        }
        return ResponseEntity
                .status(HttpStatus.CREATED)
                .body(created);
    }

    @PutMapping("/{id}")
    public ResponseEntity<Cliente> updateCliente(@PathVariable int id, @RequestBody CriarClienteRequest cliente){
        Cliente updated = clienteService.updateCliente(id, cliente);
        if (cliente == null){
            return ResponseEntity.notFound().build();
        }
        return ResponseEntity.ok(updated);
    }

    @DeleteMapping("/{id}")
    public ResponseEntity<Void> deleteCliente(@PathVariable int id){
        boolean deleted = clienteService.deleteCliente(id);
        if (!deleted){
            return ResponseEntity.notFound().build();
        }
        return ResponseEntity.noContent().build();
    }


}
