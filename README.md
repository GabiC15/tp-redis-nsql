# API The Mandalorian

### URLs

1. Genere un ruta agregar personajes, la cual reciba como parámetro el número episodio
   y el nombre del personaje.<br/>
   http://localhost:5000/load_character?episode=1&name=IG-11

2. Genere una ruta para quitar personajes, ídem anterior.<br/>
   http://localhost:5000/remove_character?episode=1&name=IG-11<br/>

3. Genere una ruta para listar los personajes de un episodio, la cual reciba como
   parámetro el número episodio.<br/>
   http://localhost:5000/list_charapters_episode?episode=3

4. Genere un ruta para listar los capítulos deberá indicar si están disponibles, alquilado o
   reservado.<br/>
   http://localhost:5000/list_episodes

5. Cuando se alquile un capítulo deberá quedar reservado por 4 minutos, hasta que se
   confirme el pago, de no confirmarse el pago deberá estar disponible nuevamente una
   vez pasado el tiempo.<br/>
   http://localhost:5000/rent_episode?episode=1

6. Genere una ruta para confirmar el pago la cual recibirá el número del capítulo y el
   precio, para que se pueda confirme el pago y registre el alquiler por 24 hs.<br/>
   http://localhost:5000/confirm_pay?episode=1&price=15
