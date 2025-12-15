package pt.natixis.Tech_Gadgets_Hub.controller;

import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.security.crypto.password.PasswordEncoder;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;
import pt.natixis.Tech_Gadgets_Hub.dto.LoginRequest;
import pt.natixis.Tech_Gadgets_Hub.model.Utilizador;
import pt.natixis.Tech_Gadgets_Hub.service.UtilizadorService;

@RequestMapping()
@RestController
public class AuthController {

    private final UtilizadorService utilizadorService;
    private final PasswordEncoder passwordEncoder;

    public AuthController(UtilizadorService service, PasswordEncoder passwordEncoder){
        this.utilizadorService = service;
        this.passwordEncoder = passwordEncoder;
    }

    @PostMapping("/login")
    public ResponseEntity<Utilizador> login(@RequestBody LoginRequest request) {
        Utilizador utilizador = utilizadorService.getUtilizadorByUsernameOrEmail(request.getUsername(), request.getEmail());
        if(utilizador == null){
            return ResponseEntity.status(HttpStatus.UNAUTHORIZED).build();
        }
        if (!passwordEncoder.matches(request.getPassword(), utilizador.getPalavraPasse())) {
            return ResponseEntity.status(HttpStatus.UNAUTHORIZED).build();
        }
        return ResponseEntity
                .status(HttpStatus.CREATED)
                .body(utilizador);
    }
}
