package com.bastion.transferencias.application.service;

import java.util.Objects;
import java.util.UUID;

import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import com.bastion.transferencias.application.exception.TransferenciaNoEncontradaException;
import com.bastion.transferencias.application.port.in.ProcesarCompensacionRechazadaUseCase;
import com.bastion.transferencias.application.port.out.TransferenciaRepository;
import com.bastion.transferencias.domain.model.Transferencia;

@Service
public class ProcesarCompensacionRechazadaService
        implements ProcesarCompensacionRechazadaUseCase {

    private final TransferenciaRepository transferenciaRepository;

    public ProcesarCompensacionRechazadaService(
            TransferenciaRepository transferenciaRepository) {
        this.transferenciaRepository = Objects.requireNonNull(
                transferenciaRepository,
                "transferenciaRepository no puede ser null"
        );
    }

    @Override
    @Transactional
    public void ejecutar(UUID transferenciaId, String motivo) {
        Objects.requireNonNull(transferenciaId, "transferenciaId no puede ser null");

        Transferencia transferencia = transferenciaRepository.buscarPorId(transferenciaId)
                .orElseThrow(() ->
                        new TransferenciaNoEncontradaException(transferenciaId));

        transferencia.registrarCompensacionRechazada(motivo);
        transferenciaRepository.guardar(transferencia);
    }
}