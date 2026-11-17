package com.bastion.cuentas.application.service;

import static org.assertj.core.api.Assertions.assertThatExceptionOfType;
import static org.assertj.core.api.AssertionsForClassTypes.assertThat;
import static org.mockito.ArgumentMatchers.any;
import static org.mockito.Mockito.mock;
import static org.mockito.Mockito.never;
import static org.mockito.Mockito.verify;
import static org.mockito.Mockito.when;

import java.util.Currency;
import java.util.Optional;
import java.util.UUID;

import org.junit.jupiter.api.Test;

import com.bastion.cuentas.application.exception.CuentaNoEncontradaException;
import com.bastion.cuentas.application.port.out.EventoOutboxPort;
import com.bastion.cuentas.domain.model.Cuenta;
import com.bastion.cuentas.domain.model.EstadoCuenta;
import com.bastion.cuentas.domain.port.out.CuentaRepository;
import com.bastion.eventos.contrato.Evento;

class BloquearCuentaServiceTest {

    @Test
    void bloquearCuentaGuardaYRegistraEventoCuandoCambiaElEstado() {
        CuentaRepository cuentaRepository = mock(CuentaRepository.class);
        EventoOutboxPort eventoOutboxPort = mock(EventoOutboxPort.class);
        UUID cuentaId = UUID.randomUUID();
        Cuenta cuenta = nuevaCuenta(cuentaId);

        when(cuentaRepository.buscarPorId(cuentaId)).thenReturn(Optional.of(cuenta));
        when(cuentaRepository.guardar(cuenta)).thenReturn(cuenta);

        BloquearCuentaService servicio = new BloquearCuentaService(
                cuentaRepository,
                eventoOutboxPort
        );

        boolean cambioRealizado = servicio.ejecutar(cuentaId, "Solicitud del titular");

        assertThat(cambioRealizado).isTrue();
        assertThat(cuenta.estado()).isEqualTo(EstadoCuenta.BLOQUEADA);
        verify(cuentaRepository).guardar(cuenta);
        verify(eventoOutboxPort).registrar(any(Evento.class));
    }

    @Test
    void bloquearCuentaNoGuardaNiRegistraEventoSiYaEstabaBloqueada() {
        CuentaRepository cuentaRepository = mock(CuentaRepository.class);
        EventoOutboxPort eventoOutboxPort = mock(EventoOutboxPort.class);
        UUID cuentaId = UUID.randomUUID();
        Cuenta cuenta = nuevaCuenta(cuentaId);
        cuenta.bloquear();

        when(cuentaRepository.buscarPorId(cuentaId)).thenReturn(Optional.of(cuenta));

        BloquearCuentaService servicio = new BloquearCuentaService(
                cuentaRepository,
                eventoOutboxPort
        );

        boolean cambioRealizado = servicio.ejecutar(cuentaId, "Solicitud del titular");

        assertThat(cambioRealizado).isFalse();
        verify(cuentaRepository, never()).guardar(any(Cuenta.class));
        verify(eventoOutboxPort, never()).registrar(any(Evento.class));
    }

    @Test
    void bloquearCuentaInexistenteLanzaExcepcionYNoRegistraEvento() {
        CuentaRepository cuentaRepository = mock(CuentaRepository.class);
        EventoOutboxPort eventoOutboxPort = mock(EventoOutboxPort.class);
        UUID cuentaId = UUID.randomUUID();

        when(cuentaRepository.buscarPorId(cuentaId)).thenReturn(Optional.empty());

        BloquearCuentaService servicio = new BloquearCuentaService(
                cuentaRepository,
                eventoOutboxPort
        );

        assertThatExceptionOfType(CuentaNoEncontradaException.class)
                .isThrownBy(() -> servicio.ejecutar(cuentaId, "Solicitud del titular"));

        verify(cuentaRepository, never()).guardar(any(Cuenta.class));
        verify(eventoOutboxPort, never()).registrar(any(Evento.class));
    }

    private Cuenta nuevaCuenta(UUID cuentaId) {
        return new Cuenta(
                cuentaId,
                UUID.randomUUID(),
                Currency.getInstance("EUR")
        );
    }
}