import cv2
import numpy as np
import matplotlib.pyplot as plt
import os
from PIL import Image, ImageFilter, ImageOps


def redimensionar(ruta, red):
    """Redimensiona para Youtube/Instagram/Twitter/Facebook y guarda en fotos_mejoradas."""
    tamanios = {"Youtube": (1280, 720), "Instagram": (1080, 1080),
                "Twitter": (1200, 675), "Facebook": (1200, 630)}

    red = red.strip().capitalize()
    if red not in tamanios:
        raise ValueError("Red no valida.")

    try:
        img = Image.open(ruta)
    except Exception as e:
        raise FileNotFoundError(f"No se pudo abrir la imagen: {e}")

    os.makedirs("fotos_mejoradas", exist_ok=True)
    img = ImageOps.contain(img, tamanios[red])  # escala sin distorsion (no resize)
    img = img.convert("RGB")
    img.save(f"fotos_mejoradas/redimensionada_{red}.jpg")
    return img


def ecualizar(imagen, nombre):
    """Ecualiza el contraste usando el histograma y guarda la comparacion."""
    if imagen is None:
        raise ValueError("Primero debes cargar una imagen.")

    try:
        img_array = np.array(imagen.convert("L"))  # gris: equalizeHist requiere 1 canal
        equ = cv2.equalizeHist(img_array)
        print(f"Ecualizacion: original min={img_array.min()} max={img_array.max()} mean={img_array.mean():.1f} -> ecualizada min={equ.min()} max={equ.max()} mean={equ.mean():.1f}")
    except Exception as e:
        raise RuntimeError(f"Error al ecualizar: {e}")

    fig, ejes = plt.subplots(1, 2, figsize=(10, 4))
    ejes[0].imshow(img_array, cmap="gray")
    ejes[0].set_title(f"{nombre} original")
    ejes[0].axis("off")
    ejes[1].imshow(equ, cmap="gray")
    ejes[1].set_title("ecualizada")
    ejes[1].axis("off")

    plt.savefig(f"fotos_mejoradas/{nombre}.png")
    plt.show()
    plt.close()  # libera memoria


def aplicar_filtro(imagen, nombre_filtro):
    """Aplica uno de los 9 filtros de Pillow y guarda original vs filtrada."""
    filtros = {
        "Blur": ImageFilter.BLUR, "Contour": ImageFilter.CONTOUR, "Detail": ImageFilter.DETAIL,
        "Edge Enhance": ImageFilter.EDGE_ENHANCE, "Edge Enhance More": ImageFilter.EDGE_ENHANCE_MORE,
        "Emboss": ImageFilter.EMBOSS, "Find Edges": ImageFilter.FIND_EDGES,
        "Sharpen": ImageFilter.SHARPEN, "Smooth": ImageFilter.SMOOTH
    }

    if imagen is None:
        raise ValueError("Primero debes cargar una imagen.")
    if nombre_filtro not in filtros:
        raise ValueError("Filtro no valido.")

    try:
        resultado = imagen.filter(filtros[nombre_filtro])
    except Exception as e:
        raise RuntimeError(f"Error al aplicar el filtro: {e}")

    plt.figure(figsize=(8, 4))
    plt.subplot(1, 2, 1)
    plt.imshow(imagen)
    plt.title("Original")
    plt.axis("off")
    plt.subplot(1, 2, 2)
    plt.imshow(resultado)
    plt.title(nombre_filtro)
    plt.axis("off")

    plt.savefig(f"fotos_mejoradas/filtro_{nombre_filtro}.png")
    plt.show()
    plt.close()  # libera memoria


