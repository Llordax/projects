package com.bastion.transferencias.application.service;

import java.util.Objects;
import java.util.UUID;

import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import com.bastion.transferencias.application.exception.TransferenciaNoEncontradaException;
import com.bastion.transferencias.application.port.in.ConsultarTransferenciaUseCase;
import com.bastion.transferencias.application.port.out.TransferenciaRepository;
import com.bastion.transferencias.domain.model.Transferencia;

@Service
public class ConsultarTransferenciaService implements ConsultarTransferenciaUseCase {

    private final TransferenciaRepository transferenciaRepository;

    public ConsultarTransferenciaService(
            TransferenciaRepository transferenciaRepository) {
        this.transferenciaRepository = Objects.requireNonNull(
                transferenciaRepository,
                "transferenciaRepository no puede ser null"
        );
    }

    @Override
    @Transactional(readOnly = true)
    public Transferencia ejecutar(UUID transferenciaId) {
        Objects.requireNonNull(transferenciaId, "transferenciaId no puede ser null");

        return transferenciaRepository.buscarPorId(transferenciaId)
                .orElseThrow(() ->
                        new TransferenciaNoEncontradaException(transferenciaId));
    }
}