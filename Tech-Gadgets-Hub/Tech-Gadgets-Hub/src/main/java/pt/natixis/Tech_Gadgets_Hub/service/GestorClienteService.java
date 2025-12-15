package pt.natixis.Tech_Gadgets_Hub.service;

import org.springframework.stereotype.Service;
import pt.natixis.Tech_Gadgets_Hub.model.Cliente;
import pt.natixis.Tech_Gadgets_Hub.model.Gestor;
import pt.natixis.Tech_Gadgets_Hub.model.GestorCliente;
import pt.natixis.Tech_Gadgets_Hub.repository.ClienteRepository;
import pt.natixis.Tech_Gadgets_Hub.repository.GestorClienteRepository;
import pt.natixis.Tech_Gadgets_Hub.repository.GestorRepository;

import java.util.List;
import java.util.stream.Collectors;

@Service
public class GestorClienteService {

    private final GestorClienteRepository gestorClienteRepository;
    private final GestorRepository gestorRepository;
    private final ClienteRepository clienteRepository;

    public GestorClienteService(
            GestorClienteRepository gestorClienteRepository,
            GestorRepository gestorRepository,
            ClienteRepository clienteRepository
    ) {
        this.gestorClienteRepository = gestorClienteRepository;
        this.gestorRepository = gestorRepository;
        this.clienteRepository = clienteRepository;
    }

    public List<GestorCliente> getAllGestorClientes() {
        return gestorClienteRepository.findAll();
    }

    public List<Cliente> getClientesByGestor(Integer gestorId) {

        List<GestorCliente> relations =
                gestorClienteRepository.findByGestor_Id(gestorId);

        return relations.stream()
                .map(GestorCliente::getCliente)
                .collect(Collectors.toList());
    }

    public void associarClientes(Integer gestorId, List<Integer> clienteIds) {
        Gestor gestor = gestorRepository.findById(gestorId)
                .orElseThrow(() ->
                        new IllegalArgumentException("Gestor not found: " + gestorId)
                );

        for (Integer clienteId : clienteIds) {
            Cliente cliente = clienteRepository
                    .findById(clienteId)
                    .orElseThrow(() ->
                            new IllegalArgumentException("Gestor not found: " + clienteId)
                    );
            if (cliente == null) {
                throw new IllegalArgumentException("Cliente not found: " + clienteId);
            }

            boolean alreadyExists =
                    gestorClienteRepository.existsByGestor_IdAndCliente_Id(gestorId, clienteId);

            if (!alreadyExists) {
                GestorCliente gc = new GestorCliente(gestor, cliente);
                gestorClienteRepository.save(gc);
            }
        }
    }
}