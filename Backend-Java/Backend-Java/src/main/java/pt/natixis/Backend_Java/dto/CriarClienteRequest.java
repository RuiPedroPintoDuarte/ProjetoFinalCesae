package pt.natixis.Backend_Java.dto;

public class CriarClienteRequest {

    // Utilizador
    private String username;
    private String email;
    private String password;

    // Cliente
    private String nome;
    private String dataNascimento;
    private Integer nif;

    public String getUsername() {
        return username;
    }

    public String getEmail() {
        return email;
    }

    public String getPassword() {
        return password;
    }

    public String getNome() {
        return nome;
    }

    public String getDataNascimento() {
        return dataNascimento;
    }

    public Integer getNif() {
        return nif;
    }

    public void setUsername(String username) {
        this.username = username;
    }

    public void setEmail(String email) {
        this.email = email;
    }

    public void setPassword(String password) {
        this.password = password;
    }

    public void setNome(String nome) {
        this.nome = nome;
    }

    public void setDataNascimento(String dataNascimento) {
        this.dataNascimento = dataNascimento;
    }

    public void setNif(Integer nif) {
        this.nif = nif;
    }
}