package pt.natixis.Tech_Gadgets_Hub.repository;

import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;
import pt.natixis.Tech_Gadgets_Hub.model.Admin;
import pt.natixis.Tech_Gadgets_Hub.model.Transacao;

import java.util.List;

@Repository
public interface TransacaoRepository extends JpaRepository<Transacao, Integer> {
    Transacao findById(int id);
    List<Transacao> findByClienteId(Integer clienteId);
}
