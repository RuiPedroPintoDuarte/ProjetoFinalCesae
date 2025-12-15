package pt.natixis.Tech_Gadgets_Hub.repository;

import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;
import pt.natixis.Tech_Gadgets_Hub.model.Gestor;
import pt.natixis.Tech_Gadgets_Hub.model.Utilizador;

import java.util.Optional;

@Repository
public interface GestorRepository extends JpaRepository<Gestor, Integer> {
    Gestor findById(int id);
}