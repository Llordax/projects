package com.bastion.antifraude.domain.model;

import java.util.List;
import java.util.Objects;

public record ResultadoEvaluacionAntifraude(
        DecisionAntifraude decision,
        List<String> reglasAplicadas,
        String motivoRechazo
) {
    public ResultadoEvaluacionAntifraude {
        Objects.requireNonNull(decision, "decision no puede ser null");
        reglasAplicadas = List.copyOf(
                Objects.requireNonNull(reglasAplicadas, "reglasAplicadas no puede ser null")
        );

        if (reglasAplicadas.stream().anyMatch(regla -> regla == null || regla.isBlank()))
            throw new IllegalArgumentException(
                    "Las reglas aplicadas no pueden ser null ni estar vacías"
            );

        if (decision == DecisionAntifraude.RECHAZADA
                && (motivoRechazo == null || motivoRechazo.isBlank())) 
            throw new IllegalArgumentException(
                    "Una evaluación rechazada debe incluir un motivo"
            );

        if (decision == DecisionAntifraude.APROBADA && motivoRechazo != null) 
            throw new IllegalArgumentException(
                    "Una evaluación aprobada no debe incluir motivo de rechazo"
            );
    }

    public static ResultadoEvaluacionAntifraude aprobada(List<String> reglasAplicadas) {
        return new ResultadoEvaluacionAntifraude(
                DecisionAntifraude.APROBADA,
                reglasAplicadas,
                null
        );
    }

    public static ResultadoEvaluacionAntifraude rechazada(
            List<String> reglasAplicadas,
            String motivoRechazo
    ) {
        return new ResultadoEvaluacionAntifraude(
                DecisionAntifraude.RECHAZADA,
                reglasAplicadas,
                motivoRechazo
        );
    }
}