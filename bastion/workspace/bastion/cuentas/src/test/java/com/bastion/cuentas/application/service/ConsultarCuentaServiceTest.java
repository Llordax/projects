package com.bastion.cuentas.application.service;

import static org.assertj.core.api.AssertionsForClassTypes.assertThat;
import static org.mockito.Mockito.mock;
import static org.mockito.Mockito.verify;
import static org.mockito.Mockito.when;

import java.util.Currency;
import java.util.Optional;
import java.util.UUID;

import org.junit.jupiter.api.Test;

import com.bastion.cuentas.domain.model.Cuenta;
import com.bastion.cuentas.domain.port.out.CuentaRepository;

class ConsultarCuentaServiceTest {

    @Test
    void consultarCuentaDevuelveLaCuentaCuandoExiste() {
        CuentaRepository cuentaRepository = mock(CuentaRepository.class);
        UUID cuentaId = UUID.randomUUID();
        Cuenta cuenta = new Cuenta(
                cuentaId,
                UUID.randomUUID(),
                Currency.getInstance("EUR")
        );

        when(cuentaRepository.buscarPorId(cuentaId)).thenReturn(Optional.of(cuenta));

        ConsultarCuentaService servicio = new ConsultarCuentaService(cuentaRepository);

        Optional<Cuenta> resultado = servicio.ejecutar(cuentaId);

        assertThat(resultado).contains(cuenta);
        verify(cuentaRepository).buscarPorId(cuentaId);
    }

    @Test
    void consultarCuentaDevuelveOptionalVacioCuandoNoExiste() {
        CuentaRepository cuentaRepository = mock(CuentaRepository.class);
        UUID cuentaId = UUID.randomUUID();

        when(cuentaRepository.buscarPorId(cuentaId)).thenReturn(Optional.empty());

        ConsultarCuentaService servicio = new ConsultarCuentaService(cuentaRepository);

        Optional<Cuenta> resultado = servicio.ejecutar(cuentaId);

        assertThat(resultado).isEmpty();
        verify(cuentaRepository).buscarPorId(cuentaId);
    }
}