package com.bastion.antifraude.domain.service;

import java.util.ArrayList;
import java.util.List;
import java.util.Objects;
import java.util.Optional;

import com.bastion.antifraude.domain.model.ResultadoEvaluacionAntifraude;
import com.bastion.antifraude.domain.model.SolicitudAntifraude;
import com.bastion.antifraude.domain.rule.ReglaAntifraude;

public class EvaluadorAntifraude {

    private final List<ReglaAntifraude> reglas;

    public EvaluadorAntifraude(List<ReglaAntifraude> reglas) {
        Objects.requireNonNull(reglas, "reglas no puede ser null");

        if (reglas.isEmpty()) 
            throw new IllegalArgumentException(
                    "Debe configurarse al menos una regla antifraude"
            );

        this.reglas = List.copyOf(reglas);
    }

    public ResultadoEvaluacionAntifraude evaluar(SolicitudAntifraude solicitud) {
        Objects.requireNonNull(solicitud, "solicitud no puede ser null");

        List<String> reglasAplicadas = new ArrayList<>();

        for (ReglaAntifraude regla : reglas) {
            Objects.requireNonNull(regla, "La lista no puede contener reglas null");

            String codigo = Objects.requireNonNull(
                    regla.codigo(),
                    "El código de la regla no puede ser null"
            );

            if (codigo.isBlank()) 
                throw new IllegalStateException("El código de la regla no puede estar vacío");

            reglasAplicadas.add(codigo);

            Optional<String> motivoRechazo = Objects.requireNonNull(
                    regla.evaluar(solicitud),
                    "La regla debe devolver un Optional"
            );

            if (motivoRechazo.isPresent()) 
                return ResultadoEvaluacionAntifraude.rechazada(
                        reglasAplicadas,
                        motivoRechazo.get()
                );
        }

        return ResultadoEvaluacionAntifraude.aprobada(reglasAplicadas);
    }
}