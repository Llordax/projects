package com.bastion.transferencias.infrastructure.adapter.in.rest;

import java.net.URI;
import java.util.Currency;
import java.util.UUID;

import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import com.bastion.transferencias.application.port.in.ConsultarTransferenciaUseCase;
import com.bastion.transferencias.application.port.in.SolicitarTransferenciaUseCase;
import com.bastion.transferencias.domain.model.Transferencia;
import com.bastion.transferencias.infrastructure.adapter.in.rest.dto.SolicitarTransferenciaRequest;
import com.bastion.transferencias.infrastructure.adapter.in.rest.dto.TransferenciaResponse;

import jakarta.validation.Valid;

@RestController
@RequestMapping("/api/v1/transferencias")
public class TransferenciaController {

    private final SolicitarTransferenciaUseCase solicitarTransferenciaUseCase;
    private final ConsultarTransferenciaUseCase consultarTransferenciaUseCase;

    public TransferenciaController(
            SolicitarTransferenciaUseCase solicitarTransferenciaUseCase,
            ConsultarTransferenciaUseCase consultarTransferenciaUseCase) {
        this.solicitarTransferenciaUseCase = solicitarTransferenciaUseCase;
        this.consultarTransferenciaUseCase = consultarTransferenciaUseCase;
    }

    @PostMapping
    public ResponseEntity<TransferenciaResponse> solicitar(
            @Valid @RequestBody SolicitarTransferenciaRequest request) {

        Transferencia transferencia = solicitarTransferenciaUseCase.ejecutar(
                request.cuentaOrigenId(),
                request.cuentaDestinoId(),
                request.importe(),
                Currency.getInstance(request.moneda())
        );

        TransferenciaResponse response =
                TransferenciaResponse.desdeDominio(transferencia);

        URI location = URI.create(
                "/api/v1/transferencias/" + transferencia.id()
        );

        return ResponseEntity.created(location).body(response);
    }

    @GetMapping("/{transferenciaId}")
    public ResponseEntity<TransferenciaResponse> consultar(
    		@PathVariable("transferenciaId") UUID transferenciaId) {

        Transferencia transferencia =
                consultarTransferenciaUseCase.ejecutar(transferenciaId);

        return ResponseEntity.ok(
                TransferenciaResponse.desdeDominio(transferencia)
        );
    }
}