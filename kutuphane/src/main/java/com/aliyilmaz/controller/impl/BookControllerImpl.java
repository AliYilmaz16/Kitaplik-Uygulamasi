package com.aliyilmaz.controller.impl;

import java.util.List;
import java.util.Optional;

import com.aliyilmaz.services.impl.BookServiceImpl;

import org.springframework.beans.BeanUtils;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.DeleteMapping;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.PutMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

import com.aliyilmaz.controller.IBookController;
import com.aliyilmaz.dto.DtoBook;
import com.aliyilmaz.dto.DtoBookIU;
import com.aliyilmaz.entities.Book;
import com.aliyilmaz.repository.BookRepository;
import com.aliyilmaz.services.IBookService;

@RestController
@RequestMapping("/rest/api/book")
public class BookControllerImpl implements IBookController {

    private final BookServiceImpl bookServiceImpl;

	private final BookRepository bookRepository;

	@Autowired
	private IBookService bookService;

	public BookControllerImpl(BookRepository bookRepository, BookServiceImpl bookServiceImpl) {
		this.bookRepository = bookRepository;
		this.bookServiceImpl = bookServiceImpl;
	}

	@Override
	@PostMapping(path = "/save")
	public DtoBook saveBook(@RequestBody DtoBookIU dtoBookIU) {
		return bookService.saveBook(dtoBookIU);
	}

	@Override
	@GetMapping(path = "/list")
	public List<DtoBook> getAllBooks() {
		return bookService.getAllBooks();
	}

	@Override
	@GetMapping(path = "/find")
	public DtoBook findBook(
		    @RequestParam(name = "id", required = false) Integer id, 
		    @RequestParam(name = "kitapAdi", required = false) String kitapAdi, 
		    @RequestParam(name = "yazar", required = false) String yazar) {
		    
		    return bookService.findBook(id, kitapAdi, yazar);
		}

	@Override
	@DeleteMapping(path = "/delete/{id}")
	public boolean deleteBook(@PathVariable(name = "id") Integer id) {
		return bookService.deleteBook(id);
	}

	@Override
	@PutMapping(path = "/update/{id}")
	public DtoBook updateBook(@PathVariable(name = "id") Integer id,@RequestBody DtoBookIU dtoBookIU) {
		
		return bookService.updateBook(id, dtoBookIU);
	}

}
