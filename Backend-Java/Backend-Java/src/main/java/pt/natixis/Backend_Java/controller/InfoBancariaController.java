package pt.natixis.Backend_Java.controller;

import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;
import pt.natixis.Backend_Java.dto.InfoBancariaRequest;
import pt.natixis.Backend_Java.model.InfoBancaria;
import pt.natixis.Backend_Java.service.InfoBancariaService;

import java.util.List;

@RestController
@RequestMapping("/info-bancaria")
public class InfoBancariaController {

    private final InfoBancariaService service;

    public InfoBancariaController(InfoBancariaService service) {
        this.service = service;
    }

    @GetMapping
    public List<InfoBancaria> getAll() {
        return service.getAllInfoBancaria();
    }

    @GetMapping("/{clienteId}")
    public ResponseEntity<InfoBancaria> getByClienteId(@PathVariable Integer clienteId) {
        InfoBancaria info = service.getByClienteId(clienteId);
        if (info == null) {
            return ResponseEntity.notFound().build();
        }
        return ResponseEntity.ok(info);
    }

    @PostMapping("/{clienteId}")
    public ResponseEntity<InfoBancaria> createInfoBancaria(
            @PathVariable Integer clienteId,
            @RequestBody InfoBancariaRequest request
    ) {
        InfoBancaria created = service.createInfoBancaria(clienteId, request);
        if (created == null) {
            return ResponseEntity.badRequest().build();
        }
        return ResponseEntity.status(HttpStatus.CREATED).body(created);
    }

    @PutMapping("/{clienteId}")
    public ResponseEntity<InfoBancaria> updateInfoBancaria(
            @PathVariable Integer clienteId,
            @RequestBody InfoBancariaRequest request
    ) {
        InfoBancaria updated = service.updateInfoBancaria(clienteId, request);
        if (updated == null) {
            return ResponseEntity.notFound().build();
        }
        return ResponseEntity.ok(updated);
    }
}