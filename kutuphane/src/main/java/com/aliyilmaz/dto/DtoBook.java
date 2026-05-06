package com.aliyilmaz.dto;

import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;

@Data
@AllArgsConstructor
@NoArgsConstructor
public class DtoBook{
	
	private Integer id;

	private String yazar;
	
	private String kitapAdi;
	
	private String sayfaSayisi;
}
