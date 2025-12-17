package pt.natixis.Backend_Java.service;

import org.springframework.stereotype.Service;
import pt.natixis.Backend_Java.model.Cliente;
import pt.natixis.Backend_Java.model.Gestor;
import pt.natixis.Backend_Java.model.GestorCliente;
import pt.natixis.Backend_Java.repository.ClienteRepository;
import pt.natixis.Backend_Java.repository.GestorClienteRepository;
import pt.natixis.Backend_Java.repository.GestorRepository;

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
        System.out.println(gestor);

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