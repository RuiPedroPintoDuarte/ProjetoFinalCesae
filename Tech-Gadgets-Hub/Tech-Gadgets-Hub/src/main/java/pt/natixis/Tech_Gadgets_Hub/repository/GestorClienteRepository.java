package pt.natixis.Tech_Gadgets_Hub.repository;

import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;
import pt.natixis.Tech_Gadgets_Hub.model.GestorCliente;

import java.util.List;

@Repository
public interface GestorClienteRepository extends JpaRepository<GestorCliente, Integer> {

    List<GestorCliente> findByGestor_Id(Integer gestorId);

    boolean existsByGestor_IdAndCliente_Id(Integer gestorId, Integer clienteId);
}