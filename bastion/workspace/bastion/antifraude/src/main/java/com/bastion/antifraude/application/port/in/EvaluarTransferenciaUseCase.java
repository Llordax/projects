package com.bastion.antifraude.application.port.in;

import com.bastion.antifraude.domain.model.ResultadoEvaluacionAntifraude;
import com.bastion.antifraude.domain.model.SolicitudAntifraude;

public interface EvaluarTransferenciaUseCase {

    ResultadoEvaluacionAntifraude ejecutar(SolicitudAntifraude solicitud);
}