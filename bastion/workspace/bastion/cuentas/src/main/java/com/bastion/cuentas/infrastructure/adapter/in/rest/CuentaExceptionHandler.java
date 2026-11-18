package com.bastion.cuentas.infrastructure.adapter.in.web;

import org.springframework.http.HttpStatus;
import org.springframework.http.ProblemDetail;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.ExceptionHandler;
import org.springframework.web.bind.annotation.RestControllerAdvice;

import com.bastion.cuentas.application.exception.CuentaNoEncontradaException;
import com.bastion.cuentas.domain.model.ReglaCuentaException;

@RestControllerAdvice
public class CuentaExceptionHandler {

    @ExceptionHandler(CuentaNoEncontradaException.class)
    public ResponseEntity<ProblemDetail> manejarCuentaNoEncontrada(
            CuentaNoEncontradaException excepcion
    ) {
        ProblemDetail problema = ProblemDetail.forStatusAndDetail(
                HttpStatus.NOT_FOUND,
                excepcion.getMessage()
        );
        problema.setTitle("Cuenta no encontrada");
        problema.setProperty("cuentaId", excepcion.cuentaId());

        return ResponseEntity.status(HttpStatus.NOT_FOUND).body(problema);
    }

    @ExceptionHandler(ReglaCuentaException.class)
    public ResponseEntity<ProblemDetail> manejarReglaDeCuenta(
            ReglaCuentaException excepcion
    ) {
        ProblemDetail problema = ProblemDetail.forStatusAndDetail(
                HttpStatus.UNPROCESSABLE_ENTITY,
                excepcion.getMessage()
        );
        problema.setTitle("Operación de cuenta rechazada");
        problema.setProperty("codigo", excepcion.codigo().name());

        return ResponseEntity
                .status(HttpStatus.UNPROCESSABLE_ENTITY)
                .body(problema);
    }

    @ExceptionHandler(IllegalArgumentException.class)
    public ResponseEntity<ProblemDetail> manejarArgumentoInvalido(
            IllegalArgumentException excepcion
    ) {
        ProblemDetail problema = ProblemDetail.forStatusAndDetail(
                HttpStatus.BAD_REQUEST,
                excepcion.getMessage()
        );
        problema.setTitle("Solicitud inválida");

        return ResponseEntity.badRequest().body(problema);
    }
}