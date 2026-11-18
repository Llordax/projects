package com.bastion.cuentas.infrastructure.adapter.out.persistence;

import java.util.Objects;
import java.util.Optional;
import java.util.UUID;

import org.springframework.stereotype.Repository;

import com.bastion.cuentas.application.port.out.CuentaRepository;
import com.bastion.cuentas.domain.model.Cuenta;
import com.bastion.cuentas.infrastructure.persistence.entity.CuentaJpaEntity;
import com.bastion.cuentas.infrastructure.persistence.repository.CuentaSpringDataRepository;

@Repository
public class CuentaPersistenceAdapter implements CuentaRepository {

    private final CuentaSpringDataRepository cuentaSpringDataRepository;

    public CuentaPersistenceAdapter(CuentaSpringDataRepository cuentaSpringDataRepository) {
        this.cuentaSpringDataRepository = Objects.requireNonNull(
                cuentaSpringDataRepository,
                "cuentaSpringDataRepository no puede ser null"
        );
    }

    @Override
    public Cuenta guardar(Cuenta cuenta) {
        Objects.requireNonNull(cuenta, "cuenta no puede ser null");

        CuentaJpaEntity entidad = cuentaSpringDataRepository.findById(cuenta.id())
                .map(entidadExistente -> {
                    entidadExistente.actualizarDesdeDominio(cuenta);
                    return entidadExistente;
                })
                .orElseGet(() -> CuentaJpaEntity.desdeDominio(cuenta));

        return cuentaSpringDataRepository.save(entidad).aDominio();
    }

    @Override
    public Optional<Cuenta> buscarPorId(UUID id) {
        Objects.requireNonNull(id, "id no puede ser null");

        return cuentaSpringDataRepository.findById(id)
                .map(CuentaJpaEntity::aDominio);
    }
}