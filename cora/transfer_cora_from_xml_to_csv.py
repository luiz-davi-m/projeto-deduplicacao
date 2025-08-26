import xml.etree.ElementTree as ET
import csv

# Arquivo de entrada e saída
xml_file = "cora/datasets/cora-all-id.xml"
csv_file = "cora/datasets/cora.csv"

# Parse do XML
tree = ET.parse(xml_file)
root = tree.getroot()

# Abre o CSV para escrita
with open(csv_file, "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)

    # Cabeçalho do CSV
    writer.writerow(["id", "authors", "title", "venue_name", "venue_vol", "venue_date"])

    # Itera sobre cada publicação
    for pub in root.findall("publication"):
        pub_id = pub.get("id", "")

        # Coletar autores
        authors = [a.text.strip() for a in pub.findall("author") if a.text]
        authors_str = "; ".join(authors)

        # Coletar título (às vezes dividido em várias tags <title>)
        titles = [t.text.strip() for t in pub.findall("title") if t.text]
        title_str = " ".join(titles)

        # Venue (pode ter múltiplos <venue>, pegamos o primeiro)
        venue = pub.find("venue/venue")
        venue_name = ""
        venue_vol = ""
        venue_date = ""
        if venue is not None:
            names = [n.text.strip() for n in venue.findall("name") if n.text]
            venue_name = " ".join(names)
            vol = venue.find("vol")
            if vol is not None and vol.text:
                venue_vol = vol.text.strip()
            dates = [d.text.strip() for d in venue.findall("date") if d.text]
            venue_date = " ".join(dates)

        # Escreve a linha no CSV
        writer.writerow([pub_id, authors_str, title_str, venue_name, venue_vol, venue_date])

print("✅ Conversão concluída! Arquivo salvo como:", csv_file)
