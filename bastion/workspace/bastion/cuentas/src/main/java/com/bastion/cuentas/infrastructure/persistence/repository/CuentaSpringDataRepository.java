package com.bastion.cuentas.infrastructure.persistence.repository;

import java.util.UUID;

import org.springframework.data.jpa.repository.JpaRepository;

import com.bastion.cuentas.infrastructure.persistence.entity.CuentaJpaEntity;

public interface CuentaSpringDataRepository extends JpaRepository<CuentaJpaEntity, UUID> {
}