def hacer_boceto(imagen_pil):
    """Recibe una imagen y devuelve otra que resalta bordes y contornos."""
    if imagen_pil is None:
        raise ValueError("Primero debes cargar una imagen.")

    try:
        imagen_pil = imagen_pil.convert("RGB")
        img = np.array(imagen_pil)
        gris = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)  # OpenCV requiere gris para Canny/threshold
        canny = cv2.Canny(gris, 50, 150)
        _, umbral = cv2.threshold(gris, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)  # se descarta el umbral con _
    except Exception as e:
        raise RuntimeError(f"Error al generar el boceto: {e}")

    plt.figure(figsize=(12, 4))
    plt.subplot(1, 3, 1)
    plt.imshow(img)
    plt.title("Original")
    plt.axis("off")
    plt.subplot(1, 3, 2)
    plt.imshow(canny, cmap="gray")
    plt.title("Canny")
    plt.axis("off")
    plt.subplot(1, 3, 3)
    plt.imshow(umbral, cmap="gray")
    plt.title("Umbral (Otsu)")
    plt.axis("off")

    plt.savefig("fotos_mejoradas/boceto.png")
    plt.show()
    plt.close()  # libera memoria
    return umbral


def main():
    """Menu por consola para cargar imagen y aplicar redimensionar, ecualizar, filtros y boceto."""
    print("===================================")
    print("   BIENVENIDO A FOTOAPP   ")
    print("===================================")

    ruta_imagen = None
    imagen = None
    imagen_borde = None

    while True:
        print("\n--- MENU DE OPCIONES ---")
        print("1. Cargar imagen")
        print("2. Redimensionar para Red Social")
        print("3. Ecualizar contraste (Histograma)")
        print("4. Aplicar Filtro de Pillow")
        print("5. Hacer Boceto (Bordes)")
        print("6. Salir")

        opcion = input("\nElige una opcion (1-6): ")

        if opcion in ['2', '3', '4', '5'] and imagen is None:
            print("ERROR: Primero debes cargar una imagen (Opcion 1).")
            continue

        if opcion == '1':
            ruta_imagen = input("Ingresa la ruta de la foto (ej. imagenes_prueba/foto.jpg): ").strip(' "')
            try:
                imagen = Image.open(ruta_imagen)
                print("Imagen cargada exitosamente.")
            except Exception as e:
                print(f"Error al cargar la imagen: {e}")
                imagen = None

        elif opcion == '2':
            red = input("Para que red? (Youtube, Instagram, Twitter, Facebook): ").strip(' "')
            try:
                r = redimensionar(ruta_imagen, red)
                if r is not None:
                    print("Imagen redimensionada guardada en 'fotos_mejoradas'.")
                    plt.figure()
                    plt.imshow(r)
                    plt.title(f"Redimensionada para {red}")
                    plt.axis("off")
                    plt.show()
                    plt.close()
            except Exception as e:
                print(f"Error: {e}")

        elif opcion == '3':
            try:
                ecualizar(imagen, "foto_ecualizada")
                print("Comparacion de ecualizacion guardada.")
            except Exception as e:
                print(f"Error: {e}")

        elif opcion == '4':
            nombres_filtros = ["Blur", "Contour", "Detail", "Edge Enhance", "Edge Enhance More",
                               "Emboss", "Find Edges", "Sharpen", "Smooth"]
            print("Elige un filtro (1-9):")
            for i, f in enumerate(nombres_filtros, 1):
                print(f"{i}. {f}")
            num = input("Numero: ").strip()
            try:
                filtro = nombres_filtros[int(num) - 1]
            except (ValueError, IndexError):
                print("Filtro no valido.")
                continue
            try:
                aplicar_filtro(imagen, filtro)
                print("Filtro aplicado y guardado.")
            except Exception as e:
                print(f"Error: {e}")

        elif opcion == '5':
            try:
                imagen_borde = hacer_boceto(imagen)
                print("Boceto generado y guardado.")
            except Exception as e:
                print(f"Error: {e}")

        elif opcion == '6':
            print("Saliendo de FotoApp... Hasta luego!")
            break

        else:
            print("Opcion no valida. Intenta de nuevo.")
