API	Tipos de datos que proporciona	Costo / Plan gratuito	Límites de uso	Facilidad de implementación	Calidad de la documentación
USDA FoodData Central	
1. Datos de composición de alimentos: nutrientes, porciones, tipos: Standard Reference, Foundation Foods, branded foods, FNDDS, etc.
2.  Permite búsqueda de alimentos, detalle de nutrientes por alimento.

Gratuito. Los datos están en dominio público (licencia CC0), no hay tarifa para usar la API si tienes la clave.	

1. Límite por defecto de 1,000 solicitudes por hora por IP para la clave normal.
2.  Si se excede, la clave se bloquea temporalmente por una hora.

Muy buena: REST, endpoints claros (“search”, “food details”), ejemplos, especificación OpenAPI/Swagger. Se requiere una clave API que se obtiene gratuitamente.

Alta: la USDA tiene documentación técnica detallada, especificaciones de todos los datos, formatos JSON/CSV, descargas de datasets, ejemplos, etc.

Edamam	
1. Base de datos de alimentos, productos de supermercado, comidas genéricas, menús, etc.

2.  Permite análisis nutricional, filtrado por dietas/alergias, NLP para interpretación de texto libre, búsqueda de UPC, autocompletado.

Tiene planes de pago, y también niveles con acceso limitado gratuito o trial.

Por ejemplo, planes básicos (“Basic”, “Core”, etc.).	

1.  En los planes básicos se tienen ciertas cuotas de llamadas/mes o llamadas por minuto.
Ejemplo: Food & Grocery Database API de Edamam tiene límites dependiendo del plan: 100,000 llamadas/mes, 750,000, 5,000,000, etc.

2.  Límites de throttling (llamadas por minuto) también varían por plan.

Bastante buena. Provee funciones de NLP, parsing de UPC, autocompletado, etc., lo que añade algo de complejidad. Pero tienen ejemplos, endpoints bien organizados.	Buena documentación: explican los endpoints, qué campos devuelven, ejemplos, restricciones, reglas de atribución (mostrar su marca/link), etc.

Nutritionix	

1.  Alimentos comunes, marcas comerciales, productos de restaurante.

2.  Soporte para parsing de lenguaje natural (“natural language”), búsqueda instantánea/autocompletar, identificación de ejercicio, etc.

Tiene un plan gratuito (“free key” / desarrollador) con límites.
Planes pagos con más capacidad.
En algunas comparativas aparece que los planes empiezan en ~US$99/mes para algunos usos, o más para usos comerciales mayores.

En el plan gratuito los límites son bajos (llamadas por día/minuto o número de usuarios activos) — aunque no encontré un número exacto reciente en todos los casos. En los planes de pago estos límites 
suben bastante. Endpoint de “search/instant” para autocompletar, etc.

Relativamente fácil: usa REST + claves (“app id” + “app key”), los endpoints están bien definidos; procesamiento de lenguaje natural, parsing de ingredientes; ejemplos básicos. Hay que entender la estructura de autenticación.	

Buena, aunque algunas críticas dicen que la documentación podría aclarar más los límites exactos del plan gratuito o ejemplos más detallados en algunos casos. Pero en general es sólida.

Spoonacular	

1.  Recetas, ingredientes, nutrición de recetas, filtros de dieta/alergia, productos alimenticios, búsqueda compleja de recetas.

2.  Permite establecer rangos nutricionales, etc.

Tiene plan gratuito + varios planes pagos. En APIlayer, por ejemplo: plan gratuito con ~3,000 solicitudes/mes.

Planes pagos comienzan alrededor de $29/mes para más llamadas, $99 para más.	

1.  Gratis: ~3,000 requests/mes.

2.  Después los planes aumentan a 30,000, 100,000, etc.
•  También hay límites de uso dependiendo del endpoint y de cómo se maneje (por ejemplo cuánto procesamiento extra solicita la consulta).

Buena: tienen ejemplo “complexSearch”, filtros, parámetros claros, endpoints bastante completos. Autenticación por clave API. Los errores están documentados.	Documentación bastante buena: ejemplos, descripción de parámetros, buenas guías d“getting started”, repositorios “console” para probar.
Quizás no tan “científica” como USDA, pero muy práctica para uso de recetas/comida.


En este caso decidimos investigar a USDA FoodData Central
Al ser una opción aparentemente popular por la gente casual y el promedio
•  Foundation Foods
•	Datos de referencia de alimentos individuales (ej. manzana, arroz, pollo).
•	Incluye nutrientes, componentes, descriptores, factores de preparación, etc.
•  Standard Reference (SR Legacy)
•	Base clásica del USDA con nutrientes de miles de alimentos.
•	Es estática (ya no se actualiza, reemplazada por Foundation Foods).
•  Food and Nutrient Database for Dietary Studies (FNDDS)
•	Usada en estudios de consumo alimenticio en EE. UU. (NHANES).
•	Contiene alimentos tal como se consumen, con recetas promedio.
•  Branded Foods
•	Productos de marcas comerciales (ej. cereales, refrescos, galletas).
•	Incluye etiquetas nutricionales y datos de fabricante.
•  Experimental Foods
•	Datos de investigación en desarrollo.
Todos estos datos vienen con una fecha de publicación y escrito por distintas personas, esto parece mas una wiki comunitaria de alimentos, recetas y dietas para quienes los buscan, algo que nos permite encontrar respuestas mas
📌 ¿Cómo presentan la información?
1.	En la API (JSON):
o	Te devuelven un objeto con:
	fdcId → identificador único del alimento.
	description → nombre del alimento (ej. “Apple, raw, with skin”).
	dataType → tipo de base (Foundation, Branded, FNDDS, etc.).
	foodNutrients → lista de nutrientes con nombre, valor, unidad.
	Metadatos → categoría, fecha de publicación, medidas, marca, UPC si aplica.
👉 Esto lo hace muy estructurado y fácil de procesar en código.
2.	En la web oficial:
o	Puedes buscar alimentos directamente como si fuera un catálogo.
o	Muestran una tabla con los nutrientes (energía, macros, vitaminas, minerales).
o	Incluyen medidas de referencia (por 100 g, por porción, por pieza, etc.).
o	Para marcas: reproducen casi tal cual la etiqueta nutricional.
3.	En datasets descargables:
o	Si prefieres, puedes bajar CSV completos con todos los alimentos.
o	Son ideales para minería de datos, machine learning o análisis en Excel.
________________________________________
📌 ¿Qué tan útil es?
✅ Muy útil en proyectos de nutrición o apps de comida porque:
•	Permite consultar tanto alimentos genéricos (ej. pollo, arroz, manzana) como productos de marca.
•	Tiene valores exactos de nutrientes (macro + micro + compuestos especiales como aminoácidos o ácidos grasos).
•	Es gratuita y en dominio público, lo que la vuelve ideal para proyectos educativos, científicos y comerciales pequeños.
•	Se integra fácil en aplicaciones con llamadas REST → JSON (ej. apps de dieta, trackers de calorías, asistentes de recetas).
⚠️ Dónde puede quedarse corta:
•	Si necesitas recetas completas o recomendaciones dietéticas automáticas (eso lo hacen mejor Edamam o Spoonacular).
•	Si tu público no está en EE. UU., algunos productos de marca quizá no aparezcan.
•	Los límites de 1,000 consultas/hora pueden ser insuficientes para apps con muchos usuarios concurrentes.
Algo importante que genuinamente nos molestó bastante para investigar, es que principalmente la pagina esta en ingles por lo que si no sabes ingles necesitarías un traductor a la mano.
