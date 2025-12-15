package pt.natixis.Tech_Gadgets_Hub.service;

import org.springframework.stereotype.Service;
import pt.natixis.Tech_Gadgets_Hub.dto.TransacaoRequest;
import pt.natixis.Tech_Gadgets_Hub.model.Cliente;
import pt.natixis.Tech_Gadgets_Hub.model.Transacao;
import pt.natixis.Tech_Gadgets_Hub.repository.ClienteRepository;
import pt.natixis.Tech_Gadgets_Hub.repository.TransacaoRepository;

import java.time.LocalDate;
import java.util.List;

@Service
public class TransacaoService {

    private final TransacaoRepository transacaoRepository;
    private final ClienteRepository clienteRepository;

    public TransacaoService( TransacaoRepository transacaoRepository, ClienteRepository clienteRepository) {
        this.transacaoRepository = transacaoRepository;
        this.clienteRepository = clienteRepository;
    }

    public Transacao createTransacao(Integer clienteId, TransacaoRequest request) {

        Cliente cliente = clienteRepository.findById(clienteId).orElse(null);
        if (cliente == null) {
            return null;
        }

        Transacao info = new Transacao();
        info.setCliente(cliente);
        setTransacaoData(request, info);

        return transacaoRepository.save(info);
    }

    public List<Transacao> getAllTransacao() {
        return transacaoRepository.findAll();
    }

    public List<Transacao> getByClienteId(Integer clienteId) {
        return transacaoRepository.findByClienteId(clienteId);
    }

    private void setTransacaoData(TransacaoRequest request, Transacao info) {
        info.setDataTransacao(LocalDate.parse(request.getDataTransacao()));
        info.setCategoria(request.getCategoria());
        info.setDescricao(request.getDescricao());
        info.setQuantidade(request.getQuantidade());
    }
}
