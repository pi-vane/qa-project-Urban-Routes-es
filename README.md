# *Proyecto:* qa-proyect-Urban-Routes-es


___

### Descripción del proyecto:

- Las pruebas automatizadas UI que se encuentran en este repositorio están orientadas a la aplicación UrbanRoutes
y la visibilidad de elementos claves al realizar un pedido de taxi en la plataforma. Se usa el lenguaje de Python, 
con algunos JavaScript incluidos, Las pruebas se corren en **PyCharm**, 
para lo cual se necesitan tener instaladas previamente para su ejecución:


- *Selenium WebDriver* para Chrome, en consola: 
  >   pip install selenium

- *Pytest*, en consola: 
    > pip install pytest

 >**Las pruebas son dependientes una de la otra, hay esperas dentro de ellas por lo cual
 > podrían fallar en algunos casos las pruebas consecuentes como resultado de esto.**
 

### **Lista de pruebas**:
1. __Ingreso de direcciones, Desde y Hasta.__ Indispensable para todas las pruebas que le siguen.
2. Selección de tarifa: *Comfort*.
3. __Ingreso y verificación de número telefónico__.
4. Cambio de tipo de pago a **Tarjeta**.
5. Ingreso de comentario al conductor y *comprobación de mensaje de error visible*.
6. Comprobación de activado de switch en el campo *Manta y pañuelos*.
7. Comprobación de botón para cambiar *cantidades* del pedido en el campo *Helado*.
8. **Comprobación de apertura del modal de pedido de taxi trás llenar todos los campos indispensables.**
9. Verificación de cambio en modal de búsqueda de taxi a *asignación de conductor (nombre) y número de orden en el modal*.
___

### Tecnologías usadas

- PyCharm:
    >**Lenguaje de programación usado: Python**
- Selenium WebDriver para Chrome
- Pytest
- WebDriverWait
- JavaScript executor
- Chrome
    >**Navegador Chrome en su versión 149.07**

-Las técnicas usadas en este proyecto son tomadas de Page Object Model (POM)
Por lo que al abrir el repertorio cosnta de ek archivo .gitignore, este archivo README.md, y otros dos.

- El archivo __data.py__ del cual se toma la información
de usuario para los tests.

- El archivo __main.py__, en este se concentra todo el modelado de objetos para la automatización de pruebas UI en la página.

  1. Se encuentra la función __def retrieve_phone_code()__
  necesario para la verificación del número télefonico del usuario. __Por lo cual se recomienda no modificarlo__.

  2. Después de esta función, se encuentran los elementos. Todos estos serán usados para 
  localización de los elementos necesarios para cada paso de las pruebas.

  3. Como tercera parte se encuentran, los métodos de ubicación y procesamiento de
  dichos objetos en orden a sus pruebas.

  4. Por último se encuentra englobado la construcción de componentes en el 
  apartado: **class TestUrbanRoutes** donde contiene el class de setup para
  preparar la ejecución de la lista de pruebas consecutivas. 

> Recordar de cambiar la __URL__ del servidor en data.py antes de los tests.

 