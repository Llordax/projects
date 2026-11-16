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
import com.bastion.cuentas.domain.model.Cuenta;
import com.bastion.cuentas.domain.port.out.CuentaRepository;

class AcreditarCuentaServiceTest {

    @Test
    void acreditarSumaElImporteYGuardaLaCuenta() {
        CuentaRepository cuentaRepository = mock(CuentaRepository.class);
        UUID cuentaId = UUID.randomUUID();
        Cuenta cuenta = new Cuenta(
                cuentaId,
                UUID.randomUUID(),
                Currency.getInstance("EUR")
        );

        when(cuentaRepository.buscarPorId(cuentaId)).thenReturn(Optional.of(cuenta));
        when(cuentaRepository.guardar(cuenta)).thenReturn(cuenta);

        AcreditarCuentaService servicio = new AcreditarCuentaService(cuentaRepository);

        Cuenta resultado = servicio.ejecutar(cuentaId, new BigDecimal("25.50"));

        assertThat(resultado).isSameAs(cuenta);
        assertThat(resultado.saldo()).isEqualByComparingTo("25.50");
        verify(cuentaRepository).guardar(cuenta);
    }

    @Test
    void acreditarCuentaInexistenteLanzaExcepcion() {
        CuentaRepository cuentaRepository = mock(CuentaRepository.class);
        UUID cuentaId = UUID.randomUUID();

        when(cuentaRepository.buscarPorId(cuentaId)).thenReturn(Optional.empty());

        AcreditarCuentaService servicio = new AcreditarCuentaService(cuentaRepository);

        assertThatExceptionOfType(CuentaNoEncontradaException.class)
                .isThrownBy(() -> servicio.ejecutar(cuentaId, new BigDecimal("10.00")));

        verify(cuentaRepository, never()).guardar(any(Cuenta.class));
    }

    @Test
    void acreditarConImporteCeroNoGuardaLaCuenta() {
        CuentaRepository cuentaRepository = mock(CuentaRepository.class);
        UUID cuentaId = UUID.randomUUID();
        Cuenta cuenta = new Cuenta(
                cuentaId,
                UUID.randomUUID(),
                Currency.getInstance("EUR")
        );

        when(cuentaRepository.buscarPorId(cuentaId)).thenReturn(Optional.of(cuenta));

        AcreditarCuentaService servicio = new AcreditarCuentaService(cuentaRepository);

        assertThatExceptionOfType(IllegalArgumentException.class)
                .isThrownBy(() -> servicio.ejecutar(cuentaId, BigDecimal.ZERO));

        verify(cuentaRepository, never()).guardar(any(Cuenta.class));
    }
}