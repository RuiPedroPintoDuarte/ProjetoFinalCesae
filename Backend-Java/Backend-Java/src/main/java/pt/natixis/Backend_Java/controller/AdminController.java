package pt.natixis.Backend_Java.controller;

import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;
import pt.natixis.Backend_Java.dto.CriarUtilizadorRequest;
import pt.natixis.Backend_Java.model.Admin;
import pt.natixis.Backend_Java.service.AdminService;

import java.util.List;

@RequestMapping("/admins")
@RestController
public class AdminController {

    private final AdminService service;

    public AdminController(AdminService service){
        this.service = service;
    }

    @GetMapping()
    public List<Admin> getAdmins() {
        return service.getAllAdmins();
    }

    @GetMapping("/{id}")
    public ResponseEntity<Admin> getAdminById(@PathVariable Integer id) {
        Admin admin = service.getAdminById(id);
        if (admin == null){
            return ResponseEntity.notFound().build();
        }
        return ResponseEntity.ok(admin);
    }

    @PostMapping("/criar-admin")
    public ResponseEntity<Admin> createAdmin(@RequestBody CriarUtilizadorRequest createUtilizadorRequest) {
        Admin created = service.createAdmin(createUtilizadorRequest);
        if(created == null){
            return ResponseEntity.badRequest().build();
        }
        return ResponseEntity
                .status(HttpStatus.CREATED)
                .body(created);
    }

    @PutMapping("/{id}")
    public ResponseEntity<Admin> updateAdmin(@PathVariable Integer id, @RequestBody CriarUtilizadorRequest admin) {
        Admin updated = service.updateAdmin(id, admin);
        if (updated == null){
            return ResponseEntity.notFound().build();
        }
        return ResponseEntity.ok(updated);
    }

    @DeleteMapping("/{id}")
    public ResponseEntity<Void> deactivateAdmin(@PathVariable Integer id) {
        boolean deleted = service.deactivateAdmin(id);
        if (!deleted){
            return ResponseEntity.notFound().build();
        }
        return ResponseEntity.noContent().build();
    }
}
