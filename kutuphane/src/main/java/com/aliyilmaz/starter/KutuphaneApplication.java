package com.aliyilmaz.starter;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.domain.EntityScan;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.context.annotation.ComponentScan;
import org.springframework.data.jpa.repository.config.EnableJpaRepositories;

@SpringBootApplication
@EntityScan(basePackages = {"com.aliyilmaz"})
@ComponentScan(basePackages = {"com.aliyilmaz"})
@EnableJpaRepositories(basePackages = {"com.aliyilmaz"})
public class KutuphaneApplication {

	public static void main(String[] args) {
		SpringApplication.run(KutuphaneApplication.class, args);
	}

}
