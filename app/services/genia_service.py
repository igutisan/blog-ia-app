from google import genai
from google.genai import types
from PIL import Image
from io import BytesIO
import os, uuid, dotenv

dotenv.load_dotenv()


def generate_blog_content(topic: str):
    system_prompt = f"""
Eres un experto en redacción de contenidos y marketing digital especializado en **copywriting para blogs de e-commerce**.

Tu tarea es crear **artículos de blog completos y optimizados para SEO** a partir de un tema o idea que recibirás como entrada.

🎯 **Objetivo:** Generar un artículo atractivo, informativo y persuasivo que conecte con el público objetivo y posicione bien en buscadores.

🧠 **Instrucciones:**
- Redacta un **título principal (H1)** llamativo y natural, que despierte interés y contenga la palabra clave principal.
- Escribe un **cuerpo** de entre **400 y 600 palabras**, dividido en párrafos claros y bien estructurados.
- Mantén un tono **cercano, profesional y persuasivo**, evitando sonar artificial o sobreoptimizado.
- Menciona beneficios, soluciones o consejos relacionados con el tema.
- Incluye **palabras clave relevantes** de forma orgánica (sin forzar).
- Finaliza con un **llamado a la acción** que invite a leer más, comprar o seguir explorando.
- Genera una **meta descripción SEO** de entre **130 y 160 caracteres** que resuma el artículo y motive a hacer clic.
- Responde **únicamente en formato JSON**, siguiendo esta estructura exacta:

{{
  "title": "[título atractivo con palabra clave]",
  "body": "[texto completo del artículo]",
  "seoDescription": "[meta descripción optimizada para buscadores]"
}}

📝 **Entrada del usuario:**
Tema: {topic}

📘 **Ejemplo de salida:**
{{
  "title": "Cómo elegir la botella inteligente perfecta para mantenerte hidratado",
  "body": "Mantener una buena hidratación es clave para tu salud, pero muchas veces lo olvidamos. Las botellas inteligentes han llegado para cambiar eso... [continúa con el desarrollo del artículo]",
  "seoDescription": "Descubre cómo elegir la mejor botella inteligente para mantenerte hidratado y alcanzar tus metas de bienestar diario."
}}
"""
    client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=[system_prompt],
    )
    return response.text


def generate_image(product_name: str, product_description: str):
    system_prompt = f"Genera una imagen de {product_name} que refleje su descripción: {product_description}"
    client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
    response = client.models.generate_content(
        model="gemini-2.5-flash-image-preview",
        contents=[system_prompt],
    )
    filename = f"generated_{uuid.uuid4().hex}.png"
    image_path = f"static/{filename}"
    for part in response.candidates[0].content.parts:
        if part.text is not None:
            print(part.text)
        elif part.inline_data is not None:
            image = Image.open(BytesIO(part.inline_data.data))
            image.save(image_path)
    image_url = f"http://localhost:8000/static/{filename}"
    return image_url
