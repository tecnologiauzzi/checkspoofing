import streamlit as st
from urllib.parse import urlparse

CYRILLIC_RANGE = (
    (0x0400, 0x04FF),  # Cyrillic
    (0x0500, 0x052F),  # Cyrillic Supplement
    (0x2DE0, 0x2DFF),  # Cyrillic Extended-A
    (0xA640, 0xA69F),  # Cyrillic Extended-B
)

def contains_cyrillic(text):
    for char in text:
        if any(start <= ord(char) <= end for start, end in CYRILLIC_RANGE):
            return True
    return False

def contains_mixed_alphabets(text):
    has_cyrillic = any(any(start <= ord(c) <= end for start, end in CYRILLIC_RANGE) for c in text)
    has_latin = any('a' <= c.lower() <= 'z' for c in text)
    return has_cyrillic and has_latin

def analyze_url(url):
    try:
        parsed = urlparse(url)
        domain = parsed.netloc or parsed.path.split('/')[0]
        if not domain:
            return ("URL inválida.", "warning", None)
        if contains_mixed_alphabets(domain):
            try:
                punycode = domain.encode('idna').decode('ascii')
            except Exception:
                punycode = None
            return ("O domínio contém mistura de caracteres do alfabeto latino e cirílico. POSSÍVEL PHISHING!", "error", punycode)
        elif contains_cyrillic(domain):
            return ("O domínio contém caracteres cirílicos. Verifique se a URL é confiável.", "warning", None)
        else:
            return ("Domínio parece legítimo (sem caracteres cirílicos detectados).", "success", None)
    except Exception as e:
        return (f"Erro ao analisar a URL: {e}", "error", None)

st.set_page_config(page_title="Detector de Phishing com Cirílico", page_icon="🔎")
st.title("🔎 Detector de Phishing com Cirílico")
st.write("Cole uma URL abaixo para verificar se ela utiliza caracteres suspeitos no domínio.")

url = st.text_input("URL para análise", "")

if url:
    msg, status, punycode = analyze_url(url)
    if status == "error":
        st.error(msg)
        if punycode:
            st.info(f"Domínio em Punycode (como o navegador enxerga): `{punycode}`")
    elif status == "warning":
        st.warning(msg)
    elif status == "success":
        st.success(msg)
