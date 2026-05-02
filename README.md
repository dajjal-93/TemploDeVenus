# Templo de Venus

Sitio Jekyll alojado en GitHub Pages.

## Cómo publicar un texto nuevo

1. Crear un archivo en `_posts/` con el formato `YYYY-MM-DD-titulo-en-minusculas.md`.
2. Front matter mínimo:

   ```yaml
   ---
   title: Título del texto
   date: 2026-05-02 21:00:00 -0600
   ---
   ```

   Opcionales: `subtitle`, `epigraph`, `epigraph_source`.

3. Escribir el texto en markdown debajo del front matter.
4. `git add . && git commit -m "..." && git push`. GitHub Pages construye y publica en 1–2 minutos.

## Centrar líneas como invocaciones

Después de un párrafo que quieras centrar, agrega `{:.centered}` en su propia línea:

```markdown
"Amor mío, ¿a dónde te has ido?"
{:.centered}
```

## Imágenes, GIFs, video

Coloca el archivo en `assets/imagenes/` (o `assets/videos/`) y embébelo así:

```html
<figure>
  <img src="{{ '/assets/imagenes/nombre.jpg' | relative_url }}" alt="descripción">
  <figcaption>Pie de imagen — autor, año.</figcaption>
</figure>
```

Para que la pieza desborde un poco la columna en pantallas grandes, añade `class="wide"` a la `<figure>`.

## Citas

```markdown
> El alma tiene la forma de la casa que la guarda;
> la casa, la forma del alma que la habita.

<cite>— Gaston Bachelard, *La poética del espacio*</cite>
```

## Estructura

```
.
├── _config.yml         · configuración del sitio
├── _includes/          · cabecera, pie, head
├── _layouts/           · plantillas (default, home, post)
├── _posts/             · los textos
├── assets/
│   ├── css/main.scss   · estilos
│   ├── imagenes/
│   └── videos/
└── index.html          · home
```

## Probar localmente (opcional)

No es necesario — GitHub Pages construye en su servidor. Si quieres preview local:

```sh
bundle install
bundle exec jekyll serve
```

Abrir `http://localhost:4000/TemploDeVenus/`.
