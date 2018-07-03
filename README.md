necestovka
==========

Installace a spusteni
---------------------

Toto je potreba projit vzdy pri prvnim (inicializacnim spustenim)
  - pip3 install -r requirements.txt
  - ./manage.py syncdb
  - ./manage.py createsuperuser
  - ./manage.py runscript init_database
  - ./manage.py runserver

- aplikace ve vychozim stavu posloucha na 127.0.0.1:8000
- pro testovaci ucely se pouziva sqlite
- repozitar obsahuje heslo k emailovemu uctu, proto by repozitar nemel byt verejny, pripadne je nutne provest zpetne procisteni gitu

Spousteni uloh:
---------------
Parsovani emailu z amadea je zde (nebyl pristup k zadnemu API):

  ./manage.py runscript amadeus_parser    




Bussiness Flow
--------------

1. zakaznik zada na webu objednavku a zavola se funkce 
	order_create(
		fly={
			1:{
				"from":
				"to":
				"start_date":
				"return_date":
			}
		},
		primary_email="",
		primary_phone="",
		passengers=int(),
		checked_luggage=int()
	)
	- funkce vraci vygenerovane order_id= %M + %y + rand(4)  (napr 11181234)  - pouziva se jako VS 


2. zamestnanec vyzvedne objednavku, zjisti dalsi informace
	- kontakty na osoby doplni do IS
	- doplnkove sluzby doplni do IS 
	- vytvori nabidku v amadeovi

3. IS naimportuje z emailu lety pod uzivatele v objednavce pomoci funkce 
	order.add_flights_to_user(
		user="",
		fly={

		}
	)
	a nastavi se stav na in progress

4. zamestnanec doplni v objednavce ceny a vygeneruje DOCX, ktery pripadne jeste upravi a posila zakaznikovi

5. po zaplaceni se zmeni u objednavky stav na zaplacena




objednavka
----------

je vicemene toto:

[
	{
		"order_id": ""
		"contact_email": "",
		"contact_name": "",
		"contact_phone":"",
		"passangers": int(),
		"checked_luggage": int()
		"bank_name": "",
		"final_price": "",
		"state": 
		"extras" : [
			dict(id,name,description,cost),
			dict(...)
		],
		"ordered_fly": [
			dict(from, start_date, to, return_date),
			dict(...)
		],
		"passengers": [
			{
				"name": "",
				"email": "",
				"born_date": "",
				"flights": [
					fly1_from_amadeus,
					fly2_from_amadeus,
				]
			},
			{
				"... next user"
			}
		]
	},
	{
		"order_id": ""
		...
	}
]


naparovat letenku pod uzivatele aby slo tisknout letenky pro 
