import cv2
import numpy as np
class RectangleDetector:
    def __init__(self, image_path):
        self.image_path = image_path
        self.image = cv2.imread(self.image_path)
        if self.image is None:
            raise ValueError(f"Image at path {image_path} could not be loaded.")
        self.center_of_image = (self.image.shape[1] // 2, self.image.shape[0] // 2)


    def detect_rectangles(self, area_threshold=5000, blur=True):
        # Cargar la imagen
        image = cv2.imread(self.image_path)
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        #blur
        if blur:
            gray = cv2.medianBlur(gray, 5)

        # Aplicar un filtro de borde
        edges = cv2.Canny(gray, 50, 150, apertureSize=3)

        # Encontrar contornos
        contours, _ = cv2.findContours(edges, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        # Filtrar los contornos aproximados a rectángulos por área
        rectangles = []
        for contour in contours:
            peri = cv2.arcLength(contour, True)
            approx = cv2.approxPolyDP(contour, 0.04 * peri, True)
            if len(approx) == 4:
                x, y, w, h = cv2.boundingRect(approx)
                area = w * h
                if area > area_threshold:
                    rectangles.append(approx)

        return rectangles

    def draw_rectangles(self, rectangles, autodestroy=False):
        # Cargar la imagen
        image = cv2.imread(self.image_path)

        # Dibujar los rectángulos detectados y mostrar coordenadas
        for rect in rectangles:
            if rect is not None:
                cv2.drawContours(image, [rect], -1, (0, 255, 0), 2)
                # Obtener coordenadas del rectángulo
                x, y, w, h = cv2.boundingRect(rect)
                # Mostrar las coordenadas al lado del rectángulo
                cv2.putText(image, f'({x}, {y})', (x, y), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)

        # Mostrar la imagen con los rectángulos detectados y sus coordenadas
        cv2.imshow('Rectangles Detected', image)
        if not autodestroy:
            cv2.waitKey(0)
        cv2.destroyAllWindows()
        return image

    def save_image(self, filename, rectangles):
        image = self.draw_rectangles(rectangles, autodestroy=True)
        cv2.imwrite(filename, image)

    def get_most_central_rectangle(self, rectangles):
        min_distance = float('inf')
        central_rectangle = None
        for rect in rectangles:
            x, y, w, h = cv2.boundingRect(rect)
            center_of_rect = (x + w // 2, y + h // 2)
            distance = np.linalg.norm(np.array(self.center_of_image) - np.array(center_of_rect))
            if distance < min_distance:
                min_distance = distance
                central_rectangle = rect
        return central_rectangle
    
    def get_n_most_central_rectangles(self, rectangles, n):
        # Lista para guardar los rectángulos y sus distancias al centro
        distances_and_rectangles = []
        
        for rect in rectangles:
            x, y, w, h = cv2.boundingRect(rect)
            center_of_rect = (x + w // 2, y + h // 2)
            distance = np.linalg.norm(np.array(self.center_of_image) - np.array(center_of_rect))
            
            # Añadir la tupla (distancia, rectángulo) a la lista
            distances_and_rectangles.append((distance, rect))
        
        # Ordenar la lista por distancia
        distances_and_rectangles.sort(key=lambda x: x[0])
        
        # Devolver los n rectángulos más centrales (omitir la distancia)
        n_most_central_rectangles = [rect for _, rect in distances_and_rectangles[:min(n, len(rectangles))]]
        
        return n_most_central_rectangles
    
    def get_widest_rectangle(self, rectangles, min_x=-1, max_x=10000000):
        max_ratio = 0
        widest_rectangle = None
        for rect in rectangles:
            x, y, w, h = cv2.boundingRect(rect)
            ratio = w / h  # Calcula la proporción anchura/altura
            if ratio > max_ratio and x > min_x and x < max_x and h > 10:
                max_ratio = ratio
                widest_rectangle = rect
        return cv2.boundingRect(widest_rectangle), widest_rectangle


# Uso de la clase
#detector = RectangleDetector('anuncio.JPG')
#rectangles = detector.detect_rectangles()
#*_, widest = detector.get_widest_rectangle(rectangles)
#detector.draw_rectangles(widest) 
#print(f"found {len(rectangles)} recs")
#print(rectangles)
#print("Most central square:", widest)
