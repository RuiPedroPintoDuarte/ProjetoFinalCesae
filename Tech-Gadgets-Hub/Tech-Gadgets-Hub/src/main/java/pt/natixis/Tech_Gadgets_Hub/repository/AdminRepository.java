package pt.natixis.Tech_Gadgets_Hub.repository;

import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;
import pt.natixis.Tech_Gadgets_Hub.model.Admin;

@Repository
public interface AdminRepository extends JpaRepository<Admin, Integer> {
    Admin findById(int id);
}