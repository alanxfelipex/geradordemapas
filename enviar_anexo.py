import argparse
import smtplib
from os.path import basename
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
import pandas as pd
import geopandas as gpd
import folium
from folium.plugins import MarkerCluster, Draw
from geopy.geocoders import Nominatim
from geopy.extra.rate_limiter import RateLimiter
from shapely.geometry import Point

def enviar_anexo(to_addr, filename):
    from_addr = 'geradordemapas@gmail.com'
    password = 'toeweifmzoxttkaq'
    subject = 'Seu Mapa Está pronto'
    content = 'Segue anexo o seu mapa'

    msg = MIMEMultipart()
    msg['From'] = from_addr
    msg['To'] = to_addr
    msg['Subject'] = subject
    body = MIMEText(content, 'plain')
    msg.attach(body)

    with open(filename, 'r') as f:
        part = MIMEApplication(f.read(), Name=basename(filename))
        part['Content-Disposition'] = 'attachment; filename="{}"'.format(basename(filename))
    msg.attach(part)

    s = smtplib.SMTP('smtp.gmail.com: 587')
    s.starttls()
    # Login Credentials for sending the mail
    s.login(msg['From'], password)
    s.sendmail(msg['From'], [msg['To']], msg.as_string().encode('utf-8'))



def cor_pino(elev, vermelho, azul, verde, roxo, laranja, vinho):
    if elev == vermelho and elev != '-':
        col = 'red'
    elif elev == azul and elev != '-':
        col = 'blue'
    elif elev == verde and elev != '-':
        col = 'green'
    elif elev == roxo and elev != '-':
        col = 'purple'
    elif elev == laranja and elev != '-':
        col = 'orange'
    elif elev == vinho and elev != '-':
        col = 'darkred'
    else:
        col = 'gray'
    return col

def geocodificar(x, geocode):
    valor = geocode(x, exactly_one=False, country_codes='br', limit=1)
    if valor != None:
        return valor[0]
    else:
        return None

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--datafile', type=str, help='Caminho para o arquivo de dados CSV')
    parser.add_argument('--email', type=str, help='Caminho para o arquivo de dados CSV')
    parser.add_argument('--rua', type=str, help='Caminho para o arquivo de dados CSV')
    parser.add_argument('--numero', type=str, help='Caminho para o arquivo de dados CSV')
    parser.add_argument('--bairro', type=str, help='Caminho para o arquivo de dados CSV')
    parser.add_argument('--cidade', type=str, help='Caminho para o arquivo de dados CSV')
    parser.add_argument('--uf', type=str, help='Caminho para o arquivo de dados CSV')
    parser.add_argument('--cor', type=str, help='Caminho para o arquivo de dados CSV')
    parser.add_argument('--vermelho', type=str, help='Caminho para o arquivo de dados CSV')
    parser.add_argument('--azul', type=str, help='Caminho para o arquivo de dados CSV')
    parser.add_argument('--verde', type=str, help='Caminho para o arquivo de dados CSV')
    parser.add_argument('--roxo', type=str, help='Caminho para o arquivo de dados CSV')
    parser.add_argument('--laranja', type=str, help='Caminho para o arquivo de dados CSV')
    parser.add_argument('--vinho', type=str, help='Caminho para o arquivo de dados CSV')

    args = parser.parse_args()

    df = pd.read_csv(args.datafile)

    df['validados'] = df[[args.rua, args.numero, args.bairro, args.cidade, args.uf]].notnull().any(axis=1)
    df = df.query('validados == True').reset_index(drop=True)

    df['local'] = df[args.rua] + ', ' + df[args.numero].astype(str) + ' - ' + df[args.bairro] + ' - ' + df[args.cidade] + ' - ' + df[args.uf]

    # instanciando a biblioteca que tratá as informações de geolocalização
    locator = Nominatim(user_agent='MyGeocoder')
    geocode = RateLimiter(locator.geocode, min_delay_seconds=1)

    # aplicar a geolocalização
    df['location'] = df['local'].apply(lambda x: geocodificar(x, geocode) if x else None)

    # pegando ponto, latitude, longitude e criando a coordenada
    df['point'] = df['location'].apply(lambda x: x.point if x else None)
    df['latitude'] = df['location'].apply(lambda x: x.latitude if x else None)
    df['longitude'] = df['location'].apply(lambda x: x.longitude if x else None)
    df['coordenada'] = df.apply(lambda row: Point(row['longitude'], row['latitude']), axis=1)

    # transformando em um geodataframe
    df_coordenada = gpd.GeoDataFrame(df, geometry='coordenada', crs='EPSG:4326')

    # Tirando média da latitude e longitude
    media_latitude = df_coordenada['latitude'].mean()
    media_longitude = df_coordenada['longitude'].mean()

    # Criando mapa e mostrando a partir da média da latitude e longitude
    fmap = folium.Map(location=(media_latitude, media_longitude))

    # colocando a possibilidade de recortar
    draw = Draw(export=True)
    draw.add_to(fmap)

    # Criar pontos
    mc = MarkerCluster().add_to(fmap)

    # Criando os popups
    for i, row in df_coordenada.iterrows():
        try:
            folium.Marker([row['latitude'], row['longitude']],
                          popup=f"""<strong>{args.cor}:</strong> {row[args.cor]}
                                            <br><strong>Nome:</strong> {row['Razao Social/Nome']}
                                            <br><strong>Endereco:</strong> {row['local']}
                                            <br><strong>Celular:</strong> {row['Celular']}
                                            <br><strong>Observação:</strong> {row['Observacoes']}""",
                          icon=folium.Icon(
                              color=cor_pino(row[args.cor], args.vermelho, args.azul, args.verde,
                                             args.roxo, args.laranja, args.vinho)),
                          icon_color='white',
                          ).add_to(mc)
        except:
            continue
    mc.add_to(fmap)

    # Salvar o mapa em um arquivo HTML temporário
    map_html = "mapa.html"
    fmap.save(map_html)

    enviar_anexo(args.email, map_html)


if __name__ == "__main__":
    main()


