.. _usecases:

Use-cases
=========

This page provides additional information for the specific use-cases.

Product search
--------------

Documents correspond to products in an `online toy store <http://www.regiojatek.hu/>`_.
The amount of text available for individual products is limited (and is in Hungarian),
but there are structural and semantic annotations, including

* Organization of products into a two-level deep topical categorization system
* Toy characters associated with the product (Barbie, Spiderman, Hello Kitty, etc.)
* Brand (Beados, LEGO, Simba, etc.)
* Gender and age recommendations (for many products).


Doclist
~~~~~~~

A fundamental characteristic of e-commerce is that the inventory (as well as the prices)
are constantly changing. This is something to keep in mind, since a single ranking will
be used throughout the entire test period of the challenge, without the possibility of
updating it.

The :ref:`api-participants_doclist` request returns all products that were available
in the (recent) past.  I.e., it also includes products that may not be available at
the moment (but might become available again in the future). Participating systems are
strongly encouraged to consider all products from this list. Those that are currently
unavailable will not be displayed to users.

It may happen during the test period that new products arrive; experimental systems will
not be able to include these in their ranking (but this is the same for all participants),
while the production system might return them. This can potentially affect the number
of wins against the production system (for the advantage of the production system), but
it will not affect the comparison across experimental systems.


Doc
~~~

Each document represents a product and contains the following fields (sorted alphabetically):

================== ===========
Field              Description
================== ===========
age_max            Recommended maximum age (may be empty, i.e., 0)
age_min            Recommended minimum age (may be empty, i.e., 0)
arrived            When the product arrived (first became available); only for products that arrived after 2014-08-28
available          Indicates if the product is currently available (1) or not (0)
bonus_price        Provided only if the product is on sale; this is the new (sales) price
brand              Name of the brand (may be empty)
category           Name of the (leaf-level) product category
category_id        Unique ID of the (leaf-level) product category
characters         List of toy characters associated with the product (may be empty)
description        Full textual description of the product (may be empty)
main_category      Name of the main (top-level) product category
main_category_id   Unique ID of the main (top-level) product category
gender             Gender recommendation. (0: for both girls and boys (or unclassified); 1: for boys; 2: for girls)
photos             List of photos about the product
price              Normal price
product_name       Name of the product
queries            Distribution of (frequent) queries that led to this product (may be empty)
short_description  Short textual description of the product (may be empty)
================== ===========

The text fields (brand, category, characters, description, main_category,
product_name, queries, short_description) are UTF-8 encoded.

An example product record is shown below::

	{
		"age_max": 10,
		"age_min": 6,
		"arrived": "2014-08-28",
		"available": 1,
		"bonus_price": 6245.0,
		"brand": "Blue-Box",
		"category": "K\u00f6nyv",
		"category_id": "103",
		"characters": [
			"Hello Kitty"
		],
		"description": "Kitty-n\u00e9l biztos helye lesz jegyzeteidnek, eml\u00e9keidnek! Hello Kitty bar\u00e1ts\u00e1g napl\u00f3dat saj\u00e1t titkos jelsz\u00f3val nyithatod. A napl\u00f3ban ceruz\u00e1ra illeszthet\u0151 Hello Kitty \u00e9s Tippy figur\u00e1kat \u00e9s titkos rekeszt is tal\u00e1lsz. A doboz tartalma: 1 napl\u00f3, 1 jegyzett\u00f6mb, 1 ceruza, haszn\u00e1lati \u00fatmutat\u00f3. A csomagol\u00e1s m\u00e9rete: kb. 20x25x7 cm. 6 \u00e9ves kort\u00f3l aj\u00e1nljuk.\n",
		"gender": 2,
		"main_category": "Kreat\u00edv fejleszt\u0151",
		"main_category_id": "16",
		"photos": [
			"http://regiojatek.hu/data/regio_images/normal/79698_0.jpg",
			"http://regiojatek.hu/data/regio_images/normal/79698_1.jpg",
			"http://regiojatek.hu/data/regio_images/normal/79698_2.jpg",
			"http://regiojatek.hu/data/regio_images/normal/79698_3.jpg"
		],
		"price": 9995.0,
		"product_name": "Hello Kitty Bar\u00e1ts\u00e1g napl\u00f3 jelsz\u00f3val",
		"queries": {
			"hello kitty": "0.36364",
			"napl\u00f3": "0.36364",
			"titkos napl\u00f3": "0.27273"
		},
		"short_description": "Kitty-n\u00e9l biztos helye lesz jegyzeteidnek, eml\u00e9keidnek!"
	}


