package com.aliyilmaz.services.impl;

import java.util.ArrayList;
import java.util.List;
import java.util.Optional;

import org.springframework.beans.BeanUtils;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Repository;
import org.springframework.stereotype.Service;

import com.aliyilmaz.dto.DtoBook;
import com.aliyilmaz.dto.DtoBookIU;
import com.aliyilmaz.entities.Book;
import com.aliyilmaz.repository.BookRepository;
import com.aliyilmaz.services.IBookService;

@Service
public class BookServiceImpl implements IBookService{
	@Autowired
	private BookRepository bookRepository;

	private DtoBook convertToDto(Book book) {
        DtoBook dto = new DtoBook();
        BeanUtils.copyProperties(book, dto);
        return dto;
    }
	
	@Override
	public DtoBook saveBook(DtoBookIU dtoBookIU) {
		DtoBook dtoBook = new DtoBook();
		Book book = new Book();
		
		BeanUtils.copyProperties(dtoBookIU, book);
		
		Book dbBook = bookRepository.save(book);
		
		BeanUtils.copyProperties(dbBook, dtoBook);
		
		return dtoBook;
	}

	@Override
	public List<DtoBook> getAllBooks() {
		List<DtoBook> dtoBookList = new ArrayList<>();
		
		List<Book> bookList = bookRepository.findAll();
		
		for (Book book : bookList) {
			DtoBook dtoBook = new DtoBook();
			BeanUtils.copyProperties(book, dtoBook);
			
			dtoBookList.add(dtoBook);
		}
		return dtoBookList;
	}

	@Override
	public boolean deleteBook(Integer id) {
		Optional<Book> dbBook = bookRepository.findById(id);
		if (dbBook.isPresent()) {
			bookRepository.deleteById(id);
			return true;
		}
		return false;
	}

	@Override
	public DtoBook updateBook(Integer id, DtoBookIU dtoBookIU) {
		DtoBook dtoBook = new DtoBook();
		Optional<Book> dbBook = bookRepository.findById(id);
		if (dbBook.isPresent()) {
			
			dbBook.get().setKitapAdi(dtoBookIU.getKitapAdi());
			dbBook.get().setSayfaSayisi(dtoBookIU.getSayfaSayisi());
			dbBook.get().setYazar(dtoBookIU.getYazar());
			
			bookRepository.save(dbBook.get());
			BeanUtils.copyProperties(dbBook.get(), dtoBook);
		}
		return dtoBook;
	}

	@Override
	public DtoBook findBook(Integer id, String kitapAdi, String yazar) {
		if (id != null) {
	        return  bookRepository.findById(id).map(this::convertToDto).orElse(null);
	    }
	    if (kitapAdi != null && !kitapAdi.isEmpty()) {
	        return bookRepository.findBykitapAdi(kitapAdi).map(this::convertToDto).orElse(null);
	    }
	    if (yazar != null && !yazar.isEmpty()) {
	        return bookRepository.findByyazar(yazar).map(this::convertToDto).orElse(null);
	    }
	    return null;
	}
	
}
