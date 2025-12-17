package pt.natixis.Backend_Java.repository;

import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;
import pt.natixis.Backend_Java.model.Transacao;

import java.util.List;

@Repository
public interface TransacaoRepository extends JpaRepository<Transacao, Integer> {
    Transacao findById(int id);
    List<Transacao> findByClienteId(Integer clienteId);
}
