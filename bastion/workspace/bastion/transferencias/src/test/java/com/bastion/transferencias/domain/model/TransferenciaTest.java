package com.bastion.transferencias.domain.model;

import static org.assertj.core.api.AssertionsForClassTypes.assertThat;
import static org.junit.jupiter.api.Assertions.assertThrows;

import java.math.BigDecimal;
import java.util.Currency;
import java.util.UUID;

import org.junit.jupiter.api.Test;

class TransferenciaTest {

    @Test
    void nuevaTransferenciaComienzaSolicitada() {
        Transferencia transferencia = nuevaTransferencia();

        assertThat(transferencia.estado()).isEqualTo(EstadoTransferencia.SOLICITADA);
        assertThat(transferencia.motivoRechazo()).isNull();
    }

    @Test
    void flujoExitosoCompletaLaTransferencia() {
        Transferencia transferencia = nuevaTransferencia();

        transferencia.iniciarEvaluacionAntifraude();
        transferencia.aprobarAntifraude();
        transferencia.registrarDebitoRealizado();
        transferencia.registrarCreditoRealizado();

        assertThat(transferencia.estado()).isEqualTo(EstadoTransferencia.COMPLETADA);
    }

    @Test
    void rechazoAntifraudeRechazaLaTransferencia() {
        Transferencia transferencia = nuevaTransferencia();

        transferencia.iniciarEvaluacionAntifraude();
        transferencia.rechazarAntifraude("Riesgo elevado");

        assertThat(transferencia.estado()).isEqualTo(EstadoTransferencia.RECHAZADA);
        assertThat(transferencia.motivoRechazo()).isEqualTo("Riesgo elevado");
    }

    @Test
    void rechazoDelCreditoPermiteCompensarElDebito() {
        Transferencia transferencia = nuevaTransferencia();

        transferencia.iniciarEvaluacionAntifraude();
        transferencia.aprobarAntifraude();
        transferencia.registrarDebitoRealizado();
        transferencia.registrarCreditoRechazado("Cuenta destino bloqueada");

        assertThat(transferencia.estado())
                .isEqualTo(EstadoTransferencia.PENDIENTE_COMPENSACION);

        transferencia.registrarCompensacionRealizada();

        assertThat(transferencia.estado()).isEqualTo(EstadoTransferencia.COMPENSADA);
    }

    @Test
    void rechazoDeLaCompensacionDejaLaTransferenciaEnError() {
        Transferencia transferencia = nuevaTransferencia();

        transferencia.iniciarEvaluacionAntifraude();
        transferencia.aprobarAntifraude();
        transferencia.registrarDebitoRealizado();
        transferencia.registrarCreditoRechazado("Cuenta destino bloqueada");
        transferencia.registrarCompensacionRechazada("Cuenta origen bloqueada");

        assertThat(transferencia.estado())
                .isEqualTo(EstadoTransferencia.ERROR_COMPENSACION);
        assertThat(transferencia.motivoRechazo()).isEqualTo("Cuenta origen bloqueada");
    }

    @Test
    void noPermiteCompletarAntesDeRegistrarElDebito() {
        Transferencia transferencia = nuevaTransferencia();

        assertThrows(
                IllegalStateException.class,
                transferencia::registrarCreditoRealizado
        );
    }

    @Test
    void noPermiteTransferirAlaMismaCuenta() {
        UUID cuentaId = UUID.randomUUID();

        assertThrows(
                IllegalArgumentException.class,
                () -> new Transferencia(
                        UUID.randomUUID(),
                        cuentaId,
                        cuentaId,
                        new BigDecimal("10.00"),
                        Currency.getInstance("EUR")
                )
        );
    }

    private Transferencia nuevaTransferencia() {
        return new Transferencia(
                UUID.randomUUID(),
                UUID.randomUUID(),
                UUID.randomUUID(),
                new BigDecimal("25.00"),
                Currency.getInstance("EUR")
        );
    }
}