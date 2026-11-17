package com.bastion.cuentas.application.service;

import static org.assertj.core.api.Assertions.assertThatExceptionOfType;
import static org.assertj.core.api.AssertionsForClassTypes.assertThat;
import static org.mockito.ArgumentMatchers.any;
import static org.mockito.Mockito.mock;
import static org.mockito.Mockito.never;
import static org.mockito.Mockito.verify;
import static org.mockito.Mockito.when;

import java.math.BigDecimal;
import java.util.Currency;
import java.util.Optional;
import java.util.UUID;

import org.junit.jupiter.api.Test;

import com.bastion.cuentas.application.exception.CuentaNoEncontradaException;
import com.bastion.cuentas.application.port.out.EventoOutboxPort;
import com.bastion.cuentas.domain.model.Cuenta;
import com.bastion.cuentas.domain.port.out.CuentaRepository;
import com.bastion.eventos.contrato.Evento;

class AcreditarCuentaServiceTest {

    @Test
    void acreditarSumaElImporteGuardaLaCuentaYRegistraEvento() {
        CuentaRepository cuentaRepository = mock(CuentaRepository.class);
        EventoOutboxPort eventoOutboxPort = mock(EventoOutboxPort.class);
        UUID cuentaId = UUID.randomUUID();
        UUID transferenciaId = UUID.randomUUID();
        Cuenta cuenta = nuevaCuenta(cuentaId);

        when(cuentaRepository.buscarPorId(cuentaId)).thenReturn(Optional.of(cuenta));
        when(cuentaRepository.guardar(cuenta)).thenReturn(cuenta);

        AcreditarCuentaService servicio = new AcreditarCuentaService(
                cuentaRepository,
                eventoOutboxPort
        );

        Cuenta resultado = servicio.ejecutar(
                cuentaId,
                transferenciaId,
                new BigDecimal("25.50")
        );

        assertThat(resultado).isSameAs(cuenta);
        assertThat(resultado.saldo()).isEqualByComparingTo("25.50");
        verify(cuentaRepository).guardar(cuenta);
        verify(eventoOutboxPort).registrar(any(Evento.class));
    }

    @Test
    void acreditarCuentaInexistenteLanzaExcepcionYNoRegistraEvento() {
        CuentaRepository cuentaRepository = mock(CuentaRepository.class);
        EventoOutboxPort eventoOutboxPort = mock(EventoOutboxPort.class);
        UUID cuentaId = UUID.randomUUID();
        UUID transferenciaId = UUID.randomUUID();

        when(cuentaRepository.buscarPorId(cuentaId)).thenReturn(Optional.empty());

        AcreditarCuentaService servicio = new AcreditarCuentaService(
                cuentaRepository,
                eventoOutboxPort
        );

        assertThatExceptionOfType(CuentaNoEncontradaException.class)
                .isThrownBy(() -> servicio.ejecutar(
                        cuentaId,
                        transferenciaId,
                        new BigDecimal("10.00")
                ));

        verify(cuentaRepository, never()).guardar(any(Cuenta.class));
        verify(eventoOutboxPort, never()).registrar(any(Evento.class));
    }

    @Test
    void acreditarConImporteCeroLanzaExcepcionYNoRegistraEvento() {
        CuentaRepository cuentaRepository = mock(CuentaRepository.class);
        EventoOutboxPort eventoOutboxPort = mock(EventoOutboxPort.class);
        UUID cuentaId = UUID.randomUUID();
        UUID transferenciaId = UUID.randomUUID();
        Cuenta cuenta = nuevaCuenta(cuentaId);

        when(cuentaRepository.buscarPorId(cuentaId)).thenReturn(Optional.of(cuenta));

        AcreditarCuentaService servicio = new AcreditarCuentaService(
                cuentaRepository,
                eventoOutboxPort
        );

        assertThatExceptionOfType(IllegalArgumentException.class)
                .isThrownBy(() -> servicio.ejecutar(
                        cuentaId,
                        transferenciaId,
                        BigDecimal.ZERO
                ));

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