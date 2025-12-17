package pt.natixis.Backend_Java.service;

import org.springframework.security.crypto.password.PasswordEncoder;
import org.springframework.stereotype.Service;
import pt.natixis.Backend_Java.dto.CriarClienteRequest;
import pt.natixis.Backend_Java.model.Cliente;
import pt.natixis.Backend_Java.model.Utilizador;
import pt.natixis.Backend_Java.repository.ClienteRepository;
import pt.natixis.Backend_Java.repository.UtilizadorRepository;

import java.time.LocalDate;
import java.util.List;

@Service
public class ClienteService {
    private final ClienteRepository repository;
    private final UtilizadorRepository utilizadorRepository;
    private final PasswordEncoder passwordEncoder;

    public ClienteService(ClienteRepository clienteRepository, UtilizadorRepository utilizadorRepository, PasswordEncoder passwordEncoder){

        this.repository = clienteRepository;
        this.utilizadorRepository = utilizadorRepository;
        this.passwordEncoder = passwordEncoder;
    }

    public List<Cliente> getAllClientes(){
        return repository.findAll();
    }

    public Cliente getClienteByClienteId(int clienteId){
        return repository.findById(clienteId);
    }

    public Cliente createCliente(CriarClienteRequest request) {
        String password = passwordEncoder.encode(request.getPassword());
        Utilizador utilizador = new Utilizador(request.getUsername(), request.getEmail(), password, "CLIENTE", true);
        utilizadorRepository.save(utilizador);
        Cliente cliente = new Cliente(utilizador, request.getNome(), LocalDate.parse(request.getDataNascimento()), request.getNif());
        return repository.save(cliente);
    }

    public Cliente updateCliente(int clienteId, CriarClienteRequest request){
        Cliente existing = repository.findById(clienteId);
        if (existing ==  null){
            return null;
        }
        Utilizador utilizador = existing.getUtilizador();
        String password = passwordEncoder.encode(request.getPassword());
        Utilizador updatedUtilizador = new Utilizador(request.getUsername(), request.getEmail(), password,
                utilizador.getRole(),utilizador.getAtivo());
        updatedUtilizador.setId(utilizador.getId());
        utilizadorRepository.save(updatedUtilizador);

        Cliente updatedCliente = new Cliente(updatedUtilizador, request.getNome(), LocalDate.parse(request.getDataNascimento()), request.getNif());
        updatedCliente.setId(existing.getId());
        return repository.save(updatedCliente);
    }
    public boolean deleteCliente(int id){
        Cliente existing = repository.findById(id);
        if (existing ==  null){
            return false;
        }
        existing.getUtilizador().setAtivo(false);
        utilizadorRepository.save(existing.getUtilizador());
        return true;
    }

}

