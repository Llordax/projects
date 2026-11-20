package com.bastion.antifraude.domain.rule;

import java.util.Optional;

import com.bastion.antifraude.domain.model.SolicitudAntifraude;

public interface ReglaAntifraude {

    String codigo();

    /**
     * Devuelve el motivo del rechazo cuando la solicitud incumple esta regla.
     * Un Optional vacío indica que la regla se ha superado.
     */
    Optional<String> evaluar(SolicitudAntifraude solicitud);
}