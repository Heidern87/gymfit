import json
from deep_translator import GoogleTranslator

# Inicializa o tradutor
translator = GoogleTranslator(source='en', target='pt')

# Carrega o arquivo original
with open('exercises.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

print(f"📚 Traduzindo {len(data)} exercícios (apenas campos essenciais)...")

for idx, item in enumerate(data):
    try:
        # Traduz título
        if 'title' in item and item['title']:
            item['title'] = translator.translate(item['title'])
        
        # Traduz tipo (compound, isolation, etc)
        if 'type' in item and item['type']:
            item['type'] = translator.translate(item['type'])
        
        # Traduz grupo muscular principal
        if 'primary' in item and item['primary']:
            item['primary'] = translator.translate(item['primary'])
        
        # Traduz equipamentos (array)
        if 'equipment' in item and item['equipment']:
            item['equipment'] = [translator.translate(e) for e in item['equipment']]
        
        # Progresso
        if (idx + 1) % 50 == 0:
            print(f"✅ {idx + 1} exercícios traduzidos...")
            
    except Exception as e:
        print(f"⚠️ Erro no item {idx + 1} ({item.get('title', 'desconhecido')}): {e}")
        # Continua mesmo com erro

# Salva o arquivo traduzido
with open('exercises_pt.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print(f"\n🎉 Tradução concluída! Arquivo salvo como 'exercises_pt.json'")
