package pt.natixis.Tech_Gadgets_Hub.repository;

import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;
import pt.natixis.Tech_Gadgets_Hub.model.Cliente;
import pt.natixis.Tech_Gadgets_Hub.model.Gestor;
import pt.natixis.Tech_Gadgets_Hub.model.InfoBancaria;

@Repository
public interface InfoBancariaRepository extends JpaRepository<InfoBancaria, Integer> {
    InfoBancaria findByClienteId(Integer clienteId);
}