package pt.natixis.Tech_Gadgets_Hub.repository;

import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;
import pt.natixis.Tech_Gadgets_Hub.model.Cliente;
import pt.natixis.Tech_Gadgets_Hub.model.Utilizador;

import java.util.List;

@Repository
public interface UtilizadorRepository extends JpaRepository<Utilizador, Long> {
    Utilizador findById(long clienteId);
    Utilizador findByUsernameOrEmail(String username, String email);
}