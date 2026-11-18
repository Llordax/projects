package com.bastion.cuentas.application.service;

import static org.assertj.core.api.AssertionsForClassTypes.assertThat;
import static org.mockito.ArgumentMatchers.any;
import static org.mockito.Mockito.mock;
import static org.mockito.Mockito.verify;
import static org.mockito.Mockito.when;

import java.util.Currency;
import java.util.UUID;

import org.junit.jupiter.api.Test;

import com.bastion.cuentas.application.port.out.CuentaRepository;
import com.bastion.cuentas.application.port.out.EventoOutboxPort;
import com.bastion.cuentas.domain.model.Cuenta;
import com.bastion.cuentas.domain.model.EstadoCuenta;
import com.bastion.eventos.contrato.Evento;

class CrearCuentaServiceTest {

    @Test
    void crearCuentaGuardaYRegistraElEventoOutbox() {
        CuentaRepository cuentaRepository = mock(CuentaRepository.class);
        EventoOutboxPort eventoOutboxPort = mock(EventoOutboxPort.class);

        when(cuentaRepository.guardar(any(Cuenta.class)))
                .thenAnswer(invocacion -> invocacion.getArgument(0));

        CrearCuentaService servicio = new CrearCuentaService(
                cuentaRepository,
                eventoOutboxPort
        );
        UUID titularId = UUID.randomUUID();
        Currency moneda = Currency.getInstance("EUR");

        Cuenta cuenta = servicio.ejecutar(titularId, moneda);

        assertThat(cuenta).isNotNull();
        assertThat(cuenta.id()).isNotNull();
        assertThat(cuenta.titularId()).isEqualTo(titularId);
        assertThat(cuenta.moneda()).isEqualTo(moneda);
        assertThat(cuenta.estado()).isEqualTo(EstadoCuenta.ACTIVA);

        verify(cuentaRepository).guardar(cuenta);
        verify(eventoOutboxPort).registrar(any(Evento.class));
    }
}