package com.bastion.transferencias.infrastructure.adapter.in.rest;

import org.springframework.http.HttpStatus;
import org.springframework.http.ProblemDetail;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.ExceptionHandler;
import org.springframework.web.bind.annotation.RestControllerAdvice;

import com.bastion.transferencias.application.exception.TransferenciaNoEncontradaException;

@RestControllerAdvice
public class TransferenciaExceptionHandler {

    @ExceptionHandler(TransferenciaNoEncontradaException.class)
    public ResponseEntity<ProblemDetail> manejarTransferenciaNoEncontrada(
            TransferenciaNoEncontradaException excepcion) {

        ProblemDetail problema = ProblemDetail.forStatusAndDetail(
                HttpStatus.NOT_FOUND,
                excepcion.getMessage()
        );
        problema.setTitle("Transferencia no encontrada");
        problema.setProperty("transferenciaId", excepcion.transferenciaId());

        return ResponseEntity.status(HttpStatus.NOT_FOUND).body(problema);
    }

    @ExceptionHandler(IllegalArgumentException.class)
    public ResponseEntity<ProblemDetail> manejarArgumentoInvalido(
            IllegalArgumentException excepcion) {

        ProblemDetail problema = ProblemDetail.forStatusAndDetail(
                HttpStatus.BAD_REQUEST,
                excepcion.getMessage()
        );
        problema.setTitle("Solicitud de transferencia inválida");

        return ResponseEntity.badRequest().body(problema);
    }
}