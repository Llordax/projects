package com.bastion.transferencias.application.service;

import java.time.Instant;
import java.util.Objects;
import java.util.UUID;

import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import com.bastion.eventos.contrato.Evento;
import com.bastion.eventos.contrato.TiposEvento;
import com.bastion.eventos.contrato.cuentas.CreditoSolicitadoData;
import com.bastion.transferencias.application.exception.TransferenciaNoEncontradaException;
import com.bastion.transferencias.application.port.in.ProcesarDebitoRealizadoUseCase;
import com.bastion.transferencias.application.port.out.EventoOutboxPort;
import com.bastion.transferencias.application.port.out.TransferenciaRepository;
import com.bastion.transferencias.domain.model.Transferencia;

@Service
public class ProcesarDebitoRealizadoService implements ProcesarDebitoRealizadoUseCase {

    private final TransferenciaRepository transferenciaRepository;
    private final EventoOutboxPort eventoOutboxPort;

    public ProcesarDebitoRealizadoService(
            TransferenciaRepository transferenciaRepository,
            EventoOutboxPort eventoOutboxPort) {
        this.transferenciaRepository = Objects.requireNonNull(
                transferenciaRepository,
                "transferenciaRepository no puede ser null"
        );
        this.eventoOutboxPort = Objects.requireNonNull(
                eventoOutboxPort,
                "eventoOutboxPort no puede ser null"
        );
    }

    @Override
    @Transactional
    public void ejecutar(UUID transferenciaId, UUID correlationId) {
        Objects.requireNonNull(transferenciaId, "transferenciaId no puede ser null");
        Objects.requireNonNull(correlationId, "correlationId no puede ser null");

        Transferencia transferencia = transferenciaRepository.buscarPorId(transferenciaId)
                .orElseThrow(() ->
                        new TransferenciaNoEncontradaException(transferenciaId));

        transferencia.registrarDebitoRealizado();
        Transferencia guardada = transferenciaRepository.guardar(transferencia);

        UUID eventId = UUID.randomUUID();
        Evento<CreditoSolicitadoData> evento = new Evento<>(
                eventId,
                TiposEvento.CREDITO_SOLICITADO,
                1,
                Instant.now(),
                guardada.id().toString(),
                correlationId,
                new CreditoSolicitadoData(
                        guardada.id(),
                        guardada.cuentaDestinoId(),
                        guardada.importe(),
                        guardada.moneda().getCurrencyCode()
                )
        );

        eventoOutboxPort.registrar(evento);
    }
}