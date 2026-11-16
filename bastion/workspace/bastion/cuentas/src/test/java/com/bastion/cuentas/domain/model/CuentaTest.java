package com.bastion.cuentas.domain.model;

import static org.assertj.core.api.Assertions.*;

import java.math.BigDecimal;
import java.util.Currency;
import java.util.UUID;

import org.junit.jupiter.api.Test;

class CuentaTest {

    @Test
    void cuentaNuevaEmpiezaActivaYConSaldoCero() {
        Cuenta cuenta = nuevaCuenta();

        assertThat(cuenta.estado()).isEqualTo(EstadoCuenta.ACTIVA);
        assertThat(cuenta.saldo()).isEqualByComparingTo(BigDecimal.ZERO);
    }

    @Test
    void debitarReduceElSaldo() {
        Cuenta cuenta = nuevaCuenta();
        cuenta.acreditar(new BigDecimal("100.00"));

        cuenta.debitar(new BigDecimal("35.50"));

        assertThat(cuenta.saldo()).isEqualByComparingTo("64.50");
    }

    @Test
    void debitarConSaldoInsuficienteLanzaErrorDeDominio() {
        Cuenta cuenta = nuevaCuenta();
        cuenta.acreditar(new BigDecimal("20.00"));

        assertThatExceptionOfType(ReglaCuentaException.class)
                .isThrownBy(() -> cuenta.debitar(new BigDecimal("25.00")))
                .satisfies(excepcion ->
                        assertThat(excepcion.codigo())
                                .isEqualTo(ReglaCuentaException.Codigo.SALDO_INSUFICIENTE)
                );
    }

    @Test
    void cuentaBloqueadaNoPermiteDebitar() {
        Cuenta cuenta = nuevaCuenta();
        cuenta.acreditar(new BigDecimal("50.00"));
        cuenta.bloquear();

        assertThatExceptionOfType(ReglaCuentaException.class)
                .isThrownBy(() -> cuenta.debitar(new BigDecimal("10.00")))
                .satisfies(excepcion ->
                        assertThat(excepcion.codigo())
                                .isEqualTo(ReglaCuentaException.Codigo.CUENTA_BLOQUEADA)
                );
    }

    @Test
    void cuentaBloqueadaPuedeRecibirUnAbono() {
        Cuenta cuenta = nuevaCuenta();
        cuenta.bloquear();

        cuenta.acreditar(new BigDecimal("15.00"));

        assertThat(cuenta.estado()).isEqualTo(EstadoCuenta.BLOQUEADA);
        assertThat(cuenta.saldo()).isEqualByComparingTo("15.00");
    }

    @Test
    void bloquearYDesbloquearDevuelvenSiHuboUnCambio() {
        Cuenta cuenta = nuevaCuenta();

        assertThat(cuenta.bloquear()).isTrue();
        assertThat(cuenta.bloquear()).isFalse();
        assertThat(cuenta.desbloquear()).isTrue();
        assertThat(cuenta.desbloquear()).isFalse();
    }

    private Cuenta nuevaCuenta() {
        return new Cuenta(
                UUID.randomUUID(),
                UUID.randomUUID(),
                Currency.getInstance("EUR")
        );
    }
}