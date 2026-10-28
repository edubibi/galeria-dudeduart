import http.server
import socketserver
import json
import os
import subprocess
import webbrowser

PORT = 8000
METADATA_FILE = "metadata.json"
HTML_FILE = "documentacion_y_planificacion/resumen_precios_excel.html"

# TIER prices to apply in bulk
TIER_PRICES = {
    # Nivel 3: Premium (1.800€) - 15 copias
    "00 EDUSSE": "1.800,00",
    "12 CRISTAL CÚBICO": "1.800,00",
    "12 CRISTAL C\ufffdBICO": "1.800,00",
    "12 CRISTAL CBICO": "1.800,00",
    "22 NEO-LUMINA": "1.800,00",
    "22NEO-LUMINA": "1.800,00",
    "23 TRIDIM-BURST": "1.800,00",
    "23TRIDIM-BURST": "1.800,00",
    "39 MATERDIGISSE": "1.800,00",
    "40 MECHPASTOSSE": "1.800,00",
    "41 GESSOLUX": "1.800,00",
    "42 GESSOLUX EXTREMUM": "1.800,00",
    "44 GESSOLUX AZURITE": "1.800,00",
    "45 GESSOLUX IRIS": "1.800,00",
    "46 ESPATAC-EXTREME": "1.800,00",
    "46ESPATAC-EXTREME": "1.800,00",
    "48BESSELUXY_L": "1.800,00",
    "50 NEO FAUVE": "1.800,00",
    "49 ARTE CIBERNETICO NATURE": "1.800,00",
    "52 EDUSSE_CLASSIC": "1.800,00",
    "52 EDUSSE CLASSIC": "1.800,00",
    "52EDUSSE_CLASSIC": "1.800,00",
    "53 MONETESSE": "1.800,00",
    "53MONETESSE": "1.800,00",

    # Nivel 2: Medio (750€) - 30 copias
    "01 EXP NEOCIRC": "750,00",
    "02 CUBESSE STILO": "750,00",
    "03 EXPNEOPLUS": "750,00",
    "08BORACARBON": "750,00",
    "10OLEOCUBBO": "750,00",
    "15CUBESSEPLUS": "750,00",
    "20BORASSIE": "750,00",
    "21OCE-BURST": "750,00",
    "24BORACARBON MONUMENTOS": "750,00",
    "28ESPATAC": "750,00",
    "29ESPATAC-MAT": "750,00",
    "30OLONATUR-COLOR": "750,00",
    "31OLENATUR": "750,00",
    "37 IMPASTUS PAINT": "750,00",

    # Nivel 1: Acceso (250€) - 45 copias
    "05 PLUMINK": "250,00",
    "06 IDE CLASSIC": "250,00",
    "07 NEOINK": "250,00",
    "09FRACNEO": "250,00",
    "11URBANSPHERIC": "250,00",
    "16EXPNEO": "250,00",
    "17FUZZTESS": "250,00",
    "18 ABSTRACTO CONFLUENCIA": "250,00",
    "19 FUZZLINE ABS": "250,00",
    "25CAPLIVE": "250,00",
    "26CARL_LINE": "250,00",
    "27LINEVORT": "250,00",
    "32SINNOIR": "250,00",
    "33MINIGESTPOETIC": "250,00",
    "34EXPTERICO": "250,00",
    "35PAPERCHIN": "250,00",
    "36 LINEART": "250,00",
    "47 NEBULÓNICO": "250,00",
    "47 NEBULNICO": "250,00",
    "47 NEBULÍNICO": "250,00",
    "49 ARTE CIBERNÉTICO": "1.200,00",
    "49 ARTE CIBERNETICO": "1.200,00",

    # Nivel 4 (anteriormente Nivel 4 Aplicado, ahora también en Acceso con 50 copias)
    "04 APLICC": "180,00",
    "13RECTESSE": "180,00",
    "14TEREXSE": "180,00",

    # Especial: Numismática (Consultar/Subasta) - En estudio
    "HISTORIA CINCELADA": "1.500,00"
}

