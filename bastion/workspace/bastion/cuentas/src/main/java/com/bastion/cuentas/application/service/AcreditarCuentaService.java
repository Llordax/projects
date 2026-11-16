package com.bastion.cuentas.application.service;

import java.math.BigDecimal;
import java.util.Objects;
import java.util.UUID;

import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import com.bastion.cuentas.application.exception.CuentaNoEncontradaException;
import com.bastion.cuentas.application.port.in.AcreditarCuentaUseCase;
import com.bastion.cuentas.domain.model.Cuenta;
import com.bastion.cuentas.domain.port.out.CuentaRepository;

@Service
public class AcreditarCuentaService implements AcreditarCuentaUseCase {

    private final CuentaRepository cuentaRepository;

    public AcreditarCuentaService(CuentaRepository cuentaRepository) {
        this.cuentaRepository = Objects.requireNonNull(
                cuentaRepository,
                "cuentaRepository no puede ser null"
        );
    }

    @Override
    @Transactional
    public Cuenta ejecutar(UUID cuentaId, BigDecimal importe) {
        Objects.requireNonNull(cuentaId, "cuentaId no puede ser null");

        Cuenta cuenta = cuentaRepository.buscarPorId(cuentaId)
                .orElseThrow(() -> new CuentaNoEncontradaException(cuentaId));

        cuenta.acreditar(importe);

        return cuentaRepository.guardar(cuenta);
    }
}