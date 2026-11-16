package com.bastion.cuentas.application.service;

import static org.assertj.core.api.Assertions.assertThatExceptionOfType;
import static org.assertj.core.api.AssertionsForClassTypes.assertThat;
import static org.mockito.Mockito.mock;
import static org.mockito.Mockito.never;
import static org.mockito.Mockito.verify;
import static org.mockito.Mockito.when;

import java.util.Currency;
import java.util.Optional;
import java.util.UUID;

import org.junit.jupiter.api.Test;

import com.bastion.cuentas.application.exception.CuentaNoEncontradaException;
import com.bastion.cuentas.domain.model.Cuenta;
import com.bastion.cuentas.domain.port.out.CuentaRepository;

class BloquearCuentaServiceTest {

    @Test
    void bloquearCuentaGuardaCuandoCambiaElEstado() {
        CuentaRepository cuentaRepository = mock(CuentaRepository.class);
        UUID cuentaId = UUID.randomUUID();
        Cuenta cuenta = new Cuenta(
                cuentaId,
                UUID.randomUUID(),
                Currency.getInstance("EUR")
        );

        when(cuentaRepository.buscarPorId(cuentaId)).thenReturn(Optional.of(cuenta));

        BloquearCuentaService servicio = new BloquearCuentaService(cuentaRepository);

        boolean cambioRealizado = servicio.ejecutar(cuentaId);

        assertThat(cambioRealizado).isTrue();
        assertThat(cuenta.estado()).isEqualTo(com.bastion.cuentas.domain.model.EstadoCuenta.BLOQUEADA);
        verify(cuentaRepository).guardar(cuenta);
    }

    @Test
    void bloquearCuentaNoGuardaSiYaEstabaBloqueada() {
        CuentaRepository cuentaRepository = mock(CuentaRepository.class);
        UUID cuentaId = UUID.randomUUID();
        Cuenta cuenta = new Cuenta(
                cuentaId,
                UUID.randomUUID(),
                Currency.getInstance("EUR")
        );
        cuenta.bloquear();

        when(cuentaRepository.buscarPorId(cuentaId)).thenReturn(Optional.of(cuenta));

        BloquearCuentaService servicio = new BloquearCuentaService(cuentaRepository);

        boolean cambioRealizado = servicio.ejecutar(cuentaId);

        assertThat(cambioRealizado).isFalse();
        verify(cuentaRepository, never()).guardar(cuenta);
    }

    @Test
    void bloquearCuentaInexistenteLanzaExcepcion() {
        CuentaRepository cuentaRepository = mock(CuentaRepository.class);
        UUID cuentaId = UUID.randomUUID();

        when(cuentaRepository.buscarPorId(cuentaId)).thenReturn(Optional.empty());

        BloquearCuentaService servicio = new BloquearCuentaService(cuentaRepository);

        assertThatExceptionOfType(CuentaNoEncontradaException.class)
                .isThrownBy(() -> servicio.ejecutar(cuentaId))
                .satisfies(excepcion -> assertThat(excepcion.cuentaId()).isEqualTo(cuentaId));

        verify(cuentaRepository, never()).guardar(org.mockito.ArgumentMatchers.any());
    }
}