B2B_MAGNA_WORKS = [
    "Trilogía Argéntea", "Burbble Memory", "Camino Empedrado", "Drago", "Entre Sombras", 
    "Foruminmetal", "Gemanium", "Mar de Galicia", "Marea sobre Acantilado", "Pantano Rich", 
    "Raíces", "Rasgo Perdido", "Romeo y Juliette", "Saltos en las Rocas", "Verano bajo el Mar", 
    "Braxis", "Agnosis", "Arabita", "Bluequita", "Cristiomata", "Neumonita", "Petreossis", "Petritus", "Indian Oceanica"
]

def initialize_b2b_works():
    """Add B2B Magna works to metadata.json if they don't exist yet so they can be edited."""
    if not os.path.exists(METADATA_FILE):
        return
    
    with open(METADATA_FILE, "r", encoding="utf-8") as f:
        db = json.load(f)
    
    changed = False
    for idx, title in enumerate(B2B_MAGNA_WORKS, 1):
        b2b_id = f"b2b_magna_{idx:03d}"
        if b2b_id not in db:
            db[b2b_id] = {
                "id": b2b_id,
                "title": title,
                "category": "B2B MAGNA (ACCESO EXCLUSIVO)",
                "src": f"C:\\Users\\Usuario\\Desktop\\MARKETING EDUSSE UNIVERSE\\MATERIAL VIDEO\\{title.lower()}.png",
                "description": "Obra exclusiva de la colección Magna B2B.",
                "price": "450€ - 850€",
                "size": "Consultar",
                "b2b_only": True
            }
            changed = True
            
    if changed:
        with open(METADATA_FILE, "w", encoding="utf-8") as f:
            json.dump(db, f, indent=4, ensure_ascii=False)
        print("B2B Magna works initialized in metadata.json.")

