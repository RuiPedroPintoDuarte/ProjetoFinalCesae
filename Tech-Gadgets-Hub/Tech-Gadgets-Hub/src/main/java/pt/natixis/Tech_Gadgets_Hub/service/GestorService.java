package pt.natixis.Tech_Gadgets_Hub.service;

import org.springframework.security.crypto.password.PasswordEncoder;
import org.springframework.stereotype.Service;
import pt.natixis.Tech_Gadgets_Hub.dto.CriarUtilizadorRequest;
import pt.natixis.Tech_Gadgets_Hub.model.Gestor;
import pt.natixis.Tech_Gadgets_Hub.model.Utilizador;
import pt.natixis.Tech_Gadgets_Hub.repository.GestorRepository;
import pt.natixis.Tech_Gadgets_Hub.repository.UtilizadorRepository;
import pt.natixis.Tech_Gadgets_Hub.auth.SecurityConfig.*;

import java.util.List;

@Service
public class GestorService {

    private final GestorRepository gestorRepository;
    private final UtilizadorRepository utilizadorRepository;
    private final PasswordEncoder passwordEncoder;

    public GestorService(GestorRepository gestorRepository, UtilizadorRepository utilizadorRepository, PasswordEncoder passwordEncoder) {
        this.gestorRepository = gestorRepository;
        this.utilizadorRepository = utilizadorRepository;
        this.passwordEncoder = passwordEncoder;
    }

    public Gestor createGestor(CriarUtilizadorRequest request) {
        // Create Utilizador
        Utilizador utilizador = new Utilizador();
        utilizador.setUsername(request.getUsername());
        utilizador.setEmail(request.getEmail());
        utilizador.setPalavraPasse(
                passwordEncoder.encode(request.getPassword())
        );
        utilizador.setRole("GESTOR");
        utilizador.setAtivo(true);

        utilizador = utilizadorRepository.save(utilizador);

        // Create Gestor
        Gestor gestor = new Gestor();
        gestor.setUtilizador(utilizador);

        // Return + Persist Gestor
        return gestorRepository.save(gestor);
    }

    public List<Gestor> getAllGestores() {
        return gestorRepository.findAll();
    }

    public Gestor getGestorById(Integer id) {
        return gestorRepository
                .findById(id)
                .orElseThrow(() ->
                        new IllegalArgumentException("Gestor not found: " + id)
                );
    }

    public Gestor updateGestor(Integer id, CriarUtilizadorRequest request) {
        Gestor gestor = getGestorById(id);
        if (gestor ==  null){
            return null;
        }
        Utilizador utilizador = gestor.getUtilizador();
        String password = passwordEncoder.encode(request.getPassword());
        Utilizador updatedUtilizador = new Utilizador(request.getUsername(), request.getEmail(), password,
                utilizador.getRole(),utilizador.getAtivo());
        updatedUtilizador.setId(utilizador.getId());
        //Update Utilizador
        utilizadorRepository.save(updatedUtilizador);

        gestor.setUtilizador(updatedUtilizador);

        //Update Gestor
        return gestorRepository.save(gestor);
    }

    // Soft delete
    public boolean deactivateGestor(Integer id) {
        Gestor gestor = getGestorById(id);
        if (gestor ==  null){
            return false;
        }
        Utilizador utilizador = gestor.getUtilizador();
        utilizador.setAtivo(false);

        utilizadorRepository.save(utilizador);
        return true;
    }
}