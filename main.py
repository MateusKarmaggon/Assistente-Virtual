import speech_recognition as sr
import pyttsx3
import pywhatkit

# Inicializa o motor de voz
engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)  # Escolhe a primeira voz

# Lista de afazeres
todo_list = []

def speak(text):
    """Fala em voz alta e imprime no console."""
    print(f"Assistente: {text}")
    engine.say(text)
    engine.runAndWait()

def listen_command(timeout=8, phrase_time_limit=15):
    """Escuta o comando do usuário com limite de tempo."""
    recognizer = sr.Recognizer()

    try:
        with sr.Microphone() as source:
            print("Microfone ativado. Ajustando para ruídos de fundo...")
            recognizer.adjust_for_ambient_noise(source)

            speak("Estou ouvindo, pode falar!")
            audio = recognizer.listen(source, timeout=timeout, phrase_time_limit=phrase_time_limit)

        command = recognizer.recognize_google(audio, language='pt-BR')
        print(f"Você disse: {command}")
        return command.lower()

    except sr.WaitTimeoutError:
        speak("Não ouvi nada. Tente novamente.")
        return ""

    except sr.UnknownValueError:
        speak("Não entendi. Pode repetir?")
        return ""

    except sr.RequestError as e:
        speak(f"Erro ao conectar ao serviço: {e}")
        return ""

def run_assistant():
    """Executa a assistente em loop."""
    speak("")
    while True:
        command = listen_command()

        if "adicionar tarefa" in command:
            speak("Qual item deseja adicionar?")
            item = listen_command()
            if item:
                todo_list.append(item)
                speak(f"{item} foi adicionado à sua lista de afazeres.")

        elif "mostrar afazeres" in command:
            if todo_list:
                speak("Sua lista de afazeres contém:")
                for task in todo_list:
                    speak(task)
            else:
                speak("Sua lista de afazeres está vazia.")

        elif "pesquisar por" in command:
            query = command.replace("pesquisar por", "").strip()
            speak(f"Pesquisando por {query}")
            pywhatkit.search(query)

        elif "sair" in command or "encerrar" in command or "pare" in command:
            speak("Aura encerrando. Até mais!")
            break

        else:
            speak("Comando não reconhecido. Tente novamente.")

if __name__ == "__main__":
    try:
        speak("Aura iniciando. Como posso ajudar?")
        run_assistant()
    except KeyboardInterrupt:
        speak("Aura encerrando. Até logo!")
        print("Assistente finalizada.")
