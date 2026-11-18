package com.bastion.transferencias.infrastructure.persistence.entity;

import java.math.BigDecimal;
import java.util.Currency;
import java.util.UUID;

import com.bastion.transferencias.domain.model.EstadoTransferencia;
import com.bastion.transferencias.domain.model.Transferencia;

import jakarta.persistence.Column;
import jakarta.persistence.Entity;
import jakarta.persistence.EnumType;
import jakarta.persistence.Enumerated;
import jakarta.persistence.Id;
import jakarta.persistence.Table;
import jakarta.persistence.Version;

@Entity
@Table(name = "transferencias")
public class TransferenciaJpaEntity {

    @Id
    private UUID id;

    @Column(name = "cuenta_origen_id", nullable = false)
    private UUID cuentaOrigenId;

    @Column(name = "cuenta_destino_id", nullable = false)
    private UUID cuentaDestinoId;

    @Column(nullable = false, precision = 19, scale = 4)
    private BigDecimal importe;

    @Column(nullable = false, length = 3)
    private String moneda;

    @Enumerated(EnumType.STRING)
    @Column(nullable = false, length = 40)
    private EstadoTransferencia estado;

    @Column(name = "motivo_rechazo", length = 500)
    private String motivoRechazo;

    @Version
    private Long version;

    protected TransferenciaJpaEntity() {
        // Requerido por JPA.
    }

    public static TransferenciaJpaEntity desdeDominio(Transferencia transferencia) {
        TransferenciaJpaEntity entidad = new TransferenciaJpaEntity();
        entidad.actualizarDesdeDominio(transferencia);
        return entidad;
    }

    public void actualizarDesdeDominio(Transferencia transferencia) {
        this.id = transferencia.id();
        this.cuentaOrigenId = transferencia.cuentaOrigenId();
        this.cuentaDestinoId = transferencia.cuentaDestinoId();
        this.importe = transferencia.importe();
        this.moneda = transferencia.moneda().getCurrencyCode();
        this.estado = transferencia.estado();
        this.motivoRechazo = transferencia.motivoRechazo();
    }

    public Transferencia aDominio() {
        return Transferencia.rehidratar(
                id,
                cuentaOrigenId,
                cuentaDestinoId,
                importe,
                Currency.getInstance(moneda),
                estado,
                motivoRechazo
        );
    }
}