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
import com.bastion.cuentas.domain.model.ReglaCuentaException;
import com.bastion.cuentas.domain.port.out.CuentaRepository;

class DebitarCuentaServiceTest {

    @Test
    void debitarRestaElImporteYGuardaLaCuenta() {
        CuentaRepository cuentaRepository = mock(CuentaRepository.class);
        UUID cuentaId = UUID.randomUUID();
        Cuenta cuenta = nuevaCuenta(cuentaId);
        cuenta.acreditar(new BigDecimal("100.00"));

        when(cuentaRepository.buscarPorId(cuentaId)).thenReturn(Optional.of(cuenta));
        when(cuentaRepository.guardar(cuenta)).thenReturn(cuenta);

        DebitarCuentaService servicio = new DebitarCuentaService(cuentaRepository);

        Cuenta resultado = servicio.ejecutar(cuentaId, new BigDecimal("35.50"));

        assertThat(resultado.saldo()).isEqualByComparingTo("64.50");
        verify(cuentaRepository).guardar(cuenta);
    }

    @Test
    void debitarConSaldoInsuficienteNoGuardaLaCuenta() {
        CuentaRepository cuentaRepository = mock(CuentaRepository.class);
        UUID cuentaId = UUID.randomUUID();
        Cuenta cuenta = nuevaCuenta(cuentaId);
        cuenta.acreditar(new BigDecimal("20.00"));

        when(cuentaRepository.buscarPorId(cuentaId)).thenReturn(Optional.of(cuenta));

        DebitarCuentaService servicio = new DebitarCuentaService(cuentaRepository);

        assertThatExceptionOfType(ReglaCuentaException.class)
                .isThrownBy(() -> servicio.ejecutar(cuentaId, new BigDecimal("25.00")))
                .satisfies(excepcion -> assertThat(excepcion.codigo())
                        .isEqualTo(ReglaCuentaException.Codigo.SALDO_INSUFICIENTE));

        verify(cuentaRepository, never()).guardar(any(Cuenta.class));
    }

    @Test
    void debitarDeCuentaBloqueadaNoGuardaLaCuenta() {
        CuentaRepository cuentaRepository = mock(CuentaRepository.class);
        UUID cuentaId = UUID.randomUUID();
        Cuenta cuenta = nuevaCuenta(cuentaId);
        cuenta.acreditar(new BigDecimal("50.00"));
        cuenta.bloquear();

        when(cuentaRepository.buscarPorId(cuentaId)).thenReturn(Optional.of(cuenta));

        DebitarCuentaService servicio = new DebitarCuentaService(cuentaRepository);

        assertThatExceptionOfType(ReglaCuentaException.class)
                .isThrownBy(() -> servicio.ejecutar(cuentaId, new BigDecimal("10.00")))
                .satisfies(excepcion -> assertThat(excepcion.codigo())
                        .isEqualTo(ReglaCuentaException.Codigo.CUENTA_BLOQUEADA));

        verify(cuentaRepository, never()).guardar(any(Cuenta.class));
    }

    @Test
    void debitarCuentaInexistenteLanzaExcepcion() {
        CuentaRepository cuentaRepository = mock(CuentaRepository.class);
        UUID cuentaId = UUID.randomUUID();

        when(cuentaRepository.buscarPorId(cuentaId)).thenReturn(Optional.empty());

        DebitarCuentaService servicio = new DebitarCuentaService(cuentaRepository);

        assertThatExceptionOfType(CuentaNoEncontradaException.class)
                .isThrownBy(() -> servicio.ejecutar(cuentaId, new BigDecimal("10.00")));

        verify(cuentaRepository, never()).guardar(any(Cuenta.class));
    }

    private Cuenta nuevaCuenta(UUID cuentaId) {
        return new Cuenta(
                cuentaId,
                UUID.randomUUID(),
                Currency.getInstance("EUR")
        );
    }
}