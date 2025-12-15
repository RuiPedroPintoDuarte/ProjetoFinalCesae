package pt.natixis.Tech_Gadgets_Hub.service;

import org.springframework.stereotype.Service;
import pt.natixis.Tech_Gadgets_Hub.model.Cliente;
import pt.natixis.Tech_Gadgets_Hub.model.Utilizador;
import pt.natixis.Tech_Gadgets_Hub.repository.ClienteRepository;
import pt.natixis.Tech_Gadgets_Hub.repository.UtilizadorRepository;

import java.time.LocalDateTime;
import java.util.List;

@Service
public class UtilizadorService {

    private final UtilizadorRepository repository;

    public UtilizadorService(UtilizadorRepository utilizadorRepository) {
        this.repository = utilizadorRepository;
    }

    public Utilizador createUtilizador(Utilizador utilizador) {
        utilizador.setAtivo(true);
        return repository.save(utilizador);
    }

    public List<Utilizador> getAllUtilizadores() {
        return repository.findAll();
    }

    public Utilizador getUtilizadorById(Integer id) {
        return repository.findById(id);
    }

    public Utilizador updateUtilizador(Integer id, Utilizador updatedUtilizador) {
        Utilizador utilizador = getUtilizadorById(id);
        if (utilizador ==  null){
            return null;
        }
        updatedUtilizador.setId(id);
        return repository.save(updatedUtilizador);
    }

    // Soft delete
    public boolean deactivateUtilizador(Integer id) {
        Utilizador utilizador = getUtilizadorById(id);
        if (utilizador ==  null){
            return false;
        }
        utilizador.setAtivo(false);
        repository.save(utilizador);
        return true;
    }

    public Utilizador getUtilizadorByUsernameOrEmail(String username, String email) {
        return repository.findByUsernameOrEmail(username, email);
    }
}

