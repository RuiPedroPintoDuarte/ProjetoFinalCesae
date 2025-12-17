package pt.natixis.Backend_Java.controller;

import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;
import pt.natixis.Backend_Java.model.InfoBancaria;
import pt.natixis.Backend_Java.service.InfoBancariaService;
import pt.natixis.Backend_Java.MachineLearning;

@RestController
@RequestMapping("/modelo")
public class MachineLearningController {

    private final InfoBancariaService service;

    public MachineLearningController(InfoBancariaService service) {
        this.service = service;
    }

    @GetMapping("/{clienteId}")
    public ResponseEntity<Double> getByClienteId(@PathVariable Integer clienteId) {
        InfoBancaria info = service.getByClienteId(clienteId);
        if (info == null) {
            return ResponseEntity.notFound().build();
        }
        double prediction = MachineLearning.predict(info);
        return ResponseEntity.ok(prediction);
    }
}
