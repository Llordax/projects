package com.bastion.transferencias.application.service;

import static org.assertj.core.api.AssertionsForClassTypes.assertThat;
import static org.junit.jupiter.api.Assertions.assertThrows;
import static org.mockito.ArgumentMatchers.any;
import static org.mockito.Mockito.mock;
import static org.mockito.Mockito.never;
import static org.mockito.Mockito.verify;
import static org.mockito.Mockito.when;

import java.math.BigDecimal;
import java.util.Currency;
import java.util.UUID;

import org.junit.jupiter.api.Test;

import com.bastion.eventos.contrato.Evento;
import com.bastion.transferencias.application.port.out.EventoOutboxPort;
import com.bastion.transferencias.application.port.out.TransferenciaRepository;
import com.bastion.transferencias.domain.model.EstadoTransferencia;
import com.bastion.transferencias.domain.model.Transferencia;

class SolicitarTransferenciaServiceTest {

    @Test
    void solicitarTransferenciaGuardaYRegistraEvento() {
        TransferenciaRepository transferenciaRepository =
                mock(TransferenciaRepository.class);
        EventoOutboxPort eventoOutboxPort = mock(EventoOutboxPort.class);

        when(transferenciaRepository.guardar(any(Transferencia.class)))
                .thenAnswer(invocacion -> invocacion.getArgument(0));

        SolicitarTransferenciaService servicio = new SolicitarTransferenciaService(
                transferenciaRepository,
                eventoOutboxPort
        );

        UUID cuentaOrigenId = UUID.randomUUID();
        UUID cuentaDestinoId = UUID.randomUUID();

        Transferencia transferencia = servicio.ejecutar(
                cuentaOrigenId,
                cuentaDestinoId,
                new BigDecimal("25.00"),
                Currency.getInstance("EUR")
        );

        assertThat(transferencia.id()).isNotNull();
        assertThat(transferencia.cuentaOrigenId()).isEqualTo(cuentaOrigenId);
        assertThat(transferencia.cuentaDestinoId()).isEqualTo(cuentaDestinoId);
        assertThat(transferencia.importe()).isEqualByComparingTo("25.00");
        assertThat(transferencia.estado())
                .isEqualTo(EstadoTransferencia.PENDIENTE_ANTIFRAUDE);

        verify(transferenciaRepository).guardar(transferencia);
        verify(eventoOutboxPort).registrar(any(Evento.class));
    }

    @Test
    void solicitarTransferenciaALaMismaCuentaNoGuardaNiRegistraEvento() {
        TransferenciaRepository transferenciaRepository =
                mock(TransferenciaRepository.class);
        EventoOutboxPort eventoOutboxPort = mock(EventoOutboxPort.class);
        SolicitarTransferenciaService servicio = new SolicitarTransferenciaService(
                transferenciaRepository,
                eventoOutboxPort
        );
        UUID cuentaId = UUID.randomUUID();

        assertThrows(
                IllegalArgumentException.class,
                () -> servicio.ejecutar(
                        cuentaId,
                        cuentaId,
                        new BigDecimal("25.00"),
                        Currency.getInstance("EUR")
                )
        );

        verify(transferenciaRepository, never()).guardar(any(Transferencia.class));
        verify(eventoOutboxPort, never()).registrar(any(Evento.class));
    }
}