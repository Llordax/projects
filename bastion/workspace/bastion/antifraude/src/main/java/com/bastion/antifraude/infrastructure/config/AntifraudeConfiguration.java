package com.bastion.antifraude.infrastructure.config;

import java.math.BigDecimal;
import java.util.List;

import org.springframework.beans.factory.annotation.Value;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;

import com.bastion.antifraude.domain.rule.ImporteMaximoAntifraudeRegla;
import com.bastion.antifraude.domain.rule.ReglaAntifraude;
import com.bastion.antifraude.domain.service.EvaluadorAntifraude;
import com.fasterxml.jackson.databind.ObjectMapper;
import com.fasterxml.jackson.databind.SerializationFeature;
import com.fasterxml.jackson.datatype.jsr310.JavaTimeModule;

@Configuration
public class AntifraudeConfiguration {

    @Bean
    public ObjectMapper objectMapper() {
        ObjectMapper objectMapper = new ObjectMapper();
        objectMapper.registerModule(new JavaTimeModule());
        objectMapper.disable(SerializationFeature.WRITE_DATES_AS_TIMESTAMPS);
        return objectMapper;
    }

    @Bean
    public ReglaAntifraude importeMaximoAntifraudeRegla(
            @Value("${bastion.antifraude.importe-maximo}") BigDecimal importeMaximo) {
        return new ImporteMaximoAntifraudeRegla(importeMaximo);
    }

    @Bean
    public EvaluadorAntifraude evaluadorAntifraude(List<ReglaAntifraude> reglas) {
        return new EvaluadorAntifraude(reglas);
    }
}