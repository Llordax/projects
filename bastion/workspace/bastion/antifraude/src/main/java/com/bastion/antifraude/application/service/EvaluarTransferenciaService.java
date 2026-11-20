package com.bastion.antifraude.application.service;

import java.util.Objects;

import org.springframework.stereotype.Service;

import com.bastion.antifraude.application.port.in.EvaluarTransferenciaUseCase;
import com.bastion.antifraude.domain.model.ResultadoEvaluacionAntifraude;
import com.bastion.antifraude.domain.model.SolicitudAntifraude;
import com.bastion.antifraude.domain.service.EvaluadorAntifraude;

@Service
public class EvaluarTransferenciaService implements EvaluarTransferenciaUseCase {

    private final EvaluadorAntifraude evaluadorAntifraude;

    public EvaluarTransferenciaService(EvaluadorAntifraude evaluadorAntifraude) {
        this.evaluadorAntifraude = Objects.requireNonNull(
                evaluadorAntifraude,
                "evaluadorAntifraude no puede ser null"
        );
    }

    @Override
    public ResultadoEvaluacionAntifraude ejecutar(SolicitudAntifraude solicitud) {
        return evaluadorAntifraude.evaluar(solicitud);
    }
}