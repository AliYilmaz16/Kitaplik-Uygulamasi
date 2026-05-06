package com.aliyilmaz.services;

import java.util.List;

import com.aliyilmaz.dto.DtoBook;
import com.aliyilmaz.dto.DtoBookIU;

public interface IBookService {

	public DtoBook saveBook(DtoBookIU dtoBookIU);
	public List<DtoBook> getAllBooks();
	public DtoBook findBook(Integer id, String kitapAdi, String yazar);
	public boolean deleteBook(Integer id);
	public DtoBook updateBook(Integer id, DtoBookIU dtoBookIU);
}
