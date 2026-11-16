package com.bastion.cuentas.application.service;

import java.util.Objects;
import java.util.UUID;
import java.util.Currency;

import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import com.bastion.cuentas.application.port.in.CrearCuentaUseCase;
import com.bastion.cuentas.domain.model.Cuenta;
import com.bastion.cuentas.domain.port.out.CuentaRepository;

@Service
public class CrearCuentaService implements CrearCuentaUseCase {

    private final CuentaRepository cuentaRepository;

    public CrearCuentaService(CuentaRepository cuentaRepository) {
        this.cuentaRepository = Objects.requireNonNull(
                cuentaRepository,
                "cuentaRepository no puede ser null"
        );
    }

    @Override
    @Transactional
    public Cuenta ejecutar(UUID titularId, Currency moneda) {
        Cuenta cuenta = new Cuenta(UUID.randomUUID(), titularId, moneda);
        return cuentaRepository.guardar(cuenta);
    }
}