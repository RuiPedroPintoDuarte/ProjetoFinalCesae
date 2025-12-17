package pt.natixis.Backend_Java.service;

import org.springframework.security.crypto.password.PasswordEncoder;
import org.springframework.stereotype.Service;
import pt.natixis.Backend_Java.dto.CriarUtilizadorRequest;
import pt.natixis.Backend_Java.model.Admin;
import pt.natixis.Backend_Java.model.Utilizador;
import pt.natixis.Backend_Java.repository.AdminRepository;
import pt.natixis.Backend_Java.repository.UtilizadorRepository;

import java.util.List;

@Service
public class AdminService {

    private final AdminRepository adminRepository;
    private final UtilizadorRepository utilizadorRepository;
    private final PasswordEncoder passwordEncoder;

    public AdminService(AdminRepository adminRepository, UtilizadorRepository utilizadorRepository, PasswordEncoder passwordEncoder) {
        this.adminRepository = adminRepository;
        this.utilizadorRepository = utilizadorRepository;
        this.passwordEncoder = passwordEncoder;
    }

    public Admin createAdmin(CriarUtilizadorRequest request) {
        // Create Utilizador
        Utilizador utilizador = new Utilizador();
        utilizador.setUsername(request.getUsername());
        utilizador.setEmail(request.getEmail());
        utilizador.setPalavraPasse(
                passwordEncoder.encode(request.getPassword())
        );
        utilizador.setRole("ADMIN");
        utilizador.setAtivo(true);

        utilizador = utilizadorRepository.save(utilizador);

        // Create Admin
        Admin admin = new Admin();
        admin.setUtilizador(utilizador);

        // Return + Persist Admin
        return adminRepository.save(admin);
    }

    public List<Admin> getAllAdmins() {
        return adminRepository.findAll();
    }

    public Admin getAdminById(Integer id) {
        return adminRepository
                .findById(id)
                .orElseThrow(() ->
                        new IllegalArgumentException("Admin not found: " + id)
                );
    }

    public Admin updateAdmin(Integer id, CriarUtilizadorRequest request) {
        Admin admin = getAdminById(id);
        if (admin ==  null){
            return null;
        }
        Utilizador utilizador = admin.getUtilizador();
        String password = passwordEncoder.encode(request.getPassword());
        Utilizador updatedUtilizador = new Utilizador(request.getUsername(), request.getEmail(), password,
                utilizador.getRole(),utilizador.getAtivo());
        updatedUtilizador.setId(utilizador.getId());
        //Update Utilizador
        utilizadorRepository.save(updatedUtilizador);

        admin.setUtilizador(updatedUtilizador);

        //Update Admin
        return adminRepository.save(admin);
    }

    // Soft delete
    public boolean deactivateAdmin(Integer id) {
        Admin admin = getAdminById(id);
        if (admin ==  null){
            return false;
        }
        Utilizador utilizador = admin.getUtilizador();
        utilizador.setAtivo(false);

        utilizadorRepository.save(utilizador);
        return true;
    }
}