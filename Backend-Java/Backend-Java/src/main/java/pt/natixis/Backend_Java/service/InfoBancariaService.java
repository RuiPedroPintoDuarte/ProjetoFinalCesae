package pt.natixis.Backend_Java.service;

import org.springframework.stereotype.Service;
import pt.natixis.Backend_Java.dto.InfoBancariaRequest;
import pt.natixis.Backend_Java.model.Cliente;
import pt.natixis.Backend_Java.model.InfoBancaria;
import pt.natixis.Backend_Java.repository.ClienteRepository;
import pt.natixis.Backend_Java.repository.InfoBancariaRepository;

import java.time.LocalDate;
import java.util.List;

@Service
public class InfoBancariaService {

    private final InfoBancariaRepository infoBancariaRepository;
    private final ClienteRepository clienteRepository;

    public InfoBancariaService(
            InfoBancariaRepository infoBancariaRepository,
            ClienteRepository clienteRepository
    ) {
        this.infoBancariaRepository = infoBancariaRepository;
        this.clienteRepository = clienteRepository;
    }

    public InfoBancaria createInfoBancaria(Integer clienteId, InfoBancariaRequest request) {

        Cliente cliente = clienteRepository.findById(clienteId).orElse(null);
        if (cliente == null) {
            return null;
        }

        InfoBancaria info = new InfoBancaria();
        info.setCliente(cliente);
        setInfoBancariaData(request, info);
        info.setDataRegisto(LocalDate.now());

        return infoBancariaRepository.save(info);
    }

    public List<InfoBancaria> getAllInfoBancaria() {
        return infoBancariaRepository.findAll();
    }

    public InfoBancaria getByClienteId(Integer clienteId) {
        return infoBancariaRepository.findByClienteId(clienteId);
    }

    public InfoBancaria updateInfoBancaria(Integer clienteId, InfoBancariaRequest request) {

        InfoBancaria info = getByClienteId(clienteId);
        if (info == null) {
            return null;
        }

        setInfoBancariaData(request, info);

        return infoBancariaRepository.save(info);
    }

    public boolean deleteInfoBancaria(Integer clienteId) {
        InfoBancaria info = getByClienteId(clienteId);
        if (info == null) {
            return false;
        }
        infoBancariaRepository.delete(info);
        return true;
    }

    private void setInfoBancariaData(InfoBancariaRequest request, InfoBancaria info) {
        info.setEmprego(request.getEmprego());
        info.setEstadoCivil(request.getEstadoCivil());
        info.setEducacao(request.getEducacao());
        info.setDefaultCredit(request.getDefaultCredit());
        info.setSaldo(request.getSaldo());
        info.setEmprestimoCasa(request.getEmprestimoCasa());
        info.setEmprestimoPessoal(request.getEmprestimoPessoal());
    }
}