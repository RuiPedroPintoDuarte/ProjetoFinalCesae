package pt.natixis.Backend_Java.controller;

import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;
import pt.natixis.Backend_Java.dto.CriarUtilizadorRequest;
import pt.natixis.Backend_Java.model.Gestor;
import pt.natixis.Backend_Java.service.GestorService;

import java.util.List;

@RequestMapping("/gestores")
@RestController
public class GestorController {

    private final GestorService service;

    public GestorController(GestorService service){
        this.service = service;
    }

    @GetMapping()
    public List<Gestor> getGestores() {
        return service.getAllGestores();
    }

    @GetMapping("/{id}")
    public ResponseEntity<Gestor> getGestorById(@PathVariable Integer id) {
        Gestor gestor = service.getGestorById(id);
        if (gestor == null){
            return ResponseEntity.notFound().build();
        }
        return ResponseEntity.ok(gestor);
    }

    @PostMapping("/criar-gestor")
    public ResponseEntity<Gestor> createGestor(@RequestBody CriarUtilizadorRequest createUtilizadorRequest) {
        Gestor created = service.createGestor(createUtilizadorRequest);
        if(created == null){
            return ResponseEntity.badRequest().build();
        }
        return ResponseEntity
                .status(HttpStatus.CREATED)
                .body(created);
    }

    @PutMapping("/{id}")
    public ResponseEntity<Gestor> updateGestor(@PathVariable Integer id, @RequestBody CriarUtilizadorRequest gestor) {
        Gestor updated = service.updateGestor(id, gestor);
        if (updated == null){
            return ResponseEntity.notFound().build();
        }
        return ResponseEntity.ok(updated);
    }

    @DeleteMapping("/{id}")
    public ResponseEntity<Void> deactivateGestor(@PathVariable Integer id) {
        boolean deleted = service.deactivateGestor(id);
        if (!deleted){
            return ResponseEntity.notFound().build();
        }
        return ResponseEntity.noContent().build();
    }
}
