# ---------------------------------------------------------------------------
# PEGAR AS FERRAMENTAS (BIBLIOTECAS)
# ---------------------------------------------------------------------------
import speech_recognition as sr # AS ORELHAS: Serve para o computador te ouvir. [cite: 14]
import webbrowser # O EXPLORADOR: Abre sites como o Youtube. [cite: 18]
import os # O ZELADOR: Sabe onde as pastas e arquivos estao no PC. [cite: 5]
import pygame # O RÁDIO: Serve para tocar o som da voz. [cite: 12, 13]
import tinytuya # O DEDO: Serve para apertar o botao da luz. [cite: 17]
import random # O DADO: Serve para escolher uma frase aleatoria do arquivo de falas. [cite: 5]
from gtts import gTTS # A BOCA: A voz gratis do Google que fala com voce. [cite: 5]
from AppOpener import open as open_app # A MÃO: Abre os programas do Windows. [cite: 17]
import falas # O LIVRO: Pega as frases que escrevemos no outro arquivo. 

# DIZ PARA O JARVIS ONDE ELE ESTA SENTADO (Pasta do projeto)
os.chdir(os.path.dirname(os.path.abspath(__file__)))

# ---------------------------------------------------------------------------
# FUNÇÃO DE FALAR (A BOCA)
# ---------------------------------------------------------------------------
def falar(texto):
    try:
        # CRIA O AUDIO COM A VOZ DO GOOGLE
        tts = gTTS(text=texto, lang='pt', tld='com.br')
        # SALVA O AUDIO NUM ARQUIVO CHAMADO voz.mp3
        tts.save("voz.mp3")
        # LIGA O RADIO
        pygame.mixer.init()
        # COLOCA A VOZ NO RADIO
        pygame.mixer.music.load("voz.mp3")
        # APERTA O PLAY
        pygame.mixer.music.play()
        # ESPERA A VOZ TERMINAR PARA NAO CORTAR A FALA
        while pygame.mixer.music.get_busy():
            pygame.time.Clock().tick(10)
        # DESLIGA O RADIO E JOGA O ARQUIVO NO LIXO
        pygame.mixer.music.unload()
        pygame.mixer.quit()
        os.remove("voz.mp3")
    except Exception as e:
        print(f"Erro na voz: {e}")

# ---------------------------------------------------------------------------
# FUNÇÃO DE OUVIR (OS OUVIDOS)
# ---------------------------------------------------------------------------
def ouvir():
    rec = sr.Recognizer() # CRIA O TIMPANO DO OUVIDO
    with sr.Microphone() as mic: # ABRE O MICROFONE
        rec.adjust_for_ambient_noise(mic, duration=0.2) # TIRA O CHIADO DO VENTILADOR
        audio = rec.listen(mic) # ESCUTA O QUE VOCE DIZ
        try:
            texto = rec.recognize_google(audio, language="pt-br") # TRADUZ SOM PARA LETRA
            print(f"> Voce disse: {texto}")
            return texto.lower() # DEVOLVE O TEXTO MINUSCULO
        except:
            return "" # SE NAO ENTENDER, RETORNA NADA [cite: 16]

# ---------------------------------------------------------------------------
# FUNÇÃO DA LUZ (O DEDO NO INTERRUPTOR)
# ---------------------------------------------------------------------------
def controlar_luz(acao):
    try:
        # CONECTA NA LAMPADA USANDO O IP E A CHAVE QUE ACHAMOS
        lampada = tinytuya.BulbDevice(
            dev_id='3738024610521ce8be8a', # ID DA LUZ
            address='192.168.18.12', # IP DA LUZ
            local_key='*zD=0VIXIkvsg{xb', # CHAVE NOVA [cite: 7]
            version=3.3
        )
        if acao == "ligar":
            lampada.turn_on() # APERTA O BOTAO DE LIGAR
            falar(random.choice(falas.acender_luz)) # FALA UMA FRASE DO LIVRO [cite: 3]
            #lampada.set_colour(r, g, b)
        else:
            lampada.turn_off() # APERTA O BOTAO DE DESLIGAR
            falar(random.choice(falas.desligar_luz)) # FALA UMA FRASE DO LIVRO [cite: 3]
    except Exception as e:
        print(f"Erro na luz: {e}")

# ---------------------------------------------------------------------------
# LOGICA DE ORDENS (O QUE ELE FAZ QUANDO ESCUTA)
# ---------------------------------------------------------------------------
def executar_comando(comando):
    # SE VOCE FALAR "LIGAR A LUZ"
    if "acender a luz" in comando or "ligar a luz" in comando:
        controlar_luz("ligar")

    # SE VOCE FALAR "APAGAR A LUZ"
    elif "apagar a luz" in comando or "desligar a luz" in comando:
        controlar_luz("desligar")

    # SE VOCE FALAR "YOUTUBE"
    elif "youtube" in comando:
        falar(random.choice(falas.yt_fala)) # [cite: 2]
        webbrowser.open("https://www.youtube.com")

    # SE VOCE FALAR "INSTAGRAM"
    elif "instagram" in comando:
        falar("Abrindo o Instagram para voce.")
        webbrowser.open("https://www.instagram.com")

    # SE VOCE FALAR "SPOTIFY"
    elif "spotify" in comando:
        falar(random.choice(falas.spotify_fala)) # [cite: 2]
        open_app("spotify") 

    # SE VOCE DISSER "TCHAU"
    elif "desligar" in comando or "tchau" in comando:
        falar(random.choice(falas.offline)) # [cite: 2]
        exit()

# ---------------------------------------------------------------------------
# O CORAÇÃO (FICA VIVO ESPERANDO VOCE CHAMAR)
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    print("Iniciando Jarvis...")
    falar(random.choice(falas.online)) # FALA QUE CHEGOU [cite: 1]

    while True: # LOOP INFINITO (CORAÇÃO BATENDO)
        escuta = ouvir() # FICA SEMPRE OUVINDO
        if "jarvis" in escuta: # SE VOCE FALAR O NOME DELE
            comando = escuta.replace("jarvis", "").strip() # TIRA O NOME "JARVIS" DA FRASE [cite: 19]
            if comando:
                executar_comando(comando) # FAZ A ORDEM [cite: 20]
            else:
                falar("Sim, Igor?") # SE CHAMAR SO O NOME, ELE RESPONDE [cite: 20]