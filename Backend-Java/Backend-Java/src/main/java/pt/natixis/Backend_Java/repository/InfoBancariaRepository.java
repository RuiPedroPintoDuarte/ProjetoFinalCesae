package pt.natixis.Backend_Java.repository;

import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;
import pt.natixis.Backend_Java.model.InfoBancaria;

@Repository
public interface InfoBancariaRepository extends JpaRepository<InfoBancaria, Integer> {
    InfoBancaria findByClienteId(Integer clienteId);
}