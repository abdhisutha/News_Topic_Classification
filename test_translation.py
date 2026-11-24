
from deep_translator import GoogleTranslator

text = "వరుసగా మూడు టీ20లు గెలిచి రెండు మ్యాచ్లుండగానే సిరీస్ను సొంతం చేసుకుంది."

try:
    result = GoogleTranslator(source="auto", target="en").translate(text)
    print("English Translation:", result)
except Exception as error:
    print("Translation Error:", error)