class PricingAdminHandler(http.server.SimpleHTTPRequestHandler):
    def log_message(self, format, *args):
        # Silence logging to keep output clean
        pass

    def do_GET(self):
        import urllib.parse
        decoded_path = urllib.parse.unquote(self.path)
        
        # Check if the request is for the B2B Magna images from the Desktop
        if "MARKETING" in decoded_path or "MATERIAL" in decoded_path or "trilog" in decoded_path.lower() or "burbble" in decoded_path.lower() or decoded_path.lower().endswith(".png") and ("b2b" in decoded_path.lower() or any(x.lower() in decoded_path.lower() for x in B2B_MAGNA_WORKS)):
            filename = os.path.basename(decoded_path)
            desktop_path = "C:\\Users\\Usuario\\Desktop\\MARKETING EDUSSE UNIVERSE\\MATERIAL VIDEO"
            local_file = os.path.join(desktop_path, filename)
            
            if not os.path.exists(local_file) and os.path.exists(desktop_path):
                # Fallback case-insensitive match
                for f in os.listdir(desktop_path):
                    if f.lower() == filename.lower():
                        local_file = os.path.join(desktop_path, f)
                        break
            
            if os.path.exists(local_file) and os.path.isfile(local_file):
                self.send_response(200)
                if local_file.lower().endswith(".png"):
                    self.send_header("Content-Type", "image/png")
                elif local_file.lower().endswith((".jpg", ".jpeg")):
                    self.send_header("Content-Type", "image/jpeg")
                self.end_headers()
                with open(local_file, "rb") as f:
                    self.wfile.write(f.read())
                return

        if self.path == "/" or self.path == "/resumen_precios_excel.html" or "resumen_precios_excel.html" in self.path:
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.end_headers()
            with open(HTML_FILE, "r", encoding="utf-8") as f:
                self.wfile.write(f.read().encode("utf-8"))
        else:
            super().do_GET()

    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        
        if self.path == "/update_price":
            try:
                data = json.loads(post_data.decode('utf-8'))
                artwork_id = data.get("id")
                new_price = data.get("price")
                
                with open(METADATA_FILE, "r", encoding="utf-8") as f:
                    db = json.load(f)
                
                if artwork_id in db:
                    db[artwork_id]["price"] = new_price
                    with open(METADATA_FILE, "w", encoding="utf-8") as f:
                        json.dump(db, f, indent=4, ensure_ascii=False)
                    
                    subprocess.run(["py", "herramientas_mantenimiento/generate_pricing_dashboard.py"])
                    
                    self.send_response(200)
                    self.send_header("Content-Type", "application/json")
                    self.end_headers()
                    self.wfile.write(json.dumps({"status": "success"}).encode("utf-8"))
                else:
                    self.send_response(404)
                    self.send_header("Content-Type", "application/json")
                    self.end_headers()
                    self.wfile.write(json.dumps({"status": "error", "message": "Obra no encontrada"}).encode("utf-8"))
            except Exception as e:
                self.send_response(500)
                self.send_header("Content-Type", "application/json")
                self.end_headers()
                self.wfile.write(json.dumps({"status": "error", "message": str(e)}).encode("utf-8"))

        elif self.path == "/bulk_apply":
            try:
                with open(METADATA_FILE, "r", encoding="utf-8") as f:
                    db = json.load(f)
                
                for key, val in db.items():
                    if isinstance(val, dict) and "category" in val:
                        cat = val["category"]
                        if cat in TIER_PRICES:
                            db[key]["price"] = TIER_PRICES[cat]
                
                with open(METADATA_FILE, "w", encoding="utf-8") as f:
                    json.dump(db, f, indent=4, ensure_ascii=False)
                
                subprocess.run(["py", "herramientas_mantenimiento/generate_pricing_dashboard.py"])
                
                self.send_response(200)
                self.send_header("Content-Type", "application/json")
                self.end_headers()
                self.wfile.write(json.dumps({"status": "success"}).encode("utf-8"))
            except Exception as e:
                self.send_response(500)
                self.send_header("Content-Type", "application/json")
                self.end_headers()
                self.wfile.write(json.dumps({"status": "error", "message": str(e)}).encode("utf-8"))

        elif self.path == "/rebuild":
            try:
                with open(METADATA_FILE, "r", encoding="utf-8") as f:
                    data = json.load(f)
                
                artwork_list = []
                for key, item in data.items():
                    if isinstance(item, dict) and "id" in item:
                        # Include all works, including B2B Magna, in public gallery
                        artwork_list.append(item)
                
                artwork_list.sort(key=lambda x: (x.get("category", ""), x.get("id", "")))
                
                DATA_JS_FILE = "js/data.js"
                header = "const categoryCovers = {};\n\n"
                if os.path.exists(DATA_JS_FILE):
                    with open(DATA_JS_FILE, "r", encoding="utf-8") as f:
                        content = f.read()
                        parts = content.split("const artworkData =")
                        if len(parts) > 0:
                            header = parts[0]
                
                new_js_content = header + "const artworkData = " + json.dumps(artwork_list, indent=4, ensure_ascii=False) + ";"
                with open(DATA_JS_FILE, "w", encoding="utf-8") as f:
                    f.write(new_js_content)
                
                # Sync with Backup workspace
                BACKUP_WORKSPACE_DIR = "C:/Users/Usuario/.gemini/antigravity/scratch/GALERIA_DUDEDUART"
                if os.path.exists(BACKUP_WORKSPACE_DIR):
                    import shutil
                    shutil.copy(METADATA_FILE, os.path.join(BACKUP_WORKSPACE_DIR, METADATA_FILE))
                    shutil.copy(DATA_JS_FILE, os.path.join(BACKUP_WORKSPACE_DIR, DATA_JS_FILE))
                
                self.send_response(200)
                self.send_header("Content-Type", "application/json")
                self.end_headers()
                self.wfile.write(json.dumps({"status": "success"}).encode("utf-8"))
            except Exception as e:
                self.send_response(500)
                self.send_header("Content-Type", "application/json")
                self.end_headers()
                self.wfile.write(json.dumps({"status": "error", "message": str(e)}).encode("utf-8"))

if __name__ == "__main__":
    # Initialize B2B Magna works in metadata.json so they are editable
    initialize_b2b_works()
    
    # Regenerate dashboard HTML
    subprocess.run(["py", "herramientas_mantenimiento/generate_pricing_dashboard.py"])
    
    socketserver.TCPServer.allow_reuse_address = True
    with socketserver.TCPServer(("", PORT), PricingAdminHandler) as httpd:
        print(f"\n=======================================================")
        print(f"Servidor de Administracion de Precios Iniciado!")
        print(f"Abre tu navegador en: http://localhost:{PORT}")
        print(f"=======================================================")
        
        # Automatically open the browser
        webbrowser.open(f"http://localhost:{PORT}")
        
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nServidor detenido.")
