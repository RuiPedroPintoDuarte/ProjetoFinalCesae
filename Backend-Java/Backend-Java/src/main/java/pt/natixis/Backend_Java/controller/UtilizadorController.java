package pt.natixis.Backend_Java.controller;

import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;
import pt.natixis.Backend_Java.model.Utilizador;
import pt.natixis.Backend_Java.service.UtilizadorService;

import java.util.List;

@RequestMapping("/utilizadores")
@RestController
public class UtilizadorController {

    private final UtilizadorService service;

    public UtilizadorController(UtilizadorService service){
        this.service = service;
    }

    @GetMapping()
    public List<Utilizador> getUtilizadores() {
        return service.getAllUtilizadores();
    }

    @GetMapping("/{id}")
    public ResponseEntity<Utilizador> getUtilizadorById(@PathVariable Integer id) {
        Utilizador utilizador = service.getUtilizadorById(id);
        if (utilizador == null){
            return ResponseEntity.notFound().build();
        }
        return ResponseEntity.ok(utilizador);
    }

    @PostMapping
    public ResponseEntity<Utilizador> createCliente(@RequestBody Utilizador utilizador) {
        Utilizador created = service.createUtilizador(utilizador);
        if(created == null){
            return ResponseEntity.badRequest().build();
        }
        return ResponseEntity
                .status(HttpStatus.CREATED)
                .body(created);
    }

    @PutMapping("/{id}")
    public ResponseEntity<Utilizador> updateUtilizador(@PathVariable Integer id, @RequestBody Utilizador utilizador) {
        Utilizador updated = service.updateUtilizador(id, utilizador);
        if (updated == null){
            return ResponseEntity.notFound().build();
        }
        return ResponseEntity.ok(updated);
    }

    @DeleteMapping("/{id}")
    public ResponseEntity<Void> deactivateUtilizador(@PathVariable Integer id) {
        boolean deleted = service.deactivateUtilizador(id);
        if (!deleted){
            return ResponseEntity.notFound().build();
        }
        return ResponseEntity.noContent().build();
    }
}
