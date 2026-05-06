package com.aliyilmaz.repository;

import java.util.Optional;

import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import com.aliyilmaz.entities.Book;

@Repository
public interface BookRepository extends JpaRepository<Book, Integer> {
	
	Optional<Book> findByyazar(String yazar);
    Optional<Book> findBykitapAdi(String kitapAdi);

}
