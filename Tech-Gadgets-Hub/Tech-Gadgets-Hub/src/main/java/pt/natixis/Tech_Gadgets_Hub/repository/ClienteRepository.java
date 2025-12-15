package pt.natixis.Tech_Gadgets_Hub.repository;

import pt.natixis.Tech_Gadgets_Hub.model.Cliente;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import java.util.List;

@Repository
public interface ClienteRepository extends JpaRepository<Cliente, Integer> {
    Cliente findById(int clienteId);
}