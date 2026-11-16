package com.bastion.cuentas.application.service;

import java.util.Objects;
import java.util.UUID;

import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import com.bastion.cuentas.application.exception.CuentaNoEncontradaException;
import com.bastion.cuentas.application.port.in.DesbloquearCuentaUseCase;
import com.bastion.cuentas.domain.model.Cuenta;
import com.bastion.cuentas.domain.port.out.CuentaRepository;

@Service
public class DesbloquearCuentaService implements DesbloquearCuentaUseCase {

    private final CuentaRepository cuentaRepository;

    public DesbloquearCuentaService(CuentaRepository cuentaRepository) {
        this.cuentaRepository = Objects.requireNonNull(
                cuentaRepository,
                "cuentaRepository no puede ser null"
        );
    }

    @Override
    @Transactional
    public boolean ejecutar(UUID cuentaId) {
        Objects.requireNonNull(cuentaId, "cuentaId no puede ser null");

        Cuenta cuenta = cuentaRepository.buscarPorId(cuentaId)
                .orElseThrow(() -> new CuentaNoEncontradaException(cuentaId));

        boolean cambioRealizado = cuenta.desbloquear();

        if (cambioRealizado) 
            cuentaRepository.guardar(cuenta);

        return cambioRealizado;
    }
}