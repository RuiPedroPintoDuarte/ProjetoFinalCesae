package pt.natixis.Backend_Java.controller;

import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;
import pt.natixis.Backend_Java.dto.TransacaoRequest;
import pt.natixis.Backend_Java.model.Transacao;
import pt.natixis.Backend_Java.service.TransacaoService;

import java.util.List;

@RestController
@RequestMapping("/transacao")
public class TransacaoController {

    private final TransacaoService service;

    public TransacaoController(TransacaoService service) {
        this.service = service;
    }

    @GetMapping
    public List<Transacao> getAll() {
        return service.getAllTransacao();
    }

    @GetMapping("/{clienteId}")
    public ResponseEntity<List<Transacao>> getByClienteId(@PathVariable Integer clienteId) {
        List<Transacao> info = service.getByClienteId(clienteId);
        if (info == null) {
            return ResponseEntity.notFound().build();
        }
        return ResponseEntity.ok(info);
    }

    @PostMapping("/{clienteId}")
    public ResponseEntity<Transacao> createTransacao(
            @PathVariable Integer clienteId,
            @RequestBody TransacaoRequest request
    ) {
        Transacao created = service.createTransacao(clienteId, request);
        if (created == null) {
            return ResponseEntity.badRequest().build();
        }
        return ResponseEntity.status(HttpStatus.CREATED).body(created);
    }
}
