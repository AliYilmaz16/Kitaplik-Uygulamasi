package com.aliyilmaz.dto;

import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;

@Data
@NoArgsConstructor
@AllArgsConstructor
public class DtoBookIU {

	private String yazar;
	
	private String kitapAdi;
	
	private String sayfaSayisi;
}
