package com.bastion.cuentas.application.service;

import java.util.Objects;
import java.util.Optional;
import java.util.UUID;

import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import com.bastion.cuentas.application.port.in.ConsultarCuentaUseCase;
import com.bastion.cuentas.application.port.out.CuentaRepository;
import com.bastion.cuentas.domain.model.Cuenta;

@Service
public class ConsultarCuentaService implements ConsultarCuentaUseCase {

    private final CuentaRepository cuentaRepository;

    public ConsultarCuentaService(CuentaRepository cuentaRepository) {
        this.cuentaRepository = Objects.requireNonNull(
                cuentaRepository,
                "cuentaRepository no puede ser null"
        );
    }

    @Override
    @Transactional(readOnly = true)
    public Optional<Cuenta> ejecutar(UUID cuentaId) {
        Objects.requireNonNull(cuentaId, "cuentaId no puede ser null");
        return cuentaRepository.buscarPorId(cuentaId);
    }
}