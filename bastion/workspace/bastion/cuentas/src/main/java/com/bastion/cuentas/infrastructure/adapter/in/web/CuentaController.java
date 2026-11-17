package com.bastion.cuentas.infrastructure.adapter.in.web;

import java.net.URI;
import java.util.Currency;
import java.util.UUID;

import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.PutMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;
import org.springframework.web.server.ResponseStatusException;

import com.bastion.cuentas.application.port.in.AcreditarCuentaUseCase;
import com.bastion.cuentas.application.port.in.BloquearCuentaUseCase;
import com.bastion.cuentas.application.port.in.ConsultarCuentaUseCase;
import com.bastion.cuentas.application.port.in.CrearCuentaUseCase;
import com.bastion.cuentas.application.port.in.DebitarCuentaUseCase;
import com.bastion.cuentas.application.port.in.DesbloquearCuentaUseCase;
import com.bastion.cuentas.domain.model.Cuenta;
import com.bastion.cuentas.infrastructure.adapter.in.web.dto.CambioEstadoCuentaRequest;
import com.bastion.cuentas.infrastructure.adapter.in.web.dto.CuentaResponse;
import com.bastion.cuentas.infrastructure.adapter.in.web.dto.CrearCuentaRequest;
import com.bastion.cuentas.infrastructure.adapter.in.web.dto.MovimientoCuentaRequest;

import jakarta.validation.Valid;

@RestController
@RequestMapping("/api/v1/cuentas")
public class CuentaController {

    private final CrearCuentaUseCase crearCuentaUseCase;
    private final ConsultarCuentaUseCase consultarCuentaUseCase;
    private final BloquearCuentaUseCase bloquearCuentaUseCase;
    private final DesbloquearCuentaUseCase desbloquearCuentaUseCase;
    private final AcreditarCuentaUseCase acreditarCuentaUseCase;
    private final DebitarCuentaUseCase debitarCuentaUseCase;

    public CuentaController(
            CrearCuentaUseCase crearCuentaUseCase,
            ConsultarCuentaUseCase consultarCuentaUseCase,
            BloquearCuentaUseCase bloquearCuentaUseCase,
            DesbloquearCuentaUseCase desbloquearCuentaUseCase,
            AcreditarCuentaUseCase acreditarCuentaUseCase,
            DebitarCuentaUseCase debitarCuentaUseCase
    ) {
        this.crearCuentaUseCase = crearCuentaUseCase;
        this.consultarCuentaUseCase = consultarCuentaUseCase;
        this.bloquearCuentaUseCase = bloquearCuentaUseCase;
        this.desbloquearCuentaUseCase = desbloquearCuentaUseCase;
        this.acreditarCuentaUseCase = acreditarCuentaUseCase;
        this.debitarCuentaUseCase = debitarCuentaUseCase;
    }

    @PostMapping
    public ResponseEntity<CuentaResponse> crearCuenta(
            @Valid @RequestBody CrearCuentaRequest request
    ) {
        Currency moneda;

        try {
            moneda = Currency.getInstance(request.moneda());
        } catch (IllegalArgumentException excepcion) {
            throw new ResponseStatusException(
                    HttpStatus.BAD_REQUEST,
                    "El código de moneda no está soportado",
                    excepcion
            );
        }

        Cuenta cuenta = crearCuentaUseCase.ejecutar(request.titularId(), moneda);
        CuentaResponse respuesta = CuentaResponse.desdeDominio(cuenta);
        URI ubicacion = URI.create("/api/v1/cuentas/" + cuenta.id());

        return ResponseEntity.created(ubicacion).body(respuesta);
    }

    @GetMapping("/{cuentaId}")
    public CuentaResponse consultarCuenta(
            @PathVariable("cuentaId") UUID cuentaId
    ) {
        Cuenta cuenta = consultarCuentaUseCase.ejecutar(cuentaId)
                .orElseThrow(() -> new ResponseStatusException(
                        HttpStatus.NOT_FOUND,
                        "No se encontró la cuenta con id: " + cuentaId
                ));

        return CuentaResponse.desdeDominio(cuenta);
    }

    @PutMapping("/{cuentaId}/bloqueo")
    public ResponseEntity<Boolean> bloquearCuenta(
            @PathVariable("cuentaId") UUID cuentaId,
            @Valid @RequestBody CambioEstadoCuentaRequest request
    ) {
        boolean cambioRealizado = bloquearCuentaUseCase.ejecutar(
                cuentaId,
                request.motivo()
        );
        return ResponseEntity.ok(cambioRealizado);
    }

    @PutMapping("/{cuentaId}/desbloqueo")
    public ResponseEntity<Boolean> desbloquearCuenta(
            @PathVariable("cuentaId") UUID cuentaId,
            @Valid @RequestBody CambioEstadoCuentaRequest request
    ) {
        boolean cambioRealizado = desbloquearCuentaUseCase.ejecutar(
                cuentaId,
                request.motivo()
        );
        return ResponseEntity.ok(cambioRealizado);
    }

    @PostMapping("/{cuentaId}/creditos")
    public CuentaResponse acreditar(
            @PathVariable("cuentaId") UUID cuentaId,
            @Valid @RequestBody MovimientoCuentaRequest request
    ) {
        Cuenta cuenta = acreditarCuentaUseCase.ejecutar(
                cuentaId,
                request.transferenciaId(),
                request.importe()
        );

        return CuentaResponse.desdeDominio(cuenta);
    }

    @PostMapping("/{cuentaId}/debitos")
    public CuentaResponse debitar(
            @PathVariable("cuentaId") UUID cuentaId,
            @Valid @RequestBody MovimientoCuentaRequest request
    ) {
        Cuenta cuenta = debitarCuentaUseCase.ejecutar(
                cuentaId,
                request.transferenciaId(),
                request.importe()
        );

        return CuentaResponse.desdeDominio(cuenta);
    }
}