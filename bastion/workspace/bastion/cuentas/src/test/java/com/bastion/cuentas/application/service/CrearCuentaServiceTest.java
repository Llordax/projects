package com.bastion.cuentas.application.service;

import static org.assertj.core.api.AssertionsForClassTypes.assertThat;
import static org.mockito.ArgumentMatchers.any;
import static org.mockito.Mockito.mock;
import static org.mockito.Mockito.verify;
import static org.mockito.Mockito.when;

import java.util.Currency;
import java.util.UUID;

import org.junit.jupiter.api.Test;

import com.bastion.cuentas.domain.model.Cuenta;
import com.bastion.cuentas.domain.model.EstadoCuenta;
import com.bastion.cuentas.domain.port.out.CuentaRepository;

class CrearCuentaServiceTest {

    @Test
    void crearCuentaGuardaYDevuelveLaCuenta() {
        CuentaRepository cuentaRepository = mock(CuentaRepository.class);

        when(cuentaRepository.guardar(any(Cuenta.class)))
                .thenAnswer(invocacion -> invocacion.getArgument(0));

        CrearCuentaService servicio = new CrearCuentaService(cuentaRepository);
        UUID titularId = UUID.randomUUID();
        Currency moneda = Currency.getInstance("EUR");

        Cuenta cuenta = servicio.ejecutar(titularId, moneda);

        assertThat(cuenta).isNotNull();
        assertThat(cuenta.id()).isNotNull();
        assertThat(cuenta.titularId()).isEqualTo(titularId);
        assertThat(cuenta.moneda()).isEqualTo(moneda);
        assertThat(cuenta.estado()).isEqualTo(EstadoCuenta.ACTIVA);

        verify(cuentaRepository).guardar(cuenta);
    }
}