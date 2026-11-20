package com.bastion.antifraude.infrastructure.persistence.repository;

import java.util.UUID;

import org.springframework.data.jpa.repository.JpaRepository;

import com.bastion.antifraude.infrastructure.persistence.entity.OutboxJpaEntity;

public interface OutboxSpringDataRepository
        extends JpaRepository<OutboxJpaEntity, UUID> {
}