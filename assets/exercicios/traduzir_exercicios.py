import json
from deep_translator import GoogleTranslator
from googletrans import Translator as GTranslator
import time

# Inicializa os tradutores
translator_deep = GoogleTranslator(source='en', target='pt')
translator_goog = GTranslator()

def translate_text(text):
    if not text:
        return text
    try:
        # Tenta com deep_translator primeiro
        return translator_deep.translate(text)
    except Exception as e:
        try:
            # Fallback para googletrans
            return translator_goog.translate(text, src='en', dest='pt').text
        except Exception as e2:
            # Se ambos falharem, mantém o original
            print(f"  ⚠️ Falha ao traduzir: '{text[:50]}...' - mantendo original")
            return text

# Carrega o arquivo original
with open('exercises.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

print(f"📚 Traduzindo {len(data)} exercícios...")

# Traduz cada campo de texto
for idx, item in enumerate(data):
    try:
        if 'title' in item and item['title']:
            item['title'] = translate_text(item['title'])
        if 'primer' in item and item['primer']:
            item['primer'] = translate_text(item['primer'])
        if 'primary' in item and item['primary']:
            item['primary'] = translate_text(item['primary'])
        if 'secondary' in item and item['secondary']:
            item['secondary'] = [translate_text(s) for s in item['secondary']]
        if 'equipment' in item and item['equipment']:
            item['equipment'] = [translate_text(e) for e in item['equipment']]
        if 'steps' in item and item['steps']:
            item['steps'] = [translate_text(s) for s in item['steps']]
        if 'tips' in item and item['tips']:
            item['tips'] = [translate_text(t) for t in item['tips']]
        
        if (idx + 1) % 50 == 0:
            print(f"✅ {idx + 1} exercícios traduzidos...")
        
        # Pequena pausa para evitar bloqueio
        time.sleep(0.05)
            
    except Exception as e:
        print(f"⚠️ Erro crítico no item {idx + 1}: {e}")

# Salva o arquivo traduzido
with open('exercises_pt.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print(f"\n🎉 Tradução concluída! Arquivo salvo como 'exercises_pt.json'")