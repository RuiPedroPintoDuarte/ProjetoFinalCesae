package pt.natixis.Backend_Java.repository;

import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;
import pt.natixis.Backend_Java.model.Gestor;

@Repository
public interface GestorRepository extends JpaRepository<Gestor, Integer> {
    Gestor findById(int id);
}